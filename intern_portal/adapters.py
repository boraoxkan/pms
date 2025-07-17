from django.contrib import messages
from django.shortcuts import redirect
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter to restrict Google SSO to @oneeyespace.com domain only
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Called just after a user successfully authenticates via a social provider,
        but before the login is processed by Django.
        """
        user = sociallogin.user
        email = user.email
        
        # Check if the email domain is allowed
        if not email or not email.endswith('@oneeyespace.com'):
            messages.error(
                request, 
                'Yalnızca @oneeyespace.com e-posta adresine sahip kullanıcılar giriş yapabilir. '
                'Lütfen şirket e-posta adresinizle tekrar deneyin.'
            )
            # Redirect to home page with error message
            raise ImmediateHttpResponse(
                HttpResponseRedirect(reverse('home_page'))
            )
    
    def save_user(self, request, sociallogin, form=None):
        """
        Called when a user is saved for the first time after social login.
        We can use this to create the corresponding Intern object.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Create or get the corresponding Intern object
        self.create_or_update_intern(user)
        
        return user
    
    def create_or_update_intern(self, user):
        """
        Create or update the Intern object for the authenticated user
        """
        from .models import Intern
        
        # Extract first and last name from the user
        first_name = user.first_name or ''
        last_name = user.last_name or ''
        
        # If names are empty, try to extract from email
        if not first_name and not last_name:
            email_parts = user.email.split('@')[0].split('.')
            if len(email_parts) >= 2:
                first_name = email_parts[0].capitalize()
                last_name = email_parts[1].capitalize()
            else:
                first_name = email_parts[0].capitalize()
        
        # Create or update the Intern object
        intern, created = Intern.objects.get_or_create(
            email=user.email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'user': user,
                'is_active': True,
            }
        )
        
        # If intern already exists but doesn't have a user linked, link it
        if not created and not intern.user:
            intern.user = user
            intern.save()
        
        return intern