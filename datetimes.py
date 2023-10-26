import datetime
# from dateutil import parser
import json

# subclass the regular encoder to convert datetime objects to iso string
# otherwise JSON parser may fail to convert datetime objects to JSON

class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

# tell json.dumps to use the custom encoder
def dumps(obj):
    return json.dumps(obj, cls=JSONDateTimeEncoder)

now_string = dumps({'time': datetime.datetime.now()})
print(now_string)

# look at datetime.strptime for converting date strings back to datetime objects