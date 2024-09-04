from bs4 import BeautifulSoup
import requests
import time
import os
import csv
import random
#import re

spath = 'out'
csv_file = "output.csv"

search_only = True

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
data = {"keysearch":id}
#time.sleep()

#time.sleep(random.random()))

#print(random.uniform(1,2))
time.sleep(random.uniform(0,1.75))

res = requests.post(burl,headers=head,data=data)

bs = res.text
soup = BeautifulSoup(bs,'html.parser')
#print(soup)

table = soup.find("tbody")
table = soup.find_all("td")
#print(table)

name = str(table[1]).split("<p class=\"text-th\">")
gender = str(table[2]).split("<p class=\"text-th\">")
faculty = str(table[3]).split("<p class=\"text-th\">")
major = str(table[4]).split("<p class=\"text-th\">")
degree = str(table[5]).split("<p class=\"text-th\">")

# split en and th
faculty_en = faculty[0][4:]
faculty_th = faculty[1].replace("</p></td>","")

major_en = major[0][4:]
major_th = major[1].replace("</p></td>","")

degree_en = degree[0][4:]
degree_th = degree[1].replace("</p></td>","")

curriculum_type = str(table[6])[4:-5]

if "F" not in gender[1]:
    gender_en = "MALE"
    gender_th = "ชาย"
else:
    gender_en = "FEMALE"
    gender_th = "หญิง"

name_en = name[0][4:].strip().split()
name_en = " ".join(name_en)

name_th = name[1].replace("</p></td>","").strip().split()
name_th = " ".join(name_th)

# en/th
table2 = str(table[7]).split("\n")
nationality = table2[5].split("</td><td>")[1][:-10]
faculty2 = table2[6].split("</td><td>")[1][:-10]
degree2 = table2[7].split("</td><td>")[1][:-10]
degree_name = table2[8].split("</td><td>")[1][:-10]
major2 = table2[9].split("</td><td>")[1][:-10]
submajor = table2[10].split("</td><td>")[1][:-10]
adviser = table2[11].split("</td><td>")[1][:-10].split()
adviser = " ".join(adviser)
admission = table2[12].split("</td><td>")[1][:-10]

#name = soup.find_all(class_="text-th")
#name = str(name[0]).split(">")[1].strip("</p").strip().split()
#name = " ".join(name)

# write to csv
if not search_only:
    with open('output.csv',mode='a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id,name_th])
else:
    print(f"name : {name_en} / {name_th}")
    print(f"nationality : {nationality}")
    print(f"faculty : {faculty2}")
    print(f"degree : {degree2} | {degree_name}")
    print(f"major : {major2} | sub-major : {submajor}")
    print(f"adviser : {adviser}")
    print(f"admission : {admission}")

#print("                                                                                                ".count(" "))
#fpage = soup.find_all(class_="thumb-listing-page-header")[-1].find('h2')
