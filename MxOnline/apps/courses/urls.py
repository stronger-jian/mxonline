__author__: 'jian'
__date__: '2018/7/17 10:14'

from django.urls import path,include
from .views import CourseListView,CourseDtailView,CourseInfoView,CommentsView,AddCommentsView, VideoPlayView


urlpatterns = [
    # 课程机构列表首页
    path('list/', CourseListView.as_view(), name='course_list'),
    #课程详情页面
    path('detail/<course_id>', CourseDtailView.as_view(), name='course_detail'),
    # 课程章节信息页面
    path('info/<course_id>', CourseInfoView.as_view(), name='course_info'),
    #课程评论信息页面
    path('comments/<course_id>', CommentsView.as_view(), name='course_comments'),
    #添加课程评论
    path('add_commment/', AddCommentsView.as_view(), name='add_comments'),
    #章节视频播放
    path('video/<video_id>', VideoPlayView.as_view(), name='video_play'),

    ]