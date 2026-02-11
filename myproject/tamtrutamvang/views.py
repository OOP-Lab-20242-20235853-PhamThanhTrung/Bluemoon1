from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import TamTruTamVang
from .forms import TamTruTamVangForm
from django.utils import timezone
from datetime import date

# 1. Hàm xem danh sách
def danh_sach_tam_tru_tam_vang(request):
    # 1. Lấy tham số từ URL
    search_query = request.GET.get('q', '').strip() 
    filter_type = request.GET.get('filter', '') 

    # 2. Bắt đầu với toàn bộ danh sách (Sắp xếp mới nhất lên đầu)
    danh_sach = TamTruTamVang.objects.all().order_by('-thoigian')

    # 3. XỬ LÝ LỌC TRẠNG THÁI (Nên lọc cái này trước cho nhẹ)
    if filter_type == 'tam_tru':
        # Lấy cả 'tam tru' (không dấu) và 'Tạm trú' (có dấu)
        danh_sach = danh_sach.filter(trangthai='Tạm trú')
        
    elif filter_type == 'tam_vang':
        danh_sach = danh_sach.filter(trangthai='Tạm vắng')

    # 4. XỬ LÝ TÌM KIẾM TỪ KHÓA (Logic chuẩn dùng Q Object)
    if search_query:
        danh_sach = danh_sach.filter(
            Q(nhankhau__hoten__icontains=search_query) |       # Tìm theo Tên
            Q(nhankhau__cccd__icontains=search_query) |        # Tìm theo CCCD
            Q(diachitamtrutamvang__icontains=search_query)     # Tìm theo Địa chỉ
        )
    # 5. Trả về kết quả
    context = {
        'danh_sach': danh_sach,
        'current_filter': filter_type,
        'search_query': search_query
    }

    return render(request, 'tam_tru_tam_vang/index.html', context)

# 2. Hàm thêm mới
def them_moi_tttv(request):
    if request.method == 'POST':
        form = TamTruTamVangForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã thêm hồ sơ thành công!')
            return redirect('danh_sach_tttv')
    else:
        form = TamTruTamVangForm()
    
    return render(request, 'tam_tru_tam_vang/form.html', {'form': form, 'title': 'Đăng ký mới'})

# 3. Hàm sửa
def sua_tttv(request, id):
    ho_so = get_object_or_404(TamTruTamVang, pk=id)
    if request.method == 'POST':
        form = TamTruTamVangForm(request.POST, instance=ho_so)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect('danh_sach_tttv')
    else:
        form = TamTruTamVangForm(instance=ho_so)
        
    return render(request, 'tam_tru_tam_vang/form.html', {'form': form, 'title': 'Cập nhật hồ sơ'})

def in_phieu_tttv(request, id):
    # Lấy hồ sơ theo ID
    ho_so = get_object_or_404(TamTruTamVang, pk=id)
    
    # Trả về giao diện in riêng biệt
    return render(request, 'tam_tru_tam_vang/print.html', {'item': ho_so})

def dem_tam_tru_tam_vang():
    """
    Tính số lượng dựa trên trạng thái MỚI NHẤT của từng người tính đến hôm nay.
    """
    today = date.today()
    
    # 1. Lấy tất cả hồ sơ trong quá khứ và hiện tại (loại bỏ tương lai)
    # Sắp xếp theo thời gian tăng dần (cũ trước, mới sau)
    tat_ca_ho_so = TamTruTamVang.objects.filter(
        thoigian__lte=today
    ).order_by('thoigian', 'id') 
    # Thêm 'id' vào order_by để nếu cùng ngày thì bản ghi nhập sau sẽ được tính là mới nhất

    # 2. Dùng Dictionary để lưu trạng thái cuối cùng của từng nhân khẩu
    # Key = ID nhân khẩu, Value = Trạng thái ('Tạm trú' hoặc 'Tạm vắng')
    trang_thai_hien_tai = {}

    for ho_so in tat_ca_ho_so:
        # Vì vòng lặp chạy theo thời gian từ cũ -> mới
        # Nên trạng thái sau cùng sẽ ghi đè trạng thái trước đó
        trang_thai_hien_tai[ho_so.nhankhau_id] = ho_so.trangthai

    # 3. Đếm kết quả từ trạng thái cuối cùng
    dem_tam_tru = 0
    dem_tam_vang = 0

    for trangthai in trang_thai_hien_tai.values():
        if trangthai == 'Tạm trú':
            dem_tam_tru += 1
        elif trangthai == 'Tạm vắng':
            dem_tam_vang += 1
            
    return dem_tam_tru, dem_tam_vang
