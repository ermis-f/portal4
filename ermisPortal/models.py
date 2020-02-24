from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    organization = models.CharField(max_length=100, blank=True)
    gn_is_active = models.BooleanField(null=False, blank=False, default=False)
    gn_is_staff = models.BooleanField(null=False, blank=False, default=False)
    gn_is_superuser = models.BooleanField(null=False, blank=False, default=False)
    kb_is_active = models.BooleanField(null=False, blank=False, default=False)
    kb_is_staff = models.BooleanField(null=False, blank=False, default=False)
    kb_is_superuser = models.BooleanField(null=False, blank=False, default=False)
    kb_is_editor = models.BooleanField(null=False, blank=False, default=False)
    cr_is_active = models.BooleanField(null=False, blank=False, default=False)
    cr_is_staff = models.BooleanField(null=False, blank=False, default=False)
    cr_is_superuser = models.BooleanField(null=False, blank=False, default=False)
    cr_is_editor = models.BooleanField(null=False, blank=False, default=False)
    sm_is_active = models.BooleanField(null=False, blank=False, default=False)
    sm_is_staff = models.BooleanField(null=False, blank=False, default=False)
    sm_is_superuser = models.BooleanField(null=False, blank=False, default=False)
    ews_is_active = models.BooleanField(null=False, blank=False, default=False)
    ews_is_staff = models.BooleanField(null=False, blank=False, default=False)
    ews_is_superuser = models.BooleanField(null=False, blank=False, default=False)
