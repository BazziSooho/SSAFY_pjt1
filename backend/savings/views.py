from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from .models import SavingProduct, ProductInterest, UserSaving
from .serializers import UserSavingSerializer, ProductInterestSerializer
from accounts.serializers import UserWithSavingSerializer

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
    max_intr = ProductInterest.objects.aggregate(max('intr_rate2'))
    serializer = ProductInterestSerializer(intr_rate2=max_intr)
    return Response(serializer.data, status=status.HTTP_200_OK)
