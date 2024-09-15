from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserInfo

class UserInfoCreationForm(UserCreationForm):
    class Meta:
        model = UserInfo
        fields = ('user_email', 'user_name', 'user_tel1', 'user_tel2', 'user_addr1', 'user_addr2', 
                  'user_corpname', 'user_corpdept', 'user_corptype', 'password1', 'password2')
        labels = {
            'user_email': '이메일',
            'user_name': '이름',
            'user_tel1': '유선번호',
            'user_tel2': '무선번호(핸드폰)',
            'user_addr1': '주소',
            'user_addr2': '세부주소',
            'user_corpname': '소속회사',
            'user_corpdept': '소속부서',
            'user_corptype': '회사유형',
        }
        widgets = {
            'user_addr1': forms.TextInput(attrs={'placeholder': '기본 주소'}),
            'user_addr2': forms.TextInput(attrs={'placeholder': '상세 주소'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 선택적 필드에 대해 required=False 설정
        optional_fields = ['user_tel1', 'user_addr1', 'user_addr2']
        for field in optional_fields:
            self.fields[field].required = False

    def clean_user_email(self):
        email = self.cleaned_data['user_email']
        if UserInfo.objects.filter(user_email=email).exists():
            raise forms.ValidationError("이미 사용 중인 이메일 주소입니다.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user