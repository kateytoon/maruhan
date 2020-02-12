
import urllib.request
from urllib.parse import urlparse
import json
import pprint
import pandas as pd
import datetime
import codecs
import os
import concurrent
import numpy as np
import getTime
from concurrent.futures.thread import ThreadPoolExecutor
import getInfo
import getSlump


p_cols = ['number', 'model_name', 'slump','allStarts','bb','rb','judge']

# 空のデータフレームを作成
p_df = pd.DataFrame(index = [], columns = p_cols)
executor = ThreadPoolExecutor(max_workers=8)
futures = []
def searchMachine(keyword):
    print(keyword)
    url='https://nifmbapi.maruhan.co.jp/api/v1.4/hall/machine/search'
    query={
        'hall_code' : 1061,
        'key_word' : keyword,
        'ps_type' : 'S'
    }
    #1クエリストリングの作成
    url_with_query = "{}?{}".format(url, urllib.parse.urlencode(query))
    #print(url_with_query)
    response = urllib.request.urlopen(url_with_query)
    content = json.loads(response.read().decode('utf8'))
    #pprint.pprint(content)
    
    if not (content["child_halls"]):
        #print("要素なし")
        return 
    else:
        model_name = content["child_halls"][0]["models"][0]["model_name"]
        machine_number = content["child_halls"][0]["models"][0]["groups"][0]["machines"][0]["machine_number"]
        slump = getSlump.getSlump(content["child_halls"][0]["models"][0]["groups"][0]["machines"][0]["machine_id"])
        allStarts , bb , rb = getInfo.getInfo(content["child_halls"][0]["models"][0]["groups"][0]["machines"][0]["machine_id"])
        
        '''
        print("機種名："+ model_name)
        print("台番号："+ machine_number)
        print("差枚："+ str(slump))
        print("総回転数："+ str(allStarts))
        '''
        return createDF(model_name,machine_number,slump,allStarts,bb,rb)
        
def createDF(model_name,machine_number,slump,allStarts,bb,rb):
    if slump > 0:
        #勝ちカウントするための値設定
        judge = "win"
    else:
        judge = "lose"
    p_df_tmp = pd.DataFrame(
            data = [[machine_number, model_name, slump,allStarts,bb,rb,judge]],
             columns=p_cols)
    # データフレームに追加
    return p_df_tmp

        
    
    

def writeCsv():
    time = int(getTime.getTime())
    #print(time)
    p_outputFilePath = "results/"+ str(time)+".csv"
    global p_df
    if not os.path.exists('results/'):
        os.makedirs('results/')
    
    if not(os.path.exists(p_outputFilePath)) :
        p_df.to_csv('maruhan/results/'+str(time)+'.csv', encoding='utf_8_sig')
        #print("書き込んだ"+p_outputFilePath)



#p = Pool(8)
#p.map( searchMachine, range(2001,2011) )
#searchMachine(2560)
def main():
    global p_df
    for i in range(2001,2561):
        future = executor.submit(searchMachine, i)
        futures.append(future)
    for future in futures: 
        p_df = p_df.append(future.result(), ignore_index = True)
    writeCsv()
    pd.options.display.max_columns = None
    #print(p_df)
    
    #print(p_df.set_index('number'))
    #print(p_df.astype({'number':int, 'model_name':str, 'slump':int,'allStarts':int,'bb':int,'rb':int}).dtypes)
    
    return p_df
    
'''
    
    
    print(p_df)
'''
