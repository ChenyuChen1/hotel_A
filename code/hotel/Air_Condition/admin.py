from django.contrib import admin
# from .models import Scheduler
from .models import ServingQueue, WaitingQueue, Server, Scheduler, Room
# Register your models here.

# class SchedulerAdmin(admin.ModelAdmin):

# 告诉管理页面，Scheduler对象需要被管理。
admin.site.register(Scheduler)
admin.site.register(ServingQueue)
admin.site.register(WaitingQueue)
admin.site.register(Server)
admin.site.register(Room)

