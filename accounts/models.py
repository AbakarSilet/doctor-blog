from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .utils import generate_profile_image
import os


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Le champ Email doit être renseigné')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('adresse email'), unique=True)
    first_name = models.CharField(_('prénom'), max_length=150)
    last_name = models.CharField(_('nom'), max_length=150)
    profile_image = models.ImageField(
        _('image de profil'),
        upload_to='profiles_images/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Redéfinition des relations many-to-many avec related_name personnalisé
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):

        if not self.profile_image:
            initials = f"{self.first_name[0].upper()}{self.last_name[0].upper()}"
            relative_path = f'profiles_images/{self.name}_profile.png'
            output_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            generate_profile_image(initials, output_path)
            self.profile_image.name = relative_path

        if self.pk:
            old_user = User.objects.get(pk=self.pk)
            if old_user.profile_image and old_user.profile_image != self.profile_image:
                old_user.profile_image.delete(save=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.profile_image:
            self.profile_image.delete(save=False)
        super().delete(*args, **kwargs)
