# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RequestView, Shortlist

@receiver(post_save, sender=RequestView)
def bump_views(sender, instance, created, **kwargs):
    if created:
        req = instance.request
        req.views = req.view_logs.count()
        req.save(update_fields=['views'])

@receiver(post_save, sender=Shortlist)
def bump_shortlists(sender, instance, created, **kwargs):
    if created:
        req = instance.request
        req.shortlists = req.shortlist_logs.count()
        req.save(update_fields=['shortlists'])