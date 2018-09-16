from django.db import models

# Create your models here.
class goods(models.Model):
    goods_name = models.CharField(max_length=30,primary_key=True)
    seller_name = models.ForeignKey("user",on_delete=models.CASCADE)
    minimum_price = models.PositiveIntegerField
    status = (
        ('review','WaitingforReview'),
        ('pre','preparing'),
        ('in','inAuction'),
        ('end','endAuction')
    )
    start_time = models.DateTimeField
    highest_price = models.PositiveIntegerField(default=minimum_price)

class user(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=15)
    nickname = models.CharField(max_length=20,default=username)
    assets = models.PositiveIntegerField(default=0)
    status = (
        ('0','normal'),
        ('1','banned')
    )

class RoleofUser(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    role = (
        ('GU','general_user'),
        ('GA','goods_administrator')
    )

class auction(models.Model):
    goods_name = models.CharField(max_length=30,primary_key=True)
    lastbid_username = models.CharField(max_length=20,null=True)
    lastbid_time = models.DateTimeField(null=True)
    lastprice = models.IntegerField

class PrivateChat(models.Model):
    sourceName = models.CharField(max_length=20,primary_key=True)
    sourceIP = models.URLField
    targetName = models.ForeignKey("user",on_delete=models.CASCADE)
