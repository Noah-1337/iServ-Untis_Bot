from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from discord.ext import commands
from sys import platform
import discord

###########################################################################
#Bot settings
prefix = "?"
TOKEN = "YOUR DISCORD BOT TOKEN HERE"
staticdiscordchannel = 133769420

iservuser = "YOUR USERNAME HERE"
iservpw = "YOUR PASSWORD HERE"

#Notes: Automatic check times can be configured in @bot.event
#       URLs have to be changed in every def by hand

###########################################################################




vorherigerPlanHeute = ""
vorherigerPlanMorgen = ""
bot = commands.Bot(command_prefix=prefix)

async def VertretungsPlanHeuteAuto():

    global vorherigerPlanHeute
    
    await bot.wait_until_ready()
    ctx = bot.get_channel(staticdiscordchannel)
    await ctx.send("Abfrage für den Vertretungsplan von heute wird durchgeführt")
    await ctx.send("Bitte warten...")
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
    driver.get("https://gaussschule-bs.de/iserv/infodisplay/file/186/infodisplay/0/Vertretungsplan/plaene/schueler_heute/subst_001.htm")

    driver.find_element_by_name("_username").send_keys(iservuser)
    driver.find_element_by_name("_password").send_keys(iservpw)
    driver.find_element_by_css_selector(".btn").click()

    BetroffeneKlassen = driver.find_element_by_css_selector("tr.info:nth-child(3) > td:nth-child(2)").text
    AbwesendeKlassen = driver.find_element_by_css_selector("tr.info:nth-child(4) > td:nth-child(2)").text
    Datum = driver.find_element_by_css_selector(".mon_title").text
    print (BetroffeneKlassen)


    if ("11A" in BetroffeneKlassen or "11A" in AbwesendeKlassen):
        print ("11A")


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

    if "Empty" in dfObj:
        await ctx.send("Keinen Eintrag im Vertretungsplan gefunden.")
    elif vorherigerPlanHeute == dfObj:
        await ctx.send("Keinen neuen Eintrag gefunden")
    else:
        await ctx.send("Eintrag im Vertretungsplan gefunden! @everyone")
        await ctx.send(dfObj)
        vorherigerPlanHeute = dfObj

async def VertretungsPlanMorgenAuto():

    global vorherigerPlanMorgen

    await bot.wait_until_ready()
    ctx = bot.get_channel(staticdiscordchannel)
    await ctx.send("Abfrage für den Vertretungsplan von morgen wird durchgeführt")
    await ctx.send("Bitte warten...")
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
    driver.get("https://gaussschule-bs.de/iserv/infodisplay/file/186/infodisplay/0/Vertretungsplan/plaene/schueler_morgen/subst_001.htm")

    driver.find_element_by_name("_username").send_keys(iservuser)
    driver.find_element_by_name("_password").send_keys(iservpw)
    driver.find_element_by_css_selector(".btn").click()

    BetroffeneKlassen = driver.find_element_by_css_selector("tr.info:nth-child(3) > td:nth-child(2)").text
    AbwesendeKlassen = driver.find_element_by_css_selector("tr.info:nth-child(4) > td:nth-child(2)").text
    Datum = driver.find_element_by_css_selector(".mon_title").text
    print (BetroffeneKlassen)


    if ("11A" in BetroffeneKlassen or "11A" in AbwesendeKlassen):
        print ("11A")


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
        #index = ["", "", "", "", "", ""]
        )

    " ".join(dfObj)
    
    
    codeblockind = "```"
    dfObj = f"{codeblockind}\n{Datum}\n\n{dfObj}\n{codeblockind}"
    print(dfObj)
    
    if "Empty" in dfObj:
        await ctx.send("Keinen Eintrag im Vertretungsplan gefunden.")
    elif vorherigerPlanHeute == dfObj:
        await ctx.send("Keinen neuen Eintrag gefunden")
    else:
        await ctx.send("Eintrag im Vertretungsplan gefunden! @everyone")
        await ctx.send(dfObj)
        vorherigerPlanHeute = dfObj

@bot.command()
async def VertretungsPlanHeute(ctx):

    global vorherigerPlanHeute
    
    await bot.wait_until_ready()
    
    await ctx.send("Abfrage für den Vertretungsplan von heute wird durchgeführt")
    await ctx.send("Bitte warten...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver.exe')

    driver.maximize_window()
    #launch URL
    driver.get("https://gaussschule-bs.de/iserv/infodisplay/file/186/infodisplay/0/Vertretungsplan/plaene/schueler_heute/subst_001.htm")

    driver.find_element_by_name("_username").send_keys(iservuser)
    driver.find_element_by_name("_password").send_keys(iservpw)
    driver.find_element_by_css_selector(".btn").click()

    BetroffeneKlassen = driver.find_element_by_css_selector("tr.info:nth-child(3) > td:nth-child(2)").text
    AbwesendeKlassen = driver.find_element_by_css_selector("tr.info:nth-child(4) > td:nth-child(2)").text
    Datum = driver.find_element_by_css_selector(".mon_title").text
    print (BetroffeneKlassen)


    if ("11A" in BetroffeneKlassen or "11A" in AbwesendeKlassen):
        print ("11A")


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

    if "Empty" in dfObj:
        await ctx.send("Keinen Eintrag im Vertretungsplan gefunden.")
    elif vorherigerPlanHeute == dfObj:
        await ctx.send("Keinen neuen Eintrag gefunden")
    else:
        await ctx.send("Eintrag im Vertretungsplan gefunden! @everyone")
        await ctx.send(dfObj)
        vorherigerPlanHeute = dfObj

@bot.command()
async def VertretungsPlanMorgen(ctx):

    global vorherigerPlanMorgen

    await bot.wait_until_ready()
    
    await ctx.send("Abfrage für den Vertretungsplan von morgen wird durchgeführt")
    await ctx.send("Bitte warten...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver.exe')

    driver.maximize_window()
    #launch URL
    driver.get("https://gaussschule-bs.de/iserv/infodisplay/file/186/infodisplay/0/Vertretungsplan/plaene/schueler_morgen/subst_001.htm")

    driver.find_element_by_name("_username").send_keys(iservuser)
    driver.find_element_by_name("_password").send_keys(iservpw)
    driver.find_element_by_css_selector(".btn").click()

    BetroffeneKlassen = driver.find_element_by_css_selector("tr.info:nth-child(3) > td:nth-child(2)").text
    AbwesendeKlassen = driver.find_element_by_css_selector("tr.info:nth-child(4) > td:nth-child(2)").text
    Datum = driver.find_element_by_css_selector(".mon_title").text
    print (BetroffeneKlassen)


    if ("11A" in BetroffeneKlassen or "11A" in AbwesendeKlassen):
        print ("11A")


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
        #index = ["", "", "", "", "", ""]
        )

    " ".join(dfObj)


    codeblockind = "```"
    dfObj = f"{codeblockind}\n{Datum}\n\n{dfObj}\n{codeblockind}"
    print(dfObj)
    
    if "Empty" in dfObj:
        await ctx.send("Keinen Eintrag im Vertretungsplan gefunden.")
    elif vorherigerPlanHeute == dfObj:
        await ctx.send("Keinen neuen Eintrag gefunden")
    else:
        await ctx.send("Eintrag im Vertretungsplan gefunden! @everyone")
        await ctx.send(dfObj)
        vorherigerPlanHeute = dfObj

@bot.event
async def on_ready():
    print("Ready")
    
    ctx = bot.get_channel(staticdiscordchannel)
    print(ctx)


    #initializing scheduler
    scheduler = AsyncIOScheduler()

    #sends "Your Message" at 12PM and 18PM (Local Time)
    scheduler.add_job(VertretungsPlanHeuteAuto, CronTrigger(hour="7", minute="0", second="0")) 
    scheduler.add_job(VertretungsPlanHeuteAuto, CronTrigger(hour="7", minute="40", second="0"))
    scheduler.add_job(VertretungsPlanMorgenAuto, CronTrigger(hour="22", minute="0", second="0"))
    #starting the scheduler
    scheduler.start()

bot.run(TOKEN)