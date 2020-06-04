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

    # 服务对象数
    service_num = models.IntegerField(verbose_name='服务对象数', default=0)

    # 发出开机请求的房间数
    request_num = models.IntegerField(verbose_name='发出开机请求的房间数', default=0)

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

    # 创建的服务对象
    servers = []

    def power_on(self):
        """
        开启中控机，中控机状态修改为”WORKING“
        :return:
        """
        self.state = 1

    def request_on(self, room_id, current_room_temp):
        self.request_num += 1
        return_list = []          # 返回列表
        if self.service_num < 3:       #  服务对象数小于3，则创建一个服务对象
            server = Server()
            self.servers.append(server)
            return_list = server.set_attribute(room_id, timezone.now(), current_room_temp)  # 初始化服务对象
            self.service_num += 1  # 服务对象数增加
            self.request_num -= 1
        elif self.service_num >= 3:    # 服务对象数达到上限
            flag = True  #  判断服务对象是否都在工作状态
            for server in self.servers:
                if server.state == 2:        # 此服务对象是空闲状态
                    flag = False
                    return_list = server.set_attribute(room_id, timezone.now(), current_room_temp)  # 将房间交给这个空闲的服务对象
                    self.request_num -= 1
                    break
            if flag:           #  正在被服务的房间数等于3，即没有空闲的服务对象
              # return_list = waiting_queue.requestOn(room_id, current_room_temp)  # 房间的开机请求进入等待队列,必须立即处理此请求
               pass
        return return_list      #返回房间的状态，目标温度，费率以及费用

    def set_service_num(self, service_num):
        """

        :param service_num:
        :return:
        """
        self.service_num = service_num

    def create_server(self):
        pass

    def change_target_temp(self, room_id, target_temp):   #处理调温请求
        flag = 0     # 判断请求的房间是否在被服务
        for server in self.servers:       # 查看请求的房间是否正在被服务
            if server.room_id == room_id:
                flag = 1
                if server.change_target_temp(target_temp):    # 服务对象成功修改目标温度
                    return True
        if flag == 0:   # 发出请求的房间在等待队列中
            #if waiting_queue.set_target_temp(room_id,target_temp)：   # 将请求交给等待队列
            #     return True
            pass

    def change_fan_speed(self, room_id, fan_speed):    # 处理调风请求
        flag = 0  # 判断请求的房间是否在被服务
        for server in self.servers:  # 查看请求的房间是否正在被服务
            if server.room_id == room_id:
                flag = 1
                if server.change_fan_speed(fan_speed):    # 服务对象成功修改目标风速
                    return True

        if flag == 0:  # 发出请求的房间在等待队列中
            # if waiting_queue.set_fan_speed(room_id,fan_speed):   # 将请求交给等待队列
            #     return True
            pass

    def check_room_state(self, list_room):
        pass

    def set_para(self, temp_high_limit, temp_low_limit, default_target_temp, fee_rate_h, fee_rate_l, fee_rate_m):
        pass

    def request_off(self, room_id):   # 处理房间的关机请求(未开机时，不能发出关机请求)
        flag = 0   # 判断请求的房间是否在被服务
        fee = 0.0
        for server in self.servers:          # 房间正在被服务
            if server.room_id == room_id:
                flag = 1
                fee = server.delete_server()   # 删除房间与服务对象的关联
                break

        #  删除等待队列中的房间
        if flag == 0:    # 发出请求的房间在等待队列中
           # fee = waiting_queue.delete(room_id)
           pass
        return fee


class Server(models.Model):
    """
    名称：服务对象
    作用：服务对象最多仅存在3个，每个服务对象对应一个房间，供调度算法以及温控使用。
    """
    STATE_CHOICE = [
        (1, 'WORKING'),
        (2, 'FREE'),
    ]

    # 服务对象的服务状态
    state = models.IntegerField(verbose_name='服务状态', choices=STATE_CHOICE, default=2)

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

    # 服务对象所服务的房间的风速,默认值为2--middle
    fan_speed = models.IntegerField(verbose_name='风速', default=2)

    def set_attribute(self, room_id, start_time, current_room_temp):
        """
        服务对象的初始化，与某一个房间关联起来；
        :param room_id:
        :param start_time:
        :param current_room_temp:
        :return:
        """
        self.room_id = room_id
        self.start_time = start_time
        self.serve_time = 0.0
        self.state = 1    # 状态为working
        self.target_temp = 26
        self.fan_speed = 2  # 默认为中速风2--middle
        self.fee = 0.0
        self.fee_rate = 0.8
        return_list = [self.state, self.target_temp, self.fee_rate, self.fee]
        return return_list

    def change_target_temp(self, target_temp):
        """
        修改正在服务房间的目标温度
        :param target_temp:
        :return:
        """
        self.target_temp = target_temp
        return True

    def change_fan_speed(self, fan_speed):
        """
        修改正在服务房间的风速
        :param fan_speed:
        :return:
        """
        self.fan_speed = fan_speed
        return True

    def delete_server(self):
        """
        删除服务对象与被服务房间的关联
        :return:
        """
        #  将信息写入数据库
        # 。。。
        self.room_id = 0  # 将服务对象设置为空闲
        self.state = 2   #  状态为FREE
        return self.fee

    def set_serve_time(self):
        """
        修改服务时长
        :return:
        """
        self.serve_time = timezone.now() - self.start_time

    def set_fee(self, fee):
        """
        修改被服务房间的费用
        :return:
        """
        self.fee = fee


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


class WaitingQueue(models.Model):
    """
    等待队列，存放所有等待服务的房间对象
    """
    room_list = []

    def __init__(self):
        super().__init__()
        pass

    def request_on(self, room_id, current_room_temp):   #处理开机请求，尽快处理，直接加入调度队列
        pass

    def set_target_temp(self, room_id, target_temp):
        for room in self.room_list:
            if room.room_id == room_id:
                room.target_temp = target_temp
                break
        return True

    def set_fan_speed(self, room_id, fan_speed):
        for room in self.room_list:
            if room.room_id == room_id:
                room.fan_speed= fan_speed
                break
        return True

    def delete(self, room_id):
        #  将room_id 对应的房间信息写入数据库
        for room in self.room_list:
            if room.room_id == room_id:
                fee = room.fee
                self.room_list.remove(room)
                break
        return fee

    def insert(self, room):
        self.room_list.append(room)


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
    duration = models.FloatField(verbose_name='服务时长')

    # 服务状态
    state = models.IntegerField(verbose_name='服务状态', choices=ROOM_STATE)

    # 费率
    fee_rate = models.FloatField(verbose_name='费率')

    # 费用
    fee = models.FloatField(verbose_name='费用')

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
