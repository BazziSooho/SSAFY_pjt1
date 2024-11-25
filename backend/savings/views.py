from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from .models import SavingProduct, ProductInterest, UserSaving
from .serializers import UserSavingSerializer, ProductInterestSerializer, SavingProductWithInterestSerializer
from accounts.serializers import UserWithSavingSerializer
import random

# recommendation functions for views
def max_profit():           # 만기 시 최대이익인 적금을 serializer로 리턴
    product_details = ProductInterest.objects.all() 
    for product_detail in product_details:
        product = product_detail.fin_prdt_cd        # 해당 상세정보의 원 상품(foreignkey로 연결된 savingproduct)
        current_max = 0

        max_limit = product.max_limit               # 최대 한도
        interest = product_detail.intr_rate2/100    # 최대 이율
        exp_month = product_detail.save_trm         # 저축 기간
        intr_type = product_detail.intr_rate_type   # 단리/복리

        if intr_type == 'S':    # 단리일때
            exp_money = max_limit*exp_month + (1+exp_month)//2*max_limit*interest
        else:                   # 복리일때
            exp_money = 0
            for i in range(1, exp_month+1):
                current_interest = (1+interest)**i
                exp_money += max_limit*current_interest
        
        if exp_money > current_max:
            current_max = exp_money
            serializer = SavingProductWithInterestSerializer(fin_prdt_cd=product)
        
    return serializer

def gacha():           # 랜덤픽 - 고민하기 싫은 사람들을 위한 최적의 픽
    product_details = ProductInterest.objects.all()
    random_pick = random.choice(product_details)
    serializer = SavingProductWithInterestSerializer(random_pick)
    return serializer

def high_score(pk):       # 유저가 선택한 적금 정보대로
    product_details = ProductInterest.objects.all()
    user_saving = UserSaving(pk=pk)
    if user_saving.join_deny != 1:
        product_details = ProductInterest.objects.exclude(fin_prdt_cd__join_deny=1)     # join_deny가 1이 아닌 상품들만 쿼리로 추출
    user_limit = user_saving.max_limit
    user_intr = user_saving.intr
    user_intr_type = user_saving.intr_rate_type
    user_saving_type = user_saving.rsrv_type
    user_exp_month = user_saving.save_trm
    
    high_score = 0
    
    for product_detail in product_details:
        product = product_detail.fin_prdt_cd        # 해당 상세정보의 원 상품(foreignkey로 연결된 savingproduct)
        prdt_limit = product_detail.fin_prdt_cd.max_limit
        prdt_intr = product_detail.intr_rate
        prdt_intr_type = product_detail.intr_rate_type
        prdt_saving_type = product_detail.rsrv_type
        prdt_exp_month = product_detail.save_trm

        score = 0
        intr_ratio = prdt_intr / user_intr
        limit_ratio = prdt_limit / user_limit
        exp_ratio = prdt_exp_month / user_exp_month

        if user_intr_type == prdt_intr_type and user_intr_type == 'S':      # 둘다 단리일때
            score += intr_ratio * limit_ratio * exp_ratio
            score += 3
        elif user_intr_type == prdt_intr_type and user_intr_type == 'M':    # 둘다 복리일때
            score += limit_ratio * (intr_ratio ** exp_ratio)
            score += 3
        elif user_intr_type == 'S' and prdt_intr_type == 'M':               # 유저는 단리 상품은 복리일때
            limit_ratio * intr_ratio
        else:                                                               # 유저가 복리고 상품은 단리일때(구려서 패스)
            continue

        if user_saving_type == prdt_saving_type:                            # 저축 방식이 같으면 가산점 왕창
            score += 10

        if score > high_score:
            high_score = score
            serializer = SavingProductWithInterestSerializer(fin_prdt_cd=product)
        
        
    return serializer

# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_saving(request):      # 입력받는 창 & 입력 받은 데이터 전송
    serializer = UserSavingSerializer()
    if request.method == 'GET':
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # 요청 데이터를 시리얼라이저로 전달
        serializer = UserSavingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 현재 로그인한 유저 정보와 함께 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])         # 적금 추천 해달라하는 창 - 어떤 적금 할건지 선택해서 추천 버튼 꾹
@permission_classes([IsAuthenticated])
def savings_recommendation(request):
    user = request.user
    if UserSavingSerializer(user.pk):                   # user가 입력한 적금이 있다면
        serializer = UserWithSavingSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:                                               # 적금이 없으면 아래 메세지를 띄우면서 추천 버튼 비활성화해야함
        return Response({"message": "적합한 추천 상품을 찾을 수 없습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_saving(request):     # 꾹햇을때 적금 추천하는 view
    interest = request.data.get('intr')
    print(interest)
    # 1. 가중치 추천 - 각 param마다 이익 점수 설정/ pk 값 받아서
    high_score_serializer = high_score(pk)
    # 1.1 유사도 추천 - 각 param마다 얼마나 유사한 지를 기준으로 가중치
        
    # 2. 랜덤픽 - 고민하기 싫은 사람들을 위한 최적의 픽
    random_serializer = gacha()
    # 3. 만기 시 최대 이익 추천 - 단리/복리에 따라 계산달리해서 추천
    max_serializer = max_profit()
    
    return Response({
        'random_data': random_serializer,
        'max_data': max_serializer,
        }, 
        status=status.HTTP_200_OK)
