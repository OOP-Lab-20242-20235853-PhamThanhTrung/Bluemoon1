
from django.urls import path
from . import views

urlpatterns = [
    path('', views.nhankhau, name='nhankhau'),
    path('create/', views.create_nhankhau, name='create_nhankhau'),
    path('xem/<int:id>/', views.xem_nhankhau, name='xem_nhankhau'),
    path('update/<int:id>/', views.update_nhankhau, name='update_nhankhau'),
]