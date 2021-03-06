from django.shortcuts import render, HttpResponse

# Create your views here.
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings


def send_sms(request):
    tpl = request.GET.get('tpl')
    print(tpl)
    template_id = settings.TENCENT_SMS_TEMPLATE[tpl]
    if not template_id:
        return HttpResponse('模板不存在')
    code = random.randrange(1000, 9999)
    res = send_sms_single('15705426039', template_id=template_id, template_param_list=[code, 1])
    print(res)
    return HttpResponse('成功')


from django import forms
from app01 import models

from django.core.validators import RegexValidator


class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')],
                                   widget=forms.TextInput())
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(
    ))
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ('username','email','password','confirm_password','mobile_phone','code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
            filed.widget.attrs['placeholder'] = '请输入{}'.format(filed.label)


def register(request):
    form = RegisterModelForm()
    return render(request, 'app01/register.html', {"form": form})
    pass
