from django.db.models.signals import post_save
from .models import Community


def add_staff(sender, instance, created, **kwargs):
    if created:
        user = instance.admin
        instance.staff.add(user)


post_save.connect(add_staff, sender=Community)
