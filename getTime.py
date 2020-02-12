import datetime

def getTime():
    tdatetime = datetime.date.today()
    tstr = tdatetime.strftime('%Y%m%d')
    tstr = int(tstr)-1
    return tstr

getTime()
