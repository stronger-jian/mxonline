__author__: 'jian'
__date__: '2018/7/2 16:30'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from .models import PageBanner

class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True

class GloabalSetting(object):
    site_title="幕学在线学习后台"
    site_footer="幕学在线学习网"
    menu_style="accordion"

class EmailVerifyRecordAdmin(object):
    list_display= ['code', 'email', 'send_type', 'send_time']
    search_fields= ['code', 'email', 'send_type']
    list_filter= ['code', 'email', 'send_type', 'send_time']
    model_icon= 'fa fa-envelope'


class PageBannerAdmin(object):
    list_display=['title', 'image', 'url', 'index', 'add_time']
    search_fields=['title', 'image', 'url', 'index']
    list_filter=['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(PageBanner, PageBannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GloabalSetting)