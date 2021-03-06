from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
# Create your models here.

USERTYPE_CHOICES = (
    ('SUPER_ADMIN', 'Super Admin'),
    ('ADMISSION_OFFICER', 'Admission Officer'),
    ('SENIOR_COUNSELOR', 'Senior Counselor'),
    ('COUNSELOR', 'Counselor'),
    ('RECEPTIONIST', 'Receptionist'),
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20,choices=USERTYPE_CHOICES,null=True,blank=True)
    branch = models.ForeignKey('branch.Branch',on_delete=models.CASCADE,related_name='branch_members',null=True,blank=True)
    active = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. User'
