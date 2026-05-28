from django import forms
from .models import IpAddress, Person


class IpEditForm(forms.ModelForm):
    """IP 수정 전용 폼 — IP 주소·그룹은 읽기 전용, 사용자는 AJAX 검색으로 선택"""

    # AJAX로 선택된 person pk를 받는 숨김 필드
    person_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = IpAddress
        fields = ['note', 'start_date', 'end_date']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
        }
        labels = {
            'note': '메모',
            'start_date': '사용 시작일',
            'end_date': '사용 종료일',
        }

    def clean(self):
        cleaned = super().clean()
        pid = cleaned.get('person_id')
        if pid:
            try:
                cleaned['_person'] = Person.objects.get(pk=pid)
            except Person.DoesNotExist:
                self.add_error('person_id', '존재하지 않는 사용자입니다.')
        else:
            cleaned['_person'] = None
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.person = self.cleaned_data.get('_person')
        if commit:
            obj.save()
        return obj
