import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

def crawl_notice(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    today = datetime.today().strftime('%Y.%m.%d.')
    y = datetime.today().strftime('%Y')
    m = datetime.today().strftime('%m')
    d = datetime.today().strftime('%d')
    # 공지사항 제목, 링크 추출
    notices = []
    notices.append(f"📍 {y}년 {m}월 {d}일 공지입니다.")

    for item in soup.select('li'):  # 공지사항 항목이 포함된 li 태그 선택
        if item.select_one('span.fix'):
            continue

        # 제목이 포함된 p.tit 태그 선택
        title_tag = item.select_one('p.tit')
        if title_tag:
            title = title_tag.get_text(strip=True)  # 제목만 추출

            # 링크가 포함된 a 태그 선택
            link_tag = item.select_one('a[href]')
            if link_tag:
                onclick_value = link_tag.get('onclick', '')
                
                # goDetail() 함수에서 숫자 추출
                match = re.search(r'goDetail\((\d+)\)', onclick_value)
                if match:
                    detail_id = match.group(1)  # 숫자 추출
                    link = f"https://www.dongguk.edu/article/HAKSANOTICE/detail/{detail_id}"  # 링크 생성
                else:
                    link = '링크 없음'
            else:
                link = '링크 없음'
            
            # 날짜 정보가 담긴 .info 클래스가 있는 div 태그 찾기
            info_tag = item.select_one('.info')
            if info_tag:
                date_str = info_tag.select_one('span').get_text(strip=True)
                
                try:
                    notice_date = datetime.strptime(date_str, '%Y.%m.%d.').strftime('%Y.%m.%d.')
                except ValueError:
                    continue  # 날짜 형식이 맞지 않으면 건너뜀

                # 오늘 날짜의 공지사항만 추가
                if notice_date == today:
                    notices.append(f"{title}\n{link}")
    
    # 오늘 날짜에 올라온 공지가 없으면 안내 문구 추가
    if len(notices) == 1:  # 첫 번째 항목은 "오늘 공지입니다."라서, 그 이후에 공지사항이 없으면
        notices.append("오늘 올라온 공지가 없습니다.")

    # 공지사항을 텍스트로 반환 (디스코드 봇에서 사용 가능)
    return "\n\n".join(notices)


if __name__ == "__main__":
    today = crawl_notice()
    notices = crawl_notice()
    print(notices)  # 추출된 공지사항을 출력
