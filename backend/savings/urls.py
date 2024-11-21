from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('mysaving/', views.user_saving),
]
