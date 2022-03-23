import datetime
import pytz


tz = pytz.timezone('Asia/Almaty')
print(datetime.datetime.now(tz))