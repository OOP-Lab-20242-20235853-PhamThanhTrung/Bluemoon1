from django.shortcuts import render, redirect, get_object_or_404
from .models import KhoanThu
from hokhau.models import HoKhau
from noptien.models import NopTien

# Create your views here.
def khoanthu(request):
    khoanthus = KhoanThu.objects.order_by("id")
    return render(request, 'khoanthu.html', {'khoanthus': khoanthus})


def create_khoanthu(request):
    """
    Trang tạo mới KhoanThu.
    Nhận dữ liệu từ form và lưu vào database, sau đó quay lại danh sách khoản thu.
    Sau khi tạo, tự động tạo hóa đơn cho tất cả hộ khẩu (bắt buộc hoặc tự nguyện).
    """
    if request.method == 'POST':
        khoanthu = KhoanThu(
            tenkhoanthu=request.POST['tenkhoanthu'],
            ngaytao=request.POST['ngaytao'],
            thoihan=request.POST['thoihan'],
            batbuoc=bool(request.POST.get('batbuoc')),
            ghichu=request.POST.get('ghichu', ''),
            sotien=request.POST['sotien'],
        )
        khoanthu.save()

        # Tự động tạo hóa đơn cho tất cả hộ khẩu (bất kể khoản thu bắt buộc hay tự nguyện)
        hokhaus = HoKhau.objects.all()
        for hokhau in hokhaus:
            # Kiểm tra xem đã có hóa đơn cho hộ khẩu này và khoản thu này chưa
            if not NopTien.objects.filter(hokhau=hokhau, khoanthu=khoanthu).exists():
                NopTien.objects.create(
                    hokhau=hokhau,
                    khoanthu=khoanthu,
                    nguoinoptien=hokhau.chuhokhau.hoten if hasattr(hokhau, "chuhokhau") and hokhau.chuhokhau else "Chưa nộp",
                    sotien=khoanthu.sotien * hokhau.sothanhvien,  # Nhân với số thành viên
                    ngaynop=None,  # Để trống, sẽ cập nhật khi xác nhận thanh toán
                )
        
        return redirect('khoanthu')

    return render(request, 'create_khoanthu.html')


def xem_khoanthu(request, id):
    """Xem chi tiết một khoản thu."""
    khoanthu = get_object_or_404(KhoanThu, id=id)
    da_dong = NopTien.objects.filter(khoanthu=khoanthu, ngaynop__isnull=False).count()
    chua_dong = NopTien.objects.filter(khoanthu=khoanthu, ngaynop__isnull=True).count()
    return render(request, 'xem_khoanthu.html', {
        'khoanthu': khoanthu,
        'da_dong': da_dong,
        'chua_dong': chua_dong
    })


def update_khoanthu(request, id):
    """
    Cập nhật thông tin một khoản thu.
    Nếu chuyển từ không bắt buộc sang bắt buộc, tự động tạo hóa đơn cho các hộ khẩu chưa có.
    """
    khoanthu = get_object_or_404(KhoanThu, id=id)
    was_batbuoc = khoanthu.batbuoc  # Lưu trạng thái cũ

    if request.method == 'POST':
        khoanthu.tenkhoanthu = request.POST['tenkhoanthu']
        khoanthu.ngaytao = request.POST['ngaytao']
        khoanthu.thoihan = request.POST['thoihan']
        khoanthu.batbuoc = bool(request.POST.get('batbuoc'))
        khoanthu.ghichu = request.POST.get('ghichu', '')
        khoanthu.sotien = request.POST['sotien']
        khoanthu.save()
        
        # Cập nhật sotien cho các NopTien liên quan
        noptien_list = NopTien.objects.filter(khoanthu=khoanthu)
        for noptien in noptien_list:
            noptien.sotien = khoanthu.sotien * noptien.hokhau.sothanhvien
            noptien.save()
        
        # Nếu chuyển từ không bắt buộc sang bắt buộc, tạo hóa đơn cho các hộ khẩu chưa có
        if not was_batbuoc and khoanthu.batbuoc:
            hokhaus = HoKhau.objects.all()
            for hokhau in hokhaus:
                # Chỉ tạo nếu chưa có hóa đơn cho hộ khẩu này và khoản thu này
                if not NopTien.objects.filter(hokhau=hokhau, khoanthu=khoanthu).exists():
                    NopTien.objects.create(
                        hokhau=hokhau,
                        khoanthu=khoanthu,
                        nguoinoptien=hokhau.chuhokhau.hoten if hokhau.chuhokhau else "Chưa nộp",
                        sotien=khoanthu.sotien * hokhau.sothanhvien,
                        ngaynop=None,  # Để trống, sẽ cập nhật khi xác nhận thanh toán
                    )
        
        return redirect('khoanthu')

    return render(request, 'update_khoanthu.html', {'khoanthu': khoanthu})
