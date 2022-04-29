from django.db import models

# Create your models here.
from users.models import MemberUser
from django.db.models.signals import pre_save


class Plan(models.Model):
    options_plan = (
        ('basic', 'basic'),
        ('business', 'business'),
        ('agency', 'agency'),
    )
    subscription = models.CharField(max_length=20, choices=options_plan)
    user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name='subscription_user')
    limit = models.IntegerField(blank=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'User : {self.user}, Plan : {self.subscription}'


def set_limit_of_requests(sender, instance, **kwargs):
    if instance.subscription == 'basic':
        instance.limit = 50
    elif instance.subscription == 'business':
        instance.limit = 150
    elif instance.subscription == 'agency':
        instance.limit = 500


pre_save.connect(set_limit_of_requests, sender=Plan)


class Vendor(models.Model):
    mac = models.CharField(max_length=6)
    vendor = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.mac},{self.vendor}'
