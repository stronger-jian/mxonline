from datetime import datetime

from django.db import models

from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher

# Create your models here.



class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', on_delete=models.CASCADE,null=True,blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name=u'机构教师', on_delete=models.CASCADE, null=True, blank=True)
    is_banner=models.BooleanField(verbose_name=u'轮播课程', default=False)
    name=models.CharField(max_length=20,verbose_name=u'课程名称')
    desc=models.CharField(max_length=100,verbose_name=u'课程描述')
    detail=UEditorField(u'课程详情	',width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/", default='')
    degree=models.CharField(choices=(('CJ',u'初级'),('ZJ',u'中级'),('GJ',u'高级')),verbose_name=u'课程难度',max_length=10)
    learn_times=models.IntegerField(verbose_name=u'课程时长',default=0)
    students=models.IntegerField(verbose_name=u'学习人数',default=0)
    fan_nums=models.IntegerField(verbose_name=u'收藏人数',default=0)
    image=models.ImageField(upload_to='courses/%Y/%m',max_length=100,verbose_name=u'封面图片')
    click_nums=models.IntegerField(verbose_name=u'点击数',default=0)
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    tag = models.CharField(max_length=20, verbose_name=u'课程标签', default='')
    category=models.CharField(max_length=20,default= u'后端开发',verbose_name=u'课程类别')
    need_know= models.CharField(max_length=200,default= '', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=200, default='', verbose_name='老师告知')

    class Meta:
        verbose_name=u'课程信息表'
        verbose_name_plural=verbose_name

    def get_zj_nums(self):
        #计算课程章节
        zj_nums=self.lesson_set.all().count()
        return zj_nums
    get_zj_nums.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</>")
    go_to.short_description = '跳转'

    #得到课程章节
    def get_course_lesson(self):
        return self.lesson_set.all()

    #查看学习用户
    def get_course_user(self):
        return self.usercourse_set.all()[:5]

    def __str__(self):
        return self.name


class Lesson(models.Model):#课程Course和课程Lesson是一对多的关系，Python中一对多和多对多的关系都是用到外键
    course=models.ForeignKey(Course,verbose_name=u'课程',on_delete=models.CASCADE)#指向课程的外键
    name=models.CharField(verbose_name=u'章节名',max_length=20)
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    #得到课程视频
    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
            return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name=u'轮播课程'
        verbose_name_plural=verbose_name
        proxy=True


class Video(models.Model):
    lesson=models.ForeignKey(Lesson,verbose_name=u'章节',on_delete=models.CASCADE)#指向章节的外键
    name = models.CharField(verbose_name=u'视频名', max_length=20)
    url = models.CharField(verbose_name=u'视频地址', max_length=200, default='')
    learn_times = models.IntegerField(verbose_name=u'课程时长(分钟)', default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程',on_delete=models.CASCADE)  # 指向课程的外键
    name = models.CharField(verbose_name=u'课程资源名称', max_length=20)
    download=models.FileField(upload_to='course/resource/%Y/%m',max_length=100,verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name