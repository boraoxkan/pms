from django.urls import path
from . import views

urlpatterns = [
    path('intern/<uuid:token>/', views.intern_home, name='intern_home'),
    path('intern/<uuid:token>/project/<int:pk>/', views.project_detail, name='project_detail'),
    path('intern/<uuid:token>/preferences/', views.submit_preferences, name='submit_preferences'),
] 