# Create: intern_portal/management/commands/setup_dev_oauth.py

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup OAuth for development environment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='127.0.0.1:8000',
            help='Domain for development (default: 127.0.0.1:8000)'
        )

    def handle(self, *args, **options):
        domain = options['domain']
        
        # Update the site for development
        site = Site.objects.get(pk=1)
        old_domain = site.domain
        site.domain = domain
        site.name = f'PMS Intern Portal ({domain})'
        site.save()
        
        self.stdout.write(f"✅ Updated site domain: {old_domain} → {domain}")
        
        # Make sure Google app is linked to the updated site
        try:
            google_app = SocialApp.objects.get(provider='google')
            google_app.sites.clear()
            google_app.sites.add(site)
            
            self.stdout.write(f"✅ Google OAuth app linked to {domain}")
            self.stdout.write(f"   Client ID: {google_app.client_id[:10]}...")
            self.stdout.write(f"   Has secret: {'✅' if google_app.secret else '❌'}")
            
        except SocialApp.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ Google OAuth app not found"))
            return
        
        # Show test URLs
        self.stdout.write(f"\n🔗 Test URLs:")
        self.stdout.write(f"   Google Login: http://{domain}/accounts/google/login/")
        self.stdout.write(f"   Home Page: http://{domain}/")
        self.stdout.write(f"   Debug Page: http://{domain}/debug-google/")
        
        # Show Google Console requirements
        self.stdout.write(f"\n📋 Make sure your Google OAuth app has these redirect URIs:")
        self.stdout.write(f"   http://{domain}/accounts/google/login/callback/")
        if domain == '127.0.0.1:8000':
            self.stdout.write(f"   http://localhost:8000/accounts/google/login/callback/")
        
        self.stdout.write(f"\n🎉 Setup complete! Restart your dev server and test the login.")

# Usage:
# python manage.py setup_dev_oauth
# python manage.py setup_dev_oauth --domain="localhost:8000"