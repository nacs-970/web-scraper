from bs4 import BeautifulSoup
import requests
import time
import re
import os

spath = 'out'

# create folder
if not os.path.exists(spath):
    os.mkdir(spath)

tags = '1girl'
burl = f'https://safebooru.org/index.php?page=post&s=list&tags={tags}+&pid='
bs = requests.get(burl).text
soup = BeautifulSoup(bs,'html.parser')

# Page 40 / 40 = 2
# Start page 1 = 0 page 2 = 40

maxpage = 80
#maxpage = int(str(soup.find(['a'],alt = 'last page').get('href')).split('=')[4])//40
page = 0

print(f'Download {(maxpage//40)+1} pages ...')

while page <= maxpage:
    
    aurl = []

    burl = f'https://safebooru.org/index.php?page=post&s=list&tags={tags}+&pid={page}'
    bs = requests.get(burl).text
    soup = BeautifulSoup(bs,'html.parser')
    urls = soup.find_all(['a'],id = re.compile('^p[0-9]+'))
    # urls = soup.find_all(['a'],href = re.compile('^index\.php\?page\=post\&s\=view\&id=+'))

    for url in urls:

        # iurl = url.get('id').split('p')[1]
        # aurl.append(f'https://safebooru.org/index.php?page=post&s=view&id={iurl}')

        iurl = url.get('href')
        aurl.append(f'https://safebooru.org/{iurl}')

    for url in aurl:
        ibs = requests.get(url).text
        isoup = BeautifulSoup(ibs,'html.parser')
        img = isoup.find(['a'],string = "Original image",href = re.compile('^https://safebooru.org//images/+')).get('href')
        
        id = url.split('=')[-1] # get image id
        sid = img.split('/')[-1].split('.')[0][:6] # Get 6 first char
        fname = f"{id}-{sid}.{img.split('.')[2]}"
         
        print(f'Download {fname} from {img} to file')
        file = os.path.join(spath,fname)
        print(file)
        
        imgu = requests.get(img).content
        with open(file, 'wb') as f: 
            f.write(imgu)
            f.flush()
            time.sleep(0.5)

    page += 40
