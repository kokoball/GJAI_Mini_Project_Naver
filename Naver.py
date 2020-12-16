import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import openpyxl # 저는 이거 설치해야 되던데 !pip install openpyxl
import re

url='https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&listType=paper&sid1=001&date=20200826&page='

title=[]
href=[]
content=[]
result={}

for i in range(1,10):
    page=str(i)
    response=requests.get(url+page)
    soup=BeautifulSoup(response.text,'html.parser')
    # print(soup)
    ul=soup.find('div',class_='list_body newsflash_body')

    print(ul)

    # for i in ul.find_all('a',class_='nclicks(cnt_papaerart1)'):
    #     title.append(i.get_text().replace('\t','').replace('\n',''))
    #     href.append(i['href'])

for contents in href:
    res=requests.get(contents)
    soup=BeautifulSoup(res.text,'html.parser')
    div=soup.find('div',class_='_article_body_contents').get_text()
    content.append(div)

# print(title)
# print(href)
# print(content)

result = {"title":title, "content":content, "href":href } #딕셔너리 변환
df = pd.DataFrame(result) #df로 변환
now = datetime.now() #오늘 날짜 변환
file_path = 'C:/Users' #파일 경로
filename = '%s-%s-%s %s시 %s분 %s초 Naver_news.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
df.to_excel(file_path +filename, sheet_name='sheet1')
# 파일 경로 + 파일 이름, sheet_name = 시트네임(기본sheet1)