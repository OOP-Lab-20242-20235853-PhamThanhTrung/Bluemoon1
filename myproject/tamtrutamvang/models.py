from django.db import models

from nhankhau.models import NhanKhau

# Create your models here.
class TamTruTamVang(models.Model):
    nhankhau = models.ForeignKey(NhanKhau, on_delete=models.PROTECT)
    trangthai = models.CharField(max_length=20) # 'tam tru' hoac 'tam vang'
    diachitamtrutamvang = models.CharField(max_length=200)
    thoigian = models.DateField()
    noidungdenghi = models.TextField(null=True, blank=True)
