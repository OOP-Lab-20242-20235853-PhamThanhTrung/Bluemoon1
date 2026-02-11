from django import forms
from .models import TamTruTamVang

class TamTruTamVangForm(forms.ModelForm):
    class Meta:
        model = TamTruTamVang
        fields = ['nhankhau', 'trangthai', 'diachitamtrutamvang', 'thoigian', 'noidungdenghi']
        
        widgets = {
            'nhankhau': forms.Select(attrs={'class': 'form-control'}),
            'trangthai': forms.Select(choices=[('Tạm trú', '一時滞在'), ('Tạm vắng', '一時不在')], attrs={'class': 'form-control'}),
            'diachitamtrutamvang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ...'}),
            'thoigian': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'noidungdenghi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }