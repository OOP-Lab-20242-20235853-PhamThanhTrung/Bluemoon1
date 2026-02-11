from django.db import models
from hokhau.models import HoKhau
from khoanthu.models import KhoanThu
# Create your models here.
class NopTien(models.Model):
    hokhau = models.ForeignKey(HoKhau, on_delete=models.CASCADE, null=True, blank=True)
    khoanthu = models.ForeignKey(KhoanThu, on_delete=models.CASCADE)
    nguoinoptien = models.CharField(max_length=100)
    sotien = models.DecimalField(max_digits=12, decimal_places=2)
    ngaynop = models.DateField(null=True, blank=True)