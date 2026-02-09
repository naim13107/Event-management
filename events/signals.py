from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Event
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_confirmation(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for pk in pk_set:
            user = User.objects.get(pk=pk)
            subject = f"RSVP Confirmation: {instance.name}"
            message = f"Hi {user.username},\n\nYou have successfully RSVP'd for {instance.name}.\n\nLocation: {instance.location}"
            
            try:
                send_mail(
                    subject, 
                    message, 
                    settings.EMAIL_HOST_USER, 
                    [user.email], 
                    fail_silently=False
                )
            except Exception as e:
                print(f"Email failed: {e}")