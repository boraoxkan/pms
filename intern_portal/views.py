from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from .models import Project, ProjectPreference, Intern, InternAvailability
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
    New homepage with Google SSO login
    """
    # Don't redirect if user is authenticated - always show the homepage
    # Users can navigate manually if they want to go to availability
    return render(request, 'intern_portal/home_page.html')

@login_required
def select_availability(request):
    """
    New availability view for Google SSO authenticated users
    """
    # Check if user is admin (staff/superuser)
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, 'Admin kullanıcıları için müsaitlik sistemi kullanılmaz. Lütfen admin panelini kullanın.')
        return redirect('/admin/')
    
    # Get the intern object linked to the authenticated user
    # The adapter should have already linked them, so this should always work
    try:
        intern = Intern.objects.get(user=request.user)
    except Intern.DoesNotExist:
        # This should not happen if the adapter worked correctly
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
        
        return redirect('select_availability')
    
    # Prepare context for template
    context = {
        'intern': intern,
        'availability': availability,
        'days': DAYS,
        'time_slots': TIME_SLOTS,
        'availability_data': json.dumps(availability.availability_data),
    }
    
    return render(request, 'intern_portal/select_availability.html', context)

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

# Add this to your views.py for detailed debugging

from django.http import HttpResponse
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.views import oauth2_login
from django.conf import settings
from django.urls import reverse

def debug_detailed_oauth(request):
    """Detailed OAuth debugging"""
    html = "<h1>Detailed OAuth Debug</h1>"
    
    # 1. Check basic configuration
    html += "<h2>1. Basic Configuration</h2>"
    html += f"<p><strong>SITE_ID:</strong> {getattr(settings, 'SITE_ID', 'NOT SET')}</p>"
    html += f"<p><strong>SOCIALACCOUNT_LOGIN_ON_GET:</strong> {getattr(settings, 'SOCIALACCOUNT_LOGIN_ON_GET', 'NOT SET')}</p>"
    html += f"<p><strong>Current domain:</strong> {request.get_host()}</p>"
    
    # 2. Check sites
    html += "<h2>2. Sites Configuration</h2>"
    try:
        current_site = Site.objects.get(pk=settings.SITE_ID)
        html += f"<p><strong>Current Site:</strong> {current_site.domain} (ID: {current_site.id})</p>"
        if current_site.domain != request.get_host():
            html += f"<p style='color: red;'><strong>⚠️ MISMATCH:</strong> Site domain ({current_site.domain}) != Request host ({request.get_host()})</p>"
    except Site.DoesNotExist:
        html += f"<p style='color: red;'><strong>❌ ERROR:</strong> Site with ID {settings.SITE_ID} does not exist</p>"
    
    # 3. Check Google app
    html += "<h2>3. Google OAuth App</h2>"
    try:
        google_app = SocialApp.objects.get(provider='google')
        html += f"<p><strong>Google App Found:</strong> ✅</p>"
        html += f"<p><strong>Client ID:</strong> {google_app.client_id[:20]}...</p>"
        html += f"<p><strong>Has Secret:</strong> {'✅' if google_app.secret else '❌'}</p>"
        html += f"<p><strong>App Sites:</strong> {[s.domain for s in google_app.sites.all()]}</p>"
        
        # Check if current site is linked to Google app
        if current_site in google_app.sites.all():
            html += f"<p><strong>Site Linked:</strong> ✅</p>"
        else:
            html += f"<p style='color: red;'><strong>❌ Site NOT linked to Google app</strong></p>"
            
    except SocialApp.DoesNotExist:
        html += f"<p style='color: red;'><strong>❌ Google OAuth app not found</strong></p>"
    
    # 4. Test URL generation
    html += "<h2>4. URL Testing</h2>"
    try:
        from allauth.socialaccount.providers.google.urls import urlpatterns as google_urls
        html += f"<p><strong>Google URLs loaded:</strong> ✅ ({len(google_urls)} patterns)</p>"
    except Exception as e:
        html += f"<p style='color: red;'><strong>❌ Google URLs error:</strong> {e}</p>"
    
    # 5. Test OAuth URL generation
    html += "<h2>5. OAuth URL Generation</h2>"
    try:
        from allauth.socialaccount.providers import registry
        google_provider = registry.by_id('google')
        html += f"<p><strong>Google Provider:</strong> ✅ {google_provider}</p>"
        
        # Try to get the OAuth URL
        oauth_url = google_provider.get_login_url(request)
        html += f"<p><strong>OAuth URL:</strong> <a href='{oauth_url}' target='_blank'>{oauth_url}</a></p>"
        
        if 'accounts.google.com' in oauth_url:
            html += f"<p style='color: green;'><strong>✅ OAuth URL looks correct</strong></p>"
        else:
            html += f"<p style='color: red;'><strong>❌ OAuth URL doesn't point to Google</strong></p>"
            
    except Exception as e:
        html += f"<p style='color: red;'><strong>❌ OAuth URL generation error:</strong> {e}</p>"
    
    # 6. Test direct access
    html += "<h2>6. Direct Access Test</h2>"
    from django.test import Client
    client = Client()
    try:
        response = client.get('/accounts/google/login/', HTTP_HOST=request.get_host())
        html += f"<p><strong>Direct access status:</strong> {response.status_code}</p>"
        if response.status_code == 302:
            html += f"<p><strong>Redirects to:</strong> <a href='{response.url}' target='_blank'>{response.url}</a></p>"
        elif response.status_code == 200:
            html += f"<p style='color: orange;'><strong>Shows page (should redirect)</strong></p>"
        else:
            html += f"<p style='color: red;'><strong>Unexpected status</strong></p>"
    except Exception as e:
        html += f"<p style='color: red;'><strong>Direct access error:</strong> {e}</p>"
    
    # 7. Recommendations
    html += "<h2>7. Recommendations</h2>"
    html += "<ul>"
    
    try:
        current_site = Site.objects.get(pk=settings.SITE_ID)
        if current_site.domain != request.get_host():
            html += f"<li style='color: red;'>Update site domain to match request host: <code>python manage.py setup_dev_oauth --domain='{request.get_host()}'</code></li>"
    except:
        pass
    
    try:
        google_app = SocialApp.objects.get(provider='google')
        if current_site not in google_app.sites.all():
            html += f"<li style='color: red;'>Link Google app to current site</li>"
    except:
        html += f"<li style='color: red;'>Create Google OAuth app</li>"
    
    html += f"<li>Ensure Google Console has redirect URI: <code>http://{request.get_host()}/accounts/google/login/callback/</code></li>"
    html += "</ul>"
    
    return HttpResponse(html)

# Add this URL to your urls.py: