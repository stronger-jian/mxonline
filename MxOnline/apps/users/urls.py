__author__: 'jian'
__date__: '2018/7/21 9:36'

from django.urls import path, include
from .views import UsersInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView
from .views import UsersMyCourseView, UserMyFavOrgView, UserMyFavTeacherView,UserMyFavCourseView, MyMessageView


app_name = 'users'
urlpatterns = [
    # 用户个人中心首页
    path('info/', UsersInfoView.as_view(), name='uesr_info'),
    #用户上传个人头像
    path('upload/image/', UploadImageView.as_view(), name='upload_image'),
    #用户修改个人密码
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    path('email_code/', SendEmailCodeView.as_view(), name='email_code'),
    # 用户修改个人邮箱
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),

    # 用户个人中心 我的课程
    path('mycourse/', UsersMyCourseView.as_view(), name='mycourse'),
    # 用户个人中心 我的收藏    机构收藏
    path('myfav/org', UserMyFavOrgView.as_view(), name='myfav_org'),
    # 用户个人中心 我的收藏    授课老师
    path('myfav/teacher/', UserMyFavTeacherView.as_view(), name='myfav_teacher'),
    # 用户个人中心 我的收藏    公开课程
    path('myfav/course/', UserMyFavCourseView.as_view(), name='myfav_course'),
    # 用户个人中心 我的消息
    path('mymessage/', MyMessageView.as_view(), name='mymessage'),
]