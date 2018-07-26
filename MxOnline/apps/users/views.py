import json
from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.shortcuts import render_to_response

from .models import UserProfile,EmailVerifyRecord, PageBanner
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyForm, UploadImageForm, UsersInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):#自定义验证

        #完成自己后台逻辑
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            user.check_password(password)
            return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})
    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', "")  # 取到前端数据用户名
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form,'msg':'用户已经存在'})
            pass_word = request.POST.get('password', "")  # 取到前端数据密码
            user_profile=UserProfile()
            user_profile.username=user_name
            user_profile.is_active=False
            user_profile.email=user_name
            user_profile.password=make_password(pass_word)
            user_profile.save()

            #注册成功  发送用户信息
            user_message=UserMessage()
            user_message.user= user_profile.id
            user_message.message='恭喜您注册成功'
            user_message.save()

            send_register_email(user_name,'register')#发送邮件
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', { 'register_form':register_form})


class ActiveUserView(View):#激活
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class LogOutView(View):#退出
    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse('index'))


class LoginView(View):#登录
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', "")  # 取到前端数据用户名
            pass_word = request.POST.get('password', "")  # 取到前端数据密码
            # 开始认证用户名，密码使用auth的 authenticate
            user = authenticate(username=user_name, password=pass_word)  # 传递user_name和pass_word必须指明参数名称
            if user is not None:
                if user.is_active:
                    # 然后使用auth的login 方法完成登录
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                    # return render(request, 'index.html', {'login_form':login_form})这种方法 在登陆时没有ind数据

                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request,'login.html',{'msg': '用户名或密码错误！'})
        else:
            return render(request, 'login.html', {'login_form':login_form})
# Create your views here.
# def user_login(request):
#     if request.method == "POST":#前段把数据放在POST 中
#         user_name=request.POST.get('username',"")#取到前端数据用户名
#         pass_word=request.POST.get('password',"")#取到前端数据密码
#         #开始认证用户名，密码使用auth的 authenticate
#         user=authenticate(username=user_name,password=pass_word)#传递user_name和pass_word必须指明参数名称
#         if user is not None:
#             #然后使用auth的login 方法完成登录
#             login(request,user)
#             return render(request,'index.html')
#         else:
#             return render(request, 'login.html', {'msg':'用户名或密码错误！'})
#
#     elif request.method == "GET":
#         return render(request, 'login.html',{})


class ForgetPwdView(View):
    def get(self,request):
        forget_form=ForgetForm()
        return render(request,'forgetpwd.html', {'forget_form':forget_form})

    def post(self,request):
        forget_form=ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email', '')
            send_register_email(email,'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ReSetView(View):#找回密码
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')

class ModifyPwdView(View):
    """
    未登录状态下  修改密码
    """
    def post(self,request):
        modify_form=ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email=request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email},{'msg':'密码不一致'})
            user=UserProfile.objects.get(email=email)
            user.password=make_password(pwd2)#加密
            user.save()
            return render(request, 'login.html')
        else:
            email=request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email}, {'modify_form': modify_form})


#用户中心首页
class UsersInfoView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })
    def post(self, request):
        user_info_form = UsersInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UsersMyCourseView(LoginRequiredMixin, View):
    """
    个人中心 我的 课程
    """
    def get(self, request):
        user_courses= UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses':user_courses,
        })


class UserMyFavOrgView(LoginRequiredMixin, View):
    """
    个人中心  我的收藏  机构收藏
    """
    def get(self, request):
        fav_orgs=[]
        fav_org_ids= UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org_id in fav_org_ids:
            org= CourseOrg.objects.get(id=fav_org_id.fav_id)
            fav_orgs.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'fav_orgs':fav_orgs,
        })


class UserMyFavTeacherView(LoginRequiredMixin, View):
    """
    个人中心  我的收藏  授课教师
    """
    def get(self, request):
        fav_teachers=[]
        fav_teachers_ids= UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teachers_id in fav_teachers_ids:
            teacher= Teacher.objects.get(id=fav_teachers_id.fav_id)
            fav_teachers.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'fav_teachers':fav_teachers,
        })


class UserMyFavCourseView(LoginRequiredMixin, View):
    """
    个人中心  我的收藏  公开课程
    """
    def get(self, request):
        fav_courses=[]
        fav_courses_ids= UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_courses_id in fav_courses_ids:
            course= Course.objects.get(id=fav_courses_id.fav_id)
            fav_courses.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'fav_courses':fav_courses,
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    用户中心    我的消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        #进入用户中心后 取消未读消息
        all_unread= UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread:
            unread_message.has_read=True
            unread_message.save()

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 10, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages':messages,

        })


#用户上传个人头像
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        iamge_form = UploadImageForm(request.POST, request.FILES, instance= request.user)#instance实例化model，和之前的form构成modelform，可以直接保存
        if iamge_form.is_valid():
            iamge_form.save()
            # image= iamge_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    登录状态下  用户个人中心  修改密码
    """
    def post(self,request):
        modify_form=ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail",{"msg":密码不一致}', content_type='application/json')
            user=request.user
            user.password=make_password(pwd2)#加密
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送个人中心 修改邮箱验证码
    """
    def get(self,request):
        email=request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
       修改邮箱验证码
      """

    def post(self, request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        excited_records=EmailVerifyRecord.objects.filter(code=code, email=email, send_type='update_email')
        if excited_records:
            user= request.user
            user.email=email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"邮箱验证码错误"}', content_type='application/json')


class IndexView(View):
    def get(self, request):
        banners=PageBanner.objects.all().order_by('index')[:5]
        banner_courses=Course.objects.filter(is_banner=True)[:3]
        courses=Course.objects.all()[:6]
        course_orgs=CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'banners':banners,
            'banner_courses':banner_courses,
            'courses':courses,
            'course_orgs':course_orgs,
        })


def page_not_found(request):

    # response = render_to_response('404.html',{})
    # response.status_code=404
    return render_to_response('404.html')

def page_error(request):
    response = render_to_response('500.html',{})
    return response

