from django.urls import path
from . import views

urlpatterns = [
    # Đường dẫn xem danh sách
    path('tamtrutamvang/', views.danh_sach_tam_tru_tam_vang, name='danh_sach_tttv'),
    
    # Đường dẫn thêm mới
    path('tamtrutamvang/them/', views.them_moi_tttv, name='them_moi_tttv'),
    
    # Đường dẫn sửa
    path('tamtrutamvang/sua/<int:id>/', views.sua_tttv, name='sua_tttv'),

    path('in-phieu/<int:id>/', views.in_phieu_tttv, name='in_phieu_tttv'),
]