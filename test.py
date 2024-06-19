import requests
from bs4 import BeautifulSoup
import time
import os
import re
import webbrowser

# URL 설정
url = "https://www.kitribob.kr/board/1"

def get_latest_post_no():
    # 웹페이지 요청
    response = requests.get(url)
    # 페이지 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    scripts = soup.find_all('script', type='application/javascript')
    
    pattern = r'"total_cnt":"(\d+)"'
    for script in scripts:
        # Use re.search to find the pattern in the script content
        match = re.search(pattern, script.text)
        if match:
            return match.group(1)
            break
        else :
            return None
            

def format_time():
    # 현재 시간 가져오기
    now = time.localtime()
    # 오후/오전 구분
    am_pm = "오전" if now.tm_hour < 12 else "오후"
    # 12시간 형식으로 시간 변환
    hour = now.tm_hour % 12
    hour = 12 if hour == 0 else hour
    return f"{am_pm} {hour:d}시 {now.tm_min:02d}분 {now.tm_sec:02d}초"

def flash_background():
    while True:  # 5번 반짝이기
        os.system('color 07')  # 흰색 배경, 검은색 글자
        time.sleep(0.5)
        os.system('color 70')  # 검은색 배경, 흰색 글자
        time.sleep(0.5)
    os.system('color 07')  # 원래 색으로 복원

# 현재 최신 게시물 No. 저장
current_latest_no = get_latest_post_no()

while True:
    latest_no = get_latest_post_no()
    timestamp = format_time()
    if latest_no and latest_no != current_latest_no:
    #if True:
        print(f"[{timestamp}] 새 게시물이 올라왔습니다! No.: {latest_no}")
        webbrowser.open_new(url)
        flash_background()
        current_latest_no = latest_no
    else:
        print(f"[{timestamp}] {' ' * len('새 게시물이 올라왔습니다!')} No, : {latest_no}")
    
    # 60초마다 확인
    time.sleep(60)
