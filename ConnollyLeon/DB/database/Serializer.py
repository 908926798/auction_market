from rest_framework import serializers


class GoodsReviewSerializer(serializers.Serializer):
    G_number = serializers.IntegerField()
    goods_name = serializers.CharField(max_length=30)
    seller_name = serializers.CharField(read_only=True, max_length=30)
    minimum_price = serializers.IntegerField(required=False)


class GoodsInSerializer(serializers.Serializer):
    G_number = serializers.IntegerField()
    goods_name = serializers.CharField(max_length=30)
    lastbid_username = serializers.CharField(max_length=20)
    seller_name = serializers.CharField(read_only=True, max_length=30)
    lastprice = serializers.IntegerField()

class GoodsEndSerializer(serializers.Serializer):
    G_number = serializers.IntegerField()
    goods_name = serializers.CharField(max_length=30)
    lastbid_username = serializers.CharField(max_length=20)
    lastbid_time = serializers.DateTimeField()
    lastprice = serializers.IntegerField()

class PrivateChatSerializer(serializers.Serializer):
    sourceName = serializers.CharField(max_length=20)
    sourceIP = serializers.CharField(max_length=20)
