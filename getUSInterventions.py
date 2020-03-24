#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:15:07 2020

@author: jingjingtang
"""
import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup 

def getClosureTimeofUniversitiesandColleges(outputpath = None):

    url = "https://coronavirus.1point3acres.com/_next/static/chunks/254a1764fdea81c1edb65c74503a3d7acf656504.ffc6e960ae850f135142.js"

    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    resp = requests.get(url, headers = header)
    schools = str(BeautifulSoup(resp.content, 'html.parser').contents[0]).split('[')[4].split(']')[-3][1:-1].split('},{')

    columnnames = list(json.loads('{' + schools[0] + '}').keys())
    df = pd.DataFrame(columns = columnnames, index = range(len(schools)))
    for i in range(len(schools)):
        content = schools[i].split('","')
        content[0] = content[0][1:]
        content[-1] = content[-1][:-1]
        for ele in content:
            # print(ele)
            key, value = ele.split('":"')
            df.loc[i][key] = value
    if outputpath == None:
        df.to_csv('US_Universities_closure_date.csv', sep = ',', index = False)
    else:
        df.to_csv(outputpath, sep = ',', index = False)
    return df

def getInterventionsfromWiki(outputpath = None):
    url = "https://en.wikipedia.org/wiki/U.S._state_and_local_government_response_to_the_2020_coronavirus_pandemic"
    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    resp = requests.get(url, headers = header)
    soup = BeautifulSoup(resp.content, 'html.parser')
    table = soup.select('table')[1]
    df = pd.read_html(table.prettify())[0]
    multiindex = np.array(df.keys())
    df = df.drop([multiindex[1], multiindex[-1]], axis = 1)
    columns = [multiindex[0][0], multiindex[2][0], multiindex[3][0], multiindex[4][0]] + \
        [multiindex[i][0] + '-' + multiindex[i][1] for i in range(5, multiindex.shape[0]-1)]
    df.columns = columns
    if outputpath == None:
        df.to_csv('US_interventions.csv', sep = ',', index = False)
    else:
        df.to_csv(outputpath, sep = ',', index = False)
    return df


if __name__ == '__main__':
    getClosureTimeofUniversitiesandColleges()
    getInterventionsfromWiki()
    



    

