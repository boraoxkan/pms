from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Command(BaseCommand):
    help = 'Create admin users for the system'

    def get_base_url(self):
        """Production'da doğru domain'i döndür"""
        if hasattr(settings, 'SITE_URL') and settings.SITE_URL:
            return settings.SITE_URL.rstrip('/')
        elif hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
            first_host = settings.ALLOWED_HOSTS[0]
            if first_host != '*' and first_host != '127.0.0.1':
                return f"https://{first_host}"
        return "http://127.0.0.1:8000"

    def handle(self, *args, **options):
        # Admin data - you can modify this list
        admin_users = [
            {
                'username': 'boraozkan',  # Kullanıcı adı (örnek: admin, bora.erol, etc.)
                'email': 'boraozkan@oneeyespace.com',     # @oneeyespace.com e-posta adresi
                'first_name': 'Bora Erol',  # Ad
                'last_name': 'Özkan',   # Soyad
                'is_superuser': True,  # Süper kullanıcı (tüm yetkilere sahip)
                'is_staff': True,      # Staff (admin paneline erişebilir)
                'password': '46MWP289.Fba',        # Şifre (güvenli bir şifre kullanın)
            },
        ]

        base_url = self.get_base_url()

        self.stdout.write("Admin kullanıcıları oluşturuluyor...")
        self.stdout.write("=" * 60)

        for admin_data in admin_users:
            # Skip empty entries
            if not admin_data['username'] or not admin_data['email'] or not admin_data['password']:
                continue
            
            try:
                # Check if user already exists
                existing_user = User.objects.filter(
                    models.Q(username=admin_data['username']) | 
                    models.Q(email=admin_data['email'])
                ).first()
                
                if existing_user:
                    self.stdout.write(f"⚠️  Kullanıcı zaten mevcut: {existing_user.username} ({existing_user.email})")
                    continue
                
                # Create admin user
                if admin_data['is_superuser']:
                    user = User.objects.create_superuser(
                        username=admin_data['username'],
                        email=admin_data['email'],
                        password=admin_data['password'],
                        first_name=admin_data['first_name'],
                        last_name=admin_data['last_name']
                    )
                else:
                    user = User.objects.create_user(
                        username=admin_data['username'],
                        email=admin_data['email'],
                        password=admin_data['password'],
                        first_name=admin_data['first_name'],
                        last_name=admin_data['last_name']
                    )
                    user.is_staff = admin_data['is_staff']
                    user.save()
                
                self.stdout.write(self.style.SUCCESS(f"✅ {user.get_full_name() or user.username} başarıyla oluşturuldu"))
                self.stdout.write(f"   👤 Kullanıcı Adı: {user.username}")
                self.stdout.write(f"   📧 Email: {user.email}")
                self.stdout.write(f"   🔐 Yetki: {'Süper Admin' if user.is_superuser else 'Admin'}")
                self.stdout.write(f"   🏢 Staff: {'Evet' if user.is_staff else 'Hayır'}")
                self.stdout.write(f"   🌐 Google SSO: {'Evet' if user.email.endswith('@oneeyespace.com') else 'Hayır'}")
                self.stdout.write("-" * 60)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Hata: {admin_data['username']} oluşturulurken hata: {e}"))
                self.stdout.write("-" * 60)

        self.stdout.write(self.style.SUCCESS("✨ Admin kullanıcı oluşturma işlemi tamamlandı!"))
        self.stdout.write(f"🔧 Admin Panel: {base_url}/admin/")
        self.stdout.write(f"🏠 Ana Sayfa: {base_url}/")

        self.stdout.write("\n🎯 Admin Yetkileri:")
        self.stdout.write("   is_superuser=True: Tüm yetkilere sahip süper admin")
        self.stdout.write("   is_staff=True: Admin paneline erişebilir")
        self.stdout.write("   is_superuser=False, is_staff=True: Sınırlı admin yetkisi")

        self.stdout.write("\n🔒 Güvenlik Önerileri:")
        self.stdout.write("   • Güçlü şifreler kullanın (en az 8 karakter, büyük/küçük harf, sayı)")
        self.stdout.write("   • Şifreleri güvenli bir yerde saklayın")
        self.stdout.write("   • Gereksiz süper admin hesapları oluşturmayın")