# 1. HTML받아와서 html변수에 문자열을할당
#  1-1. 만약 'data/episode_list.html'이 없다면
#   -> 내장모듈 os의 'exists'함수를 사용해본다
#   -> 파이썬 공식문서 확인
# http://comic.naver.com/webtoon/list.nhn?titleId=703845&weekday=wed
# 죽음에 관하여 (재) 페이지를
# requests를 사용해서 data/episode_list.html에 저장
#  list.nhn뒤 ?부터는 url에 넣지 말고 GET parameters로
#   -> requests문서의 'Passing Parameters In URLs'
# 저장 후에는
#  requests로 받은 데이터를 html변수에 할당
#
#  1-2. 이미 'data/episode_list.html'이 있다면
#   html변수에 파일을 불러와 할당

# 1.
#  os.path.exists(경로)의 결과는 파일이 존재하는지, 존재하지 않는지 여부를 True/False로 반환해준다
#  os.path.exists()의 결과를 분기로
#   파일이 존재하면 -> open()을 사용해 가져온 파일 객체를 read()한 결과 문자를 html변수에 할당
#   존재하지 않으면 -> 1. requests.get()의 결과인 response의 text속성값을 html변수에 할당
#               -> 2. response의 text속성값을 'data/episode_list.html'파일에 저장

# requests문서 아래 3개는 보고나서 진행
# Make a Request
# Passing Parameters In URLs
# Response Content
import os

import requests
from bs4 import BeautifulSoup

# HTML파일을 저장하거나 불러올 경로
file_path = 'data/episode_list.html'
# HTTP요청을 보낼 주소
url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
# HTTP요청시 전달할 GET Parameters
params = {
    'titleId': 703845,
}

# HTML파일이 로컬에 저장되어 있는지 검사
if os.path.exists(file_path):
    # 저장되어 있다면, 해당 파일을 읽어서 html변수에 할당
    html = open(file_path, 'rt').read()
else:
    # 저장되어 있지 않다면, requests를 사용해 HTTP GET요청
    response = requests.get(url_episode_list, params)
    # 요청 응답객체의 text속성값을 html변수에 할당
    html = response.text
    # 받은 텍스트 데이터를 HTML파일로 저장
    open(file_path, 'wt').write(html)

# BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
soup = BeautifulSoup(html, 'lxml')

# div.detail > h2 (제목, 작가)의
#  0번째 자식: 제목 텍스트
#  1번째 자식: 작가정보 span Tag
#   Tag로부터 문자열을 가져올때는 get_text()
h2_title = soup.select_one('div.detail > h2')
title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
# div.detail > p (설명)
description = soup.select_one('div.detail > p').get_text(strip=True)

print(title)
print(author)
print(description)


# 3. 에피소드 정보 목록을 가져오기
#  url_thumbnail:   썸네일 URL
#  title:           제목
#  rating:          별점
#  created_date:    등록일
#  no:              에피소드 상세페이지의 고유 번호
#   각 에피소드들은 하나의 dict데이터
#   모든 에피소드들을 list에 넣는다
