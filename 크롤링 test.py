import requests
import json
import requests
from bs4 import BeautifulSoup
import requests
import re


#*****************************1차적으로 첫번째 페이지를 불러온다*******************************#


# 베이스 urlhttps://news.naver.com/main/list.nhn?mode=LS2D&sid2=258&mid=shm&sid1=101&
url='https://news.naver.com/main/list.nhn?mode=LS2D&sid2=258&mid=shm&sid1=101&'
# r_date='20200826'ㄴ
response=requests.get(url)
soup=BeautifulSoup(response.text,'html.parser')

title=[]
l_date=[]
l_page=[]

content=soup.find('div',class_='content')
page=content.find('div',class_='paging')
date=content.find('div',class_='pagenavi_day')

# 일단 첫번째 페이지에서는 몇 페이지까지 있는지 확인이 불가하므로 먼저 제목을 1차적으로 뽑아준다

# 1. 다른 date로 들어갔을때 각각 페이지 수가 다르다. 고로, 첫번째 페이지 기준으로 날짜를 1차적으로 구함
    # 첫번째 페이지는 base url으로 먼저 구해준다

# 2. 날짜를 구했으면 날짜만 넣은 url을 구한구 각각의 페이지수를 구할 수 있음
# 3. 그 페이지 수를 기준으로 제목을 불러올 수 있다

first_title=soup.find('ul',class_='type06_headline')
for i in first_title.find_all('a'):
    a=i.get_text().replace('\t','').replace('\n','')
    title.append(a)
# print(title)


# 날짜 //이하 동문
for i in date.find_all('a'):
    a=i['href']
    a=re.sub(r'.*date=','date=',a)
    l_date.append(a)

# print(l_page)
# print(l_date)


#**************************이제 2차적으로 for문을 돌려 각각의 url을 획득**********************************#

# 날짜별로 url을 구해준다
l_url2=[]
for i in l_date:
    l_url2.append(url+i)
# print(l_url2)

# 날짜별 url의 페이지url을 구해준다

l_url2_p=[]
all_url=[]

for i in l_url2:
    response=requests.get(i)
    soup=BeautifulSoup(response.text,'html')
    page=soup.find('div',class_='paging')
    l_url2_p.append('page=1')
    all_url.append(i+'&page=1')
    for j in page.find_all('a'):
        a=j['href']
        # print(a)  //각 날짜의 페이지수를 구해준다
        # 페이지 수만 구해주기위해 sub를 통해 잘라주고 1페이지 추가
        a=re.sub(r'.*page=','page=',a)        
        all_url.append(i+'&'+a)
# print(all_url)


#**************************이제 3차적으로 첫 페이지를 제외한 모든 페이지의 제목을 가져온다**********************************#

for i in all_url:
    response=requests.get(i)
    soup=BeautifulSoup(response.text,'html.parser')
    ul=soup.find('ul',class_='type06_headline')

    for i in ul.find_all('a'):
        title.append(i.get_text().replace('\t','').replace('\n',''))

print(title)