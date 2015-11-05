from django.db import models
# Create your models here.

#充值
class Consumption(models.Model):
    orderid=models.IntegerField(primary_key=True)
    userid = models.IntegerField(null=False)
    total = models.FloatField(null=False)
    score = models.IntegerField(null=False)
    time = models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(null=False)
#兑换
class Exchange ( models.Model):
    userid = models.IntegerField(null=False)
    prop = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)
    score = models.IntegerField(null=False)
    time = models.DateTimeField(auto_now_add=True)
#用户积分信息
class User_info(models.Model):
    userid = models.IntegerField(null=False)
    score = models.IntegerField(null=False)
#用户道具信息
class User_prop(models.Model):
    userid = models.IntegerField(null=False)
    prop = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)
