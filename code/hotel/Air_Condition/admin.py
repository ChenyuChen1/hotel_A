from django.contrib import admin
# from .models import Scheduler
from .models import ServingQueue, WaitingQueue, Server, Scheduler, Room
# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ['request_time', 'room_id', 'current_temp', 'target_temp', 'fan_speed', 'fee']


# 告诉管理页面，Scheduler对象需要被管理。
admin.site.register(Scheduler)
admin.site.register(ServingQueue)
admin.site.register(WaitingQueue)
admin.site.register(Server)
admin.site.register(Room, RoomAdmin)

