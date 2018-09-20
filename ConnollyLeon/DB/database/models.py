from django.db import models




# Create your models here.
class Goods(models.Model):
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
    G_number = models.AutoField(primary_key=True)
    goods_name = models.CharField(max_length=30)
    seller_name = models.ForeignKey("user", on_delete=models.CASCADE)
    minimum_price = models.PositiveIntegerField()
    detail = models.TextField()
    choice = (
        ('review', 'WaitingforReview'),
        ('in', 'inAuction'),
        ('end', 'endAuction'),
        ('ready','ReadyforAuction')
    )
    status = models.CharField(max_length=6, choices=choice, default='review')
    lastbid_username = models.CharField(max_length=20, null=True)
    lastbid_time = models.DateTimeField(null=True)
    lastprice = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.goods_name


class User(models.Model):
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=256)
    nickname = models.CharField(max_length=20, default='none')
    assets = models.PositiveIntegerField(default=0)
    choice = (
        ('0', 'normal'),
        ('1', 'banned')
    )
    choice1 = (
        ('0', 'not_administrator'),
        ('1', 'goods_administrator')
    )

    choice2 = (
        ('0', 'not_general_user'),
        ('1', 'general_user')
    )

    isAdministrator = models.CharField(max_length=20, choices=choice1, default='0')
    isGeneralUser = models.CharField(max_length=20, choices=choice2, default='1')
    status = models.CharField(max_length=6, choices=choice, default='0')

    def __str__(self):
        return self.username


class PrivateChat(models.Model):
    class Meta:
        verbose_name = '私聊'
        verbose_name_plural = '私聊'
    sourceName = models.ForeignKey(User, related_name='sourceName')
    targetName = models.ForeignKey(User, related_name='targetName')
    sourceIP = models.CharField(max_length=20)

    def __str__(self):
        return self.sourceIP
