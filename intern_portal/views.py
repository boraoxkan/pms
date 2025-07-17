from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Project, ProjectPreference, Intern, InternAvailability
from .forms import ProjectPreferenceForm
import json

def verify_token(view_func):
    def wrapper(request, token, *args, **kwargs):
        try:
            intern = Intern.objects.get(access_token=token, is_active=True)
            request.intern = intern
            return view_func(request, token, *args, **kwargs)
        except (Intern.DoesNotExist, ValueError):
            raise Http404("Geçersiz veya süresi dolmuş bağlantı.")
    return wrapper

@verify_token
def intern_home(request, token):
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
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'intern_portal/project_detail.html', {
        'project': project,
        'intern': request.intern
    })

@verify_token
def submit_preferences(request, token):
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
def select_availability(request, token):
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
        
        return redirect('select_availability', token=token)
    
    # Prepare context for template
    context = {
        'intern': request.intern,
        'availability': availability,
        'days': DAYS,
        'time_slots': TIME_SLOTS,
        'availability_data': json.dumps(availability.availability_data),
    }
    
    return render(request, 'intern_portal/select_availability.html', context)