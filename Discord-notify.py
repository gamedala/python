# 導入 Discord.py 套件
import discord

# 取得 Discord client 物件才能操作
client = discord.Client(intents=discord.Intents.default())


# 調用 event 函式庫
@client.event

# 當機器人完成啟動時在終端機顯示提示訊息
async def on_ready():
    print(f'目前登入身份：{client.user}')

# 調用 event 函式庫
@client.event
# 當有訊息時
async def on_message(message):
    
    # 排除機器人本身發出的訊息，避免機器人自問自答的無限迴圈
    if message.author == client.user:
        return
    
    # 如果我們說了「誰是機器人」，機器人就會回「誰叫我？」
    if message.content == '誰是機器人':
        await message.channel.send('誰叫我？')


client.run('098701b4fe8f123a9df6284ad88a20c0fee91111faaec41ffa4b7aaa1af9960a',) #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面