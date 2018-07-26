__author__: 'jian'
__date__: '2018/7/14 14:36'
import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name', ]

    def clean_mobile(self):
        """

        验证手机号码

        """

        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^[1][3,4,5,7,8][0-9]{9}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码错误', code='mobile_error')

