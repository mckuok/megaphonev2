from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class MYMGR(BaseUserManager):
    def _create_user(self, email, name, password, is_staff):
        user = self.model(email=email, name=name, last_login=timezone.now(), is_staff=is_staff)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, name, password):
        return self._create_user(email, name, password, False)

    def create_superuser(self, email, name, password):
        return self._create_user(email, name, password, True)


class User(AbstractBaseUser):
    objects = MYMGR()
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=20, unique=True)
    role = models.CharField(max_length=20)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    subscribe_domain = models.CharField(max_length=300, default="", blank=True)
    subscribe_page = models.CharField(max_length=300, default="", blank=True)
    last_access = models.DateTimeField(null=True, blank=True)
    checked_announcement = models.BooleanField(default=False)
    checked_event = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        pass

    def get_short_name(self):
        pass

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def __unicode__(self):
        day = int(self.date_joined.day)
        month = int(self.date_joined.month)
        year = int(self.date_joined.year)
        return "%s - %d/%d/%d" % (self.name, month, day, year)
