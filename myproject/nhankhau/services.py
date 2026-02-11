from .models import NhanKhau

def get_total_nhankhau():
    return NhanKhau.objects.count()