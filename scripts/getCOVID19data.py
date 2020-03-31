#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:15:07 2020

@author: jingjingtang
"""
import requests
import json
import os 
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup 

def getClosureTimeofUniversitiesandColleges(outputpath = None):

    url = "https://coronavirus.1point3acres.com/_next/static/chunks/e53538f4a6331cce5409b69446448c719a696032.888606a2f00cf42865ea.js"

    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    resp = requests.get(url, headers = header)
    schools = str(BeautifulSoup(resp.content, 'html.parser').contents[0]).split('[')[4].split(']')[-3][1:-1].split('},{')

    columnnames = list(json.loads('{' + schools[3] + '}').keys())
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
        df.to_csv('../data/US_universities_closure_dates.csv', sep = ',', index = False)
    else:
        df.to_csv(outputpath, sep = ',', index = False)
    return df

def getUSInterventionsfromWiki(outputpath = None):
    url = "https://en.wikipedia.org/wiki/U.S._state_and_local_government_response_to_the_2020_coronavirus_pandemic"
    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    resp = requests.get(url, headers = header)
    soup = BeautifulSoup(resp.content, 'html.parser')
    table = soup.select('table')[1]
    df = pd.read_html(table.prettify())[0]
    multiindex = np.array(df.keys())
    df = df.drop([multiindex[1], multiindex[-2], multiindex[-1]], axis = 1)
    columns = [multiindex[0][0], multiindex[2][0], multiindex[3][0], multiindex[4][0]] + \
        [multiindex[i][0] + '-' + multiindex[i][1] for i in range(5, multiindex.shape[0]-2)]
    df.columns = columns
    if outputpath == None:
        df.to_csv('../data/US_interventions.csv', sep = ',', index = False)
    else:
        df.to_csv(outputpath, sep = ',', index = False)
    return df


def getWorldCovid19fromWorldometer():
    """
    get covid19 case data from worldometer
    Haven't found time series 
    """  
    os.mkdir('../data/Data_from_Worldometer')
    url = "https://www.worldometers.info/coronavirus/#countries"
    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    resp = requests.get(url, headers = header)
    soup = BeautifulSoup(resp.content, 'html.parser')
    table = soup.select('table')[0]
    df = pd.read_html(table.prettify())[0]
    df.to_csv('../data/Data_from_Worldometer/Covid19data_from_worldometer_worldwide.csv', sep = ',', index = False)
    
    return df

def getItalyCovid19fromWiki():
    url = "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Italy"
    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    resp = requests.get(url, headers = header)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    #Confirmed COVID-19 cases in Italy by region
    table = soup.select('table')[8]
    df = pd.read_html(table.prettify().replace(';', ''))[0]
    colnames = [x[0] + x[1] if x[0] != x[1] else x[0] for x in df.keys()]
    df.columns = colnames
    df.iloc[:-1, :].to_csv('../data/Italy_covid19_confirmedcases_byregion.csv', sep = ',', index = False)
    
    # Daily COVID-19 cases in Italy by region
    table = soup.select('table')[9]
    df = pd.read_html(table.prettify().replace(';', ''))[0]
    colnames = [x[0] + '_' + x[1] if x[0] != x[1] else x[0] for x in df.keys()]
    df.columns = colnames
    df.iloc[:-2, :].to_csv('../data/Italy_covid19_daily_confirmedcases_byregion.csv', sep = ',', index = False)
    
    #Confirmed COVID-19 cases in Italy by gender and age
    # table = soup.select('table')[11]
    # df = pd.read_html(table.prettify().replace(';', ''))[0]
    # colnames = [x[0] + '_' + x[1] if x[0] != x[1] else x[0] for x in df.keys()]
    # df.columns = colnames
    # df.iloc[:-2, :].to_csv('../data/Italy_covid19_daily_confirmedcases_byregion.csv', sep = ',', index = False)
    
def getGermanyCovid19fromWiki():
    url = "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Germany"
    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    resp = requests.get(url, headers = header)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    #Confirmed cumulative infections (deaths in brackets) according to data from the Robert Koch Institute
    table = soup.select('table')[3]
    df = pd.read_html(table.prettify().replace(';', ''))[0]
    colnames = [x[0] + '_'+ x[1] if x[0] != x[1] else x[0] for x in df.keys()]
    df.columns = colnames
    df.iloc[:-1, :].to_csv('../data/Germany_covid19_confirmedcases_bystate.csv', sep = ',', index = False)


if __name__ == '__main__':
    getClosureTimeofUniversitiesandColleges()
    getUSInterventionsfromWiki()
    



    

