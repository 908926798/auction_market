from django.db import models

from pygments.lexers import get_all_lexers         # 一个实现代码高亮的模块
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS]) # 得到所有编程语言的选项
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())     # 列出所有配色风格


# Create your models here.
class Goods(models.Model):
    G_number = models.AutoField(primary_key=True)
    goods_name = models.CharField(max_length=30)
    seller_name = models.ForeignKey("user", on_delete=models.CASCADE)
    minimum_price = models.PositiveIntegerField()
    detail = models.TextField()
    choice = (
        ('review', 'WaitingforReview'),
        ('in', 'inAuction'),
        ('end', 'endAuction')
    )
    status = models.CharField(max_length=6, choices=choice, default='review')
    lastbid_username = models.CharField(max_length=20, null=True)
    lastbid_time = models.DateTimeField(null=True)
    lastprice = models.IntegerField(null=True)

    def __str__(self):
        return self.goods_name


class User(models.Model):
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
    sourceName = models.CharField(max_length=20, primary_key=True)
    sourceIP = models.CharField(max_length=20)
    targetName = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return self.sourceIP


