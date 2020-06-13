from datetime import datetime

from django.test import TestCase
from faker import Faker

from .models import Scheduler, Room, StatisticController


# class SchedulerModelTests(TestCase):
#     def test_if_the_Scheduler_run(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#
#         scheduler = Scheduler()
#         self.assertIs(scheduler.state, 2)
#         scheduler.power_on()
#         scheduler.set_para(28, 18, 25, 1, 0.3, 0.5)
#
#         scheduler.start_up()
#         room_0 = scheduler.request_on(0, 29)
#         room_1 = scheduler.request_on(1, 28)
#         room_2 = scheduler.request_on(2, 30)
#         room_3 = scheduler.request_on(3, 29)
#         room_4 = scheduler.request_on(4, 35)
#         scheduler.set_init_temp(0, 32)
#         scheduler.change_target_temp(0, 25)
#
#         for i in range(5):
#             room = scheduler.update_room_state(i)
#             print("room %d " % room.room_id)
#             print("target_temp = %d" % room.target_temp)
#             print("current_temp = %d " % room.current_temp)
#             print("fan_speed = %s" % room.get_fan_speed_display())
#             print("state = %s " % room.get_state_display())
#             print("fee = %f " % room.fee)
#
#
#         #self.assertIs(scheduler.state, 3)

# class RoomModel(TestCase):
#     @staticmethod
#     def test_create_rdr():
#         begin_date = datetime(2020, 2, 11, 6, 0)
#         end_date = datetime(2020, 6, 10, 10, 0)
#         room_id = 1
#         StatisticController.create_rdr(room_id, begin_date, end_date)
#
#     @staticmethod
#     def test_create_bill():
#         begin_date = datetime(2020, 2, 11, 6, 0)
#         end_date = datetime.now()
#         room_id = 1
#         StatisticController.create_bill(room_id, begin_date, end_date)
#
#     @staticmethod
#     def test_print_rdr():
#         begin_date = datetime(2020, 2, 11, 6, 0)
#         end_date = datetime.now()
#         room_id = 1
#         StatisticController.print_rdr(room_id, begin_date, end_date)


class StatisticControllerTest(TestCase):
    @staticmethod
    def test_print_report():
        faker = Faker()
        for i in range(100):
            """产生10000条数据"""
            request_id = i
            request_time = faker.date_time_between_dates(datetime(2017, 1, 1, 1, 1, 1), datetime.now())
            room_id = faker.random_int(min=0, max=4)
            current_temp = faker.random_int(min=20, max=30)
            init_temp = faker.random_int(min=20, max=30)
            target_temp = faker.random_int(min=20, max=30)
            fan_speed = faker.random_int(min=1, max=3)
            state = faker.random_int(min=1, max=4)
            fee_rate = 0.5
            fee = faker.random_int(min=0, max=999)
            serve_time = faker.random_int(min=1, max=99)
            wait_time = faker.random_int(min=0, max=30)
            operation = faker.random_int(min=1, max=4)
            scheduling_num = faker.random_int(min=1, max=30)
            detail = Room.objects.create(request_id, request_time, room_id, current_temp, init_temp,
                          target_temp, fan_speed, state, fee_rate, fee, serve_time, wait_time, operation, scheduling_num)
            # print(detail.request_id)
            detail.save()
