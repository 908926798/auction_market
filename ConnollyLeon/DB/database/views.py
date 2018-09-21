# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .models import *
from hashlib import md5
from django.core.exceptions import *
from django.http import *
from .Serializer import *
from rest_framework.decorators import api_view
import json
import memcache


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

        # print(username)
        # print(password)
        try:
            m2 = md5()
            m2.update(password.encode('utf8'))
            password = m2.hexdigest()
            user = User.objects.get(username=username)
            print(user.password)
            if user.password == password:
                result['status'] = 1
                result['money'] = user.assets
                result['U'] = user.isGeneralUser
                result['GM'] = user.isAdministrator
                print(result)
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


@csrf_exempt
def user(request,pk):

    if request.method =='PUT':
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            result = {}
            result['status'] = 0
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')

        put = QueryDict(request.body)
        assets = put.get('assets')
        print(assets)
        user.assets=assets
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    elif request.method=='GET':
        try:
            user = User.objects.get(username=pk)
        except User.DoesNotExist:
            print('HTTP404')
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    else:
        result = {}
        result['status'] = 0
        result = json.dumps(result)
        return HttpResponse(result, content_type='application/json;charset=utf-8')


@csrf_exempt
def goodsstatus(request, status):
    # mc = memcache.Client(['192.168.43.23:11211'], debug=True)
    if request.method == 'POST':
        username = request.POST.get("username")
        itemname = request.POST.get('itemname')
        price = request.POST.get('price')
        detail = request.POST.get('detail')

        print(username)
        print(itemname)
        print(price)
        print(detail)
        result = {}
        try:
            print('testing')
            user = User.objects.get(username=username)
            print('hello')
            Goods.objects.create(seller_name=user, goods_name=itemname, minimum_price=price, detail=detail,
                                 lastprice=price)
            print('Am I here?')
            result['status'] = 1
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')
        except ObjectDoesNotExist as e:
            result['status'] = 0
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')

    elif request.method == 'GET':
        # status = request.GET.get('status')
        if status == '1':
            goods = Goods.objects.filter(status='review')
            serializer = GoodsReviewSerializer(goods, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif status == '2':
            goods = Goods.objects.filter(status='in')
            serializer = GoodsInSerializer(goods, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif status == '3':
            goods = Goods.objects.filter(status='end')
            print(goods)
            # a = mc.get('list')
            serializer = GoodsEndSerializer(goods, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif status == '4':
            goods = Goods.objects.filter(status='ready')
            serializer = GoodsSerializer(goods, many=True)
            return JsonResponse(serializer.data, safe=False)
        result = {}
        result['status'] = 0
        result = json.dumps(result)

        return HttpResponse(result, content_type='application/json;charset=utf-8')


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        fromname = request.POST.get("fromname")
        toname = request.POST.get("toname")
        fromip = request.POST.get("fromip")
        print(fromname)
        print(toname)
        print(fromip)
        result = {}
        try:
            fromuser = User.objects.get(username=fromname)
            touser = User.objects.get(username=toname)
            try:
                chat = PrivateChat.objects.get(sourceName=fromuser, targetName=touser)
                chat.sourceIP = fromip
                chat.save()
            except ObjectDoesNotExist as e:
                chat = PrivateChat.objects.create(sourceName=fromuser, targetName=touser, sourceIP=fromip)
            result['status'] = 1
            result = json.dumps(result)
            print(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')

        except ObjectDoesNotExist as e:
            result['status'] = 0
            result = json.dumps(result)
            print(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')
    elif request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        chats = PrivateChat.objects.filter(targetName=user)
        serializer = PrivateChatSerializer(chats, many=True)
        return JsonResponse(serializer.data, safe=False)

    else:
        delete = QueryDict(request.body)
        fromname = delete.get('fromname')
        toname = delete.get('toname')
        try:
            fromuser = User.objects.get(username=fromname)
            touser = User.objects.get(username=toname)
            try:
                chat = PrivateChat.objects.get(sourceName=fromuser, targetName=touser)
                chat.delete()
            except ObjectDoesNotExist as e:
                pass
            chats = PrivateChat.objects.filter(targetName=touser)
            serializer = PrivateChatSerializer(chats, many=True)
            return JsonResponse(serializer.data, safe=False)
        except ObjectDoesNotExist as e:
            pass


@csrf_exempt
@api_view(['GET', 'PUT'])
def money(request):
    if request.method == 'PUT':
        addMoney = request.PUT.get("money")
        username = request.PUT.get("username")
        user = User.objects.get(username=username)
        user.assets += int(addMoney)
        user.save()

        result = {}
        result['status'] = 1
        result['money'] = user.assets
        result = json.dumps(result)
        print(result)

        return HttpResponse(result, content_type='application/json;charset=utf-8')

    elif request.method == 'GET':
        username = request.GET.get("username")
        user = User.objects.get(username=username)
        print(user.assets)
        return HttpResponse(user.assets)



@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def goods(request, pk):
    try:
        goods = Goods.objects.get(G_number=pk)
    except Goods.DoesNotExist:
        print('HTTP404')

    if request.method == 'GET':
        serializer = GoodsSerializer(goods)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        goods.status = 'ready'
        goods.save()
        serializer = GoodsSerializer(goods)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'DELETE':
        goods.delete()
        result = {}
        result['status'] = 1
        result = json.dumps(result)
        return HttpResponse(result, content_type='application/json;charset=utf-8')


@csrf_exempt
def postgoods(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        itemname = request.POST.get('itemname')
        price = request.POST.get('price')
        detail = request.POST.get('detail')

        print(username)
        print(itemname)
        print(price)
        print(detail)
        result = {}
        try:
            print('testing')
            user = User.objects.get(username=username)
            print('hello')
            Goods.objects.create(seller_name=user, goods_name=itemname, minimum_price=price, detail=detail,
                                 lastprice=price)
            print('Am I here?')
            result['status'] = 1
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')
        except ObjectDoesNotExist as e:
            result['status'] = 0
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')


@csrf_exempt
def postuser(request):
    if request.method == 'POST':
        result = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        gm = request.POST.get('gm')
        u = request.POST.get('u')
        print(username)
        print(password)
        print(gm)
        print(u)

        try:
            print('trying to get objects')
            User.objects.get(username=username)
            print('obeject got')
            result['status'] = 0
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')
        except ObjectDoesNotExist as e:
            m2 = md5()
            # if(password):

            m2.update(password.encode('utf8'))
            password = m2.hexdigest()
            registAdd = User.objects.create(username=username, password=password, isAdministrator=gm, isGeneralUser=u)
            # registAdd.save()
            result['status'] = 1
            result = json.dumps(result)
            return HttpResponse(result, content_type='application/json;charset=utf-8')