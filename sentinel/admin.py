from django.contrib import admin

# Register your models here.
from sentinel.models import end_user, access_lvl, activity_log, notification, notification_recipient, audit_log

class EndUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'firstName', 'lastName', 'accessID']
    ordering = ['firstName']
admin.site.register(end_user)

class AccessLvl(admin.ModelAdmin):
    list_display = ['accessID', 'accessName']
    ordering = ['accessID']
admin.site.register(access_lvl)

admin.site.register(activity_log)
admin.site.register(notification)
admin.site.register(notification_recipient)
admin.site.register(audit_log)
