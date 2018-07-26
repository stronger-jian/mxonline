__author__: 'jian'
__date__: '2018/7/14 14:52'

from django.urls import path,include

#机构相关view
from .views import OrgListView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView
#教师相关view
from .views import TeacherListView,TeacherDetailView
app_name ='org'
urlpatterns = [
    # 课程机构列表首页
    path('list/', OrgListView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    path('home/<org_id>', OrgHomeView.as_view(), name='org_home'),
    path('course/<org_id>', OrgCourseView.as_view(), name='org_course'),
    path('desc/<org_id>', OrgDescView.as_view(), name='org_desc'),
    path('org_teachers/<org_id>', OrgTeacherView.as_view(), name='org_teachers'),

    #机构收藏
    path('add_fav/', AddFavView.as_view(), name='add_fav'),

    #教师
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    #教师详情
    path('teachers/detail/<teacher_id>', TeacherDetailView.as_view(), name='teacher_detail'),
]