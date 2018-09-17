# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import *
from hashlib import md5
from django.core.exceptions import *
from django.http import *
import json


# Create your views here.

# cache time = 15min
@cache_page(60 * 15)  # 为一个方法（页面）
def test(request):
    key = '我是缓存值'
    time = 60
    result = cache.get(key)  # get(key)的方法得到缓存结果
    if not result:
        result = ""
        cache.set(key, result, time)  # 使用set(key,value,timeout)来设置缓存
    return result


def login(request):
    if request.method == 'GET':
        print('hellohello')
        result = {}
        username = request.GET.get('login_name_email')
        password = request.GET.get('login_password')

        print(username)
        print(password)
        try:
            m2 = md5()
            m2.update(password.encode('utf8'))
            password = m2.hexdigest()
            user = User.objects.get(username=username)
            print(user.password)
            print(user.user_name)
            if user.password == password:
                result['status'] = 1
                result = json.dumps(result)
                return HttpResponse(result, content_type='application/json;charset=utf-8')
            else:
                result['status'] = 0
                result = json.dumps(result)
                return HttpResponse(result, content_type='application/json;charset=utf-8')
        except:
            result['status'] = 0
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')
    else:
        result = {}
        result['status'] = 0
        result = json.dumps(result)
        return HttpResponse(result, content_type='application/json;charset=utf-8')


def register(request):
    if request.method == 'GET':
        print('hellohello')
        result = {}
        username = request.GET.get('username')
        password = request.GET.get('password')

        print(username)
        print(password)
        try:
            print('trying to get objects')
            User.objects.get(username=username)
            print('obeject got')
            result['status'] = 0
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')
        except ObjectDoesNotExist as e:
            m2 = md5()
            m2.update(password.encode('utf8'))
            password = m2.hexdigest()
            registAdd = User.objects.create(username=username, password=password)
            #registAdd.save()
            result['status'] = 1
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')
    else:
        result = {}
        result['status'] = 0
        result = json.dumps(result)
        return HttpResponse(result, content_type='application/json;charset=utf-8')
