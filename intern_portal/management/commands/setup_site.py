from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Setup the Django site for allauth'

    def handle(self, *args, **options):
        # Create or update the site
        site, created = Site.objects.get_or_create(
            pk=1,
            defaults={
                'domain': 'pms.oneeyesystems.com',
                'name': 'PMS Intern Portal'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created site: {site.domain}')
            )
        else:
            site.domain = 'pms.oneeyesystems.com'
            site.name = 'PMS Intern Portal'
            site.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated site: {site.domain}')
            )