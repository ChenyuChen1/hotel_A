from django.contrib import admin
from .models import Scheduler
# Register your models here.

# class SchedulerAdmin(admin.ModelAdmin):

# 告诉管理页面，Scheduler对象需要被管理。
admin.site.register(Scheduler)
