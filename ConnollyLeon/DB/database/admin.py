from django.contrib import admin

# Register your models here.

from django.contrib import admin
from database.models import *

admin.site.register(Goods)
admin.site.register(Auction)
admin.site.register(User)
admin.site.register(RoleofUser)
admin.site.register(PrivateChat)

admin.site.name = '后台管理'
admin.site.site_header = '后台管理'
