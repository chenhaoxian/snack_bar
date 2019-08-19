import time

class date_util:

    def __init__(self) -> None:
        super().__init__()


    def get_day_interval(self,time1,time2):
        return abs(time1.tm_yday-time2.tm_yday)

    def get_day_interval_with_sysdate_by_time_str(self, input_time_str):
        if input_time_str is None :
            return None

        input_time = time.strptime(input_time_str, "%Y-%m-%d %H:%M:%S")
        return self.get_day_interval(input_time, time.localtime())
