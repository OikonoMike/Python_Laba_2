from _datetime import datetime

def date_time():
    """Функция записи времени (now)"""
    today = datetime.today().strftime('%Y-%m-%d')
    time_now = datetime.today().strftime('%H:%M:%S')
    return f'[{today} {time_now}]'