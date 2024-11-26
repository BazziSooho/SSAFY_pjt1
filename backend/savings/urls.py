from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('list/', views.savingproduct, name='savingproduct'),
    path('list/<int:product_id>/options/', views.savingproductinterest, name='option'),
    path('usersaving/', views.save_usersaving, name='save_usersaving'),
]
