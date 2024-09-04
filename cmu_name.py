from bs4 import BeautifulSoup
import requests
import time
import os
import csv
import random
#import re

spath = 'out'
csv_file = "output.csv"
search_only = False
# create folder
if not os.path.exists(spath):
    os.mkdir(spath)

# create file if not exists
if not os.path.isfile(csv_file):
    with open(csv_file,mode='w') as file:file.write("")

#base url
burl = 'https://www1.reg.cmu.ac.th/reg-stdsearch/index.php'

# cookie login > f12 > network > headers
cookie = ''
head = {'Cookie':cookie,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}

id = int(input())
#id = 6*05*0**9
data = {"keysearch":id}
#time.sleep()

#time.sleep(random.random()))

#print(random.uniform(1,2))
time.sleep(random.uniform(0,1.75))

res = requests.post(burl,headers=head,data=data)

bs = res.text
soup = BeautifulSoup(bs,'html.parser')

name = soup.find_all(class_="text-th")
name = str(name[0]).split(">")[1].strip("</p").strip().split()
name = " ".join(name)

# write to csv
if not search_only:
    with open('output.csv',mode='a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id,name])
else:
    print(name)
#print("                                                                                                ".count(" "))
#fpage = soup.find_all(class_="thumb-listing-page-header")[-1].find('h2')
