from django.urls import path
from . import views

urlpatterns = [
    path('', views.khoanthu, name='khoanthu'),
    path('create/', views.create_khoanthu, name='create_khoanthu'),
    path('xem/<int:id>/', views.xem_khoanthu, name='xem_khoanthu'),
    path('update/<int:id>/', views.update_khoanthu, name='update_khoanthu'),
]
