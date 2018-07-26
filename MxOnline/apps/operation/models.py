from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course
# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=20, verbose_name=u'手机')
    course_name = models.CharField(max_length=20, verbose_name=u'课程名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'查询时间')

    class Meta:
        verbose_name=u'用户查询'
        verbose_name_plural=verbose_name


class CourseComments(models.Model):
    user=models.ForeignKey(UserProfile,verbose_name=u'用户',on_delete=models.CASCADE)
    course=models.ForeignKey(Course,verbose_name=u'课程',on_delete=models.CASCADE)
    comments=models.CharField(max_length=500, verbose_name=u'课程评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'评论时间')

    class Meta:
        verbose_name=u'用户评论'
        verbose_name_plural=verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户',on_delete=models.CASCADE)
    fav_id=models.IntegerField(default=0,verbose_name=u'数据id')#收藏的是课程 fav_id就是课程id  以此类推
    fav_type=models.IntegerField(choices=((1,u'课程'),(2,'课程机构'),(3,'讲师')),default=1,verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'收藏时间')

    class Meta:
        verbose_name=u'用户收藏'
        verbose_name_plural=verbose_name


class UserMessage(models.Model):
    user=models.IntegerField(default=0,verbose_name=u'接收用户')
    message=models.CharField(max_length=500, verbose_name=u'消息')
    has_read=models.BooleanField(default=False,verbose_name=u'消息是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name=u'用户消息'
        verbose_name_plural=verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=u'课程',on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'学习时间')

    class Meta:
        verbose_name=u'学习用户'
        verbose_name_plural=verbose_name