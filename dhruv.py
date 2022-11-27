# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 12:09:40 2022

@author: dhruv
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import random
import sys
import json

#Read command line
if len(sys.argv) != 3:
     print("Give correct command Usage:", sys.argv[0], "<Wiki link> <output folder link>")
     sys.exit(1)

webLinks=[]
visited=[]
subLinks=[]
folder_location=sys.argv[2]
random_num = random.randint(1,20)
print("Random Number: ",random_num)
try:
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    webLinks.append(sys.argv[1])
    for i in range(random_num):
        for j in webLinks:
            if visited.__contains__(j)==False:
                driver.get(j)
                content = driver.page_source
                soup = BeautifulSoup(content)
                for a in soup.findAll('a',href=True):
                    if "wikipedia.org" in a.attrs["href"] and a.attrs["href"].startswith("https://"):
                        subLinks.append(a.attrs["href"])
                visited.append(j)
        webLinks = webLinks+subLinks
        subLinks=[]
        print(len(webLinks))
        
    jsonData = {
      "links": webLinks,
      "total count": len(webLinks),
      "unique count": len(webLinks)-len(visited)
    }
    
    
    with open(folder_location+'data.json', 'w') as f:
      json.dump(jsonData, f)
          
    df = pd.DataFrame({'links':webLinks,'total count':len(webLinks),'unique count':len(webLinks)-len(visited)}) 
    df.to_csv(folder_location+'data.csv', index=False, encoding='utf-8')
    
except:
        print("Error occurred:", sys.exc_info()[0])    
    
    
