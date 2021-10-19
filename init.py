#!/usr/bin/env python
# coding: utf-8

# ## 한국 연예인 리스트 크롤링
# 
# ### 위키백과에서 연예인 리스트 가져오기
# * 배우 :: https://ko.wikipedia.org/wiki/분류:대한민국의_배우
# * 아이돌 :: https://ko.wikipedia.org/wiki/분류:대한민국의_아이돌
# * 가수 :: https://ko.wikipedia.org/wiki/분류:대한민국의_가수
# 
# 
# ### 위키백과 페이징
# * 배우 ::  https://ko.wikipedia.org/w/index.php?title=분류:대한민국의_배우&pagefrom=
# * 아이돌 ::  https://ko.wikipedia.org/w/index.php?title=분류:대한민국의_아이돌&pagefrom=
# * 가수 ::  https://ko.wikipedia.org/w/index.php?title=분류:대한민국의_가수&pagefrom=
# 
# * 유명하지 않은 사람도 많기때문에 유명한 사람만 가져올 방법? 
# * 위키백과에 사진이 올라와 있는 사람만 가져오기
# * 링크 :: https://ko.wikipedia.org/api/rest_v1/page/summary/김태희
# 
# 
# * pip install beautifulsoup4
# * pip install requests

# In[ ]:


from bs4 import BeautifulSoup
import requests
import json

def addResultList(nameList,startIdx,resultList): 
    for idx,name in enumerate(nameList):
        if idx<startIdx :
            continue
        nameTxt = name.text
        
        res = requests.get(url2+nameTxt)
        html = res.text
        soup = BeautifulSoup(html,'html.parser')
        detail_json = json.loads(soup.text)
        
        global lastName
        lastName = nameTxt
        #print('마지막이름 >> ',lastName)
        if not detail_json.get("thumbnail") == None:
            print(nameTxt)
            #print(detail_json.get("thumbnail").get('source'))
            resultList.append(nameTxt)  

title = '대한민국의_아이돌'

url1 = 'https://ko.wikipedia.org/wiki/분류:대한민국의_아이돌'
url2 = 'https://ko.wikipedia.org/api/rest_v1/page/summary/'
url3 = 'https://ko.wikipedia.org/w/index.php?title=분류:대한민국의_아이돌&pagefrom='

res = requests.get(url1)

lastName = ""
resultList = []

print("크롤링 시작")

if res.status_code == 200:
    html = res.text
    soup = BeautifulSoup(html,'html.parser')
    
    # 영화배우 리스트 가져오기
    # css selector 활용
    nameList = soup.select('.mw-category-group li')
    addResultList(nameList,0,resultList)
else:
    print(res.status_code, " !!error!!")
    

# 두번째 페이지 부터 페이징 url을 통해 접근
# 마지막 항목
# 배우 : 휘영
# 아이돌 : 힘찬
# 가수 : 휘인

startName = lastName

print("시작이름 :: >> ",startName)

while not startName == "휘영":
    res = requests.get(url3+resultList[-1])
    
    if res.status_code == 200:
        html = res.text
        soup = BeautifulSoup(html,'html.parser')

        # 영화배우 리스트 가져오기
        # css selector 활용
        nameList = soup.select('.mw-category-group li')
        addResultList(nameList,1,resultList)
    else:
        print(res.status_code, " !!error!!")

print("크롤링 종료 >> 파일 쓰기 시작")

f = open(title+'.txt', 'w')
for name in resultList:
    f.write(name+"\n")
f.close()