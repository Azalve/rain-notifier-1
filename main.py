import json, requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.webdriver.chrome.options import Options
# from keep_alive import keep_alive
# keep_alive()


with open("config.json", "r") as config:
  config = json.load(config)
flask = config['flask']
webhook_enable = config['webhook_enabled']
bigwebhookurl = "https://discord.com/api/webhooks/1071268691674673213/rJvKCMlhCx28jfDc-31RVE_V7bUu--P44PAn70Hq5pl7nfOo1dw0mZMJrR8VLsLYUeTM"
spamwebhookurl = "https://discord.com/api/webhooks/1071823236796526652/W8ePBN9EDLQBCxYOSDKJ8n9wUwaiQqvGP437G63wQw5F2aFcHet9S4-Fxi2D-H2i2vb1"
winnotif = config['windows_notification']
#if webhook_enable == "True":
# webhook = DiscordWebhook(url=webhookurl, content='@everyone')
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless') #testing this argument
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.implicitly_wait(10)

while True:
  try:
    driver.get('https://rest-bf.blox.land/chat/history')
    soup = BeautifulSoup(driver.page_source, 'lxml')
    check = json.loads(soup.find("body").text)['rain']
    if check['active'] == True:
      prize = str(check['prize'])[:-2]
      host = check['host']
      getduration = check['duration']
      convert = (getduration/(1000*60))%60
      duration = (int(convert))
      print(f"Bloxflip Rain!\nRain amount: {prize} R$\nExpiration: {duration} minutes\nHost: {host}\n\n")
      if webhook_enable == "True" and int(prize) >= 9999:
        webhook = DiscordWebhook(url=bigwebhookurl, content='@everyone')
        userid = requests.get(f"https://api.roblox.com/users/get-by-username?username={host}").json()['Id']
        thumburl = (f"https://www.roblox.com/headshot-thumbnail/image?userId={userid}&height=50&width=50&format=png")
        embed = DiscordEmbed(title=f"{host} is hosting a chat rain!", url="https://bloxflip.com", color=0xFFC800)
        embed.add_embed_field(name="Rain Amount", value=f"{prize} R$")
        embed.add_embed_field(name="Expiration", value=f"{duration} minutes")
        embed.add_embed_field(name="Host", value=f"[{host}](https://www.roblox.com/users/{userid}/profile)")
        embed.set_timestamp()
        embed.set_thumbnail(url=thumburl)
        webhook.add_embed(embed)
        webhook.execute()
        webhook.remove_embed(0)
        time.sleep(130)
      elif webhook_enable == "True" and int(prize) < 9999:
        webhook = DiscordWebhook(url=spamwebhookurl)
        userid = requests.get(f"https://api.roblox.com/users/get-by-username?username={host}").json()['Id']
        thumburl = (f"https://www.roblox.com/headshot-thumbnail/image?userId={userid}&height=50&width=50&format=png")
        embed = DiscordEmbed(title=f"{host} is hosting a chat rain!", url="https://bloxflip.com", color=0xFFC800)
        embed.add_embed_field(name="Rain Amount", value=f"{prize} R$")
        embed.add_embed_field(name="Expiration", value=f"{duration} minutes")
        embed.add_embed_field(name="Host", value=f"[{host}](https://www.roblox.com/users/{userid}/profile)")
        embed.set_timestamp()
        embed.set_thumbnail(url=thumburl)
        webhook.add_embed(embed)
        webhook.execute()
        webhook.remove_embed(0)
        time.sleep(130)
      elif check['active'] == False:
        time.sleep(10)
  except Exception as e:
    print(e)
    time.sleep(30)
