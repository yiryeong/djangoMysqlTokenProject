from django.db import models


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'payhere_user'


class PayHistory(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField()
    price = models.IntegerField()
    memo = models.CharField(max_length=255)
    uid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pay_history'
