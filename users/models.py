from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, role):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.email = email
        user.role = role
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password, role="admin")
        user.is_active = True
        user.sys_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    role = models.CharField(
        max_length=256,
        choices=(("doctor", "doctor"), ("patient", "patient")),
    )
    objects = MyUserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.sys_admin
