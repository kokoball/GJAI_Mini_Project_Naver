from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd

#각 크롤링 결과 저장하기 위한 리스트 선언 
title_text=[]
result={}


#엑셀로 저장하기 위한 변수
RESULT_PATH ='C:/Users/Alex/News/'  #결과 저장할 경로
now = datetime.now() #파일이름 현 시간으로 저장하기

def crawler(maxpage,query,date):

    s_from = date.replace(".","")
    page = 1  
    maxpage_t =(int(maxpage)-1)*10+1   # n*10개
    
    while page <= maxpage_t:
        url = "https://news.naver.com/main/list.nhn?mode=LS2D&sid2=" + query + "&sid1=101&mid=shm&date=" + s_from + "&page=" + str(page)
        
        response = requests.get(url)
        html = response.text
 
        #뷰티풀소프의 인자값 지정
        soup = BeautifulSoup(html, 'html.parser')
 
        #<a>태그에서 제목과 링크주소 추출
        atags = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li')
        for atag in atags:
            title_text.append(atag.text)     #제목

        #모든 리스트 딕셔너리형태로 저장
        result= {"title":title_text }  
        print(page)
        
        df = pd.DataFrame(result)  #df로 변환
        page += 10
    
    
    # 새로 만들 파일이름 지정
    outputFileName = '%s-%s-%s  %s시 %s분 %s초 Naver_news.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_excel(RESULT_PATH+outputFileName,sheet_name='sheet1')
    
    

def main():
    info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    
    maxpage = input("크롤링할 뉴스 갯수 입력하시오(n*10개): ")  
    query = input("금융:259, 경제:258, 중기/벤처:771: ")  
    date = input("날짜 입력(202x.xx.xx):")  #2019.01.04

    crawler(maxpage,query,date) 
    
main()