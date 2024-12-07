from _datetime import datetime
from datetime import datetime

from dateutil.utils import today

now = datetime.now()
date = '2024-12-03'
date_string2 = datetime.strptime(date,'%Y-%m-%d')
date_string = date_string2.strftime("%A")
print(date_string)
