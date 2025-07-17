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
    # Link to Django's User model (for Google SSO) - NEW
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kullanıcı')
    
    # Basic information
    first_name = models.CharField(max_length=100, verbose_name='Ad')
    last_name = models.CharField(max_length=100, verbose_name='Soyad')
    email = models.EmailField(unique=True, verbose_name='E-posta')
    
    # Legacy access token (keeping for backward compatibility with existing interns)
    access_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Erişim Token')
    
    # Assigned projects (NEW - for admin assignments)
    assigned_projects = models.ManyToManyField(
        Project, 
        blank=True, 
        related_name='assigned_interns',
        verbose_name='Atanmış Projeler',
        help_text='Bu stajyere atanmış projeler (admin tarafından)'
    )
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_assigned_projects_count(self):
        """Atanmış proje sayısını döndürür"""
        return self.assigned_projects.count()
    
    def get_assigned_projects_list(self):
        """Atanmış projelerin listesini döndürür"""
        return list(self.assigned_projects.all())
    
    def has_assigned_projects(self):
        """Atanmış proje var mı kontrol eder"""
        return self.assigned_projects.exists()
    
    def has_google_auth(self):
        """Google SSO ile giriş yapabilir mi kontrol eder"""
        return self.user is not None
    
    def get_auth_method(self):
        """Kimlik doğrulama metodunu döndürür"""
        if self.user:
            return "Google SSO"
        else:
            return "Token-based (Legacy)"

    class Meta:
        verbose_name = 'Stajyer'
        verbose_name_plural = 'Stajyerler'
        ordering = ['first_name', 'last_name']

class ProjectPreference(models.Model):
    """
    Existing project preference model - KEPT for backward compatibility
    This handles the old preference system where interns choose their top 3 projects
    """
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

class InternAvailability(models.Model):
    intern = models.OneToOneField(Intern, on_delete=models.CASCADE, related_name='availability')
    availability_data = models.JSONField(
        default=dict,
        help_text='JSON formatında haftalık ortak çalışma saati verileri. Format: {"monday": ["09:00-10:00", "10:00-11:00", ...], "tuesday": [...], ...}'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Stajyer Ortak Çalışma Saati'
        verbose_name_plural = 'Stajyer Ortak Çalışma Saatleri'

    def __str__(self):
        return f"{self.intern.get_full_name()} - Ortak Çalışma Saati"

    def get_availability_for_day(self, day):
        """Belirli bir gün için ortak çalışma saatlerini döndürür"""
        return self.availability_data.get(day, [])

    def has_availability_for_day(self, day):
        """Belirli bir gün için ortak çalışma saati var mı kontrol eder"""
        return bool(self.availability_data.get(day, []))

    def get_total_hours(self):
        """Toplam ortak çalışma saati sayısını döndürür"""
        total = 0
        for day_slots in self.availability_data.values():
            total += len(day_slots)
        return total

    def get_available_days(self):
        """Ortak çalışma saati olan günleri döndürür"""
        return [day for day, slots in self.availability_data.items() if slots]