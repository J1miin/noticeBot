import discord
import os
import schedule
import time
from discord.ext import commands
from crawling import crawl_notice

token_path = os.path.dirname(os.path.abspath(__file__)) + '/token.txt'
with open(token_path, "r", encoding="utf-8") as t:
    token = t.read().strip()

# intents 설정
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# 한 줄 소개
game = discord.Game("공지사항 정리")

# 활성화 상태 만들기
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game, intents=intents)

# url과 채널 ID
urls = [
    "https://www.dongguk.edu/article/HAKSANOTICE/list", 
    "https://www.dongguk.edu/article/GENERALNOTICES/list",
    "https://www.dongguk.edu/article/JANGHAKNOTICE/list",
    "https://www.dongguk.edu/article/GLOBALNOLTICE/list",
    "https://cse.dongguk.edu/article/notice/list"
]
channels = [
    1347103497006616577,
    1347156648808153088,
    1347156670207229993,
    1347156683612491837,
    1347156697205964841
]

# 공지사항을 즉시 전송하는 작업
async def send_notice_immediately():
    for url, cId in zip(urls, channels):
        channel = bot.get_channel(cId)  # 메시지를 보낼 채널 ID
        notices = crawl_notice(url)  # 각 URL에 대해 공지사항을 가져옴
        await channel.send(notices)  # 해당 채널에 공지사항 전송

# 봇 준비 완료 시 호출되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # 매일 오후 6시에 공지사항을 보내도록 스케줄 설정
    schedule.every().day.at("18:00").do(run_scheduled_task)

def run_scheduled_task():
    bot.loop.create_task(send_notice_immediately())

# 스케줄러를 실행하는 함수
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 실행

# 봇을 시작하고, 스케줄러도 같이 실행
if __name__ == "__main__":
    bot.loop.create_task(run_schedule())
    bot.run(token)
