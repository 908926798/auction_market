from rest_framework import serializers


class GoodsReviewSerializer(serializers.Serializer):
    G_number = serializers.IntegerField()
    goods_name = serializers.CharField(max_length=30)
    seller_name = serializers.CharField(read_only=True, max_length=30)
    minimum_price = serializers.IntegerField(required=False)
    detail = serializers.CharField(max_length=1000)


class GoodsInSerializer(serializers.Serializer):
    G_number = serializers.IntegerField()
    goods_name = serializers.CharField(max_length=30)
    lastbid_username = serializers.CharField(max_length=20)
    seller_name = serializers.CharField(read_only=True, max_length=30)
    lastprice = serializers.IntegerField()
    detail = serializers.CharField(max_length=1000)


class GoodsEndSerializer(serializers.Serializer):
    G_number = serializers.IntegerField()
    goods_name = serializers.CharField(max_length=30)
    lastbid_username = serializers.CharField(max_length=20)
    lastbid_time = serializers.DateTimeField()
    lastprice = serializers.IntegerField()
    detail = serializers.CharField(max_length=1000)


class GoodsSerializer(serializers.Serializer):
    G_number = serializers.IntegerField()
    goods_name = serializers.CharField(max_length=30)
    lastbid_username = serializers.CharField(max_length=20)
    lastbid_time = serializers.DateTimeField()
    lastprice = serializers.IntegerField()
    detail = serializers.CharField(max_length=1000)
    seller_name = serializers.CharField(max_length=30)
    minimum_price = serializers.IntegerField()
    status = serializers.CharField(max_length=6)


class PrivateChatSerializer(serializers.Serializer):
    sourceName = serializers.CharField(max_length=20)
    sourceIP = serializers.CharField(max_length=20)

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30,read_only=True)
    password = serializers.CharField(max_length=30)
    nickname = serializers.CharField(max_length=30)
    assets = serializers.IntegerField()