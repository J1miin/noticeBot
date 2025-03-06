import discord
import os
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
#url
#학사공지-일반-장학-국제-컴공
urls = ["https://www.dongguk.edu/article/HAKSANOTICE/list", 
        "https://www.dongguk.edu/article/GENERALNOTICES/list",
        "https://www.dongguk.edu/article/JANGHAKNOTICE/list",
        "https://www.dongguk.edu/article/GLOBALNOLTICE/list",
        "https://cse.dongguk.edu/article/notice/list"]
channels =[1347103497006616577,
           1347156648808153088,
           1347156670207229993,
           1347156683612491837,
           1347156697205964841 ]
# 공지사항을 즉시 전송하는 작업
async def send_notice_immediately():
     for url, cId in zip(urls, channels):
        # 채널 ID 입력
        channel = bot.get_channel(cId)  # 메시지를 보낼 채널 ID
        notices = crawl_notice(url)  # 각 URL에 대해 공지사항을 가져옴
        await channel.send(notices)  # 해당 채널에 공지사항 전송

# 봇 준비 완료 시 호출되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await send_notice_immediately()  # 봇이 준비되면 즉시 공지사항 보내기 실행

bot.run(token)  # 이 한 번만 호출하면 됩니다.