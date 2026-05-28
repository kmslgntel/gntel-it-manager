import ipaddress
from django import forms
from .models import IpAddress, IpGroup, Person


class IpAddressForm(forms.ModelForm):
    class Meta:
        model = IpAddress
        fields = ['ip', 'group', 'person', 'note', 'start_date', 'end_date']
        widgets = {
            'ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 192.168.1.100'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'person': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
        }
        labels = {
            'ip': 'IP 주소',
            'group': 'IP 그룹',
            'person': '사용자',
            'note': '메모',
            'start_date': '사용 시작일',
            'end_date': '사용 종료일',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].required = False
        self.fields['group'].empty_label = '-- 그룹 선택 --'
        self.fields['person'].required = False
        self.fields['person'].empty_label = '-- 미사용 --'
        self.fields['person'].queryset = Person.objects.filter(use_yn='Y').order_by('name')

    def clean_ip(self):
        ip = self.cleaned_data.get('ip', '').strip()
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise forms.ValidationError('유효한 IP 주소를 입력해주세요.')
        # 수정 시 자기 자신 제외, 등록 시 중복 체크
        qs = IpAddress.objects.filter(ip=ip)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('이미 등록된 IP 주소입니다.')
        return ip
