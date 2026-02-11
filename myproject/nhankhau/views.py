
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import NhanKhau
from .services import get_total_nhankhau
def nhankhau(request):
    total_nhankhau= get_total_nhankhau()
    query = request.GET.get('q', '')
    if query:
        nhankhaus = NhanKhau.objects.filter(
            Q(hoten__icontains=query) | Q(cccd__icontains=query)
        ).order_by("id")
    else:
        nhankhaus = NhanKhau.objects.order_by("id")
    return render(request, 'nhankhau.html', {'nhankhaus': nhankhaus, 'query': query, 'total_nhankhau': total_nhankhau})

def create_nhankhau(request):
    if request.method == 'POST':
        nhankhau = NhanKhau(
            hoten=request.POST['hoten'],
            ngaysinh=request.POST['ngaysinh'],
            gioitinh=request.POST['gioitinh'],
            dantoc=request.POST['dantoc'],
            tongiao=request.POST.get('tongiao', ''),
            cccd=request.POST['cccd'],
            ngaycap=request.POST['ngaycap'],
            noicap=request.POST['noicap'],
            nghenghiep=request.POST.get('nghenghiep', ''),
            ghichu=request.POST.get('ghichu', ''),
        )
        nhankhau.save()
        return redirect('nhankhau')
    return render(request, 'create_nhankhau.html')

def xem_nhankhau(request, id):
    nhankhau = get_object_or_404(NhanKhau, id=id)
    return render(request, 'xem_nhankhau.html', {'nhankhau': nhankhau})

def update_nhankhau(request, id):
    nhankhau = get_object_or_404(NhanKhau, id=id)
    if request.method == 'POST':
        nhankhau.hoten = request.POST['hoten']
        nhankhau.ngaysinh = request.POST['ngaysinh']
        nhankhau.gioitinh = request.POST['gioitinh']
        nhankhau.dantoc = request.POST['dantoc']
        nhankhau.tongiao = request.POST.get('tongiao', '')
        nhankhau.cccd = request.POST['cccd']
        nhankhau.ngaycap = request.POST['ngaycap']
        nhankhau.noicap = request.POST['noicap']
        nhankhau.nghenghiep = request.POST.get('nghenghiep', '')
        nhankhau.ghichu = request.POST.get('ghichu', '')
        nhankhau.save()
        return redirect('nhankhau')
    return render(request, 'update_nhankhau.html', {'nhankhau': nhankhau})