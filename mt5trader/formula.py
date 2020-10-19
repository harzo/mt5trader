import pymt5adapter as mt5
import pytz
import logging
import threading

from datetime import datetime, timedelta

window_open_event = threading.Event()
window_closed_event = threading.Event()


class DaxM5Formula:
    MARKET = 'GERMAN30_Pro'
    TIMEFRAME = mt5.TIMEFRAME_M5
    ACTIVITY_TIMES = [(7, 0, 0), (13, 30, 0)]  # UTC time
    ACTIVE_ON_WEEKENDS = False

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        self.logger.addHandler(handler)

        self.exit_thread = False

    def run(self):
        thread = threading.Thread(target=self.wait_for_next_activity)
        thread.start()

    def calculate_next_activity_time(self):
        start_time = datetime.now()
        weekday = start_time.weekday()
        next_activity_time = None
        adjust_day = 0 if weekday < 5 or self.ACTIVE_ON_WEEKENDS else 7 - weekday
        while next_activity_time is None:
            for hour, minutes, seconds in self.ACTIVITY_TIMES:
                activity_start = start_time.replace(hour=hour, minute=minutes, second=seconds, microsecond=0)
                activity_start += timedelta(days=adjust_day)
                if start_time < activity_start:
                    next_activity_time = activity_start
            adjust_day += 1 if weekday < 4 or self.ACTIVE_ON_WEEKENDS else 7 - weekday

    def wait_for_next_activity(self):
        pass

        # today = datetime.today()
        # next_window = datetime(today.year, today.month, today.day, 2, 0)
        # if t.hour >= 2:
        #     future += datetime.timedelta(days=1)
        # time.sleep((future - t).total_seconds())
        #
        # while not self.exit_thread and

    def poll_rates(self):
        select_dax = mt5.symbol_select(self.MARKET, True)
        dax = mt5.symbol_info(self.MARKET)

        timezone = pytz.timezone("Etc/UTC")
        utc_from = datetime(2020, 10, 16, tzinfo=timezone)
        utc_to = datetime(2020, 10, 16, hour=10, tzinfo=timezone)
        # rates = mt5.copy_rates_range(self.MARKET,  self.TIMEFRAME, utc_from,
        #                              utc_to)
        #
        # self.logger.info(rates)
