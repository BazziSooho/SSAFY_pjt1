from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('ask/', views.question_list, name='question_list'),
    path('answer/<int:pk>/', views.question_detail, name='question_detail'),
    path('answer/<int:question_pk>/create/', views.create_answer, name='create_answer'),  # 댓글 작성
]
