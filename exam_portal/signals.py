from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_login_failed
from .models import KNECProfile, LoginAttempt, ActivityLog

@receiver(post_save, sender=User)
def create_knec_profile(sender, instance, created, **kwargs):
    """Create a KNECProfile for new users automatically"""
    if created:
        KNECProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_knec_profile(sender, instance, **kwargs):
    """Save the user's KNECProfile when the User is saved"""
    if hasattr(instance, 'knec_profile'):
        instance.knec_profile.save()

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """Log successful login attempts"""
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Record the login attempt
    LoginAttempt.objects.create(
        user=user,
        successful=True,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    # Record activity log
    ActivityLog.objects.create(
        user=user,
        activity_type='LOGIN',
        description=f'Successful login from {ip_address}',
        ip_address=ip_address
    )

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    """Log failed login attempts"""
    username = credentials.get('username', '')
    
    # Try to find the user
    try:
        user = User.objects.get(username=username)
        
        # Record the failed login attempt
        LoginAttempt.objects.create(
            user=user,
            successful=False,
            ip_address=None,  # No request object available in this signal
            user_agent=None
        )
        
        # Record activity log
        ActivityLog.objects.create(
            user=user,
            activity_type='LOGIN_FAILED',
            description='Failed login attempt',
            ip_address=None
        )
    except User.DoesNotExist:
        # Can't log for non-existent users
        pass

# Helper function to get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip