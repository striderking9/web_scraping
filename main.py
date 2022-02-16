import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
from itertools import zip_longest

result=requests.get("https://fr.indeed.com/jobs?q=python&l=%C3%8Ele-de-France&vjk=a6d4a487d0d64edb")
print(result)

src = result.content

soup=BeautifulSoup(src,"lxml")

job_titles=soup.find_all("h2",{"class":"jobTitle jobTitle-color-purple"})
job_location=soup.find_all("div",{"class":"companyLocation"})
date=soup.find_all("span",{"class":"date"})
job_description=soup.find_all("div",{"class":"job-snippet"})

JOB_TITLES=[]
JOB_LOCATION=[]
DATE=[]
DESCRIPTION=[]

#for i in range(len(job_description)):
    #JOB_TITLES.append(job_titles[i].text)
    #JOB_LOCATION.append(job_location[i].text)
    #DATE.append(date[i].text)
    #DESCRIPTION.append(job_description[i].text)

titres=["JOB TITLES","JOB LOCATION","ONLINE","DESCRIPTION"]
with open("JOB.csv","w") as MyFile:
    f=csv.writer(MyFile)
    f.writerow(titres)

extract=[JOB_TITLES,JOB_LOCATION,DATE,DESCRIPTION]
exported=zip_longest(*extract)

with open("JOB.csv","a") as MyFile:
    f=csv.writer(MyFile)
    f.writerows(exported)

conn=sqlite3.connect("JOBS.db")
cursor=conn.cursor()

cursor.execute('''create table if not exists 
job(Titre text,Localisation text,Date text,Description text)''')

extract=[JOB_TITLES,JOB_LOCATION,DATE,DESCRIPTION]
exported=zip_longest(*extract)
cursor.executemany('''insert into job values(?,?,?,?)''',exported)
conn.commit()