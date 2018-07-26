"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,reverse,include
from django.views.generic import TemplateView
# from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.views.static import serve
from django.conf.urls import url
from django.conf.urls import handler404, handler500
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import xadmin

from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ReSetView,ModifyPwdView, LogOutView, IndexView
from organization.views import OrgListView
from MxOnline.settings import MEDIA_ROOT,MEDIA_URL
from organization import urls as app_org_url
from courses import urls as course_url
from users import urls as users_url
from users.views import *

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('',IndexView.as_view(),name='index'),
    path('logout/', LogOutView.as_view(), name='logout'),  # 退出
    path('login/', LoginView.as_view(), name='login'),#登录
    path('register/', RegisterView.as_view(), name='register'),
    path('captcha/', include('captcha.urls')),
    path('active/<active_code>/',ActiveUserView.as_view(),name='user_active'),#?P  提取变量到active_code
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    path('reset/<active_code>/', ReSetView.as_view(), name='reset_pwd'),
    path('modify_view/', ModifyPwdView.as_view(), name='modify_pwd'),

    #课程机构相关的路径
    path('org/', include((app_org_url, 'org'), namespace='org')),
    # 课程相关的路径
    path('courses/', include((course_url, 'courses'), namespace='courses')),
    # 用户中心相关的路径
    path('users/', include((users_url, 'users'), namespace='users')),
    #配置上传文件的访问处理函数, 以下两种方法没用
    # url(r'^static/(?P<path>.*)$', serve,
    #     {'document_root': STATIC_ROOT}, name='static')

    # path('static/<path>', serve, {'document_root': STATIC_ROOT}),
    # path('media/<path>', serve, {'document_root': '/media/org/2018/07/2.jpg'}),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),


]
# 配置上传文件的访问处理函数
urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(STATIC_URL,document_root=STATIC_ROOT)
# urlpatterns += static('media/<path>', document_root=MEDIA_ROOT),

#配置404  500 页面
handler404='users.views.page_not_found'
handler500='users.views.page_error'