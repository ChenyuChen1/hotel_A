from django.db import models
from django.utils import timezone

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

    def set_para(self, temp_high_limit, temp_low_limit, default_target_temp, fee_rate_h, fee_rate_l, fee_rate_m):
        pass


class Server(models.Model):
    """
    名称：服务对象
    作用：服务对象最多仅存在3个，每个服务对象对应一个房间，供调度算法以及温控使用。
    """
    STATE_CHOICE = [
        (1, 'WORKING'),
        (2, 'SHUTDOWN'),
    ]

    # 服务对象的服务状态
    state = models.IntegerField(verbose_name='服务状态', choices=STATE_CHOICE)

    # 服务开始时间
    start_time = models.DateField(verbose_name="创建时间", default=timezone.now)

    # 服务对象的服务时长
    serve_time = models.FloatField(verbose_name='服务时长')

    # 服务对象所服务的房间号
    room_id = models.IntegerField(verbose_name='服务房间号')

    # 服务对象所服务房间的目标温度
    target_temp = models.IntegerField(verbose_name='目标温度')

    # 服务对象所服务房间的费用
    fee = models.FloatField(verbose_name='费用')

    # 服务对象所服务房间的费率
    fee_rate = models.FloatField(verbose_name='费率')

    # 服务对象所服务的房间的风速
    fan_speed = models.IntegerField(verbose_name='风速')

    # 问题：为什么要有room_id？一个服务对象的不是只对应一个room吗，它的属性也有room_id了呀?
    def set_attribute(self, room_id, start_time, current_room_temp):
        """
        服务对象的服务状态，服务开始时间，目标温度，费率及费用值被赋值；
        :param room_id:
        :param start_time:
        :param current_room_temp:
        :return:
        """
        # self.room_id = room_id
        # self.start_time = timezone.now()
        pass

    def change_target_temp(self,target_temp):
        """
        修改正在服务房间的目标温度
        :param target_temp:
        :return:
        """
        pass

    def change_fan_speed(self, fan_speed):
        """
        修改正在服务房间的风速
        :param fan_speed:
        :return:
        """
        pass

    def delete_server(self, room_id):
        """
        删除服务对象与被服务房间的关联
        :param room_id:
        :return:
        """
        pass

    def set_serve_time(self):
        """
        修改服务时长
        :return:
        """
        pass

    def set_fee(self):
        """
        修改被服务房间的费用
        :return:
        """
        pass


class ServingQueue(models.Model):
    """
    正在服务的队列，存放所有正在服务的房间对象
    """
    # 在调度队列中的房间对象
    # 注：不确定这么写好不好，我觉得serve_time应该和房间对象绑定在一起可能会好一点。
    # 如果有更好的类型，请替换。
    room_list = []

    # 服务队列中该房间对象的服务时长
    serve_time = []


class Room(models.Model):

    FAN_SPEED = [
        (1, "HIGH"),
        (2, "MIDDLE"),
        (3, "LOW"),
    ]

    ROOM_STATE = [
        (1, "SERVING"),
        (2, "WAITING"),
    ]

    # 房间号，唯一表示房间，是房间的主键。
    room_id = models.IntegerField(verbose_name="房间号", primary_key=True)

    # 当前温度
    current_temp = models.IntegerField(verbose_name="当前温度")

    # 目标温度
    target_temp = models.IntegerField(verbose_name="目标温度")

    # 风速
    fan_speed = models.IntegerField(verbose_name='风速', choices=FAN_SPEED)

    # 服务时长
    duration = models.IntegerField(verbose_name='服务时长')

    # 服务状态
    state = models.IntegerField(verbose_name='服务状态', choices=ROOM_STATE)


class StatisticController(models.Model):
    """
    - 名称：统计控制器
    - 作用：负责读数据库的控制器，为前台生成详单、账单
    """

    def reception_login(self, id, password):
        """
        感觉放在这里不是特别好，应该放在view层
        如何登录请看:https://docs.djangoproject.com/zh-hans/2.2/topics/auth/default/#how-to-log-a-user-in
        :param id:
        :param password:
        :return:
        """

    def create_rdr(self, room_id, begin_date, end_date):
        """
        创建详单
        :param room_id: 房间号
        :param begin_date: 起始日期
        :param end_date: endDay
        :return:
        """

    def create_bill(self, room_id, begin_date, end_date):
        """
        创建账单
        :param room_id: 房间号
        :param begin_date: 起始日期
        :param end_date: endDay
        :return:
        """

    def print_bill(self, room_id, begin_date, end_date):
        """
        打印账单
        :param room_id: 房间号
        :param begin_date: 起始日期
        :param end_date: endDay
        :return:
        """

    def print_rdr(self, room_id, begin_date, end_date):
        """
        打印详单
        :param room_id: 房间号
        :param begin_date: 起始日期
        :param end_date: endDay
        :return:
        """

    def create_report(self,list_room_id, type_report, date):
        """
        创建报告
        :param list_room_id:房间列表
        :param type_report:报告类型
        :param date:日期
        :return:
        """

    def print_report(self,list_room_id, type_report, date):
        """
        打印报告
        :param list_room_id:房间列表
        :param type_report:报告类型
        :param date:日期
        :return:
        """
