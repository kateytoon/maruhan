#https://nifmbapi.maruhan.co.jp/api/v1.4/machine/info?hall_code=1061&machine_id=1E-6-051/070810&date=[%2220191217%22,%2220191216%22,%2220191215%22,%2220191214%22,%2220191213%22,%2220191212%22,%2220191211%22]

import urllib
import json
import pprint
import getTime

def getInfo(cstr):
    #print(cstr)
    time = int(getTime.getTime())
    #print(time)
    url='https://nifmbapi.maruhan.co.jp/api/v1.4/machine/info'
    query={
        'hall_code' : 1061,
        'machine_id' : cstr,
        'date' : '[\"'+str(time)+'\"]'
    }
    #1クエリストリングの作成
    url_with_query = "{}?{}".format(url, urllib.parse.urlencode(query))
    #print(url_with_query)
    response = urllib.request.urlopen(url_with_query)
    content = json.loads(response.read().decode('utf8'))
    #pprint.pprint(content)
    if (content["datas"]):
        #print(content['datas'][0]['number_of_all_starts'])
        return content['datas'][0]['number_of_all_starts'] , content['datas'][0]['number_of_bbs'] , content['datas'][0]['number_of_rbs']
    else:
        return 0,0,0