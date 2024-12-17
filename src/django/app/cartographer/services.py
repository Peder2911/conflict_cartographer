import math
import calendar
import datetime
from typing import Tuple,Optional

def today():
    return datetime.date.today()

def getQuarter(date: datetime.date)->int:
    return math.ceil((date.month / 12) * 4)

def currentQuarter()->int:
    return getQuarter(today())

QR = Tuple[datetime.date,datetime.date]
def quarters(year:int)->Tuple[QR,QR,QR,QR]:
    def qbounds(i):
        lastday = calendar.monthrange(year=year,month=(i*3))[1]
        s = datetime.date(year=year,day=1,month=1+((i-1)*3))
        e = datetime.date(year=year,day=lastday,month=(i*3))
        return (s,e)
    return [qbounds(i+1) for i in range(4)]

def quarterRange(date:Optional[datetime.date]=None)->Tuple[datetime.date,datetime.date]:
    if date is None:
        date = today() 
    now = date 
    return quarters(now.year)[getQuarter(now)-1]

def currentYear()->int:
    return today().year
