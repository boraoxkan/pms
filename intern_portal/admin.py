from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.conf import settings
from .models import Project, ProjectPreference, Intern
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
    list_display = ('get_full_name', 'email', 'access_link', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_active',)
    readonly_fields = ('access_token', 'access_link_display')
    fieldsets = (
        ('Stajyer Bilgileri', {
            'fields': ('first_name', 'last_name', 'email', 'is_active')
        }),
        ('Erişim Bilgileri', {
            'fields': ('access_token', 'access_link_display'),
            'classes': ('collapse',)
        }),
    )

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

# Admin site başlığını ve başlık çubuğunu özelleştir
admin.site.site_header = 'PMS Stajyer Portalı Yönetimi'
admin.site.site_title = 'PMS Stajyer Portalı'
admin.site.index_title = 'Portal Yönetimi'
