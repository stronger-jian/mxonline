__author__: 'jian'
__date__: '2018/7/3 11:19'

import xadmin

from .models import CityDict,CourseOrg,Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']

class CourseOrgAdmin(object):
    list_display = ['city_dict', 'name', 'desc','fan_nums','click_nums','image','address']
    search_fields = ['city_dict', 'name', 'desc','fan_nums','click_nums','image','address']
    list_filter = ['city_dict', 'name', 'desc','fan_nums','click_nums','image','address']
    # relfield_style='fk-ajax'  用了无效

class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years','work_company','work_position','points','fan_nums','click_nums','add_time']
    search_fields = ['org', 'name', 'work_years','work_company','work_position','points','fan_nums','click_nums']
    list_filter = ['org', 'name', 'work_years','work_company','work_position','points','fan_nums','click_nums','add_time']

xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)