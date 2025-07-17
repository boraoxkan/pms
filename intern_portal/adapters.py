from django.contrib import messages
from django.shortcuts import redirect
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse  # Updated import
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter to:
    1. Restrict Google SSO to @oneeyespace.com domain only
    2. Find existing Intern objects and link them to new User objects (NO duplicate creation)
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
        
        # CRITICAL: Check if there's already a User with this email
        # If so, we need to connect to the existing account instead of creating a new one
        from django.contrib.auth.models import User
        try:
            existing_user = User.objects.get(email=email)
            # Connect the social account to the existing user
            sociallogin.connect(request, existing_user)
            logger.info(f"Connected social account to existing user: {email}")
        except User.DoesNotExist:
            # No existing user, proceed with normal flow
            logger.info(f"No existing user found for {email}, will create new user")
            pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Called when a user is saved for the first time after social login.
        This is where we implement the "find and link" logic.
        """
        # First, save the user using the parent method
        user = super().save_user(request, sociallogin, form)
        
        # Now implement our "find and link" logic
        self.find_and_link_intern(user, request)
        
        return user
    
    def find_and_link_intern(self, user, request):
        """
        Find existing Intern by email and link to the User object.
        This is the core of our "find and link" workflow.
        """
        from .models import Intern
        
        email = user.email
        logger.info(f"Looking for existing Intern with email: {email}")
        
        try:
            with transaction.atomic():
                # Try to find existing Intern with this email
                existing_intern = Intern.objects.get(email=email)
                
                # Check if this intern is already linked to a user
                if existing_intern.user:
                    logger.warning(f"Intern {email} already linked to user {existing_intern.user.email}")
                    # This shouldn't happen in normal flow, but handle gracefully
                    if existing_intern.user.id != user.id:
                        messages.warning(
                            request, 
                            f'Bu e-posta adresi zaten başka bir kullanıcı hesabına bağlı. '
                            f'Lütfen sistem yöneticisi ile iletişime geçin.'
                        )
                    return existing_intern
                
                # Link the existing intern to the new user
                existing_intern.user = user
                
                # Update intern's name if it's missing and we have it from Google
                if not existing_intern.first_name and user.first_name:
                    existing_intern.first_name = user.first_name
                if not existing_intern.last_name and user.last_name:
                    existing_intern.last_name = user.last_name
                
                existing_intern.save()
                
                logger.info(f"✅ Successfully linked existing Intern {existing_intern.get_full_name()} to User {user.email}")
                messages.success(
                    request, 
                    f'Hoş geldiniz {existing_intern.get_full_name()}! '
                    f'Hesabınız başarıyla bağlandı.'
                )
                
                return existing_intern
                
        except Intern.DoesNotExist:
            # No existing intern found - this means admin hasn't created the intern yet
            logger.info(f"No existing Intern found for {email}. Creating new one.")
            
            # Extract names from Google profile or email
            first_name = user.first_name or ''
            last_name = user.last_name or ''
            
            # If names are empty, try to extract from email
            if not first_name and not last_name:
                email_parts = email.split('@')[0].split('.')
                if len(email_parts) >= 2:
                    first_name = email_parts[0].capitalize()
                    last_name = email_parts[1].capitalize()
                else:
                    first_name = email_parts[0].capitalize()
            
            # Create new intern (this should be rare in your workflow)
            new_intern = Intern.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=True
            )
            
            logger.info(f"✅ Created new Intern {new_intern.get_full_name()} for User {user.email}")
            messages.info(
                request, 
                f'Hoş geldiniz {new_intern.get_full_name()}! '
                f'Yeni hesabınız oluşturuldu.'
            )
            
            return new_intern
            
        except Exception as e:
            logger.error(f"Error in find_and_link_intern for {email}: {str(e)}")
            messages.error(
                request, 
                'Hesap bağlantısı sırasında bir hata oluştu. Lütfen sistem yöneticisi ile iletişime geçin.'
            )
            raise