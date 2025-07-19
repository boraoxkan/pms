from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from .models import Project, ProjectPreference, Intern, InternAvailability, AvailabilitySettings
from .forms import ProjectPreferenceForm
import json

def verify_token(view_func):
    """Decorator for legacy token-based authentication"""
    def wrapper(request, token, *args, **kwargs):
        try:
            intern = Intern.objects.get(access_token=token, is_active=True)
            request.intern = intern
            return view_func(request, token, *args, **kwargs)
        except (Intern.DoesNotExist, ValueError):
            raise Http404("Geçersiz veya süresi dolmuş bağlantı.")
    return wrapper

# ================================
# NEW VIEWS (Google SSO)
# ================================

def home_page(request):
    """
    Homepage with Google SSO login and dynamic content based on user state
    """
    context = {
        'user': request.user,
    }
    
    # If user is authenticated, add additional context
    if request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser):
        try:
            # Get intern object and related data
            intern = Intern.objects.get(user=request.user)
            
            # Get assigned projects for this intern
            assigned_projects = intern.assigned_projects.all()
            
            # Check if intern has availability data
            has_availability = False
            availability_data = None
            try:
                availability = InternAvailability.objects.get(intern=intern)
                has_availability = bool((availability.group_meeting_data and 
                                       any(slots for slots in availability.group_meeting_data.values())) or
                                      (availability.individual_work_data and 
                                       any(slots for slots in availability.individual_work_data.values())))
                availability_data = availability
            except InternAvailability.DoesNotExist:
                pass
            
            # Check if intern has submitted preferences
            has_preferences = False
            try:
                preferences = ProjectPreference.objects.get(intern=intern)
                has_preferences = preferences.is_submitted
            except ProjectPreference.DoesNotExist:
                pass
            
            # Add intern-specific context
            context.update({
                'intern': intern,
                'assigned_projects': assigned_projects,
                'assigned_projects_count': assigned_projects.count(),
                'has_assigned_projects': assigned_projects.exists(),
                'has_availability': has_availability,
                'availability_data': availability_data,
                'has_preferences': has_preferences,
            })
            
        except Intern.DoesNotExist:
            # User is authenticated but no intern record exists
            pass
    
    return render(request, 'intern_portal/home_page.html', context)

@login_required
def team_availability(request):
    """
    Display team availability calendar for Google SSO authenticated users
    Shows combined availability of all teammates (interns assigned to same projects)
    Displays full 24-hour time range (00:00 to 23:00)
    NEW: Highlights the current user's own availability
    """
    # Check if user is admin (staff/superuser)
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admin kullanıcıları için takım müsaitlik sistemi kullanılmaz. Lütfen admin panelini kullanın.')
        return redirect('/admin/')
    
    # Get the intern object linked to the authenticated user
    try:
        current_intern = Intern.objects.get(user=request.user)
    except Intern.DoesNotExist:
        messages.error(
            request, 
            'Hesabınız ile ilgili bir sorun var. Lütfen sistem yöneticisi ile iletişime geçin.'
        )
        return redirect('home_page')
    
    # Get all projects assigned to current intern
    assigned_projects = current_intern.assigned_projects.all()
    
    if not assigned_projects.exists():
        messages.info(request, 'Henüz size atanmış bir proje bulunmuyor. Takım müsaitliği görüntülemek için önce bir projeye atanmanız gerekiyor.')
        return redirect('home_page')
    
    # Find all teammates (other interns assigned to the same projects)
    teammate_ids = set()
    for project in assigned_projects:
        # Get all interns assigned to this project, excluding current intern
        project_interns = project.assigned_interns.exclude(id=current_intern.id).values_list('id', flat=True)
        teammate_ids.update(project_interns)
    
    # Get teammate objects with their assigned projects and profile pictures
    # Get teammate objects with their assigned projects and profile pictures
    # Get teammate objects with their assigned projects and profile pictures
    teammates = Intern.objects.filter(id__in=teammate_ids, is_active=True).prefetch_related('assigned_projects').select_related('user')

    # Create a detailed teammates list with ONLY common projects
    teammates_with_projects = []
    for teammate in teammates:
        teammate_projects = teammate.assigned_projects.all()
        # Find common projects between current intern and this teammate
        common_projects = assigned_projects.intersection(teammate_projects)
        
        # Only include teammates who have common projects
        if common_projects.exists():
            # Get profile picture URL (cropped if available)
            profile_picture_url = None
            if teammate.profile_picture:
                profile_picture_url = teammate.get_profile_picture_url('profile_medium')
                if not profile_picture_url:
                    profile_picture_url = teammate.profile_picture.url
            
            teammates_with_projects.append({
                'intern': teammate,
                'common_projects': common_projects,
                'common_projects_count': common_projects.count(),
                'has_availability': False,
                'availability_data': None,
                'profile_picture_url': profile_picture_url,  # Add this line
            })
    
    # Define time slots for full 24-hour day (00:00 to 23:00)
    TIME_SLOTS = [
        '00:00-01:00', '01:00-02:00', '02:00-03:00', '03:00-04:00',
        '04:00-05:00', '05:00-06:00', '06:00-07:00', '07:00-08:00',
        '08:00-09:00', '09:00-10:00', '10:00-11:00', '11:00-12:00',
        '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00',
        '16:00-17:00', '17:00-18:00', '18:00-19:00', '19:00-20:00',
        '20:00-21:00', '21:00-22:00', '22:00-23:00', '23:00-00:00'
    ]

    # Define days of the week
    WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    DAY_NAMES = {
        'monday': 'Pazartesi',
        'tuesday': 'Salı', 
        'wednesday': 'Çarşamba',
        'thursday': 'Perşembe',
        'friday': 'Cuma'
    }

    # Get current user's availability for highlighting
    current_user_availability = {}
    try:
        current_availability = InternAvailability.objects.get(intern=current_intern)
        for day_code in WEEKDAYS:
            # Get combined availability (group + individual) for current user
            group_slots = current_availability.group_meeting_data.get(day_code, [])
            individual_slots = current_availability.individual_work_data.get(day_code, [])
            all_current_slots = group_slots + individual_slots
            current_user_availability[day_code] = all_current_slots
    except InternAvailability.DoesNotExist:
        # If current user has no availability, initialize empty
        for day_code in WEEKDAYS:
            current_user_availability[day_code] = []

    # Initialize the heatmap calendar structure
    heatmap_calendar = {}
    for day in WEEKDAYS:
        heatmap_calendar[day] = {}
        for time_slot in TIME_SLOTS:
            heatmap_calendar[day][time_slot] = {
                'available_teammates': [],
                'available_count': 0,
                'is_current_user_available': False,
                'heatmap_level': 'none'  # none, low, medium, high
            }

    # Fetch availability data for all teammates
    teammate_availabilities = InternAvailability.objects.filter(
        intern__in=teammates
    ).select_related('intern')

    # Process each teammate's availability for the heatmap
    for availability in teammate_availabilities:
        intern_name = availability.intern.get_full_name()
        
        # Process both group meeting and individual work hours
        for day_code in WEEKDAYS:
            # Get combined availability (group + individual)
            group_slots = availability.group_meeting_data.get(day_code, [])
            individual_slots = availability.individual_work_data.get(day_code, [])
            all_slots = group_slots + individual_slots
            
            for time_slot in all_slots:
                if time_slot in TIME_SLOTS:
                    heatmap_calendar[day_code][time_slot]['available_teammates'].append(intern_name)
                    heatmap_calendar[day_code][time_slot]['available_count'] += 1

    # Set current user availability flags and heatmap levels
    for day_code in WEEKDAYS:
        for time_slot in TIME_SLOTS:
            # Check if current user is available
            is_current_available = time_slot in current_user_availability.get(day_code, [])
            heatmap_calendar[day_code][time_slot]['is_current_user_available'] = is_current_available
            
            # Determine heatmap level based on teammate count
            count = heatmap_calendar[day_code][time_slot]['available_count']
            if count == 0:
                level = 'none'
            elif count <= 2:
                level = 'low'
            elif count <= 4:
                level = 'medium'
            else:
                level = 'high'
            heatmap_calendar[day_code][time_slot]['heatmap_level'] = level

    # Create template-friendly heatmap grid
    heatmap_grid = []
    for day in WEEKDAYS:
        day_data = {
            'day_code': day,
            'day_name': DAY_NAMES[day],
            'time_slots': []
        }
        for time_slot in TIME_SLOTS:
            slot_data = heatmap_calendar[day][time_slot]
            day_data['time_slots'].append({
                'time': time_slot,
                'time_display': time_slot.replace('-', ' - '),
                'available_count': slot_data['available_count'],
                'available_teammates': slot_data['available_teammates'],
                'is_current_user_available': slot_data['is_current_user_available'],
                'heatmap_level': slot_data['heatmap_level'],
                'css_classes': f"heatmap-{slot_data['heatmap_level']}" + (" self-selected" if slot_data['is_current_user_available'] else "")
            })
        heatmap_grid.append(day_data)

    # Calculate statistics
    total_teammates = teammates.count()
    teammates_with_availability = teammate_availabilities.count()

    # Get current intern's projects for context
    current_intern_projects = list(assigned_projects.values('name', 'id'))

    context = {
        'current_intern': current_intern,
        'teammates': teammates,
        'teammates_with_projects': teammates_with_projects,
        'assigned_projects': assigned_projects,
        'current_intern_projects': current_intern_projects,
        'heatmap_calendar': heatmap_calendar,
        'heatmap_grid': heatmap_grid,  # Use this instead of calendar_grid
        'time_slots': TIME_SLOTS,
        'weekdays': WEEKDAYS,
        'day_names': DAY_NAMES,
        'total_teammates': total_teammates,
        'teammates_with_availability': teammates_with_availability,
    }
    
    return render(request, 'intern_portal/team_availability.html', context)

@login_required
def select_availability(request):
    """
    UPDATED: Availability selection view with two separate types:
    1. Group Meeting Hours (09:00-17:00, min 20 hours)
    2. Individual Work Hours (24h, min 10 hours)
    """
    # Check if user is admin (staff/superuser)
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admin kullanıcıları için müsaitlik sistemi kullanılmaz. Lütfen admin panelini kullanın.')
        return redirect('/admin/')
    
    # Get the intern object linked to the authenticated user
    try:
        intern = Intern.objects.get(user=request.user)
    except Intern.DoesNotExist:
        messages.error(
            request, 
            'Hesabınız ile ilgili bir sorun var. Lütfen sistem yöneticisi ile iletişime geçin.'
        )
        return redirect('home_page')
    
    # Define available days
    DAYS = [
        ('monday', 'Pazartesi'),
        ('tuesday', 'Salı'),
        ('wednesday', 'Çarşamba'),
        ('thursday', 'Perşembe'),
        ('friday', 'Cuma'),
        ('saturday', 'Cumartesi'),
    ]
    
    # Define time slots for group meetings (09:00-17:00)
    GROUP_TIME_SLOTS = [
        ('09:00-10:00', '09:00-10:00'),
        ('10:00-11:00', '10:00-11:00'),
        ('11:00-12:00', '11:00-12:00'),
        ('12:00-13:00', '12:00-13:00'),
        ('13:00-14:00', '13:00-14:00'),
        ('14:00-15:00', '14:00-15:00'),
        ('15:00-16:00', '15:00-16:00'),
        ('16:00-17:00', '16:00-17:00'),
    ]
    
    # Define time slots for individual work (24 hours)
    INDIVIDUAL_TIME_SLOTS = [
        ('00:00-01:00', '00:00-01:00'),
        ('01:00-02:00', '01:00-02:00'),
        ('02:00-03:00', '02:00-03:00'),
        ('03:00-04:00', '03:00-04:00'),
        ('04:00-05:00', '04:00-05:00'),
        ('05:00-06:00', '05:00-06:00'),
        ('06:00-07:00', '06:00-07:00'),
        ('07:00-08:00', '07:00-08:00'),
        ('08:00-09:00', '08:00-09:00'),
        ('09:00-10:00', '09:00-10:00'),
        ('10:00-11:00', '10:00-11:00'),
        ('11:00-12:00', '11:00-12:00'),
        ('12:00-13:00', '12:00-13:00'),
        ('13:00-14:00', '13:00-14:00'),
        ('14:00-15:00', '14:00-15:00'),
        ('15:00-16:00', '15:00-16:00'),
        ('16:00-17:00', '16:00-17:00'),
        ('17:00-18:00', '17:00-18:00'),
        ('18:00-19:00', '18:00-19:00'),
        ('19:00-20:00', '19:00-20:00'),
        ('20:00-21:00', '20:00-21:00'),
        ('21:00-22:00', '21:00-22:00'),
        ('22:00-23:00', '22:00-23:00'),
        ('23:00-00:00', '23:00-24:00'),
    ]
    
    # Get or create availability record for the intern
    try:
        availability = InternAvailability.objects.get(intern=intern)
    except InternAvailability.DoesNotExist:
        availability = InternAvailability.objects.create(
            intern=intern,
            group_meeting_data={},
            individual_work_data={}
        )
    
    # Check if user can modify availability (FIXED LOGIC)
    if not availability.can_modify():
        settings = AvailabilitySettings.get_settings()
        if availability.is_locked:
            messages.error(
                request,
                'Müsaitlik durumunuz yönetici tarafından kilitlenmiş. '
                'Değişiklik yapmak için lütfen sistem yöneticisi ile iletişime geçin.'
            )
        elif settings.weekly_submission_enabled and availability.submission_date:
            messages.warning(
                request,
                f'Bu hafta için müsaitlik durumunuzu zaten belirttiniz '
                f'({availability.submission_date.strftime("%d.%m.%Y %H:%M")}). '
                f'Yeni hafta başlangıcına kadar veya yönetici sıfırlamasına kadar değişiklik yapamazsınız.'
            )
        return redirect('view_availability')
    
    if request.method == 'POST':
        # Process the submitted availability data
        new_group_data = {}
        new_individual_data = {}
        
        # Process group meeting hours
        for day_code, _ in DAYS:
            selected_group_slots = request.POST.getlist(f'group_meeting_{day_code}')
            valid_group_slot_values = [slot[0] for slot in GROUP_TIME_SLOTS]
            valid_group_slots = [slot for slot in selected_group_slots if slot in valid_group_slot_values]
            
            if valid_group_slots:
                new_group_data[day_code] = valid_group_slots
        
        # Process individual work hours
        for day_code, _ in DAYS:
            selected_individual_slots = request.POST.getlist(f'individual_work_{day_code}')
            valid_individual_slot_values = [slot[0] for slot in INDIVIDUAL_TIME_SLOTS]
            valid_individual_slots = [slot for slot in selected_individual_slots if slot in valid_individual_slot_values]
            
            if valid_individual_slots:
                new_individual_data[day_code] = valid_individual_slots
        
        try:
            # Update the availability record
            availability.group_meeting_data = new_group_data
            availability.individual_work_data = new_individual_data
            availability.week_year = availability.get_current_week_year()
            availability.submission_date = timezone.now()
            
            # This will trigger validation in the save method
            availability.save()
            
            # Show success message
            group_hours = sum(len(slots) for slots in new_group_data.values())
            individual_hours = sum(len(slots) for slots in new_individual_data.values())
            total_hours = group_hours + individual_hours
            
            messages.success(
                request, 
                f'Ortak çalışma saati durumunuz başarıyla kaydedildi! '
                f'Grup toplantı: {group_hours} saat, Bireysel çalışma: {individual_hours} saat '
                f'(Toplam: {total_hours} saat)'
            )
            return redirect('view_availability')
           
        except Exception as e:
            # Handle validation errors from the model
            messages.error(request, str(e))
            # Don't redirect, show form again with error
   
    # For GET requests, prepare context for template
    saved_group_availability = {}
    saved_individual_availability = {}
    
    if availability.group_meeting_data:
        for day_code, slots in availability.group_meeting_data.items():
            saved_group_availability[day_code] = slots
            
    if availability.individual_work_data:
        for day_code, slots in availability.individual_work_data.items():
            saved_individual_availability[day_code] = slots
   
    # Add settings info to context
    settings = AvailabilitySettings.get_settings()
    context = {
        'intern': intern,
        'availability': availability,
        'days': DAYS,
        'group_time_slots': GROUP_TIME_SLOTS,
        'individual_time_slots': INDIVIDUAL_TIME_SLOTS,
        'saved_group_availability': saved_group_availability,
        'saved_individual_availability': saved_individual_availability,
        'settings': settings,
        'can_modify': availability.can_modify(),
        'is_locked': availability.is_locked,
        'current_week_submission': availability.is_current_week_submission() if availability.week_year else False,
    }
   
    return render(request, 'intern_portal/select_availability.html', context)

@login_required
def view_availability(request):
    """
    UPDATED: Read-only view to display saved availability for both types
    """
    # Check if user is admin (staff/superuser)
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admin kullanıcıları için müsaitlik sistemi kullanılmaz. Lütfen admin panelini kullanın.')
        return redirect('/admin/')
    
    # Get the intern object linked to the authenticated user
    try:
        intern = Intern.objects.get(user=request.user)
    except Intern.DoesNotExist:
        messages.error(
            request, 
            'Hesabınız ile ilgili bir sorun var. Lütfen sistem yöneticisi ile iletişime geçin.'
        )
        return redirect('home_page')
    
    # Get availability record for the intern
    try:
        availability = InternAvailability.objects.get(intern=intern)
    except InternAvailability.DoesNotExist:
        # If no availability record exists, redirect to selection page
        messages.info(request, 'Henüz ortak çalışma saati belirtmemişsiniz. Lütfen müsaitlik durumunuzu belirleyin.')
        return redirect('select_availability')
    
    # Define day names for display
    DAY_NAMES = {
        'monday': 'Pazartesi',
        'tuesday': 'Salı',
        'wednesday': 'Çarşamba',
        'thursday': 'Perşembe',
        'friday': 'Cuma',
        'saturday': 'Cumartesi',
    }
    
    # Process availability data for display
    formatted_group_availability = {}
    formatted_individual_availability = {}
    
    group_hours = 0
    individual_hours = 0
    
    # Process group meeting hours
    if availability.group_meeting_data:
        for day_code, time_slots in availability.group_meeting_data.items():
            if time_slots:
                formatted_group_availability[DAY_NAMES.get(day_code, day_code)] = time_slots
                group_hours += len(time_slots)
    
    # Process individual work hours
    if availability.individual_work_data:
        for day_code, time_slots in availability.individual_work_data.items():
            if time_slots:
                formatted_individual_availability[DAY_NAMES.get(day_code, day_code)] = time_slots
                individual_hours += len(time_slots)
    
    total_hours = group_hours + individual_hours
    has_availability = total_hours > 0
    
    context = {
        'intern': intern,
        'availability': availability,
        'formatted_group_availability': formatted_group_availability,
        'formatted_individual_availability': formatted_individual_availability,
        'group_hours': group_hours,
        'individual_hours': individual_hours,
        'total_hours': total_hours,
        'has_availability': has_availability,
        'group_days_count': len(formatted_group_availability),
        'individual_days_count': len(formatted_individual_availability),
    }
    
    return render(request, 'intern_portal/view_availability.html', context)

# ================================
# LEGACY VIEWS (Token-based) - Updated for compatibility
# ================================

@verify_token
def intern_home(request, token):
    """Legacy token-based intern home page"""
    projects = Project.objects.all()
    try:
        preference = ProjectPreference.objects.get(intern=request.intern)
        if preference.is_submitted:
            return render(request, 'intern_portal/preferences_submitted.html', {
                'intern': request.intern,
                'preference': preference
            })
    except ProjectPreference.DoesNotExist:
        preference = None

    return render(request, 'intern_portal/intern_home.html', {
        'intern': request.intern,
        'projects': projects,
        'preference': preference
    })

@verify_token
def project_detail(request, token, pk):
    """Legacy token-based project detail page"""
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'intern_portal/project_detail.html', {
        'project': project,
        'intern': request.intern
    })

@verify_token
def submit_preferences(request, token):
    """Legacy token-based preferences submission"""
    try:
        preference = ProjectPreference.objects.get(intern=request.intern)
        if preference.is_submitted:
            messages.error(request, 'Tercihleriniz zaten kaydedilmiş.')
            return redirect('intern_home', token=token)
    except ProjectPreference.DoesNotExist:
        preference = None

    if request.method == 'POST':
        form = ProjectPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            preference = form.save(commit=False)
            preference.intern = request.intern
            preference.is_submitted = True
            preference.save()
            messages.success(request, 'Tercihleriniz başarıyla kaydedildi.')
            return redirect('intern_home', token=token)
    else:
        form = ProjectPreferenceForm(instance=preference)

    return render(request, 'intern_portal/submit_preferences.html', {
        'form': form,
        'intern': request.intern,
        'preference': preference
    })

@verify_token
def legacy_select_availability(request, token):
    """UPDATED: Legacy token-based availability selection - backwards compatible"""
    # Define available days and time slots (keep legacy format for compatibility)
    DAYS = [
        ('monday', 'Pazartesi'),
        ('tuesday', 'Salı'),
        ('wednesday', 'Çarşamba'),
        ('thursday', 'Perşembe'),
        ('friday', 'Cuma'),
        ('saturday', 'Cumartesi'),
    ]
    
    # For legacy, combine all time slots
    TIME_SLOTS = [
        ('00:00-01:00', '00:00-01:00'),
        ('01:00-02:00', '01:00-02:00'),
        ('02:00-03:00', '02:00-03:00'),
        ('03:00-04:00', '03:00-04:00'),
        ('04:00-05:00', '04:00-05:00'),
        ('05:00-06:00', '05:00-06:00'),
        ('06:00-07:00', '06:00-07:00'),
        ('07:00-08:00', '07:00-08:00'),
        ('08:00-09:00', '08:00-09:00'),
        ('09:00-10:00', '09:00-10:00'),
        ('10:00-11:00', '10:00-11:00'),
        ('11:00-12:00', '11:00-12:00'),
        ('12:00-13:00', '12:00-13:00'),
        ('13:00-14:00', '13:00-14:00'),
        ('14:00-15:00', '14:00-15:00'),
        ('15:00-16:00', '15:00-16:00'),
        ('16:00-17:00', '16:00-17:00'),
        ('17:00-18:00', '17:00-18:00'),
        ('18:00-19:00', '18:00-19:00'),
        ('19:00-20:00', '19:00-20:00'),
        ('20:00-21:00', '20:00-21:00'),
        ('21:00-22:00', '21:00-22:00'),
        ('22:00-23:00', '22:00-23:00'),
        ('23:00-00:00', '23:00-24:00'),
    ]
    
    # Get or create availability record for the intern
    try:
        availability = InternAvailability.objects.get(intern=request.intern)
    except InternAvailability.DoesNotExist:
        availability = InternAvailability.objects.create(
            intern=request.intern,
            group_meeting_data={},
            individual_work_data={}
        )
    
    if request.method == 'POST':
        # Process the submitted availability data (legacy format - combine into individual work)
        new_individual_data = {}
        
        for day_code, _ in DAYS:
            # Get selected time slots for this day
            selected_slots = request.POST.getlist(f'availability_{day_code}')
            
            # Validate that selected slots are in our valid time slots
            valid_slot_values = [slot[0] for slot in TIME_SLOTS]
            valid_slots = [slot for slot in selected_slots if slot in valid_slot_values]
            
            if valid_slots:
                new_individual_data[day_code] = valid_slots
        
        # Update the availability record (legacy saves to individual work data)
        availability.individual_work_data = new_individual_data
        availability.group_meeting_data = {}  # Clear group data for legacy
        availability.save()
        
        # Show success message
        total_hours = sum(len(slots) for slots in new_individual_data.values())
        if total_hours > 0:
            messages.success(request, f'Ortak çalışma saati durumunuz başarıyla kaydedildi! Toplam {total_hours} saat ortak çalışma saati belirttiniz.')
        else:
            messages.info(request, 'Ortak çalışma saati durumunuz temizlendi.')
        
        return redirect('legacy_select_availability', token=token)
    
    # Prepare context for template (legacy format - combine both data types)
    legacy_availability_data = {}
    
    # Combine group meeting and individual work data for legacy display
    for day_code in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
        combined_slots = []
        if availability.group_meeting_data:
            combined_slots.extend(availability.group_meeting_data.get(day_code, []))
        if availability.individual_work_data:
            combined_slots.extend(availability.individual_work_data.get(day_code, []))
        if combined_slots:
            legacy_availability_data[day_code] = combined_slots
    
    context = {
        'intern': request.intern,
        'availability': availability,
        'days': DAYS,
        'time_slots': TIME_SLOTS,
        'availability_data': json.dumps(legacy_availability_data),
    }
    
    return render(request, 'intern_portal/select_availability.html', context)