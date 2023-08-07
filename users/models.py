# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from phonenumber_field.modelfields import PhoneNumberField

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, phone_no, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, phone_no=phone_no, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, phone_no, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, username, phone_no, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=150, unique=True)
#     # phone_no = models.CharField(max_length=15)
#     phone_no = PhoneNumberField()
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='customuser_set',  # Change related_name for groups
#         blank=True,
#         verbose_name='groups',
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='customuser_set',  # Change related_name for user_permissions
#         blank=True,
#         verbose_name='user permissions',
#         help_text='Specific permissions for this user.',
#         )
#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'phone_no']
    

#     def __str__(self):
#         return self.email

# --------------------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_no, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, phone_no, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_no = PhoneNumberField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_no']

    def __str__(self):
        return self.email

