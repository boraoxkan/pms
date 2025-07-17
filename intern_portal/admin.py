from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.conf import settings
from .models import Project, ProjectPreference, Intern, InternAvailability
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

# Gereksiz modelleri admin panelinden kaldır
admin.site.unregister(Group)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_size', 'work_type', 'duration')
    list_filter = ('team_size', 'work_type', 'duration')
    search_fields = ('name', 'short_description')
    fieldsets = (
        ('Proje Bilgileri', {
            'fields': ('name', 'short_description', 'full_description')
        }),
        ('Proje Detayları', {
            'fields': ('team_size', 'work_type', 'duration'),
            'description': 'Projenin ekip büyüklüğü, çalışma şekli ve süresi gibi detaylarını belirleyin.'
        }),
    )

@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'get_auth_method', 'access_link', 'has_availability', 'get_assigned_projects_count', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'user__email')
    list_filter = ('is_active', 'user')  # Changed from 'user__isnull' to 'user'
    readonly_fields = ('access_token', 'access_link_display', 'get_auth_method')
    filter_horizontal = ('assigned_projects',)  # Better UI for ManyToMany
    
    fieldsets = (
        ('Stajyer Bilgileri', {
            'fields': ('first_name', 'last_name', 'email', 'user', 'is_active')
        }),
        ('Proje Atamaları', {
            'fields': ('assigned_projects',),
            'description': 'Bu stajyere atanmış projeler'
        }),
        ('Kimlik Doğrulama', {
            'fields': ('get_auth_method',),
            'classes': ('collapse',)
        }),
        ('Erişim Bilgileri (Legacy)', {
            'fields': ('access_token', 'access_link_display'),
            'classes': ('collapse',)
        }),
    )

    def get_auth_method(self, obj):
        """Kimlik doğrulama metodunu gösterir"""
        if obj.user:
            return format_html('<span style="color: green;">✅ Google SSO</span>')
        else:
            return format_html('<span style="color: orange;">🔑 Token (Legacy)</span>')
    get_auth_method.short_description = 'Kimlik Doğrulama'

    def get_assigned_projects_count(self, obj):
        """Atanmış proje sayısını gösterir"""
        count = obj.get_assigned_projects_count()
        if count > 0:
            return format_html('<span style="color: blue;">📋 {} proje</span>', count)
        else:
            return format_html('<span style="color: gray;">➖ Proje yok</span>')
    get_assigned_projects_count.short_description = 'Atanmış Projeler'

    def get_base_url(self, request=None):
        """Production'da doğru domain'i döndür"""
        if hasattr(settings, 'SITE_URL') and settings.SITE_URL:
            return settings.SITE_URL.rstrip('/')
        elif request:
            return f"{request.scheme}://{request.get_host()}"
        else:
            # Fallback - ALLOWED_HOSTS'tan ilk domain'i al
            if hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
                first_host = settings.ALLOWED_HOSTS[0]
                if first_host != '*' and first_host != '127.0.0.1':
                    return f"https://{first_host}"
            return "http://127.0.0.1:8000"

    def access_link(self, obj):
        request = getattr(self, '_request', None)
        base_url = self.get_base_url(request)
        url = f"{base_url}/intern/{obj.access_token}/"
        return format_html('<a href="{}" target="_blank">🔗 Erişim Linki</a>', url)
    access_link.short_description = 'Erişim Linki'

    def access_link_display(self, obj):
        request = getattr(self, '_request', None)
        base_url = self.get_base_url(request)
        url = f"{base_url}/intern/{obj.access_token}/"
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)
    access_link_display.short_description = 'Tam Erişim URL\'si'

    def has_availability(self, obj):
        try:
            availability = obj.availability
            total_hours = availability.get_total_hours()
            if total_hours > 0:
                return format_html('<span style="color: green;">✅ {} saat</span>', total_hours)
            else:
                return format_html('<span style="color: orange;">⏳ Henüz yok</span>')
        except InternAvailability.DoesNotExist:
            return format_html('<span style="color: red;">❌ Yok</span>')
    has_availability.short_description = 'Ortak Çalışma Saati Durumu'

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Request'i instance'a ekle ki metodlarda kullanabilelim
        self._request = request
        return super().changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        # Request'i instance'a ekle ki metodlarda kullanabilelim
        self._request = request
        return super().changelist_view(request, extra_context)

@admin.register(ProjectPreference)
class ProjectPreferenceAdmin(admin.ModelAdmin):
    list_display = ('intern', 'first_choice', 'second_choice', 'third_choice', 'is_submitted')
    list_filter = ('is_submitted',)
    search_fields = ('intern__first_name', 'intern__last_name', 'intern__email')
    readonly_fields = ('is_submitted',)

@admin.register(InternAvailability)
class InternAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('intern', 'get_total_hours', 'get_available_days_count', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('intern__first_name', 'intern__last_name', 'intern__email')
    readonly_fields = ('created_at', 'updated_at', 'availability_summary')
    
    fieldsets = (
        ('Stajyer Bilgileri', {
            'fields': ('intern',)
        }),
        ('Ortak Çalışma Saati Verileri', {
            'fields': ('availability_data', 'availability_summary'),
            'description': 'JSON formatında haftalık ortak çalışma saati verileri.'
        }),
        ('Zaman Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_total_hours(self, obj):
        total = obj.get_total_hours()
        if total > 0:
            return format_html('<span style="color: green; font-weight: bold;">{} saat</span>', total)
        return format_html('<span style="color: red;">0 saat</span>')
    get_total_hours.short_description = 'Toplam Saat'

    def get_available_days_count(self, obj):
        days = obj.get_available_days()
        day_names = {
            'monday': 'Pzt',
            'tuesday': 'Sal',
            'wednesday': 'Çar',
            'thursday': 'Per',
            'friday': 'Cum',
            'saturday': 'Cmt'
        }
        if days:
            day_display = ', '.join([day_names.get(day, day) for day in days])
            return format_html('<span style="color: blue;">{} ({} gün)</span>', day_display, len(days))
        return format_html('<span style="color: red;">Ortak çalışma saati yok</span>')
    get_available_days_count.short_description = 'Ortak Çalışma Saati Günleri'

    def availability_summary(self, obj):
        if not obj.availability_data:
            return format_html('<span style="color: red;">Henüz ortak çalışma saati belirtilmemiş</span>')
        
        day_names = {
            'monday': 'Pazartesi',
            'tuesday': 'Salı',
            'wednesday': 'Çarşamba',
            'thursday': 'Perşembe',
            'friday': 'Cuma',
            'saturday': 'Cumartesi'
        }
        
        summary_html = '<div style="max-width: 600px;">'
        for day_code, day_name in day_names.items():
            slots = obj.availability_data.get(day_code, [])
            if slots:
                slots_str = ', '.join(slots)
                summary_html += f'<p><strong>{day_name}:</strong> {slots_str}</p>'
            else:
                summary_html += f'<p><strong>{day_name}:</strong> <span style="color: gray;">Ortak çalışma saati yok</span></p>'
        summary_html += '</div>'
        
        return format_html(summary_html)
    availability_summary.short_description = 'Ortak Çalışma Saati Özeti'

# Admin site başlığını ve başlık çubuğunu özelleştir
admin.site.site_header = 'PMS Stajyer Portalı Yönetimi'
admin.site.site_title = 'PMS Stajyer Portalı'
admin.site.index_title = 'Portal Yönetimi'