import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
django.setup()

from intern_portal.models import Intern
from django.conf import settings

def get_base_url():
    """Production'da doğru domain'i döndür"""
    if hasattr(settings, 'SITE_URL') and settings.SITE_URL:
        return settings.SITE_URL.rstrip('/')
    elif hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
        first_host = settings.ALLOWED_HOSTS[0]
        if first_host != '*' and first_host != '127.0.0.1':
            return f"https://{first_host}"
    return "http://127.0.0.1:8000"

interns = [
    {
        'first_name': 'Ahmet',
        'last_name': 'Yılmaz',
        'email': 'ahmet.yilmaz@email.com',
        'is_active': True
    },
    {
        'first_name': 'Ayşe',
        'last_name': 'Kaya',
        'email': 'ayse.kaya@email.com',
        'is_active': True
    },
    {
        'first_name': 'Mehmet',
        'last_name': 'Demir',
        'email': 'mehmet.demir@email.com',
        'is_active': True
    },
    {
        'first_name': 'Fatma',
        'last_name': 'Şen',
        'email': 'fatma.sen@email.com',
        'is_active': True
    },
    {
        'first_name': 'Ali',
        'last_name': 'Özkan',
        'email': 'ali.ozkan@email.com',
        'is_active': True
    }
]

base_url = get_base_url()

print("Stajyerler ekleniyor...")
print("=" * 50)

for intern_data in interns:
    intern, created = Intern.objects.get_or_create(
        email=intern_data['email'],
        defaults=intern_data
    )
    
    if created:
        print(f"✅ {intern.get_full_name()} eklendi")
        print(f"   📧 Email: {intern.email}")
        print(f"   🔗 Erişim Linki: {base_url}/intern/{intern.access_token}/")
        print(f"   🆔 Token: {intern.access_token}")
        print("-" * 50)
    else:
        print(f"⚠️  {intern.get_full_name()} zaten mevcut")
        print(f"   🔗 Erişim Linki: {base_url}/intern/{intern.access_token}/")
        print("-" * 50)

print("Stajyerler başarıyla eklendi!") 