from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import auth

from .models import CourseOrg,CityDict,Teacher
from operation.forms import UserAskForm
from  operation.models import UserFavorite
from courses.models import Course
# Create your views here.
class OrgListView(View):
    """
    课程机构列表功能
    """
    def get(self,request):
        #课程机构
        all_orgs=CourseOrg.objects.all()

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords)
                | Q(category__icontains=search_keywords) )

        #课程机构排名
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        #所在城市
        all_city=CityDict.objects.all()

        #取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs=all_orgs.filter(city_dict_id=int(city_id))
        #筛选机构类别
        category=request.GET.get('ct', '')
        if category:
            all_orgs=all_orgs.filter(category=category)
        org_nums = all_orgs.count()
        #按课程人数和课程数筛选
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')
        #对课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_city': all_city,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)#直接保存数据，不用实例化为model
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加错误"}', content_type='application/json')


class OrgHomeView(View):
    """
    课程机构首页
    """
    def get(self,request,org_id):
        current_page='home'
        course_org=CourseOrg.objects.get(id=int(org_id))
        #点击数
        course_org.click_nums+=1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        all_courses=course_org.course_set.all()[:3]
        all_teachers=course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav

        })


class OrgCourseView(View):
    """
    机构课程首页
    """

    def get(self, request, org_id):
        current_page='course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        #判断收藏状态
        has_fav=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=int(course_org.id),fav_type=2):
                has_fav=True
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav':has_fav

        })


class OrgDescView(View):
    """
    机构介绍页
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav

        })


class OrgTeacherView(View):
    """
    机构介绍页
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers=course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teachers':all_teachers,
            'current_page': current_page,
            'has_fav':has_fav

        })


class AddFavView(View):
    """
    用户收藏、收藏删除
    """
    def post(self,request):
        fav_id=request.POST.get('fav_id',0)
        fav_type=request.POST.get('fav_type',0)
        #用户登录判断
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        #用户是否收藏判断
        exsit_records=UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exsit_records:
            #如果记录存在   收藏取消
            exsit_records.delete()
            #收藏数减一
            if int(fav_type)==1:
                course= Course.objects.get(id=int(fav_id))
                course.fan_nums-=1
                if course.fan_nums<0:
                    course.fan_nums=0
                course.save()
            if int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fan_nums -= 1
                if course_org.fan_nums < 0:
                    course_org.fan_nums = 0
                course_org.save()
            if int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fan_nums -= 1
                if teacher.fan_nums < 0:
                    teacher.fan_nums = 0
                teacher.save()

            return HttpResponse('{"status":"fail","msg":"收藏"}', content_type='application/json')
        else:
            user_fav=UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                #收藏数加一
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fan_nums += 1
                    course.save()
                if int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fan_nums += 1
                    course_org.save()
                if int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fan_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self,request):

        all_teachers = Teacher.objects.all()
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))

        #按人气对教师排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        sorted_teacher= all_teachers.order_by('-click_nums')[:3]
        # 对授课教师分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 2, request=request)

        teachers = p.page(page)
        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
        })


class TeacherDetailView(View):
    def get(self,request, teacher_id):
        teacher= Teacher.objects.get(id=int(teacher_id))
        #点击数
        teacher.click_nums+=1
        teacher.save()
        all_courses=Course.objects.filter(teacher=teacher)
        #教师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        #是否收藏
        has_teacher_fav=False
        if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.id),fav_type=3):
            has_teacher_fav=True
        has_org_fav=False
        if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.org.id), fav_type=2):
            has_org_fav=True
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_fav':has_teacher_fav,
            'has_org_fav':has_org_fav
        })