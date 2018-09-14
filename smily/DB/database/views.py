# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache
# Create your views here.

#cache time = 15min
@cache_page(60*15)
def test(request):
    key = '我是缓存值'
    time=60
    result = cache.get(key)#get(key)的方法得到缓存结果
    if not result:
        result = ""
        cache.set(key,result,time)#使用set(key,value,timeout)来设置缓存
    return result
