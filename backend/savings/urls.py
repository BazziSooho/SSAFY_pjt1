from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('list/', views.savingproduct, name='savingproduct'),                           # 적금목록 조회
    path('list/<int:product_id>/options/', views.savingproductinterest, name='option'), # 적금옵션 조회
    path('usersaving/', views.user_saving, name='save_usersaving'),                     # usersaving db에 저장
    path('my-savings/', views.my_savings, name='check_usersaving'),                     # 내 적금정보 조회
    path('recommendation/', views.recommend_saving, name='recommendation'),             # 적금 추천해주는 url
]