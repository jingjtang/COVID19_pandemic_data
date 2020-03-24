#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:05:07 2020

@author: jingjingtang
"""

import json
import requests
import pandas as pd
import re
from datetime import date
today = date.today()
 

if __name__ == "__main__":
    #get city list
    get_cities_url = "https://iflow-api.uc.cn/feiyan/track?&city=1"
    resp = requests.get(get_cities_url)
    cities = resp.json()['data']['cities']

    dfind = 0
    df = pd.DataFrame(columns = ['确诊省份', '确诊城市', '性别','年龄', '状态', '住址', '确诊时间', '是否有武汉接触史', '是否有湖北接触史', '短信息', '长信息', '来源'])
    for city in cities:
        citycode = city['citycode']
#        citycode = '450100'
#        break
#        if city['city'] == '六安':
#            break
        try:
            get_patients_url = "https://iflow-api.uc.cn/feiyan/track?&city=0&citycode=" + citycode
            trackes = requests.get(get_patients_url).json()['data']['trackes']
            for track in trackes:
#                break
                temptbase = track['base_info']
                temptdetail = track['detail_info']
                
                ########  Check Sex
                if temptbase.find('男') != -1:
                    sex = '男'
                elif temptbase.find('女') != -1:
                    sex = '女'
                else:
                    sex = None
                
                ########  Check Age
                pattern = re.compile(r'\d{0,3}岁|\d{4}年|\d{0,3}周岁')
                match_res = re.findall(pattern, temptbase)
                if len(match_res) > 0:
                    if match_res[0].find('年') != -1:
                        age = 2020 - int(match_res[0].split('年')[0])
                    elif match_res[0].find('周岁') != -1:
                        age = int(match_res[0].split('周岁')[0])
                    elif match_res[0].find('岁') != -1:
                        newpattern = re.compile(r'\d{0,3}岁\d{0,3}个月')
                        newmatch_res = re.findall(newpattern, temptbase)
                        if len(newmatch_res) > 0:
                            year = int(newmatch_res[0].split('岁')[0])
                            month = int(newmatch_res[0].split('岁')[1].split('个')[0])
                            age = year + month/100
                        else:
                            age = int(match_res[0].split('岁')[0])
                else:
                    pattern = re.compile(r'\d{1,3}个月')
                    match_res = re.findall(pattern, temptbase)
                    if len(match_res)>0:
                        age = 0 + int(match_res[0].split('个月')[0])/100
#                        break
                    else:
                        match_res = re.findall(pattern, temptdetail)
                        if len(match_res)>0:
                            age = 0 + int(match_res[0].split('个月')[0])/100
                        else:
                            age = None
                
                address = None
                
                
                
                
                ########  Check Status
                
                status = '住院'               
                if temptdetail.find('死亡') != -1:
                    status = '死亡'
                elif temptdetail.find('出院') != -1:
                    status = '出院'
                
                #######  Check Confirmed date
                confirmdate = None
                pattern = re.compile(r'\d{0,3}月|\d{0,3}日|确诊|阳性')
                match_res = re.findall(pattern, temptdetail)
                if ('确诊' in match_res or '阳性' in match_res):
                        
                    month = ''
                    date = ''
                    for i in range(len(match_res)-1, -1, -1):
                        if match_res[i] == '确诊' or match_res[i] == '阳性':
                            break
                    for j in range(i, -1, -1):
                        if '日' in match_res[j]:
                            date = match_res[j]
                            break
                    for k in range(j, -1, -1):
                        if '月' in match_res[k]:
                            month = match_res[k]
                            break
                        
                    confirmdate = month + date
#                else:
                    
#                    print(temptdetail)
                
                
                ##### Check Wuhan
                CheckWuhan = '否'
                CheckHubei = '否'
                
                #### Check Hubei 
                if '湖北' in temptdetail:
                    CheckHubei = '是'
                    if '无湖北' in temptdetail:
                        CheckHubei = '否'
                        
                if '武汉' in temptdetail:
                    CheckWuhan = '是'
                    CheckHubei = '是'
                    if '无武汉' in temptdetail or '没有去过' in temptdetail: 
                        CheckWuhan = '否'
                        CheckHubei = '否'
                    
                    
                
                
                                    
                df.loc[dfind] = [track['province'],track['city'], sex, age, status, address, confirmdate, CheckWuhan, CheckHubei,track['base_info'], track['detail_info'], track['source']]
                dfind += 1
        except:
            print('get city: %s errors!', city['city'])
            print(city['citycode'])




    df.to_csv('data/Chin/患者信息%s2.csv'%today.strftime("%m_%d_%y"), index=False)
    print('update 患者信息.csv 成功！')
    
    