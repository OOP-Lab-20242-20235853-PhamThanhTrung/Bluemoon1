from django.db import models

from nhankhau.models import NhanKhau

# Create your models here.


class HoKhau(models.Model):
    sohokhau = models.CharField(max_length=20, unique=True)
    sonha = models.CharField(max_length=100)
    duong = models.CharField(max_length=100)
    phuong = models.CharField(max_length=100)
    quan = models.CharField(max_length=100)
    ngaylamhokhau = models.DateField()
    chuhokhau = models.OneToOneField(NhanKhau, on_delete=models.PROTECT)
    sothanhvien = models.IntegerField()
    ghichu = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    def __str__(self):
        return f"Hokhau {self.sohokhau} - Chu ho: {self.chuhokhau.hoten}"


class ThanhVienHoKhau(models.Model):
    hokhau = models.ForeignKey(HoKhau, on_delete=models.CASCADE)
    nhankhau = models.ForeignKey(NhanKhau, on_delete=models.PROTECT)
    quanhevoichuho = models.CharField(max_length=100)
    ngaythemnhankhau = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_sothanhvien()

    def delete(self, *args, **kwargs):
        hokhau = self.hokhau
        super().delete(*args, **kwargs)
        self.update_sothanhvien(hokhau)

    def update_sothanhvien(self, hokhau=None):
        if hokhau is None:
            hokhau = self.hokhau
        # Số thành viên = số ThanhVienHoKhau + 1 (chu ho)
        hokhau.sothanhvien = ThanhVienHoKhau.objects.filter(hokhau=hokhau).count() + 1
        hokhau.save()
        # Cập nhật sotien cho NopTien liên quan
        from noptien.models import NopTien
        for noptien in NopTien.objects.filter(hokhau=hokhau):
            noptien.sotien = noptien.khoanthu.sotien * hokhau.sothanhvien
            noptien.save()

    def __str__(self):
        return f"Thanh vien: {self.nhankhau.hoten} - Quan he voi chu ho: {self.quanhevoichuho}"


class LichSuThayDoiHoKhau(models.Model):
    hokhau = models.ForeignKey(HoKhau, on_delete=models.CASCADE)
    nhankhau = models.ForeignKey(NhanKhau, on_delete=models.PROTECT)
    loaithaydoi = models.IntegerField(
    choices=[(1, 'Them thanh vien'), (2, 'Xoa thanh vien')])
    ngaythaydoi = models.DateTimeField()

    def __str__(self):
        return f"Lich su thay doi hokhau {self.hokhau.sohokhau} ngay {self.ngaythaydoi}"
