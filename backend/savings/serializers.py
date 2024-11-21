from rest_framework import serializers
from .models import SavingProduct, ProductInterest, UserSaving


class ProductInterestSerializer(serializers.ModelSerializer):   # 이율 정보

    class Meta:
        model = ProductInterest
        fields = '__all__'

class SavingProductSerializer(serializers.ModelSerializer):     # 적금 상품

    class Meta:
        model = SavingProduct
        fields = '__all__'

class UserSavingSerializer(serializers.ModelSerializer):        # 유저 입력정보

    class Meta:
        model = UserSaving
        fields = '__all__'
        read_only = ('user')



class SavingProductWithInterestSerializer(serializers.ModelSerializer):   # 적금이율정보

    productinterest_set = ProductInterestSerializer(many=True, read_only=True)

    class Meta:
        model = SavingProduct
        fields = '__all__'

    