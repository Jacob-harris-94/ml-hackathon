# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 12:45:07 2018

@author: etu
"""
import re
from bs4 import BeautifulSoup
import requests
from time import sleep
import json
from collections import OrderedDict

def parse():
    url = "https://www.sbir.gov/sbirsearch/award/all?page="
    urlfilter = "f%5B0%5D=im_field_agencies%3A105729&f%5B1%5D=im_field_agencies%3A105744&f%5B2%5D=im_field_agencies%3A105745&f%5B3%5D=im_field_agencies%3A105753"
    pageNum = 1
    maxPage = 100
    while pageNum < maxPage:
        fullurl = url + str(pageNum) + urlfilter
        response = requests.get(fullurl, verify=False)
        print ("Parsing %s"%(fullurl))
        soup = BeautifulSoup(response.text, 'html.parser')
        sbirTitles = soup.findAll('a', {'href':re.compile(r"sbirsearch/detail")})
        openMethod = 'a'
        if pageNum == 1:
            openMethod = 'w'
        with open('outputs/sbirTitles.txt', openMethod + '+') as f_out:
            [f_out.write(hit.text + '\n') for hit in sbirTitles]
        pageNum = pageNum + 1
        sleep(0.25)
    
if __name__=="__main__":
    print ("Fetching Winning SBIR Data")
    scraped_data = parse()
    print ("Writing Winning SBIR Data to output file")
    #with open('Winning-SBIR-summary.json', 'w') as fp:
        #json.dump(scraped_data,fp,indent = 4)