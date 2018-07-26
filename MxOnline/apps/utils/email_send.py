__author__: 'jian'
__date__: '2018/7/9 11:30'

from random import Random
from django.core.mail import send_mail#django自带的发送邮件方法

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM

def send_register_email(email,send_type='register'):#register是初始化中type的值
    email_record=EmailVerifyRecord()#验证码实例化对象
    #开始生成验证码并保存到数据库
    if send_type== 'update_email':
        code = random_str(4)
    else:
        code=random_str(16)#生成16位随即字符串
    email_record.code=code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    #定义邮件内容，发送有Python 自定义的方法
    email_title=''
    email_body=''
    #区别邮件发送类型
    if send_type=='register':
        email_title='慕学在线激活链接'
        email_body='点击下面链接激活此帐号:http://127.0.0.8000/active/{0}'.format(code)

        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = '慕学在线找回密码链接'
        email_body = '点击下面链接找回此帐号密码:http://127.0.0.8000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = '慕学在线修改邮箱验证码链接'
        email_body = '验证码：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
                pass


#生成随机字符串的函数
def random_str(rangdomlength=8):
    str=''
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length=len(chars)-1
    random=Random()#根据length 生成随机长度
    for i in range(rangdomlength):
        str+=chars[random.randint(0,length)]
    return str