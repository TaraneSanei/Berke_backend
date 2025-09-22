from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from datetime import date
from django.core.validators import RegexValidator
from meditation.models import Tag
# Create your models here.

class CustomUserManager(BaseUserManager):

    def _create_user(self, phone_number, password, username, **extrafields):
        if not phone_number:
            raise ValueError(" Phone number is invalid! ")
        User = self.model(phone_number = phone_number, username = username, **extrafields)
        User.set_password(password)
        User.save()
        return User
    
    def create_user(self, phone_number = None, password = None, username = None, **extrafields):
        extrafields.setdefault("is_staff" , False)
        extrafields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, username, **extrafields)

    def create_superuser(self, phone_number = None, password = None, username = None, **extrafields):
        extrafields.setdefault("is_staff" , True)
        extrafields.setdefault("is_superuser", True)
        extrafields.setdefault("is_active", True)
        return self._create_user(phone_number, password, username, **extrafields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, primary_key=False, blank=True, null=True)
    username = models.CharField(max_length=28, primary_key=False, blank= True, null= True)
    phone_number = models.CharField(max_length=11, primary_key=False, unique=True, validators=[RegexValidator("09\d\d\d\d\d\d\d\d\d")])
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    authenticated = models.BooleanField(default=False)
    created_at= models.DateField(default= date.today)
    last_login =models.DateField(default=date.today)
    is_subscribed = models.BooleanField(default=False)
    subscribed_at = models.DateField(blank=True, null=True)
    subscription_end = models.DateField(blank=True, null=True)
    minutes_listened =models.IntegerField(default=0)
    preferences = models.ManyToManyField(Tag)
    notification = models.TimeField(null=True, blank=True)
    theme = models.CharField(max_length=100, default='sunrise')
    objects = CustomUserManager()
    USERNAME_FIELD = "phone_number"

    def auth_user(self):
        self.authenticated = True
        self.save()
        return f"{self.username} with the phone number {self.phone_number} is authenticated"
    

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=255)
    otp_code = models.CharField(max_length=6) 
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.user.username}"