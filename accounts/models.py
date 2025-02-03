from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
USER, CHEF = 'foydalanuvchi', 'oshpaz'
PHONE_NUMBER, GOOGLE, FACEBOOK = ('telefon raqam', 'google', 'facebook')
MALE, FEMALE = ('erkak', 'ayol')

class Certificates(models.Model):
    image = models.ImageField(upload_to='accounts/chef/certificate-image/', blank=True)

class User(AbstractUser):
    AUTH_TYPE = (
        (PHONE_NUMBER, 'telefon raqam'),
        (GOOGLE, 'Google'),
        (FACEBOOK, 'Facebook'),
    )

    USER_ROLE = (
        (USER, 'foydalanuvchi'),
        (CHEF, 'oshpaz'),
    )

    GENDER = (
        (MALE, 'erkak'),
        (FEMALE, 'ayol'),
    )

    phone_number = models.CharField(max_length=15, unique=True, validators=[RegexValidator(regex=r'^\+998\d{9}$', message="Telefon raqam noto'g'ri formatda")])
    fullname = models.CharField(max_length=250)
    remember_me = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPE)
    user_role = models.CharField(max_length=50, choices=USER_ROLE)
    gender = models.CharField(max_length=50, choices=GENDER)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True)
    bio = models.TextField(null=True, blank=True)
    facebook = models.CharField(max_length=250, null=True)
    instagram = models.CharField(max_length=250, null=True)
    linkedin = models.CharField(max_length=250, null=True)
    telegram = models.CharField(max_length=250, null=True)
    profile_image = models.ImageField(upload_to="accounts/chef/profile-image/")
    certificate = models.ManyToManyField(Certificates, related_name='users')
    work_places = models.CharField(max_length=250, null=True, blank=True)
    work_place_now = models.CharField(max_length=250, null=True, blank=True)
    achievements = models.ImageField(upload_to="accounts/chef/achievement-images/", blank=True)
    objects = CustomUserManager()
    REQUIRED_FIELDS = ['fullname']
    USERNAME_FIELD = 'phone_number'


class Blocklist(models.Model):
    blocker = models.ForeignKey(User, related_name="blocking", on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(User, related_name="blocked_by", on_delete=models.CASCADE)
    blocked_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked_user')


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    class Meta:
        unique_together = ('following', 'follower')