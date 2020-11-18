from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from civicconnect.models import Template, Topic

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    favorites = models.ManyToManyField(Template)
    favorites_topic = models.ManyToManyField(Topic)
    USERNAME_FIELD = 'email'

    address1 = models.CharField("Address line 1", max_length=1024, blank=True)
    zip_code = models.CharField("Zip Code", max_length=12, blank=True)
    city = models.CharField("City", max_length=1024, blank=True)
    state_cd = models.CharField("State", max_length=2, blank=True)

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

