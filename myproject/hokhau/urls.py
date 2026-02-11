
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hokhau, name='hokhau'),
    path('create/', views.create_hokhau, name='create_hokhau'),
    path('view/<int:pk>/', views.xem_hokhau, name='xem_hokhau'),
    path('update/<int:pk>/', views.update_hokhau, name='update_hokhau'),
    path('history/<int:pk>/', views.lich_su_hokhau, name='lich_su_hokhau'),

]
