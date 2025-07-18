from django.urls import path
from . import views

urlpatterns = [
    # New homepage (public)
    path('', views.home_page, name='home_page'),
    
    # New Google SSO authenticated routes
    path('portal/availability/', views.select_availability, name='select_availability'),
    path('portal/availability/view/', views.view_availability, name='view_availability'),
    path('portal/team-availability/', views.team_availability, name='team_availability'),  # NEW
    
    # Legacy token-based routes (kept for backward compatibility)
    path('intern/<uuid:token>/', views.intern_home, name='intern_home'),
    path('intern/<uuid:token>/project/<int:pk>/', views.project_detail, name='project_detail'),
    path('intern/<uuid:token>/preferences/', views.submit_preferences, name='submit_preferences'),
    path('intern/<uuid:token>/availability/', views.legacy_select_availability, name='legacy_select_availability'),
]