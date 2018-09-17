from django.db import models


# Create your models here.
class Goods(models.Model):
    goods_name = models.CharField(max_length=30, primary_key=True)
    seller_name = models.ForeignKey("user", on_delete=models.CASCADE)
    minimum_price = models.PositiveIntegerField
    choice = (
        ('review', 'WaitingforReview'),
        ('pre', 'preparing'),
        ('in', 'inAuction'),
        ('end', 'endAuction')
    )
    status = models.CharField(max_length=18,choices=choice)
    start_time = models.DateTimeField
    highest_price = models.PositiveIntegerField(default=minimum_price)

    def __str__(self):
        return self.goods_name


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=15)
    nickname = models.CharField(max_length=20, default=username)
    assets = models.PositiveIntegerField(default=0)
    choice = (
        ('0', 'normal'),
        ('1', 'banned')
    )
    status = models.CharField(max_length=6,choices=choice)

    def __str__(self):
        return self.username


class RoleofUser(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    choice = (
        ('GU', 'general_user'),
        ('GA', 'goods_administrator')
    )
    role = models.CharField(max_length=20,choices=choice)

    def __str__(self):
        return self.username


class Auction(models.Model):
    goods_name = models.CharField(max_length=30, primary_key=True)
    lastbid_username = models.CharField(max_length=20, null=True)
    lastbid_time = models.DateTimeField(null=True)
    lastprice = models.IntegerField

    def __str__(self):
        return self.goods_name


class PrivateChat(models.Model):
    sourceName = models.CharField(max_length=20, primary_key=True)
    sourceIP = models.URLField
    targetName = models.ForeignKey("user", on_delete=models.CASCADE)

    def __str__(self):
        return self.sourceIP
