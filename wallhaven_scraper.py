from bs4 import BeautifulSoup
import requests
import time
import re
import os

spath = 'out'

# create folder
if not os.path.exists(spath):
    os.mkdir(spath)

burl = 'https://wallhaven.cc/search?categories=110&purity=100&topRange=1M&sorting=toplist&order=desc&ai_art_filter=1&page='

# NSFW uncomment requests.get(x,headers=head)
#burl = 'https://wallhaven.cc/search?categories=110&purity=001&topRange=1M&sorting=toplist&order=desc&ai_art_filter=1&page='

# cookie login > f12 > network > headers
cookie = ''
head = {'Cookie':cookie,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
tsite = f'{burl}2'

res = requests.get(tsite)
#res = requests.get(tsite,headers=head)

bs = res.text
soup = BeautifulSoup(bs,'xml')
fpage = soup.find_all(class_="thumb-listing-page-header")[-1].find('h2')

maxpage = 3
#maxpage = int(str(fpage).split('/')[2].strip().split('<')[0]) # all page
page = 1

# thumb > img
print(f'Download {maxpage} pages ...')
while page <= maxpage:
    site = f'{burl}{page}'
    
    res = requests.get(site)
    #res = requests.get(site,headers=head)
    
    bs = res.text
    soup = BeautifulSoup(bs,'xml')
    
    # Grab thumbnail url
    walls = soup.find_all('a',class_='preview')
    uwall = []
    
    # Add url to list
    for wall in walls:
        uwall.append(wall.get('href'))
    
    # Download image
    for url in uwall:
        
        res2 = requests.get(url)
        #res2 = requests.get(url,headers=head)
        
        bs2 = res2.text
        soup2 = BeautifulSoup(bs2,'xml')
        
        img = soup2.find_all('img')[-1].get('src')
        #img = soup2.select('#wallpaper') # Select by id
        
        dimg = requests.get(img).content
        #dimg = requests.get(img,headers=head).content
        
        file = os.path.join(spath,img.split('/')[-1])
        print(f'Download: {img.split("/")[-1]} from {url} to {file}')
        with open(file, 'wb') as f: 
         f.write(dimg)
         f.flush()
         time.sleep(0.5)
    page += 1
