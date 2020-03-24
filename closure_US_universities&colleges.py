#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:15:07 2020

@author: jingjingtang
"""
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup 


get_cities_url = "https://coronavirus.1point3acres.com/_next/static/chunks/254a1764fdea81c1edb65c74503a3d7acf656504.ffc6e960ae850f135142.js"

header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
resp = requests.get(get_cities_url, headers = header)
schools = str(BeautifulSoup(resp.content, 'html.parser').contents[0]).split('[')[4].split(']')[-3][1:-1].split('},{')

columnnames = list(json.loads('{' + schools[0] + '}').keys())
df = pd.DataFrame(columns = columnnames, index = range(len(schools)))
for i in range(len(schools)):
    
    for key in temptdict.keys():
        df.loc[i][key] = temptdict[key]

