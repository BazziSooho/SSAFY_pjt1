from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('add/', views.user_saving, name='user-saving'),
]
