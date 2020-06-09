from django.db import models
from django.utils import timezone
import threading


# 下面这个网站提供了详细的字段类型参考，请大家仔细比较，选择最优字段类型。
# note: https://docs.djangoproject.com/zh-hans/2.2/ref/models/fields/#field-types


class ServingQueue(models.Model):
    """
    正在服务的队列，存放所有正在服务的房间对象
    """
    # 在调度队列中的房间对象
    # 注：不确定这么写好不好，我觉得serve_time应该和房间对象绑定在一起可能会好一点。
    # 如果有更好的类型，请替换。
    room_list = []

    serving_num = models.IntegerField(verbose_name='服务对象数', default=0)

    def __init__(self):
        super().__init__()
        self.serving_num = 0

    def insert(self, room):
        room.state = 1
        room.request_time = timezone.now()
        room.save(force_insert=True)
        self.room_list.append(room)
        self.room_list.sort(key=lambda x: (room.fan_speed, room.request_time))  # 按照风速排序,服务队列中风速优先
        self.serving_num += 1
        return True

    #  这里面也要加修改温度，风速，响应关机的函数
    def set_target_temp(self, room_id, target_temp):
        for room in self.room_list:
            if room.room_id == room_id:
                room.target_temp = target_temp
                room.request_time = timezone.now()
                room.save(force_insert=True)
                break
        return True

    #  修改风速
    def set_fan_speed(self, room_id, fan_speed, fee_rate):
        for room in self.room_list:
            if room.room_id == room_id:
                room.fan_speed = fan_speed
                room.fee_rate = fee_rate
                room.request_time = timezone.now()
                room.save(force_insert=True)
                self.room_list.sort(key=lambda x: (room.fan_speed, room.request_time))  # 按照风速排序,服务队列中风速优先
                break
        return True

    def delete_room(self, room):
        """
        从调度队列删除对应的房间
        :param room:
        :return:
        """
        #  将对应的房间信息写入数据库
        room.request_time = timezone.now()
        room.save(force_insert=True)
        self.room_list.remove(room)
        self.serving_num -= 1
        return True

    def auto_fee_temp(self, mode):
        """
        回温和计费函数，设定风速H:1元/min,即0.016元/s,回温2℃/min，即0.03℃/min
        M:0.5元/min,即0.008元/s,回温1.5℃/min，即0.025℃/min
        L:0.3元/min,即0.005元/s,回温1℃/min，即0.016℃/min
        mode=1,制热
        mode=2,制冷
        :return:
        """
        if mode == 1:
            for room in self.room_list:
                if room.fan_speed == 1:
                    room.fee += 0.016
                    room.current_temp += 0.03
                elif room.fan_speed == 2:
                    room.fee += 0.008
                    room.current_temp += 0.025
                else:
                    room.fee += 0.005
                    room.current_temp += 0.016
            timer = threading.Timer(1, self.auto_fee_temp, [1])  # 每1秒执行一次函数
            timer.start()
        else:
            for room in self.room_list:
                if room.fan_speed == 1:
                    room.fee += 0.016
                    room.current_temp -= 0.03
                elif room.fan_speed == 2:
                    room.fee += 0.0081
                    room.current_temp -= 0.025
                else:
                    room.fee += 0.005
                    room.current_temp -= 0.016
            timer = threading.Timer(1, self.auto_fee_temp, [2])  # 每1秒执行一次函数
            timer.start()


class WaitingQueue(models.Model):
    """
    等待队列，存放所有等待服务的房间对象
    """
    room_list = []

    waiting_num = models.IntegerField(verbose_name='等待对象数', default=0)

    def __init__(self):
        super().__init__()
        self.waiting_num = 0

    def set_target_temp(self, room_id, target_temp):
        for room in self.room_list:
            if room.room_id == room_id:
                room.target_temp = target_temp
                room.request_time = timezone.now()
                room.save(force_insert=True)
                break
        return True

    def set_fan_speed(self, room_id, fan_speed, fee_rate):
        for room in self.room_list:
            if room.room_id == room_id:
                room.fan_speed = fan_speed
                room.fee_rate = fee_rate
                room.request_time = timezone.now()
                room.save(force_insert=True)
                break
        return True

    def delete_room(self, room):
        """
        从等待队列删除对应的房间
        :param room:
        :return:
        """
        #  将room_id 对应的房间信息写入数据库
        room.request_time = timezone.now()
        room.save(force_insert=True)
        self.room_list.remove(room)
        self.waiting_num -= 1
        return True

    #   参数用room对象更好，
    def insert(self, room):
        room.state = 2
        room.save(force_insert=True)
        self.room_list.append(room)
        self.waiting_num += 1
        return True


# Create your models here.
class Scheduler(models.Model):
    """
    名称：调度器、调度对象、中控机
    作用：作为温控系统的中心，为到来的请求分配服务对象，提供计费功能
    """

    STATE_CHOICE = [
        (1, 'WORKING'),
        (2, 'SHUTDOWN'),
        (3, 'SETMODE'),
        (4, 'READY')
    ]

    # 第一次发出开机请求的房间数
    request_num = 0

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

    #  等待队列
    WQ = WaitingQueue()

    #  服务队列
    SQ = ServingQueue()

    #  存储5个房间,房间开始时的状态都是3--“SHUTDOWN”关机状态
    rooms = []

    def power_on(self):
        """
        开启中控机，中控机状态修改为”SETMODE“
        初始化房间队列
        :return:
        """
        self.state = 3
        for i in range(5):
            self.rooms.append(Room(0, 0, 0, 0))
        return self.state

    def set_init_temp(self, room_id, init_temp):
        """
        设置房间的初始温度
        :param room_id:
        :param init_temp:
        :return:
        """
        for room in self.rooms:
            if room.room_id == room_id:
                room.init_temp = init_temp

    def request_on(self, room_id, current_room_temp):
        """
        一个请求到来，第一次开机分配房间对象然后处理，否则直接处理
        调用调度算法
        问题：房间ID如何分配的
        开始计费和计温
        :param room_id:
        :param current_room_temp:
        :return:
        """
        return_list = []          # 存储返回数据的列表
        flag = 1
        for room in self.rooms:
            if room.room_id == room_id:    # 不是第一次开机，直接处理
                room.current_temp = current_room_temp
                flag = 0
                if self.SQ.serving_num < 3:    # 服务队列未满
                    self.SQ.insert(room)
                else:    # 服务队列已满
                    self.WQ.insert(room)
                    timer = threading.Timer(120, self.scheduling)  # 2min后执行调度函数
                    timer.start()
                return_list = [room.state, room.target_temp, room.fan_speed, room.fee_rate, room.fee]
                #  写入数据库
                room.request_time = timezone.now()
                room.save(force_insert=True)
        if flag == 1:  # 是第一次开机，先分配房间对象再处理
            self.request_num += 1  # 发出第一次开机请求的房间数加一
            if self.request_num > 5:  # 控制只能有五个房间开机
                return return_list  # 返回空列表
            for room in self.rooms:
                if room.room_id == 0:
                    room.room_id = room_id
                    room.current_temp = current_room_temp
                    if self.SQ.serving_num < 3:  # 服务队列未满
                        self.SQ.insert(room)
                    else:  # 服务队列已满
                        self.WQ.insert(room)
                        timer = threading.Timer(120, self.scheduling)  # 2min后执行调度函数
                        timer.start()
                    return_list = [room.state, room.target_temp, room.fan_speed, room.fee_rate, room.fee]
                    #  写入数据库
                    room.request_time = timezone.now()
                    room.save(force_insert=True)

        #  只要服务队列有房间就计费和计温,mode=1,制热mode=2,制冷
        if self.default_target_temp == 22:
            self.SQ.auto_fee_temp(1)
        else:
            self.SQ.auto_fee_temp(2)

        #  只要有服务就检查是否有房间达到目标温度
        self.check_target_arrive()
        return return_list      # 返回房间的状态，目标温度，风速，费率以及费用

    def set_service_num(self, service_num):
        """

        :param service_num:
        :return:
        """
        self.service_num = service_num


    def change_target_temp(self, room_id, target_temp):
        """
        修改目标温度
        :param room_id:
        :param target_temp:
        :return:
        """
        for room in self.rooms:
            if room.room_id == room_id:
                if room.state == 1:  # 在调度队列中
                    self.SQ.set_target_temp(room_id, target_temp)
                elif room.state == 2:  #  在等待队列中
                    self.WQ.set_target_temp(room_id, target_temp)
        return True

    def change_fan_speed(self, room_id, fan_speed):
        """
        处理调风请求
        :param room_id:
        :param fan_speed:
        :return:
        """
        if fan_speed == 1:
            fee_rate = self.fee_rate_h    #高风速时的费率
        elif fan_speed == 2:
            fee_rate = self.fee_rate_m    #中风速时的费率
        else:
            fee_rate = self.fee_rate_l    #低风速时的费率
        for room in self.rooms:
            if room.room_id == room_id:
                if room.state == 1:  # 在调度队列中
                    self.SQ.set_fan_speed(room_id, fan_speed, fee_rate)
                elif room.state == 2:  # 在等待队列中
                    self.WQ.set_fan_speed(room_id, fan_speed, fee_rate)
        return fee_rate

    def check_room_state(self):
        """
        每分钟查看一次房间状态
        :return:
        """
        timer = threading.Timer(5, self.check_room_state)  # 每五秒执行一次check函数,list_room为参数
        timer.start()
        #  return self.rooms

    def update_room_state(self, room_id):
        """
        每分钟查看一次房间状态
        :param room_id:
        :return:
        """
        return_list = []
        for room in self.rooms:
            if room.room_id == room_id:
                return_list = [room.current_temp, room.target_temp, room.fan_speed, room.sate, room.fee_rate, room.fee]
                break
        return return_list

    def set_para(self, temp_high_limit, temp_low_limit, default_target_temp, fee_rate_h, fee_rate_l, fee_rate_m):
        """
        设置中控机参数
        :param temp_high_limit:
        :param temp_low_limit:
        :param default_target_temp:
        :param fee_rate_h:
        :param fee_rate_l:
        :param fee_rate_m:
        :return:
        """
        self.temp_high_limit = temp_high_limit
        self.temp_low_limit = temp_low_limit
        self.default_target_temp = default_target_temp
        self.fee_rate_h = fee_rate_h
        self.fee_rate_l = fee_rate_l
        self.fee_rate_m = fee_rate_m
        return True

    def start_up(self):
        """
        参数设置完毕，进入READY状态
        :return:
        """
        self.state = 4
        return self.state

    def request_off(self, room_id):
        """
         # 处理房间的关机请求(未开机时，不能发出关机请求)
        :param room_id:
        :return:
        """
        fee = 0.0
        for room in self.rooms:
            if room.room_id == room_id:
                fee = room.fee
                room.current_temp = room.init_temp
                #  关机回到初始温度
                if room.state == 1:  # 在调度队列中
                    room.state = 3
                    self.SQ.delete_room(room)
                elif room.state == 2:  # 在等待队列中
                    room.state = 3
                    self.WQ.delete_room(room)
        return fee

    def check_target_arrive(self):
        """
        每分钟，遍历服务队列中的房间，将达到目标温度的房间放入等待
        :return:
        """
        for room in self.SQ.room_list:
            if room.current_temp == room.target_temp:
                self.SQ.delete_room(room)
                self.WQ.insert(room)
                if self.default_target_temp == 22:
                    room.back_temp(1)
                else:
                    room.back_temp(2)

        timer = threading.Timer(60, self.check_target_arrive)  # 每1min执行一次check函数
        timer.start()

    def scheduling(self):
        """
        调度算法
        把SQ的最后一个加入WQ，WQ的第一个放入SQ
        :return:
        """
        if self.WQ.waiting_num != 0:
            temp = self.SQ.room_list[2]
            self.SQ.delete_room(temp)
            self.WQ.insert(temp)
            temp = self.WQ.room_list[0]
            self.WQ.delete_room(temp)
            self.SQ.insert(temp)
            timer = threading.Timer(120, self.scheduling)  # 每2min执行一次调度函数
            timer.start()


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


class Room(models.Model):

    FAN_SPEED = [
        (1, "HIGH"),
        (2, "MIDDLE"),
        (3, "LOW"),
    ]

    ROOM_STATE = [
        (1, "SERVING"),
        (2, "WAITING"),
        (3, "SHUTDOWN"),
    ]

    # 请求发出时间
    request_time = models.DateTimeField(verbose_name='请求发出时间')

    # 房间号，唯一表示房间
    room_id = models.IntegerField(verbose_name="房间号")

    # 当前温度
    current_temp = models.IntegerField(verbose_name="当前温度")

    # 初始化温度
    init_temp = models.IntegerField(verbose_name="初始化温度")

    # 目标温度
    target_temp = models.IntegerField(verbose_name="目标温度", default=26)

    # 风速
    fan_speed = models.IntegerField(verbose_name='风速', choices=FAN_SPEED, default=2)

    # 房间状态
    state = models.IntegerField(verbose_name='服务状态', choices=ROOM_STATE, default=3)

    # 费率
    fee_rate = models.FloatField(verbose_name='费率', default=0.8)

    # 费用
    fee = models.FloatField(verbose_name='费用', default=0.0)

    # 当前服务时长
    serve_time = models.IntegerField(verbose_name='当前服务时长', default=0)

    # 当前等待时长
    wait_time = models.IntegerField(verbose_name='当前等待时长', default=0)

    # 初始化房间默认参数
    # def __init__(self, room_id=0, current_temp=26, target_temp=26, fan_speed=2):
    #     super().__init__()
    #     self.room_id = room_id
    #     self.current_temp = current_temp
    #     self.target_temp = target_temp
    #     self.fan_speed = fan_speed
    #     self.fee = 0
    #     if self.fan_speed == 1:
    #         self.fee_rate = Scheduler.fee_rate_h
    #     elif self.fan_speed == 2:
    #         self.fee_rate = Scheduler.fee_rate_m
    #     else:
    #         self.fee_rate = Scheduler.fee_rate_l

    def power_on(self):
        """
        房间空调开启
        :return:
        """
        Scheduler.request_on()

    def serve_time_plus(self):
        self.serve_time += 1
        self.save(update_fields=['serve_time'])

    def wait_time_plus(self):
        self.wait_time += 1
        self.save(update_fields=['wait_time'])

    def up_temp(self):
        """
        升高目标温度
        :return:
        """
        self.target_temp += 1
        self.save(update_fields=['target_temp'])
        op = Operation(
            room_id=self.room_id,
            current_temp=self.current_temp,
            target_temp=self.target_temp,
            fan_speed=self.fan_speed,
            fee=self.fee
        )
        op.save()

    def down_temp(self):
        """
        降低目标温度
        :return:
        """
        self.target_temp -= 1
        self.save(update_fields=['target_temp'])
        op = Operation(
            room_id=self.room_id,
            current_temp=self.current_temp,
            target_temp=self.target_temp,
            fan_speed=self.fan_speed,
            fee=self.fee
            )
        op.save()

    def change_speed2high(self):
        """
        设为高风速
        :return:
        """
        if self.fan_speed == 1:
            return
        self.fan_speed = 1
        self.save(update_fields=['fan_speed'])
        op = Operation(
            room_id=self.room_id,
            current_temp=self.current_temp,
            target_temp=self.target_temp,
            fan_speed=self.fan_speed,
            fee=self.fee
        )
        op.save()

    def change_speed2middle(self):
        """
        设为中风速
        :return:
        """
        if self.fan_speed == 2:
            return
        self.fan_speed = 2
        self.save(update_fields=['fan_speed'])
        op = Operation(
            room_id=self.room_id,
            current_temp=self.current_temp,
            target_temp=self.target_temp,
            fan_speed=self.fan_speed,
            fee=self.fee
        )
        op.save()

    def change_speed2low(self):
        """
        设为低风速
        :return:
        """
        if self.fan_speed == 3:
            return
        self.fan_speed = 3
        self.save(update_fields=['fan_speed'])
        op = Operation(
            room_id=self.room_id,
            current_temp=self.current_temp,
            target_temp=self.target_temp,
            fan_speed=self.fan_speed,
            fee=self.fee
        )
        op.save()

    #  达到目标温度后等待的房间启动回温算法
    def back_temp(self, mode):  # mode=1制热 mode=2制冷,回温算法0.5℃/min，即0.008℃/min
        if self.state == 2:
            if mode == 1:
                self.current_temp -= 0.008
                timer = threading.Timer(1, self.back_temp, [1])  # 每五秒执行一次函数
                timer.start()
            else:
                self.current_temp += 0.008
                timer = threading.Timer(1, self.back_temp, [2])  # 每五秒执行一次函数
                timer.start()


class Operation(models.Model):
    """
    该类用于存放每次空调状态变更的操作
    """
    FAN_SPEED = [
        (1, "HIGH"),
        (2, "MIDDLE"),
        (3, "LOW"),
    ]

    # 请求发出时间
    request_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)

    # 发出请求的房间
    room_id = models.IntegerField(verbose_name='发出请求的房间号')

    # 房间当前温度、房间目标温度、房间风速、房间当前费用
    current_temp = models.IntegerField(verbose_name="目标温度")

    # 目标温度
    target_temp = models.IntegerField(verbose_name="目标温度")

    # 风速
    fan_speed = models.IntegerField(verbose_name='风速', choices=FAN_SPEED)

    # 费用
    fee = models.FloatField(verbose_name='费用')

    class Meta:
        ordering = ('-request_time',)

        # 这里通过 verbose_name 来指定对应的 model 在 admin 后台的显示名称
        verbose_name = '操作列表'


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
