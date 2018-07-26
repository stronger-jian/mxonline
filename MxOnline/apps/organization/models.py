from datetime import datetime

from django.db import models

# Create your models here.
class CityDict(models.Model):
    name=models.CharField(max_length=20,verbose_name=u'城市名')
    desc=models.CharField(max_length=150,verbose_name=u'城市描述')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'城市名称'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    city_dict=models.ForeignKey(CityDict,verbose_name=u'城市',on_delete=models.CASCADE)#  主外关系键中，级联删除，也就是当删除主表的数据时候从表中的数据也随着一起删除
    name = models.CharField(max_length=20, verbose_name=u'机构名')
    tag = models.CharField(max_length=10, verbose_name=u'机构标签', default='全国知名')
    category=models.CharField(max_length=20, default='pxjg',verbose_name=u'课程机构类别',choices=(('pxjg','培训机构'),('gx', '高校'),('gr', '个人')))
    desc=models.TextField(verbose_name=u'机构描述')
    fan_nums = models.IntegerField(verbose_name=u'收藏人数', default=0)
    click_nums = models.IntegerField(verbose_name=u'点击数', default=0)
    students = models.IntegerField(verbose_name=u'学习人数', default=0)
    course_nums = models.IntegerField(verbose_name=u'课程数', default=0)
    image = models.ImageField(upload_to='org/%Y/%m', max_length=100, verbose_name=u'logo封面')
    address=models.CharField(verbose_name=u'机构地址',max_length=150)

    class Meta:
        verbose_name = u'机构名称'
        verbose_name_plural = verbose_name

    #机构教师人数
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org=models.ForeignKey(CourseOrg,verbose_name=u'所属机构',on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name=u'教师名')
    work_years=models.IntegerField(verbose_name=u'工作年限')
    work_company=models.CharField(max_length=50, verbose_name=u'工作地点')
    work_position= models.CharField(max_length=50, verbose_name=u'公司职位')
    points = models.CharField(max_length=150, verbose_name=u'教学特点')
    fan_nums = models.IntegerField(verbose_name=u'收藏人数', default=0)
    click_nums = models.IntegerField(verbose_name=u'点击数', default=0)
    image = models.ImageField(default='',upload_to='teachers/%Y/%m', max_length=100, verbose_name=u'教师封面')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    age= models.IntegerField(verbose_name=u'教师年龄', default=18)

    class Meta:
        verbose_name = u'教师名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return  self.course_set.all().count()