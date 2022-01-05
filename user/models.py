from django.contrib.auth.models import UserManager
from django.db import models


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    is_anonymous = False
    is_authenticated = True
    is_active = True

    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'payhere_user'
