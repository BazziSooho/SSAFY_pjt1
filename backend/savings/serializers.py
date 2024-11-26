from rest_framework import serializers
from .models import SavingProduct, ProductInterest, UserSaving


class SavingProductSerializer(serializers.ModelSerializer):     # 적금 상품

    class Meta:
        model = SavingProduct
        fields = '__all__'

class UserSavingSerializer(serializers.ModelSerializer):        # 유저 입력정보

    class Meta:
        model = UserSaving
        fields = '__all__'
        read_only_fields = ['user']


class ProductInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInterest
        fields = ['id', 'intr_rate', 'intr_rate2', 'save_trm', 'intr_rate_type', 'rsrv_type']


class SavingProductWithInterestSerializer(serializers.ModelSerializer):
    productinterest_set = ProductInterestSerializer(many=True, read_only=True)

    class Meta:
        model = SavingProduct
        fields = [
            'id', 'fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'max_limit',
            'join_deny', 'join_member', 'productinterest_set'
        ]