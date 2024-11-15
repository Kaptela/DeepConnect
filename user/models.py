from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template.defaultfilters import slugify
from phone_field import PhoneField
from django.contrib.auth.models import Group, Permission
from django.utils.text import slugify


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, phone, password, **extra_fields):
        values = [email, username, phone]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, username, phone, password, **extra_fields)

    def create_superuser(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=150, blank=True)
    name = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150, blank=True, null=True, default='')
    phone = PhoneField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True, upload_to='ava')
    
    description = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    
    # wefwefwef
    SEX_CHOICES = {
        'Female' : 'Female',
        'Male' : 'Male'
    }
    sex = models.CharField(choices=SEX_CHOICES ,max_length=10)
    
    SOCIAL_OREINTATION = {
        'Extrovert' : 'Extrovert',
        'Ambivert' : 'Ambivert',
        'Introvert' : 'Introvert'
    }
    social_orientation = models.CharField(choices=SOCIAL_OREINTATION, max_length=50)
    agreeableness = models.PositiveIntegerField(default=50)
    emotional_stablility = models.PositiveIntegerField(default=50)
    # wefoinweofne
    
    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)

    slug = models.SlugField()
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'username']

    def get_full_name(self):
        return f'{self.name} {self.lastname}'

    def get_short_name(self):
        return self.name


    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.name} {self.lastname}'
    
    

