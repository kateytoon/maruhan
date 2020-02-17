# coding=utf-8
import requests
from datetime import datetime
import hashlib
import base64
from xml.sax.saxutils import escape
from chardet.universaldetector import UniversalDetector
import random
import SystemMain
import pandas as pd
import getTime
import numpy as np

USER_NAME = 'katey_que'
BLOG_NAME = 'katey-que.hatenablog.com'
PASSWORD = 'fgpzvow4py'
TITLE = ' {0} 今日の苗穂マルハン'.format(getTime.getTime())
FILE_NAME = 'maruhan/templeates/test_article.txt'


def create_hatena_text(title, name, body, updated, categories, is_draft):
    is_draft = 'yes' if is_draft else 'no'
    categories_text = ''
    for category in categories:
        categories_text = categories_text + '<category term="{}" />\n'.format(category)
    template = """<?xml version="1.0" encoding="utf-8"?>
    <entry xmlns="http://www.w3.org/2005/Atom"
           xmlns:app="http://www.w3.org/2007/app">
      <title>{0}</title>
      <author><name>{1}</name></author>
      <content type="text/html">{2}</content>
      <updated>{3}</updated>
      {4}
      <app:control>
        <app:draft>{5}</app:draft>
      </app:control>
    </entry>"""
    text = template.format(title, name, body, updated, categories_text, is_draft).encode()
    return text


def post_hatena_blog(user_name, password, entry_id, blog_name, data):
    headers = {'X-WSSE': create_wsse_auth_text(user_name, password), 'content-type': 'application/xml'}
    if entry_id is None:
        url = 'http://blog.hatena.ne.jp/{0}/{1}/atom/entry'.format(user_name, blog_name)
    else:
        url = 'http://blog.hatena.ne.jp/{0}/{1}/atom/entry/{2}'.format(user_name, blog_name, entry_id)
    request = requests.post(url, data=data, headers=headers)
    if request.status_code == 201:
        print('POST SUCCESS!!\n')
    else:
        print('Error!\n' + 'status_code: ' + str(request.status_code) + '\n' + 'message: ' + request.text)


def create_wsse_auth_text(user_name, password):
    created = datetime.now().isoformat() + "Z"
    b_nonce = hashlib.sha1(str(random.random()).encode()).digest()
    b_digest = hashlib.sha1(b_nonce + created.encode() + password.encode()).digest()
    c = 'UsernameToken Username="{0}", PasswordDigest="{1}", Nonce="{2}", Created="{3}"'
    return c.format(user_name, base64.b64encode(b_digest).decode(), base64.b64encode(b_nonce).decode(), created)

def text_format_table_number():
    global df
    df_s = df.loc[:, ['number', 'model_name', 'slump','allStarts','bb','rb']]
    stra = ""
    for index, row in df_s.iterrows():
        if row[2] > 5000:
            stra += '<tr bgcolor="#7cfc00">'
        elif row[2] < -3000:
            stra += '<tr bgcolor="#ff0000">'
        else:
            stra += '<tr>'

        stra += "<td align='center'>"+str(row[0])+"</td><td align='center'>"+str(row[1])+"</td><td align='center'>"+ str('{:+d}'.format(row[2]))+"</td><td align='center'>"+str(row[3])+"</td><td align='center'>"+str(row[4])+"</td><td align='center'>"+str(row[5])+"</td>"
        stra += "</tr> \n"
    #print(stra)
    
    return stra

def text_format_table_slump():
    global df
    df_s = df.loc[:, ['number', 'model_name', 'slump','allStarts','bb','rb']].sort_values('slump',ascending=False)
    stra = ""
    for index, row in df_s.iterrows():
        if row[2] > 5000:
            stra += '<tr bgcolor="#7cfc00">'
        elif row[2] < -3000:
            stra += '<tr bgcolor="#ff0000">'
        else:
            stra += '<tr>'

        stra += "<td align='center'>"+str(row[0])+"</td><td align='center'>"+str(row[1])+"</td><td align='center'>"+str('{:+d}'.format(row[2]))+"</td><td align='center'>"+str(row[3])+"</td><td align='center'>"+str(row[4])+"</td><td align='center'>"+str(row[5])+"</td>"
        stra += "</tr> \n"
    #print(stra)
    
    return stra

def text_format_table_groupby():
    global df
    df = df.replace(0, np.nan)
    sum_df = df.loc[:, ['model_name', 'slump','judge']]
    cnt_df = df.loc[:, ['model_name', 'judge']]
    
    sum_df = sum_df.replace({'lose': 0, 'win': 1})
    sum_df = sum_df.groupby('model_name')['slump','judge'].sum()
    cnt_df = cnt_df.groupby('model_name')['judge'].count()
    df_s = pd.merge(sum_df, cnt_df, on="model_name", how="outer")
    stra = ""
    for index, row in df_s.iterrows():
        winRate = int(int(row[1])/int(row[2])*100)
        if row[2] > 3:
            if winRate >= 50:
                stra += '<tr bgcolor="#7cfc00">'
            else:
                stra += '<tr>'
        else:
            stra +='<tr>'
        stra += "<td align='center'>"+str(index)+"</td>"
        for data in row:
            stra += "<td align='center'>"+str(int(data))+"</td>"
        #stra += "<td>"+str(row[0])+"</td><td>"+str(row[1])+"</td><td>"+str(row[2])+"</td><td>"+str(row[3])+"</td><td>"+str(row[4])+"</td><td>"+str(row[5])+"</td>"
        stra += "<td align='center'>"+str(winRate)+"%</td>"
        stra += "</tr> \n"
    #print(stra)
    
    return stra

def text_format_table_lastnumber():
    
    global df
    tmp_df = df.replace(0, np.nan)
    tmp_df = tmp_df.astype({'number':int})
    tmp_df["lastNum"] = tmp_df["number"]%10 
    sum_df = tmp_df.loc[:, ['lastNum', 'slump','allStarts','judge']]
    cnt_df = tmp_df.loc[:, ['lastNum', 'judge']]
    sum_df = sum_df.replace({'lose': 0, 'win': 1})
    sum_df = sum_df.groupby('lastNum')['slump','allStarts','judge'].sum()
    cnt_df = cnt_df.groupby('lastNum')['judge'].count()
    df_s = pd.merge(sum_df, cnt_df, on="lastNum", how="outer")
    
    
    #print(df_s.dtypes)
    #print(df_s)
    
    stra = ""
    for index, row in df_s.iterrows():
        winRate = int(int(row[2])/int(row[3])*100)
        if row[3] > 3:
            if winRate >= 50:
                stra += '<tr bgcolor="#7cfc00">'
            else:
                stra += '<tr>'
        else:
            stra +='<tr>'
        stra += '<td align="" valign="">'+str(index)+"</td>"
        row[0] = '{:+d}'.format(int(row[0]))
        for data in row:
            try:
                stra += "<td align='center'>"+str(int(data))+"</td>"
            except:
                stra += "<td align='center'>"+str(data)+"</td>"
        stra += "<td align='center'>"+str(winRate)+"%</td>"
        #stra += "<td>"+str(int(row[1]))+"</td><td>"+str(int(row[2]))+"</td>"
        stra += "</tr> \n"
    #print(stra)
    
    return stra


def text_format_comment_sum():
    global df
    #print(df['slump'].sum())
    return "<h3>合計差枚は"+str(int(df['slump'].sum()))+"です。</h3><br>"

def text_format_comment_avg():
    global df
    df_s = df.replace('0', np.nan)
    #print(df_s['slump'].mean())
    return "<h3>平均差枚は"+str(int(df_s['slump'].mean()))+"です。</h3><br>"

df = SystemMain.main()
file = open(FILE_NAME,'r',encoding="utf-8")
body = file.read().format(text_format_table_number(),text_format_table_slump(),text_format_table_groupby(),text_format_table_lastnumber(),text_format_comment_sum(),text_format_comment_avg())
file.close()

body = escape(body)
categories = ['パチンコ','スロット', 'まとめ']
now = datetime.now()
# is_draftをFalseにすると公開になります。Trueで下書き投稿
article = create_hatena_text(TITLE, USER_NAME, body, now, categories, is_draft=True)
post_hatena_blog(USER_NAME, PASSWORD, entry_id=None, blog_name=BLOG_NAME, data=article)