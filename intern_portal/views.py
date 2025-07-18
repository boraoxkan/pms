from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils import timezone  # ADDED: Missing import
from .models import Project, ProjectPreference, Intern, InternAvailability, AvailabilitySettings  # ADDED: Missing models
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
            # FIXED: Get intern object and related data
            intern = Intern.objects.get(user=request.user)
            
            # Get assigned projects for this intern
            assigned_projects = intern.assigned_projects.all()
            
            # Check if intern has availability data
            has_availability = False
            availability_data = None
            try:
                availability = InternAvailability.objects.get(intern=intern)
                has_availability = bool(availability.availability_data and 
                                      any(slots for slots in availability.availability_data.values()))
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
            # This could happen if admin hasn't created intern record yet
            pass
    
    return render(request, 'intern_portal/home_page.html', context)

@login_required
def team_availability(request):
    """
    Display team availability calendar for Google SSO authenticated users
    Shows combined availability of all teammates (interns assigned to same projects)
    Displays full 24-hour time range (00:00 to 23:00)
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
    
    # Get teammate objects with their assigned projects
    teammates = Intern.objects.filter(id__in=teammate_ids, is_active=True).prefetch_related('assigned_projects')
    
    # Create a detailed teammates list with ONLY common projects
    teammates_with_projects = []
    for teammate in teammates:
        teammate_projects = teammate.assigned_projects.all()
        # Find common projects between current intern and this teammate
        common_projects = assigned_projects.intersection(teammate_projects)
        
        # Only include teammates who have common projects (they should by definition, but safety check)
        if common_projects.exists():
            teammates_with_projects.append({
                'intern': teammate,
                'common_projects': common_projects,  # Only show common projects
                'common_projects_count': common_projects.count(),
                'has_availability': False,
                'availability_data': None
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
    
    # Group time slots by periods for better organization
    TIME_PERIODS = {
        'Gece (00:00 - 06:00)': TIME_SLOTS[0:6],
        'Sabah (06:00 - 12:00)': TIME_SLOTS[6:12],
        'Öğleden Sonra (12:00 - 18:00)': TIME_SLOTS[12:18],
        'Akşam (18:00 - 24:00)': TIME_SLOTS[18:24]
    }
    
    # Initialize the calendar structure
    team_calendar = {}
    for day in WEEKDAYS:
        team_calendar[day] = {}
        for time_slot in TIME_SLOTS:
            team_calendar[day][time_slot] = []
    
    # Fetch availability data for all teammates
    teammate_availabilities = InternAvailability.objects.filter(
        intern__in=teammates
    ).select_related('intern')
    
    # Create a mapping of intern ID to availability for easy lookup
    availability_map = {}
    for availability in teammate_availabilities:
        availability_map[availability.intern.id] = availability
    
    # Update teammates_with_projects with availability data
    for teammate_data in teammates_with_projects:
        intern_id = teammate_data['intern'].id
        if intern_id in availability_map:
            availability = availability_map[intern_id]
            teammate_data['has_availability'] = bool(availability.availability_data and 
                                                  any(slots for slots in availability.availability_data.values()))
            teammate_data['availability_data'] = availability
    
    # Process each teammate's availability for the calendar
    for availability in teammate_availabilities:
        intern_name = availability.intern.get_full_name()
        
        if availability.availability_data:
            for day_code, time_slots in availability.availability_data.items():
                if day_code in WEEKDAYS and time_slots:
                    for time_slot in time_slots:
                        if time_slot in TIME_SLOTS:
                            team_calendar[day_code][time_slot].append(intern_name)
    
    # Create a more template-friendly structure
    calendar_grid = []
    for day in WEEKDAYS:
        day_data = {
            'day_code': day,
            'day_name': DAY_NAMES[day],
            'time_slots': []
        }
        for time_slot in TIME_SLOTS:
            available_teammates = team_calendar[day][time_slot]
            day_data['time_slots'].append({
                'time': time_slot,
                'time_display': time_slot.replace('-', ' - '),  # Format for display
                'available_count': len(available_teammates),
                'available_teammates': available_teammates
            })
        calendar_grid.append(day_data)
    
    # Calculate some statistics
    total_teammates = teammates.count()
    teammates_with_availability = teammate_availabilities.count()
    
    # Get current intern's projects for context
    current_intern_projects = list(assigned_projects.values('name', 'id'))
    
    # Find peak availability times (times when most people are available)
    peak_times = []
    max_availability = 0
    
    for day in WEEKDAYS:
        for time_slot in TIME_SLOTS:
            count = len(team_calendar[day][time_slot])
            if count > max_availability:
                max_availability = count
                peak_times = [(DAY_NAMES[day], time_slot)]
            elif count == max_availability and count > 0:
                peak_times.append((DAY_NAMES[day], time_slot))
    
    # Calculate availability statistics by time period
    period_stats = {}
    for period_name, period_slots in TIME_PERIODS.items():
        total_availability = 0
        for day in WEEKDAYS:
            for time_slot in period_slots:
                total_availability += len(team_calendar[day][time_slot])
        period_stats[period_name] = total_availability
    
    # Find most active period
    most_active_period = max(period_stats.items(), key=lambda x: x[1]) if period_stats else None
    
    context = {
        'current_intern': current_intern,
        'teammates': teammates,  # Keep original for backward compatibility
        'teammates_with_projects': teammates_with_projects,  # New enhanced data with only common projects
        'assigned_projects': assigned_projects,
        'current_intern_projects': current_intern_projects,
        'team_calendar': team_calendar,
        'calendar_grid': calendar_grid,
        'time_slots': TIME_SLOTS,
        'time_periods': TIME_PERIODS,
        'weekdays': WEEKDAYS,
        'day_names': DAY_NAMES,
        'total_teammates': total_teammates,
        'teammates_with_availability': teammates_with_availability,
        'peak_times': peak_times,
        'max_availability': max_availability,
        'period_stats': period_stats,
        'most_active_period': most_active_period,
    }
    
    return render(request, 'intern_portal/team_availability.html', context)

@login_required
def select_availability(request):
    """
    Availability selection view for Google SSO authenticated users
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
    
    # Define available days and time slots
    DAYS = [
        ('monday', 'Pazartesi'),
        ('tuesday', 'Salı'),
        ('wednesday', 'Çarşamba'),
        ('thursday', 'Perşembe'),
        ('friday', 'Cuma'),
        ('saturday', 'Cumartesi'),
    ]
    
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
        availability = InternAvailability.objects.get(intern=intern)
    except InternAvailability.DoesNotExist:
        availability = InternAvailability.objects.create(
            intern=intern,
            availability_data={}
        )
    
    # Check if user can modify availability
    if not availability.can_modify():
        settings = AvailabilitySettings.get_settings()
        if availability.is_locked:
            messages.error(
                request,
                'Müsaitlik durumunuz yönetici tarafından kilitlenmiş. '
                'Değişiklik yapmak için lütfen sistem yöneticisi ile iletişime geçin.'
            )
        elif settings.weekly_submission_enabled and availability.week_year:
            messages.warning(
                request,
                f'Bu hafta için müsaitlik durumunuzu zaten belirttiniz. '
                f'Değişiklik yapmak için lütfen sistem yöneticisi ile iletişime geçin.'
            )
        return redirect('view_availability')
    
    if request.method == 'POST':
        # Process the submitted availability data
        new_availability_data = {}
        
        for day_code, _ in DAYS:
            # Get selected time slots for this day
            selected_slots = request.POST.getlist(f'availability_{day_code}')
            
            # Validate that selected slots are in our valid time slots
            valid_slot_values = [slot[0] for slot in TIME_SLOTS]
            valid_slots = [slot for slot in selected_slots if slot in valid_slot_values]
            
            if valid_slots:
                new_availability_data[day_code] = valid_slots
        
        try:
            # Update the availability record
            availability.availability_data = new_availability_data
            availability.week_year = availability.get_current_week_year()
            availability.submission_date = timezone.now()
            
            # This will trigger validation in the save method
            availability.save()
            
            # Show success message
            total_hours = sum(len(slots) for slots in new_availability_data.values())
            messages.success(
                request, 
                f'Ortak çalışma saati durumunuz başarıyla kaydedildi! '
                f'Toplam {total_hours} saat ortak çalışma saati belirttiniz.'
            )
            return redirect('view_availability')
           
        except Exception as e:
            # Handle validation errors from the model
            messages.error(request, str(e))
            # Don't redirect, show form again with error
   
    # For GET requests, prepare context for template
    saved_availability = {}
    if availability.availability_data:
        for day_code, slots in availability.availability_data.items():
            saved_availability[day_code] = slots
   
    # Add settings info to context
    settings = AvailabilitySettings.get_settings()
    context = {
        'intern': intern,
        'availability': availability,
        'days': DAYS,
        'time_slots': TIME_SLOTS,
        'saved_availability': saved_availability,
        'settings': settings,
        'can_modify': availability.can_modify(),
        'is_locked': availability.is_locked,
        'current_week_submission': availability.is_current_week_submission() if availability.week_year else False,
    }
   
    return render(request, 'intern_portal/select_availability.html', context)

@login_required
def view_availability(request):
    """
    Read-only view to display saved availability for Google SSO authenticated users
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
    formatted_availability = {}
    total_hours = 0
    
    if availability.availability_data:
        for day_code, time_slots in availability.availability_data.items():
            if time_slots:  # Only include days with selected times
                formatted_availability[DAY_NAMES.get(day_code, day_code)] = time_slots
                total_hours += len(time_slots)
    
    # Check if user has any availability set
    has_availability = total_hours > 0
    
    context = {
        'intern': intern,
        'availability': availability,
        'formatted_availability': formatted_availability,
        'total_hours': total_hours,
        'has_availability': has_availability,
        'available_days_count': len(formatted_availability),
    }
    
    return render(request, 'intern_portal/view_availability.html', context)

# ================================
# LEGACY VIEWS (Token-based)
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
    """Legacy token-based availability selection"""
    # Define available days and time slots
    DAYS = [
        ('monday', 'Pazartesi'),
        ('tuesday', 'Salı'),
        ('wednesday', 'Çarşamba'),
        ('thursday', 'Perşembe'),
        ('friday', 'Cuma'),
        ('saturday', 'Cumartesi'),
    ]
    
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
            availability_data={}
        )
    
    if request.method == 'POST':
        # Process the submitted availability data
        new_availability_data = {}
        
        for day_code, _ in DAYS:
            # Get selected time slots for this day
            selected_slots = request.POST.getlist(f'availability_{day_code}')
            
            # Validate that selected slots are in our valid time slots
            valid_slot_values = [slot[0] for slot in TIME_SLOTS]
            valid_slots = [slot for slot in selected_slots if slot in valid_slot_values]
            
            if valid_slots:
                new_availability_data[day_code] = valid_slots
        
        # Update the availability record
        availability.availability_data = new_availability_data
        availability.save()
        
        # Show success message
        total_hours = sum(len(slots) for slots in new_availability_data.values())
        if total_hours > 0:
            messages.success(request, f'Ortak çalışma saati durumunuz başarıyla kaydedildi! Toplam {total_hours} saat ortak çalışma saati belirttiniz.')
        else:
            messages.info(request, 'Ortak çalışma saati durumunuz temizlendi.')
        
        return redirect('legacy_select_availability', token=token)
    
    # Prepare context for template
    context = {
        'intern': request.intern,
        'availability': availability,
        'days': DAYS,
        'time_slots': TIME_SLOTS,
        'availability_data': json.dumps(availability.availability_data),
    }
    
    return render(request, 'intern_portal/select_availability.html', context)