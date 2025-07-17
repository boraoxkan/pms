from django.db import models
from django.contrib.auth.models import User
import uuid
import os

# Create your models here.

class Project(models.Model):
    WORK_TYPE_CHOICES = [
        ('remote', 'Uzaktan Çalışma'),
        ('hybrid', 'Hibrit Çalışma'),
        ('office', 'Ofisten Çalışma'),
    ]

    DURATION_CHOICES = [
        ('2', '2 Ay'),
        ('3', '3 Ay'),
        ('4', '4 Ay'),
    ]

    TEAM_SIZE_CHOICES = [
        ('1', '1 Kişilik'),
        ('2-3', '2-3 Kişilik'),
        ('3-4', '3-4 Kişilik'),
        ('4+', '4+ Kişilik'),
    ]

    name = models.CharField(max_length=100, verbose_name='Proje Adı')
    short_description = models.TextField(verbose_name='Kısa Açıklama')
    full_description = models.TextField(verbose_name='Detaylı Açıklama', help_text='HTML formatında yazabilirsiniz.')
    team_size = models.CharField(max_length=10, choices=TEAM_SIZE_CHOICES, default='2-3', verbose_name='Ekip Büyüklüğü')
    work_type = models.CharField(max_length=10, choices=WORK_TYPE_CHOICES, default='remote', verbose_name='Çalışma Şekli')
    duration = models.CharField(max_length=5, choices=DURATION_CHOICES, default='3', verbose_name='Staj Süresi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Proje'
        verbose_name_plural = 'Projeler'

class Intern(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    access_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Stajyer'
        verbose_name_plural = 'Stajyerler'

class ProjectPreference(models.Model):
    intern = models.OneToOneField(Intern, on_delete=models.CASCADE)
    first_choice = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='first_choices')
    second_choice = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='second_choices')
    third_choice = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='third_choices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Proje Tercihi'
        verbose_name_plural = 'Proje Tercihleri'

    def __str__(self):
        return f"{self.intern.get_full_name()} - Proje Tercihleri"
