import datetime
import discord
import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext import commands
from discord.ext import commands
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from sys import platform

###########################################################################
#Bot settings

prefix = "?"
TOKEN = "YOUR DISCORD BOT TOKEN HERE"
staticdiscordchannel = 1337

iservuser = "YOUR USERNAME HERE"
iservpw = "YOUR PASSWORD HERE"

iservURLtoday = "https://gaussschule-bs.de/iserv/infodisplay/file/186/infodisplay/0/Vertretungsplan/plaene/schueler_heute/subst_001.htm"
iservURLtomorrow = "https://gaussschule-bs.de/iserv/infodisplay/file/186/infodisplay/0/Vertretungsplan/plaene/schueler_morgen/subst_001.htm"

#Notes: Automatic check times can be configured in @bot.event at line 418

###########################################################################




vorherigerPlanHeute = ""
vorherigerPlanMorgen = ""
bot = commands.Bot(command_prefix=prefix)
CallURL = ""
ctx = ""
dfObj = ""

async def UntisCall():

    global CallURL
    global dfObj
    
    await bot.wait_until_ready()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    if platform == "linux" or platform == "linux2":
        driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver')
    elif platform == "win32":
        driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver.exe')
    else:
        print("ERROR: Unable to identify OS")

    driver.maximize_window()
    #launch URL
    driver.get(CallURL)


    driver.find_element(by=By.NAME, value="_username").send_keys(iservuser)
    driver.find_element(by=By.NAME, value="_password").send_keys(iservpw)
    driver.find_element(by=By.CSS_SELECTOR, value=".btn").click()

    BetroffeneKlassen = driver.find_element(by=By.CSS_SELECTOR, value="tr.info:nth-child(3) > td:nth-child(2)").text
    AbwesendeKlassen = driver.find_element(by=By.CSS_SELECTOR, value="tr.info:nth-child(4) > td:nth-child(2)").text
    Datum = driver.find_element(by=By.CSS_SELECTOR, value=".mon_title").text
    
    print (BetroffeneKlassen)

    if ("11A" in BetroffeneKlassen or "11A" in AbwesendeKlassen):
        print ("What is my purpose?")
        print("Debug")

    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    table = soup.select_one('.mon_list > tbody:nth-child(1)')
    rows = table.find_all('tr')

    found = False

    infos=[]

    for row in rows:

        if found and len(row) == 1:
            found = False

        if found:
            columns = row.find_all('td')

            hours = columns[0].text
            subject = columns[1].text
            substitute_teacher = columns[2].text
            room = columns[3].text
            original_teacher = columns[4].text
            kind = columns[5].text
            info = columns[6].text
            classes = columns[7].text

            info = [[hours, subject, substitute_teacher, room, original_teacher, kind, info, classes]]
            infos = infos + info
            
        if 'Klasse 11A' in row.text:
            found = True
            
    dfObj = pd.DataFrame(infos,
        columns = ['Stunde' , 'Fach', 'Vertreter', "Raum", "(Lehrer)", "Art", "Info", "Klasse(n)"],
        )

    " ".join(dfObj)
    codeblockind = "```"
    dfObj = f"{codeblockind}\n{Datum}\n\n{dfObj}\n{codeblockind}"
    print(dfObj)

@bot.command()
async def VertretungsPlanHeute(ctx):
    global vorherigerPlanHeute
    global vorherigerPlanMorgen
    global CallURL
    CallURL = iservURLtoday
    await UntisCall()
    await checkToday()
    
@bot.command()
async def VertretungsPlanMorgen(ctx):
    global vorherigerPlanHeute
    global vorherigerPlanMorgen
    global CallURL
    CallURL = iservURLtoday
    await UntisCall()
    await checkTomorrow()

async def AutoCall():
    global vorherigerPlanHeute
    global vorherigerPlanMorgen
    global CallURL
    global ctx
    global dfObj

    
    CallURL = iservURLtoday
    await UntisCall()
    await checkToday()

    CallURL = iservURLtomorrow
    await UntisCall()
    await checkTomorrow()

async def checkToday():
    
    global vorherigerPlanHeute
    global vorherigerPlanMorgen
    global CallURL
    global ctx
    global dfObj

    if "Empty" in dfObj:
        #await ctx.send("Keinen Eintrag im Vertretungsplan gefunden.")
        now = datetime.now()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Vertretungsplan vom:  " + (now.strftime("%d.%m.%Y %H:%M:%S"))))
    elif vorherigerPlanMorgen == dfObj or vorherigerPlanHeute == dfObj:
        #await ctx.send("Keinen neuen Eintrag gefunden")
        now = datetime.now()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Vertretungsplan vom:  " + (now.strftime("%d.%m.%Y %H:%M:%S"))))
    else: 
        await ctx.send("Eintrag im Vertretungsplan gefunden! @everyone")
        await ctx.send(dfObj)  
        vorherigerPlanHeute = dfObj
        now = datetime.now()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Vertretungsplan vom:  " + (now.strftime("%d.%m.%Y %H:%M:%S"))))

async def checkTomorrow():

    
    global vorherigerPlanHeute
    global vorherigerPlanMorgen
    global CallURL
    global ctx
    global dfObj

    if "Empty" in dfObj:
        #await ctx.send("Keinen Eintrag im Vertretungsplan gefunden.")
        now = datetime.now()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Vertretungsplan vom:  " + (now.strftime("%d.%m.%Y %H:%M:%S"))))
    elif vorherigerPlanMorgen == dfObj or vorherigerPlanHeute == dfObj:
        #await ctx.send("Keinen neuen Eintrag gefunden")
        now = datetime.now()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Vertretungsplan vom:  " + (now.strftime("%d.%m.%Y %H:%M:%S"))))
    else: 
        await ctx.send("Eintrag im Vertretungsplan gefunden! @everyone")
        await ctx.send(dfObj)  
        vorherigerPlanMorgen = dfObj
        now = datetime.now()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Vertretungsplan vom:  " + (now.strftime("%d.%m.%Y %H:%M:%S"))))

@bot.event
async def on_ready():
    global ctx
    ctx = bot.get_channel(staticdiscordchannel)

    print("UntisAPI ready!")
    now = datetime.now()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Launching API..."))

    await AutoCall()

    #initializing scheduler
    scheduler = AsyncIOScheduler()
    
    #Adding defs to scheduler
    scheduler.add_job(AutoCall, CronTrigger(hour="*", minute="*/5", second="0"))

    #starting the scheduler
    scheduler.start()
    await ctx.send("Turned scheduler on")
    
    all_jobs = scheduler.get_jobs()
    print(all_jobs)


bot.run(TOKEN)
