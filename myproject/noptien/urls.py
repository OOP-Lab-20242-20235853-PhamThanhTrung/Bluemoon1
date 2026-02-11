from django.urls import path
from . import views

urlpatterns = [
    path('', views.hoadon, name='hoadon'),
    path('create/', views.create_hoadon, name='create_hoadon'),
    path('xacnhan/<int:id>/', views.xacnhan_thanh_toan, name='xacnhan_thanh_toan'),
]

