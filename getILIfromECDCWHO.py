#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:41:03 2020

@author: jingjingtang
"""

import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


url = 'https://flunewseurope.org/WebForms/ViewReport.aspx?ReportName=dinfl06&SDId=2325&SUrl=https%3a%2f%2fflunewseurope.org%2fPrimaryCareData%2fIndex%2fshare%2fdinfl06%3fts%3d20200317232612783%23dinfl06'
driver = webdriver.Chrome()
driver.get(url)
driver.refresh()

#time.sleep(3)
for i in range(2, 54):
    # select country
    
    Select(driver.find_element_by_tag_name('select')).select_by_value(str(i))

    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    options = soup.select('#fluNewsReportViewer_ctl04_ctl05_ddValue')[0].find_all('option')


    ind = 1
    for j in range(len(options)):
        if 'ILI' in str(options[j]):
            pattern = re.compile(r'\d+')
            ind = re.findall(pattern, str(options[j]))[0]
            break
    
    if type(ind) == str:
            
        # select clinical tyle
        Select(driver.find_element_by_id('fluNewsReportViewer_ctl04_ctl05_ddValue')).select_by_value(ind)
        # update
#        driver.find_element_by_id('fluNewsReportViewer_ctl04_ctl00').click()
#        time.sleep(1)
        driver.find_element_by_id('btnSelectExportType').click()
        driver.find_element_by_id('btnExportToCsv').click()
        
#        time.sleep(3)
#        driver.refresh()
        
    
    else:
        driver.refresh()
#        time.sleep(1)
        continue
        
