import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Account

from django.contrib.auth.models import Group
# Register your models here.
# admin.site.register(Account)
admin.site.unregister(Group)
from django.contrib.admin.models import LogEntry


# def export_log(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="login.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Firstname','Lastname','Address','Email','Contact','City','State','Pincode','Password'])
#     login = queryset.values_list('first_name', 'last_name','address','email','contact','city','state','pincode','password')
#     for i in login:
#         writer.writerow(i)
#     return response


# export_log.short_description = 'Export to csv'


class LogAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','contact','email','is_staff','approved_staff']
    # actions = [export_log]
    search_fields = ['first_name']
    exclude = ('user_permissions','groups','is_superuser')
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            # 'show_save': False,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False,
            'Groups': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
admin.site.register(Account, LogAdmin)


# class sellerAdmin(admin.ModelAdmin):
#     list_display = ['first_name','last_name','is_staff','is_seller']
# admin.site.register(Seller)

