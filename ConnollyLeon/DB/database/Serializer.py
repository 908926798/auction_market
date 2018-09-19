from rest_framework import serializers

class GoodsReviewSerializer(serializers.Serializer):
    goods_name = serializers.CharField(max_length=30)
    seller_name = serializers.CharField(read_only=True, max_length=30)
    minimum_price =serializers.IntegerField(required=False)

class GoodsInSerializer(serializers.Serializer):
    goods_name = serializers.CharField(max_length=30)


class PrivateChatSerializer(serializers.Serializer):
    sourceName = serializers.CharField(max_length=20)
    sourceIP = serializers.CharField(max_length=20)
