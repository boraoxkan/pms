from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Project, ProjectPreference, Intern
from .forms import ProjectPreferenceForm

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
