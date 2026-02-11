from django.db import models

# Create your models here.
class NhanKhau(models.Model):
    hoten=models.CharField(max_length=100)
    ngaysinh=models.DateField()
    gioitinh=models.CharField(max_length=10)
    dantoc=models.CharField(max_length=50)
    tongiao=models.CharField(max_length=50, blank=True, null=True)
    cccd=models.CharField(max_length=20, unique=True)
    ngaycap=models.DateField()
    noicap=models.CharField(max_length=100)
    nghenghiep=models.CharField(max_length=100, blank=True, null=True)
    ghichu=models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.hoten} - {self.cccd}"
