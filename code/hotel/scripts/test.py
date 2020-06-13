import os
import sys
import django
from datetime import datetime
# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel.settings")
    django.setup()

    from Air_Condition.models import Scheduler, Room, StatisticController
    report = StatisticController.create_report(0, 1, 2020, 6)
    report1 = StatisticController.draw_report(room_id=-1, type_report=1, year=2020, month=3)

    #rdr = StatisticController.print_rdr(0, datetime(2020,1,1), datetime.now())
    # isOK = StatisticController.print_rdr(1, datetime(2020, 1, 1), datetime.now())
    # rd1 = StatisticController.print_rdr(0, datetime(2020, 1, 1), datetime.now())
    # rd2 = StatisticController.print_rdr(0, datetime(2020, 1, 1), datetime.now())
    # rd3 = StatisticController.print_rdr(0, datetime(2020, 1, 1), datetime.now())

