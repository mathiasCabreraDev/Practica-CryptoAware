from django.urls import path
from  . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('grafico/<str:id>/', views.grafico, name='grafico'),
    path('<str:id>/', views.cryptocoin, name='cryptocoin'),
]