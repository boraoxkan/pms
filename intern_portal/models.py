from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from django.utils import timezone
from image_cropping import ImageRatioField, ImageCropField # MODIFIED: Add ImageCropField

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
    
    # MODIFIED: Changed from models.ImageField to ImageCropField
    profile_picture = ImageCropField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        verbose_name='Profil Fotoğrafı',
        help_text='Stajyer profil fotoğrafı (opsiyonel) - Yükleme sonrası kırpma yapabilirsiniz'
    )
    
    # This part should be correct
    cropping = ImageRatioField(
        'profile_picture',
        '350x350',
        verbose_name='Fotoğraf Kırpma',
        help_text='Profil fotoğrafını kare şeklinde kırpmak için kullanın'
    )
    
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

    # UPDATED: Profile picture helper methods with cropping support
    def has_profile_picture(self):
        """Profil fotoğrafı var mı kontrol eder"""
        return bool(self.profile_picture)
    
    def get_profile_picture_url(self, size='profile_large'):
        """Profil fotoğrafı URL'sini döndürür (kırpılmış versiyon)"""
        if self.profile_picture:
            from easy_thumbnails.files import get_thumbnailer
            try:
                thumbnailer = get_thumbnailer(self.profile_picture)
                if self.cropping:
                    # Use cropped version
                    thumbnail = thumbnailer.get_thumbnail({
                        'size': (350, 350) if size == 'profile_large' else (150, 150) if size == 'profile_medium' else (60, 60),
                        'box': self.cropping,
                        'crop': True,
                        'quality': 95
                    })
                    return thumbnail.url
                else:
                    # Use default thumbnail settings
                    thumbnail = thumbnailer.get_thumbnail({'size': (350, 350), 'crop': True, 'quality': 95})
                    return thumbnail.url
            except:
                # Fallback to original image if thumbnailing fails
                return self.profile_picture.url
        return None

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

class AvailabilitySettings(models.Model):
    """
    UPDATED: Global settings for availability system with separate hour requirements
    """
    # UPDATED: Split into two separate fields
    group_meeting_hours_min = models.PositiveIntegerField(
        default=20,
        verbose_name='Minimum Group Meeting Hours',
        help_text='Minimum required group meeting hours (09:00-17:00) per week'
    )
    individual_work_hours_min = models.PositiveIntegerField(
        default=10,
        verbose_name='Minimum Individual Work Hours',
        help_text='Minimum required individual work hours (any time) per week'
    )
    weekly_submission_enabled = models.BooleanField(
        default=True,
        verbose_name='Enable Weekly Submission Limit',
        help_text='If enabled, interns can only submit once per week'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Availability System Settings'
        verbose_name_plural = 'Availability System Settings'

    def __str__(self):
        return f"Group Meeting: {self.group_meeting_hours_min}h, Individual: {self.individual_work_hours_min}h, Weekly Limit: {self.weekly_submission_enabled}"

    @classmethod
    def get_settings(cls):
        """Get or create the settings object"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'group_meeting_hours_min': 20,
                'individual_work_hours_min': 10,
                'weekly_submission_enabled': True
            }
        )
        return settings

class InternAvailability(models.Model):
    intern = models.OneToOneField(Intern, on_delete=models.CASCADE, related_name='availability')
    
    # UPDATED: Split availability data into two types
    group_meeting_data = models.JSONField(
        default=dict,
        help_text='JSON formatında grup toplantı saatleri (09:00-17:00). Format: {"monday": ["09:00-10:00", "10:00-11:00", ...], "tuesday": [...], ...}'
    )
    individual_work_data = models.JSONField(
        default=dict,
        help_text='JSON formatında bireysel çalışma saatleri (24 saat). Format: {"monday": ["00:00-01:00", "01:00-02:00", ...], "tuesday": [...], ...}'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Weekly submission control fields
    week_year = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Week number and year (YYYYWW format) when this was submitted'
    )
    submission_date = models.DateTimeField(
        null=True, blank=True,
        help_text='When this availability was last submitted'
    )
    is_locked = models.BooleanField(
        default=False,
        help_text='If true, intern cannot modify until admin unlocks'
    )

    class Meta:
        verbose_name = 'Stajyer Ortak Çalışma Saati'
        verbose_name_plural = 'Stajyer Ortak Çalışma Saatleri'

    def __str__(self):
        return f"{self.intern.get_full_name()} - Ortak Çalışma Saati"

    # UPDATED: Methods for group meeting hours
    def get_group_meeting_for_day(self, day):
        """Belirli bir gün için grup toplantı saatlerini döndürür"""
        return self.group_meeting_data.get(day, [])

    def has_group_meeting_for_day(self, day):
        """Belirli bir gün için grup toplantı saati var mı kontrol eder"""
        return bool(self.group_meeting_data.get(day, []))

    def get_group_meeting_hours(self):
        """Toplam grup toplantı saati sayısını döndürür"""
        total = 0
        for day_slots in self.group_meeting_data.values():
            total += len(day_slots)
        return total

    def get_group_meeting_days(self):
        """Grup toplantı saati olan günleri döndürür"""
        return [day for day, slots in self.group_meeting_data.items() if slots]

    # UPDATED: Methods for individual work hours
    def get_individual_work_for_day(self, day):
        """Belirli bir gün için bireysel çalışma saatlerini döndürür"""
        return self.individual_work_data.get(day, [])

    def has_individual_work_for_day(self, day):
        """Belirli bir gün için bireysel çalışma saati var mı kontrol eder"""
        return bool(self.individual_work_data.get(day, []))

    def get_individual_work_hours(self):
        """Toplam bireysel çalışma saati sayısını döndürür"""
        total = 0
        for day_slots in self.individual_work_data.values():
            total += len(day_slots)
        return total

    def get_individual_work_days(self):
        """Bireysel çalışma saati olan günleri döndürür"""
        return [day for day, slots in self.individual_work_data.items() if slots]

    # LEGACY: Keep these methods for backward compatibility
    def get_availability_for_day(self, day):
        """LEGACY: Combined availability for a day"""
        group_slots = self.group_meeting_data.get(day, [])
        individual_slots = self.individual_work_data.get(day, [])
        return group_slots + individual_slots

    def has_availability_for_day(self, day):
        """LEGACY: Check if any availability exists for a day"""
        return self.has_group_meeting_for_day(day) or self.has_individual_work_for_day(day)

    def get_total_hours(self):
        """LEGACY: Total combined hours"""
        return self.get_group_meeting_hours() + self.get_individual_work_hours()

    def get_available_days(self):
        """LEGACY: Days with any availability"""
        group_days = set(self.get_group_meeting_days())
        individual_days = set(self.get_individual_work_days())
        return list(group_days.union(individual_days))

    def get_current_week_year(self):
        """Get current week in YYYYWW format"""
        from datetime import datetime
        now = datetime.now()
        year, week, _ = now.isocalendar()
        return int(f"{year}{week:02d}")

    def is_current_week_submission(self):
        """Check if this submission is for the current week"""
        current_week = self.get_current_week_year()
        return self.week_year == current_week

    def can_modify(self):
        """FIXED: Check if the intern can modify their availability"""
        if self.is_locked:
            return False
        
        settings = AvailabilitySettings.get_settings()
        if not settings.weekly_submission_enabled:
            return True
            
        # If weekly limit is enabled and there's a submission date, check if it's same week
        if self.submission_date and self.week_year:
            current_week = self.get_current_week_year()
            return current_week != self.week_year
            
        # If no submission yet, can modify
        return True

    def validate_minimum_hours(self):
        """UPDATED: Validate that both minimum hour requirements are met"""
        settings = AvailabilitySettings.get_settings()
        group_hours = self.get_group_meeting_hours()
        individual_hours = self.get_individual_work_hours()
        
        errors = []
        
        if group_hours < settings.group_meeting_hours_min:
            errors.append(
                f'Grup toplantı saatleri için en az {settings.group_meeting_hours_min} saat seçmelisiniz. '
                f'Şu anda {group_hours} saat seçtiniz.'
            )
            
        if individual_hours < settings.individual_work_hours_min:
            errors.append(
                f'Bireysel çalışma saatleri için en az {settings.individual_work_hours_min} saat seçmelisiniz. '
                f'Şu anda {individual_hours} saat seçtiniz.'
            )
        
        if errors:
            from django.core.exceptions import ValidationError
            raise ValidationError(' | '.join(errors))

    def get_availability_summary(self):
        """UPDATED: Get a formatted summary including both types"""
        if not self.group_meeting_data and not self.individual_work_data:
            return '<span style="color: red;">Henüz ortak çalışma saati belirtilmemiş</span>'
        
        day_names = {
            'monday': 'Pazartesi',
            'tuesday': 'Salı',
            'wednesday': 'Çarşamba',
            'thursday': 'Perşembe',
            'friday': 'Cuma',
            'saturday': 'Cumartesi'
        }
        
        summary_html = '<div style="max-width: 600px;">'
        
        # Group meeting hours section
        summary_html += '<h4 style="color: #3b82f6;">Grup Toplantı Saatleri</h4>'
        for day_code, day_name in day_names.items():
            slots = self.group_meeting_data.get(day_code, [])
            if slots:
                slots_str = ', '.join(slots)
                summary_html += f'<p><strong>{day_name}:</strong> {slots_str}</p>'
            else:
                summary_html += f'<p><strong>{day_name}:</strong> <span style="color: gray;">Yok</span></p>'
        
        # Individual work hours section
        summary_html += '<h4 style="color: #10b981;">Bireysel Çalışma Saatleri</h4>'
        for day_code, day_name in day_names.items():
            slots = self.individual_work_data.get(day_code, [])
            if slots:
                slots_str = ', '.join(slots)
                summary_html += f'<p><strong>{day_name}:</strong> {slots_str}</p>'
            else:
                summary_html += f'<p><strong>{day_name}:</strong> <span style="color: gray;">Yok</span></p>'
        
        summary_html += '</div>'
        return summary_html

    def save(self, *args, **kwargs):
        # Set week_year and submission_date on save if data exists
        if (self.group_meeting_data or self.individual_work_data) and not self.week_year:
            self.week_year = self.get_current_week_year()
            self.submission_date = timezone.now()
        
        # Validate minimum hours before saving
        if self.group_meeting_data or self.individual_work_data:
            self.validate_minimum_hours()
            
        super().save(*args, **kwargs)