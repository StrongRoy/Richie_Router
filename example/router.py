# encoding:utf-8
# Author:Richie
# Date:12/14/2017
from django.utils.safestring import mark_safe

import router
from .models import UserInfo, UserType, Role


@router.register(UserInfo)
class UserInfoModelRouter(router.ModelRouter):
    # list_display_links = ['name']
    def edit(self,obj=None,flag=False):
        if flag:
            return 'edit'
        info = self.router_site.name,self.model._meta.app_label, self.model._meta.model_name,obj.id,'change'

        return mark_safe('<a href="/%s/%s/%s/%s/%s" class="btn btn-primary">编辑</a>' % info )
    def check_box(self,obj=None,flag=False):
        if flag:
            return '#'
        return mark_safe('<input type="checkbox">')

    list_display = [check_box,'id','name',edit]




# router.site.register(UserInfo,UserInfoModelRouter)
router.site.register(UserType)
router.site.register(Role)
