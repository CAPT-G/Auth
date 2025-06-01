from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


# ------------------------
# 🧠 Custom User Manager
# ------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, display_name=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)

        if not display_name:
            display_name = email.split('@')[0].lower()

        if CustomUser.objects.filter(display_name=display_name).exists():
            raise ValidationError('Display name already taken')

        user = self.model(email=email, display_name=display_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, display_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not display_name:
            display_name = email.split('@')[0].lower()

        return self.create_user(email, password, display_name, **extra_fields)


# ------------------------
# 👤 Custom User Model
# ------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=False)  # Verified = True
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.email.split('@')[0].lower()
        if CustomUser.objects.exclude(pk=self.pk).filter(display_name=self.display_name).exists():
            raise ValidationError('Display name already taken.')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name


# ------------------------
# 🧬 User Profile Model
# ------------------------
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=512)

    def __str__(self):
        return f"Profile: {self.user.display_name}"


# ------------------------
# 🔐 Email Verification Code Model
# ------------------------
class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)
    terms_accepted = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.email} - {'Verified' if self.verified else 'Pending'}"
