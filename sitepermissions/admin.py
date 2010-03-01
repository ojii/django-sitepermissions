from django.contrib.admin.options import ModelAdmin, StackedInline
from django.contrib.admin.sites import NotRegistered
from django.contrib.admin import site
from django.contrib.auth.models import User, Group
from django.forms.util import ErrorDict
from sitepermissions.models import SiteGroup
    
def invalid_form(form):
    def deco(**errors):
        form._update_errors(errors)
        return False
    return deco

    
def validator(admin, request, func):
    def decorator(form):
        real = func(form)
        if not real:
            return real
        data = form.clean()
        form.invalid_form = invalid_form(form)
        return admin.validate_form(admin, request, form, **data)
    return decorator
    
    
class SiteGroupAdmin(ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(SiteGroupAdmin, self).get_form(request, obj, **kwargs)
        form.is_valid = validator(self, request, form.is_valid)
        return form
    
    @staticmethod
    def validate_form(self, request, form):
        return True


def install_site_permission_admin():
    if Group in site._registry:
        old_class = site._registry[Group].__class__
        site.unregister(Group)
    else:
        old_class = ModelAdmin
        
    class SiteGroupInline(StackedInline):
        model = SiteGroup
        max_num = 1
        
    class GroupExtendedAdmin(old_class):
        inlines = old_class.inlines + [SiteGroupInline]
        
    site.register(Group, GroupExtendedAdmin)