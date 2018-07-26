from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course,CourseResource,Video
from operation.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):

    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        search_keywords= request.GET.get('keywords', '')
        if search_keywords:
            all_courses= all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        # 按课程人数和点击量筛选
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'courses':
                all_courses = all_courses.order_by('-click_nums')
        # 对课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort':sort,
            'hot_courses':hot_courses,
        })


class CourseDtailView(View):
    """
    课程详情页面
    """
    def get(self, request, course_id):
        #获取课程
        course = Course.objects.get(id=int(course_id))
        #课程点击数
        course.click_nums+=1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                has_fav_org = True
        #相关课程推荐
        tag=course.tag
        if tag:
            relate_courses=Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses=[]
        return render(request, 'course-detail.html', {
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节页面
    """

    def get(self, request, course_id):
        # 获取课程
        course = Course.objects.get(id=int(course_id))
        #学习人数
        course.students+=1
        course.save()
        #判断课程是否关联了  该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse()
            user_course.user=request.user
            user_course.course=course
            user_course.save()

        #课程资源
        all_resources = CourseResource.objects.filter(course=course)
        #学习过该课程的人还学习过的课程  首先找到 学习过该课程的人   再找这些人学习过 哪些课程   再排序
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        #学过这门课的人还学过的  所有课程
        all_courses = Course.objects.filter(id__in= course_ids).order_by('-click_nums')
        return render(request, 'course-video.html', {
            'course':course,
            'all_resources':all_resources,
            'all_courses':all_courses,
        })


class VideoPlayView(LoginRequiredMixin, View):
    """
    课程章节视频播放页面
    """

    def get(self, request, video_id):
        # 获取视频
        video = Video.objects.get(id=int(video_id))
        course=video.lesson.course
        course.students += 1
        course.save()
        # 判断课程是否关联了  该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = course
            user_course.save()

        # 课程资源
        all_resources = CourseResource.objects.filter(course=course)
        # 学习过该课程的人还学习过的课程  首先找到 学习过该课程的人   再找这些人学习过 哪些课程   再排序
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 学过这门课的人还学过的  所有课程
        all_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'all_courses': all_courses,
            'video':video,
        })



class CommentsView(LoginRequiredMixin, View):
    """
    课程评论页面
    """

    def get(self, request, course_id):
        current_app='current_app'
        # 获取课程
        course = Course.objects.get(id=int(course_id))
        # 判断课程是否关联了  该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = course
            user_course.save()

        # 课程资源
        all_resources = CourseResource.objects.filter(course=course)
        # 学习过该课程的人还学习过的课程  首先找到 学习过该课程的人   再找这些人学习过 哪些课程   再排序
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 学过这门课的人还学过的  所有课程
        all_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        #获取评论
        all_comments= CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments':all_comments,
            'all_courses':all_courses,
            'current_app':current_app
        })


class AddCommentsView(View):
    """
    用户添加评论
    """
    def post(self,request):

        # 用户登录判断
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        #评论的课程id
        course_id = request.POST.get('course_id',0)
        #评论的内容
        comments = request.POST.get('comments','')
        if int(course_id)>0 and comments: #如果课程id 存在和评论内容不为空
            course_comment= CourseComments()  #创造CourseComments课程评论实体
            course_comment.user= request.user
            course_comment.comments=comments
            course_comment.course= Course.objects.get(id=int(course_id))
            course_comment.save()
            return HttpResponse('{"status":"success","msg":";评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论出错"}', content_type='application/json')