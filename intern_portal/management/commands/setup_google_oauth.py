# Create this file: intern_portal/management/commands/setup_google_oauth.py

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup Google OAuth for django-allauth'

    def add_arguments(self, parser):
        parser.add_argument('--client-id', type=str, help='Google OAuth Client ID')
        parser.add_argument('--client-secret', type=str, help='Google OAuth Client Secret')
        parser.add_argument('--site-domain', type=str, default='pms.oneeyesystems.com', help='Site domain')

    def handle(self, *args, **options):
        client_id = options['client_id']
        client_secret = options['client_secret']
        site_domain = options['site_domain']
        
        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR(
                    'Please provide both --client-id and --client-secret\n'
                    'Example: python manage.py setup_google_oauth --client-id="your-client-id" --client-secret="your-client-secret"'
                )
            )
            return
        
        # Get or create the site
        site, created = Site.objects.get_or_create(
            pk=1,
            defaults={
                'domain': site_domain,
                'name': 'PMS Intern Portal'
            }
        )
        
        if not created:
            site.domain = site_domain
            site.name = 'PMS Intern Portal'
            site.save()
        
        self.stdout.write(f"✅ Site configured: {site.domain}")
        
        # Create or update Google Social App
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()
        
        # Add the site to the social app
        google_app.sites.add(site)
        
        action = "Created" if created else "Updated"
        self.stdout.write(f"✅ {action} Google OAuth application")
        self.stdout.write(f"   Client ID: {client_id[:10]}...")
        self.stdout.write(f"   Sites: {', '.join([s.domain for s in google_app.sites.all()])}")
        
        # Show test URLs
        self.stdout.write(f"\n🔗 Test URLs:")
        self.stdout.write(f"   Development: http://127.0.0.1:8000/accounts/google/login/")
        self.stdout.write(f"   Production: https://{site_domain}/accounts/google/login/")
        
        self.stdout.write(f"\n📋 Google Console Redirect URIs should include:")
        self.stdout.write(f"   http://127.0.0.1:8000/accounts/google/login/callback/")
        self.stdout.write(f"   http://localhost:8000/accounts/google/login/callback/")
        self.stdout.write(f"   https://{site_domain}/accounts/google/login/callback/")
        
        self.stdout.write(f"\n🎉 Setup complete! You can now test Google OAuth login.")