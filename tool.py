
from datetime import datetime

# текущая дата время по формату
def getDateTimeNow(format = None):
    if format is None:
        format = "%Y-%m-%d %H:%M:%S"
    #NOW strftime(format, gmtime())
    NOW = datetime.now().strftime(format)
    return NOW

