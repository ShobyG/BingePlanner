from datetime import datetime
from datetime import timedelta

class CalenderEvent:
# """ Class has methods to creates events list, adds new events, create events jason, upload and retrieve from db """

    def __init__(self, events, title, start_date, start_time, length):
        self.events = events
        self.__create_event(title, start_date, start_time, length)

    def __create_event(self, title, start_date, start_time, length):
        start_end = self.__start_end_time_calculator(start_date, start_time, length)
        new_event = {
            'title': title,
            'start': start_end[0],
            'end': start_end[1],
            }
        self.events.append(new_event)

    @staticmethod
    def __start_end_time_calculator(start_date, start_time, length):
        start_time = f"{start_time}:00"
        time_str = f"{start_date} {start_time}"
        date_format_str = '%Y-%m-%d %H:%M:%S'
        given_time = datetime.strptime(time_str, date_format_str)
        n = int(length)
        final_time = given_time + timedelta(minutes=n)
        final_time_str = final_time.strftime('%Y-%m-%d %H:%M:%S')
        date_time = final_time_str.split(" ")
        start = f"{start_date}T{start_time}"
        end = f"{date_time[0]}T{date_time[1]}"
        return start, end
