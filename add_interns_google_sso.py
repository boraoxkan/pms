import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
django.setup()

from intern_portal.models import Intern
from django.contrib.auth.models import User
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

# Intern data - you can modify this list
interns_data = [
    {
        'first_name': 'Ali Naci',  # Ad
        'last_name': 'Tüysüz',   # Soyad
        'email': 'alituysuz@oneeyespace.com',       # @oneeyespace.com e-posta adresi
        'is_active': True,
        'create_user': True,  # Google SSO için User objesi oluştur
    },
    {
        'first_name': 'Berfin',
        'last_name': 'İnan',
        'email': 'berfininan@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Berna',
        'last_name': 'Çakır',
        'email': 'bernacakir@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Beyza Nur',
        'last_name': 'Doğan',
        'email': 'beyzadogan@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Erfan',
        'last_name': 'FarhangKia',
        'email': 'erfanfarhangkia@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Esma',
        'last_name': 'Aydın',
        'email': 'esmaaydin@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Esma',
        'last_name': 'Sivri',
        'email': 'esmasivri@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Mehmet Baran',
        'last_name': 'Dedeoğlu',
        'email': 'mehmetdedeoglu@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Rümeysa',
        'last_name': 'Şen',
        'email': 'rumeysasen@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Süleyman Özhan',
        'last_name': 'Karayel',
        'email': 'suleymankarayel@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Taha Yağız',
        'last_name': 'Oktar',
        'email': 'tahaoktar@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    {
        'first_name': 'Şerife Sümeyye',
        'last_name': 'Ocak',
        'email': 'serifeocak@oneeyespace.com',
        'is_active': True,
        'create_user': True,
    },
    # Daha fazla stajyer eklemek için yukarıdaki formatı kopyalayın
]

base_url = get_base_url()

print("Stajyerler ekleniyor...")
print("=" * 60)

for intern_data in interns_data:
    # Skip empty entries
    if not intern_data['first_name'] or not intern_data['email']:
        continue
    
    try:
        # Check if intern already exists
        existing_intern = Intern.objects.filter(email=intern_data['email']).first()
        if existing_intern:
            print(f"⚠️  {existing_intern.get_full_name()} zaten mevcut (Email: {existing_intern.email})")
            continue
        
        # Create or get User object for Google SSO
        user_obj = None
        if intern_data.get('create_user', False):
            user_obj, user_created = User.objects.get_or_create(
                email=intern_data['email'],
                defaults={
                    'username': intern_data['email'],  # Use email as username
                    'first_name': intern_data['first_name'],
                    'last_name': intern_data['last_name'],
                    'is_active': True,
                }
            )
            if user_created:
                print(f"👤 User objesi oluşturuldu: {user_obj.email}")
            else:
                print(f"👤 User objesi mevcut: {user_obj.email}")
        
        # Create intern
        intern = Intern.objects.create(
            first_name=intern_data['first_name'],
            last_name=intern_data['last_name'],
            email=intern_data['email'],
            user=user_obj,
            is_active=intern_data['is_active']
        )
        
        print(f"✅ {intern.get_full_name()} başarıyla eklendi")
        print(f"   📧 Email: {intern.email}")
        print(f"   🔐 Kimlik Doğrulama: {'Google SSO' if intern.user else 'Token (Legacy)'}")
        
        if intern.user:
            print(f"   🌐 Google SSO ile giriş yapabilir")
        else:
            print(f"   🔗 Legacy Erişim Linki: {base_url}/intern/{intern.access_token}/")
        
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Hata: {intern_data['first_name']} {intern_data['last_name']} eklenirken hata: {e}")
        print("-" * 60)

print("✨ Stajyer ekleme işlemi tamamlandı!")
print(f"🏠 Ana Sayfa: {base_url}/")
print(f"🔧 Admin Panel: {base_url}/admin/")