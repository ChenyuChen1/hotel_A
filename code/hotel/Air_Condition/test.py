from datetime import datetime

from django.test import TestCase


from .models import Scheduler, Room, StatisticController


# class SchedulerModelTests(TestCase):
#     # def test_if_the_Scheduler_run(self):
#     #     """
#     #     was_published_recently() returns False for questions whose pub_date
#     #     is in the future.
#     #     """
#     #
#     #     scheduler = Scheduler()
#     #     self.assertIs(scheduler.state, 2)
#     #     scheduler.power_on()
#     #     scheduler.set_para(28, 18, 25, 1, 0.3, 0.5)
#     #     scheduler.set_init_temp(room_id=1, init_temp=32)
#     #     scheduler.start_up()
#     #     room = scheduler.update_room_state(room_id=1)
#     #
#     #     print("scheduler.state = %s" % scheduler.state)
#     #     # print("room_id = %d" % room.room_id)
#     #     print("current_temp = %d" % room.current_temp)
#     #     self.assertIs(scheduler.state, 3)

class RoomModel(TestCase):
    @staticmethod
    def test_create_rdr():
        begin_date = datetime(2020, 2, 11, 6, 0)
        end_date = datetime(2020, 6, 10, 10, 0)
        room_id = 1
        StatisticController.create_rdr(room_id, begin_date, end_date)

    @staticmethod
    def test_create_bill():
        begin_date = datetime(2020, 2, 11, 6, 0)
        end_date = datetime.now()
        room_id = 1
        StatisticController.create_bill(room_id, begin_date, end_date)

    @staticmethod
    def test_print_rdr():
        begin_date = datetime(2020, 2, 11, 6, 0)
        end_date = datetime.now()
        room_id = 1
        StatisticController.print_rdr(room_id, begin_date, end_date)

