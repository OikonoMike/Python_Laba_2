from _datetime import datetime

def date_time():
    date_today = datetime.today().strftime('%Y-%m-%d')
    time_now = datetime.today().strftime('%H:%M:%S')
    return f'[{date_today} {time_now}]'