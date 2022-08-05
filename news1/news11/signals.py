from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, Category
from .views import sending_emails_to_subscribers


@receiver(post_save, sender=Post)
def send_emails_on_signal(sender, created, instance, **kwargs):
    sending_emails_to_subscribers(instance)
