from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    #定义表字段
    nick_name=models.CharField(max_length=50, verbose_name=u'昵称', default="")
    birday=models.DateField(verbose_name=u'生日', null=True,blank=True)
    gender=models.CharField(choices=(('male', u'男'), ('female', u'女')), max_length=10, default='female')
    address=models.CharField(max_length=500,default='')
    mobile=models.CharField(max_length=11,null=True,blank=True)
    image=models.ImageField(upload_to='image/%Y/%m',default=u'image/default.png',max_length=100, blank=True, null = True ,verbose_name= u'头像')

    class Meta:
        verbose_name=u'用户表信息'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username

    def get_unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):#邮箱验证码
    code=models.CharField(max_length=20,verbose_name=u'邮箱验证码')
    email=models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type=models.CharField(choices=(('register',u'注册'),('forget',u'找回密码'),('update_email',u'修改密码')),max_length=20,verbose_name=u'验证码类型')
    send_time=models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name=u'邮箱验证码'
        verbose_name_plural=verbose_name

    def __str__(self):#python3  def  Unicode   不好使
        return self.email   #'{0}{1}'.format(self.code, self.email)


class PageBanner(models.Model):
    title=models.CharField(max_length=100,verbose_name=u'标题')
    image=models.ImageField(upload_to='image/%Y/%m',verbose_name=u'轮播图片',max_length=100)
    url=models.URLField(max_length=200,verbose_name=u'访问网址')
    index=models.IntegerField(default=0,verbose_name=u'顺序')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'轮播图'
        verbose_name_plural=verbose_name

    def __str__(self):
        return  self.title