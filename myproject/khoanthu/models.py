from django.db import models

# Create your models here.
class KhoanThu(models.Model):
    tenkhoanthu = models.CharField(max_length=100)
    ngaytao = models.DateField()
    thoihan = models.DateField()
    batbuoc = models.BooleanField(default=False)
    ghichu = models.TextField(null=True, blank=True)
    sotien = models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self):
        return f"{self.tenkhoanthu} - {self.sotien} VND"