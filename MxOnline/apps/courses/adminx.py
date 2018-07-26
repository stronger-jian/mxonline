__author__: 'jian'
__date__: '2018/7/3 10:40'

import xadmin

from .models import Course,Lesson,Video,CourseResource, BannerCourse
from organization.models import CourseOrg

class LessonInline(object):
    model=Lesson
    extra=0

class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fan_nums', 'image', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fan_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fan_nums', 'image', 'click_nums',
                   'add_time']
    odering = ['-click_nums']
    # readonly_fields=['click_nums','fan_nums']
    list_editable=['degree', 'detail']

    def queryset(self):
        qs=super(BannerCourseAdmin, self).queryset()
        return qs.filter(is_banner=True)

class CourseAdmin(object):
    list_display=['name','desc','detail','degree','learn_times','students','fan_nums','image','click_nums','add_time', 'get_zj_nums', 'go_to']
    search_fields=['name','desc','detail','degree','students','fan_nums','image','click_nums']
    list_filter=['name','desc','detail','degree','learn_times','students','fan_nums','image','click_nums','add_time']
    odering=['-click_nums']
    # readonly_fields=['click_nums','fan_nums']
    exclude=['fan_nums']
    # inlines=[LessonInline]#这个内部model 没有成功
    refresh_times=[3,5]#刷新时间
    style_fields={'detail':'ueditor'}

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        return qs.filter(is_banner=False)

    def save_models(self):# 在保存课程时并统计机构课程数
        obj=self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org=obj.course_org
            course_org.course_nums=Course.objects.filter(course_org=course_org).count()
            course_org.save()


class LessonAdmin(object):
    list_display=['course','name','add_time']
    search_fields=['course','name']
    list_filter=['course__name','name','add_time']

class VideoAdmin(object):
    list_display=['lesson','name','add_time']
    search_fields=['lesson','name']
    list_filter=['lesson','name','add_time']

class CourseResourceAdmin():
    list_display=['course','name','download','add_time']
    search_fields=['course','name','download']
    list_filter=['course','name','download','add_time']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)