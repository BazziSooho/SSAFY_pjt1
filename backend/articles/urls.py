from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('ask/', views.question_list, name='question_list'),
    path('answer/', views.question_detail, name='question_detail'),
    path('compare/', views.user_saving, name='user-saving'),
]
