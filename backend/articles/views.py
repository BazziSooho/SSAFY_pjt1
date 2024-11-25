from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

# URL 설정도 해주셔야 합니다!!!!!!!!!!!
# URL 설정도 해주셔야 합니다!!!!!!!!!!!

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])                      # 현재 작성된 질문 목록(GET)과 새 질문 작성(POST) 페이지
def question_list_create(request):
    if request.method == 'GET':
        questions = Question.objects.all().order_by('-created_at')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def question_detail(request, pk):                   # 
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
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
        serializer.save(question=question, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)