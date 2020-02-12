import urllib.request
from urllib.parse import urlparse
import json
import pprint
import getTime


def getSlump(id):
    time = int(getTime.getTime())
    #print(time)
    url='https://nifmbapi.maruhan.co.jp/api/v1.4/machine/slump'
    query={
        'hall_code' : 1061,
        'machine_id' : id,
        'date' : time
    }
    #1クエリストリングの作成
    url_with_query = "{}?{}".format(url, urllib.parse.urlencode(query))
    #print(url_with_query)
    response = urllib.request.urlopen(url_with_query)
    content = json.loads(response.read().decode('utf_8_sig'))
    #pprint.pprint(content)
    if (content["datas"]):
        for item in content["datas"][0]["items"]:
            result=item["value"]
        #print(result)
        return result
    else:
        return 0
