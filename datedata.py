import os
import json
import requests
import datetime

TIME_DIFFERENCE = 9

# Timetree のスケジュールと 天気予報のデータを保持する class
class DatesData():
    def __init__(self):
        # weather forecast
        self.latitude: float = float(os.environ.get('latitude'))
        self.longitude: float = float(os.environ.get('longitude'))
        self.daily: str = 'temperature_2m_max,temperature_2m_min,weathercode'
        self.timezone: str = 'Asia%2FTokyo'
        self.url: str = f'https://api.open-meteo.com/v1/forecast?latitude={str(self.latitude)}&longitude={str(self.longitude)}&daily={self.daily}&timezone={self.timezone}'
        self.daily_forecast = json.loads(requests.get(self.url).text)['daily']
        self.dates_tuple: tuple[str] = tuple(self.daily_forecast['time'])
        
        # timetree schedule
        self.token: str = str(os.environ.get('timetree_token'))
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'accept':'application/vnd.timetree.v1+json'
        }
        self.calendar_id = str(os.environ.get('calendar_id'))
        print(json.loads(requests.get(f"https://timetreeapis.com/calendars/{self.calendar_id}/upcoming_events?days={len(self.dates_tuple)}",headers=self.headers).text))
        self.events_raw = json.loads(requests.get(f"https://timetreeapis.com/calendars/{self.calendar_id}/upcoming_events?days={len(self.dates_tuple)}",headers=self.headers).text)['data']
        
        self.events = [{
            'start_at' : datetime.datetime.strptime(event['attributes']['start_at'][:-5], '%Y-%m-%dT%H:%M:%S'),
            'end_at' : datetime.datetime.strptime(event['attributes']['end_at'][:-5], '%Y-%m-%dT%H:%M:%S'),
            'title' : event['attributes']['title']
        } for event in self.events_raw]
        
        self.__fix_time_difference__()
        
    def __fix_time_difference__(self):
        event_list = []
        for event in self.events:
            if event['start_at'] == event['end_at'] and event['start_at'].hour == 0 and event['start_at'].minute == 0:
                pass
            else:
               event['start_at'] = event['start_at'] + datetime.timedelta(hours=TIME_DIFFERENCE)
               event['end_at'] = event['end_at'] + datetime.timedelta(hours=TIME_DIFFERENCE)
            event_list.append(event)
        self.events = event_list


# 1 日のデータを管理する class
class DateData():
    def __init__(self, target_date: datetime.date, temp_max: float, temp_min: float, weather_code: str, events: dict):
        self.target_date: datetime.datetime = datetime.datetime.strptime(target_date,'%Y-%m-%d')
        self.temp_max: float = temp_max
        self.temp_min: float = temp_min
        self.weather_code: str = weather_code
        self.events = events
        self.extract_event()
    def extract_event(self):
        events = []
        for event in self.events:
            if self.target_date.date() == event['start_at'].date():
                events.append(event)
        self.events = events


def make_datedata_list():
    dsd = DatesData()
    ddl = []
    for ds in dsd.dates_tuple:
        idx = dsd.daily_forecast['time'].index(ds)
        temp_max = float(dsd.daily_forecast['temperature_2m_max'][idx])
        temp_min = float(dsd.daily_forecast['temperature_2m_min'][idx])
        weather_code = dsd.daily_forecast['weathercode'][idx]
        dd = DateData(ds, temp_max,temp_min, weather_code, dsd.events)
        ddl.append(dd)
    return ddl

if __name__ == '__main__':
    ddl = make_datedata_list()
    for dd in ddl:
        print(1)
        print(
            dd.target_date,
            dd.temp_max,
            dd.temp_min,
            dd.weather_code,
            dd.events
        )

