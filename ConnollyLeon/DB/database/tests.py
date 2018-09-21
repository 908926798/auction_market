from django.test import TestCase

# Create your tests here.

from .models import *
import memcache

mc = memcache.Client(['localhost:11211'], debug=True)
mc.set('list',[])

def refresh_memcache():
    mc = memcache.Client(['localhost:11211'], debug=True)
    goods = Goods.objects.filter(status='end')

    for i in goods:
        if i not in mc.get('list'):
            a = mc.get('list')
            a.append(i)
            mc.replace('list', a)
