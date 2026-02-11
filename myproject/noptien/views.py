from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import NopTien
from hokhau.models import HoKhau
from khoanthu.models import KhoanThu


def hoadon(request):
    """
    Trang danh sách hóa đơn (nộp tiền) cho các khoản thu.
    Hỗ trợ tìm kiếm theo số hộ khẩu.
    """
    query = request.GET.get('q', '')
    hoadons = NopTien.objects.select_related('hokhau', 'khoanthu').order_by('id')
    
    if query:
        # Tìm kiếm theo số hộ khẩu
        hoadons = hoadons.filter(hokhau__sohokhau__icontains=query)
    
    return render(request, 'hoadon.html', {'hoadons': hoadons, 'query': query})


def create_hoadon(request):
    """
    Trang tạo mới hóa đơn (NopTien).
    Chọn hộ khẩu, khoản thu từ dropdown, nhập người nộp, số tiền, ngày nộp.
    """
    hokhaus = HoKhau.objects.order_by('sohokhau')
    khoanthus = KhoanThu.objects.order_by('tenkhoanthu')

    if request.method == 'POST':
        hokhau_id = request.POST.get('hokhau')
        ho_khau = HoKhau.objects.get(id=hokhau_id) if hokhau_id else None
        khoan_thu = KhoanThu.objects.get(id=request.POST['khoanthu'])
        hoadon = NopTien(
            hokhau=ho_khau,
            khoanthu=khoan_thu,
            nguoinoptien=request.POST['nguoinoptien'],
            sotien=request.POST['sotien'],
            ngaynop=request.POST['ngaynop'],
        )
        hoadon.save()
        return redirect('hoadon')

    context = {
        'hokhaus': hokhaus,
        'khoanthus': khoanthus,
    }
    return render(request, 'create_hoadon.html', context)


def xacnhan_thanh_toan(request, id):
    """
    Xác nhận thanh toán cho một hóa đơn:
    - Cập nhật ngày nộp = ngày hiện tại
    - Quay lại danh sách hóa đơn
    """
    hoadon = get_object_or_404(NopTien, id=id)

    if request.method == 'POST':
        hoadon.ngaynop = timezone.now().date()
        hoadon.save()
        return redirect('hoadon')

    # Nếu ai đó truy cập GET, cứ chuyển về danh sách để tránh lỗi
    return redirect('hoadon')
