from django.db import models

# 下面这个网站提供了详细的字段类型参考，请大家仔细比较，选择最优字段类型。
# note: https://docs.djangoproject.com/zh-hans/2.2/ref/models/fields/#field-types

# Create your models here.
class Scheduler(models.Model):
    """
    名称：调度器、调度对象、中控机
    作用：作为温控系统的中心，为到来的请求分配服务对象，提供计费功能
    """

    STATE_CHOICE = [
        (1, 'WORKING'),
        (2, 'SHUTDOWN'),
    ]

    # 正在对房间进行服务的服务对象数
    service_num = models.IntegerField(verbose_name='服务对象数', default=0)

    # 发出请求的房间数
    request_num = models.IntegerField(verbose_name='发出请求的房间数', default=0)

    # 中控机所处的状态
    state = models.IntegerField(verbose_name='中控机状态', choices=STATE_CHOICE)

    # 最高温度限制
    temp_high_limit = models.IntegerField(verbose_name='最高温度限制', default=0)

    # 最低温度限制
    temp_low_limit = models.IntegerField(verbose_name="最低温度限制", default=0)

    # 默认目标温度
    default_target_temp = models.IntegerField(verbose_name="默认目标温度", default=26)

    # 高风速时的费率
    fee_rate_h = models.FloatField(verbose_name="高风速费率", default=1.0)

    # 低风速时的费率
    fee_rate_l = models.FloatField(verbose_name="低风速费率", default=0.5)

    # 中风速时的费率
    fee_rate_m = models.FloatField(verbose_name="中风速费率", default=0.8)

    def power_on(self):
        """
        开启中控机，中控机状态修改为”WORKING“
        :return:
        """
        self.state = 1

    def request_on(self, room_id, current_room_temp):
        pass

    def set_service_num(self, service_num):
        """

        :param service_num:
        :return:
        """
        self.service_num = service_num

    def create_server(self):
        pass

    def change_target_temp(self, room_id, target_temp):
        pass

    def change_fan_speed(self, fan_speed):
        pass

    def check_room_state(self, list_room):
        pass

    def set_para(self, temp_high):
        pass