# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 09:43:59 2018

@author: etu
"""

import re
from bs4 import BeautifulSoup
import requests
from time import sleep
import json
import argparse
from collections import OrderedDict

from multiprocessing import Pool
from functools import partial

def parse(ticker):
    url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
    response = requests.get(url, verify=False)
    print ("Parsing %s"%(url))
    sleep(4)
    soup = BeautifulSoup(response.text, 'html.parser')
    summary_table = soup.findAll("div", {"data-test":re.compile(r'summary-table')})
    #for hit in summary_table:    
        #print(hit.prettify())
    summary_data = OrderedDict()
    other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
    summary_json_response = requests.get(other_details_json_link)
    try:
        json_loaded_summary =  json.loads(summary_json_response.text)
        y_Target_Est = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
        earnings_list = json_loaded_summary["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
        eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
        datelist = [i['fmt'] for i in earnings_list['earningsData']]
        earnings_date = ' to '.join(datelist)
             
        for table_data in summary_table:
            raw_table_key=[]
            raw_table_value=[]
            filtered_table_decendants = [d for d in table_data.descendants if d.name == 'td']
            for d in filtered_table_decendants:
                for dClass in d.get('class',''):
                    if dClass == "C(black)":
                        raw_table_key.append(d.text)
                    if dClass == "Ta(end)":
                        raw_table_value.append(d.text)
                        table_key = ''.join(raw_table_key).strip()
                        table_value = ''.join(raw_table_value).strip()
                        summary_data.update({table_key:table_value})
                        raw_table_key=[]
                        raw_table_value=[]
        summary_data.update({'1y Target Est':y_Target_Est,'EPS (TTM)':eps,'Earnings Date':earnings_date,'ticker':ticker,'url':url})
        return summary_data
    except:
        print ("Failed to parse json response")
        return {"error":"Failed to parse json response"}
        
if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('ticker',help = '')
    args = argparser.parse_args()
    ticker = args.ticker
    print ("Fetching data for %s"%(ticker))
    scraped_data = parse(ticker)
    print ("Writing data to output file")
    with open('outputs/%s-summary.json'%(ticker), 'w') as fp:
        json.dump(scraped_data,fp,indent = 4)