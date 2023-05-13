# 
# from datetime import datetime, time, date
# import pytz

# today = date.today()
# start_time = datetime.combine(today, time(hour=1))
# start_time_utc = pytz.utc.localize(start_time)
# start_time_vn = start_time_utc.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))

# print("Start time (UTC):", start_time_utc)
# print("Start time (VN):", start_time_vn)
import datetime
from datetime import date, time
# print(datetime.datetime.now())
today = date.today()
start_time = datetime.datetime.combine(today, time(hour=23)) 
print(start_time)