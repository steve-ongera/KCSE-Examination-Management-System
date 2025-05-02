from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_login_failed
from .models import KNECProfile, LoginAttempt, ActivityLog

# Get the custom user model
User = get_user_model()

@receiver(post_save, sender=User)
def create_knec_profile(sender, instance, created, **kwargs):
    """Create a KNECProfile for new users automatically"""
    if created and instance.user_type == 3:  # Only create for KNEC Officials
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
    
    LoginAttempt.objects.create(
        user=user,
        successful=True,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    ActivityLog.objects.create(
        user=user,
        activity_type='LOGIN',
        description=f'Successful login from {ip_address}',
        ip_address=ip_address
    )

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request=None, **kwargs):
    """Log failed login attempts"""
    username = credentials.get('username', '')
    ip_address = get_client_ip(request) if request else None
    user_agent = request.META.get('HTTP_USER_AGENT') if request else None
    
    try:
        user = User.objects.get(username=username)
        # Create records only if user exists
        LoginAttempt.objects.create(
            user=user,
            successful=False,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        ActivityLog.objects.create(
            user=user,  # This will always have a user
            activity_type='LOGIN_FAILED',
            description='Failed login attempt',
            ip_address=ip_address
        )
    except User.DoesNotExist:
        # Only log the attempt if we have request info
        if request:
            ActivityLog.objects.create(
                user=None,  # This is the problem - either remove or make user nullable
                activity_type='LOGIN_FAILED',
                description=f'Failed login attempt for non-existent user: {username}',
                ip_address=ip_address
            )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip