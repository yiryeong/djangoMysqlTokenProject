from django.db import models


class PayHistory(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField()
    price = models.IntegerField()
    memo = models.CharField(max_length=255)
    uid = models.IntegerField()
    # uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="uid")

    class Meta:
        managed = False
        db_table = 'pay_history'
