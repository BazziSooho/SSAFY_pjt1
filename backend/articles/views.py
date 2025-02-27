from django.db.models import F
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])                      # 현재 작성된 질문 목록(GET)과 새 질문 작성(POST) 페이지
def question_list(request):
    if request.method == 'GET':
        questions = Question.objects.all().order_by('-views')      # 조회수 순으로 내림차순정렬해보자
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def question_detail(request, pk):                   #       조회수를 넣어보자
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # 조회수 증가
        Question.objects.filter(pk=pk).update(views=F('views') + 1)     # db 값에 직접 접근할때 유용한 F 메서드
        
        # 업데이트된 질문 객체 다시 가져오기
        question.refresh_from_db()                                      # models.Model의 내장 메서드 
        
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])              # 관리자일때 답글 작성 가능
def create_answer(request, question_pk):
    try:
        question = Question.objects.get(pk=question_pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AnswerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(question=question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)