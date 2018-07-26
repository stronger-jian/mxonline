__author__: 'jian'
__date__: '2018/7/6 10:58'

from django import forms


from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email=forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField()


class ForgetForm(forms.Form):
    email=forms.EmailField(required=True)
    captcha = CaptchaField()


class ModifyForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', ]


class UsersInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile' ]
