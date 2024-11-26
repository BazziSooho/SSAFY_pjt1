from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from .models import SavingProduct, ProductInterest, UserSaving
from .serializers import UserSavingSerializer, ProductInterestSerializer, SavingProductWithInterestSerializer, SavingProductSerializer
from accounts.serializers import UserWithSavingSerializer
from django.http import JsonResponse
import random, requests


# recommendation functions for views
def max_profit():
    product_details = ProductInterest.objects.all()
    current_max = 0
    serializer_data = None

    for product_detail in product_details:
        product = product_detail.fin_prdt_cd  # ForeignKey로 연결된 SavingProduct
        max_limit = product.max_limit or 0
        interest = (product_detail.intr_rate2 or 0) / 100
        exp_month = product_detail.save_trm or 0
        intr_type = product_detail.intr_rate_type

        if intr_type == 'S':  # 단리일 때
            exp_money = max_limit * exp_month + (1 + exp_month) // 2 * max_limit * interest
        else:  # 복리일 때
            exp_money = 0
            for i in range(1, exp_month + 1):
                current_interest = (1 + interest) ** i
                exp_money += max_limit * current_interest

        if exp_money > current_max:
            current_max = exp_money
            serializer_data = SavingProductWithInterestSerializer(product).data  # .data 사용

    return serializer_data

def gacha():
    product_details = ProductInterest.objects.all()
    random_pick = random.choice(product_details)
    return SavingProductWithInterestSerializer(random_pick.fin_prdt_cd).data  # .data 사용

def high_score(pk, request):
    product_details = ProductInterest.objects.all()
    user_saving = UserSaving.objects.get(pk=pk)

    user_limit = user_saving.max_limit or 1
    user_intr = user_saving.intr or 1
    user_intr_type = user_saving.intr_rate_type or 'S'
    user_saving_type = user_saving.rsrv_type or ''
    user_exp_month = user_saving.save_trm or 1

    high_score = 0
    serializer_data = None

    for product_detail in product_details:
        product = product_detail.fin_prdt_cd
        prdt_limit = product.max_limit or 1
        prdt_intr = product_detail.intr_rate or 1
        prdt_intr_type = product_detail.intr_rate_type or 'S'
        prdt_saving_type = product_detail.rsrv_type or ''
        prdt_exp_month = product_detail.save_trm or 1

        score = 0
        intr_ratio = prdt_intr / user_intr
        limit_ratio = prdt_limit / user_limit
        exp_ratio = prdt_exp_month / user_exp_month

        if user_intr_type == prdt_intr_type and user_intr_type == 'S':
            score += intr_ratio * limit_ratio * exp_ratio
            score += 3
        elif user_intr_type == prdt_intr_type and user_intr_type == 'M':
            score += limit_ratio * (intr_ratio ** exp_ratio)
            score += 3

        if score > high_score:
            high_score = score
            serializer_data = SavingProductWithInterestSerializer(product, context={'request': request}).data

    return serializer_data

@api_view(['GET'])         # 적금 추천 해달라하는 창 - 어떤 적금 할건지 선택해서 추천 버튼 꾹
@permission_classes([IsAuthenticated])
def savings_recommendation(request):
    user = request.user
    if UserSavingSerializer(user.pk):                   # user가 입력한 적금이 있다면
        serializer = UserWithSavingSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:                                               # 적금이 없으면 아래 메세지를 띄우면서 추천 버튼 비활성화해야함
        return Response({"message": "추천에 필요한 본인의 적금 정보를 먼저 입력해주세요."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_saving(request):
    try:
        saving_id = request.data.get('saving_id')  # 선택된 적금 ID 가져오기
        user_saving = UserSaving.objects.get(id=saving_id)

        # 추천 알고리즘 실행
        high_score_serializer_data = high_score(user_saving.pk, request)
        random_serializer_data = gacha()
        max_serializer_data = max_profit()

        # 추천 데이터를 배열로 반환
        recommendations = [
            {'type': 'high_score', 'data': high_score_serializer_data},
            {'type': 'random', 'data': random_serializer_data},
            {'type': 'max_profit', 'data': max_serializer_data},
        ]

        return JsonResponse(recommendations, safe=False)  # 배열로 직렬화
    except UserSaving.DoesNotExist:
        return JsonResponse({"error": "적금을 찾을 수 없습니다."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def savingproduct(request) :    # 적금 전체 리스트 보여주는 view
    products = SavingProduct.objects.all().values()
    return JsonResponse(list(products), safe=False)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def savingproductinterest(request, product_id):
    try:
        # SavingProduct의 id로 해당 상품 가져오기
        product = SavingProduct.objects.get(id=product_id)
        fin_prdt_cd = product.fin_prdt_cd  # 참조되는 fin_prdt_cd 가져오기

        # ProductInterest에서 해당 상품(fin_prdt_cd)의 옵션 데이터 가져오기
        options = ProductInterest.objects.filter(fin_prdt_cd=fin_prdt_cd).values()

        return JsonResponse({"options": list(options)}, safe=False)
    except SavingProduct.DoesNotExist:
        return JsonResponse({"error": "해당 상품을 찾을 수 없습니다."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# 개인 적금정보 조회 & usersaving에 내 적금정보 추가

@api_view(['GET'])
@permission_classes([IsAuthenticated])              # 개인 적금정보 조회             
def my_savings(request):
    user = request.user  # 현재 로그인된 사용자 가져오기
    savings = UserSaving.objects.filter(user=user)  # 로그인된 사용자의 데이터만 필터링
    data = list(savings.values('id', 'bank', 'product', 'mtrt', 'intr', 'save_trm'))
    return Response(data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_saving(request):      # 입력받는 창 & 입력 받은 데이터 전송
    try:
        data = request.data
        user = request.user

        for item in data:
            UserSaving.objects.create(
                user_id=user.id,
                bank=item.get('bank'),
                product=item.get('product'),
                mtrt=item.get('mtrt'),
                intr=item.get('intr'),
                join_deny=item.get('join_deny'),
                join_member=item.get('join_member'),
                max_limit=item.get('max_limit'),
                intr_rate_type=item.get('intr_rate_type'),
                rsrv_type=item.get('rsrv_type'),
                save_trm=item.get('save_trm', 0),
            )

        return Response({"message": "저장되었습니다."}, status=201)
    except Exception as e:
        print("Error:", str(e))  # 오류 출력
        return Response({"error": str(e)}, status=400)

