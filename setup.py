from requests import get
from re import findall
import os
import glob
from rubika.client import Bot
import requests
from rubika.tools import Tools
from rubika.encryption import encryption
from gtts import gTTS
from mutagen.mp3 import MP3
import marshal
import time
import random
import urllib
import io

print ("♡ ایروسوروس ♡")
print ("<اوکی مای گاد>")

bot = Bot("AppName", auth="xysixrukqbdywdxdxrjzetgyxcdxxqez")
target ="g0B8UTM0023cd33fe872b04a080bbb0a"
delmess = ["دولی","کصکش","کون","کص","کیر" ,"خر","کستی","دول","گو","کس","کسکش","کوبص","@ ","https://rubika.ir/","https://rubika.ir/joing/","https://rubika.ir/joinc/BDGGEHCE0XOCHDQLRMCCDQGGYZXEZAZK"]

def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me"]
	for i in links:
		if i in msg:
			return True
	
# static variable
answered, sleeped, retries = [], False, {}

alerts, blacklist = [] , []

def alert(guid,user,link=False):
	alerts.append(guid)
	coun = int(alerts.count(guid))

	haslink = ""
	if link : haslink = "گزاشتن لینک در گروه ممنوع میباشد .\n\n"

	if coun == 1:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (1/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")
	elif coun == 2:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (2/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")

	elif coun == 3:
		blacklist.append(guid)
		bot.sendMessage(target, "🚫 کاربر [ @"+user+" ] \n (3/3) اخطار دریافت کرد ، بنابراین اکنون اخراج میشود .")
		bot.banGroupMember(target, guid)

retries = {}
sleeped = False
 
plus= True

while True:
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]
		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue
		
		open("id.db","w").write(str(messages[-1].get("message_id")))

		for msg in messages:
			if msg["type"]=="Text" and not msg.get("message_id") in answered:
				if not sleeped:
					if msg.get("text") == "آنلاینی" and msg.get("author_object_guid") in admins :
						bot.sendMessage(target, "آره عشقم فعالم😉❤", message_id=msg.get("message_id"))
						
						if hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg.get("message_id")])
							alert(guid,user,True)
						
					elif "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						
					elif msg.get("text").startswith("add:") :
						bot.invite(target, [bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]])
						bot.sendMessage(target, "کاربر مورد نظر افزوده شد!", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("ماشین حساب"):
						msd = msg.get("text")
						if plus == True:
							try:
								call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
								if call[1] == "+":
									am = float(call[0]) + float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
									plus = False
							
								elif call[1] == "-":
									am = float(call[0]) - float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							
								elif call[1] == "*":
									am = float(call[0]) * float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							
								elif call[1] == "/":
									am = float(call[0]) / float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							except IndexError:
								bot.sendMessage(target, "دستور رو اشتباه وارد کردی😂🤦‍♂️" ,message_id=msg.get("message_id"))
						plus= True

					elif msg.get("text").startswith("دعوت") :
						bot.sendMessage(bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"], "https://rubika.ir/joing/BFCJDDFA0HOZPHICIIQLADWYCOAAIAJJ\nسلام کاربر گرامی شما به گروه ما دعوت شدید❤️☘\nراستی قوانین گپ را رعایت کن✅\nفحش=ریمو❌\nناسزاگویی=ریمو❌\nشاخ=ریمو❌\nاسپم=ریمو❌\nکد هنگی=ریمو❌\nممنون میشیم وارد گروهمون شوید❤️\nعشــــــــــــــــــــــــــــــــــــــقی❤️💐"+""+" ".join(msg.get("text").split(" ")[2:]))
						bot.sendMessage(target, "✅", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("!send:") :
						bot.sendMessage(bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"], "شما یک پیام ناشناس دارید:\n"+" ".join(msg.get("text").split(" ")[2:]))
						bot.sendMessage(target, "پیام ناشناستو ارسال کردم😉👌", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("هلیکوپتر") :
						bot.sendMessage(target, "▂▄▄▓▄▄▂\n◢◤ █▀▀████▄▄▄◢◤╬\n█▄ ██▄ ███▀▀▀▀▀▀\n◥█████◤\n══╩══╩═\nاینم از هلیکوپتر😅", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "خرگوش":
						bot.sendMessage(target, "∩_∩ \n\n '（„• ֊ •„) ' \n\n •━━∪∪━━• \n\n اینم از خرگوش🐰🥕", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "میمون":
						bot.sendMessage(target, ".⠀╱▔▔▔▔▔╲ \n⠀╱⠀⠀╱▔╲╲╲ \n╱⠀⠀╱━╱▔▔▔▔▔╲━╮⠀⠀ \n▏⠀▕┃▕╱▔╲╱▔╲▕╮┃⠀⠀ \n▏⠀▕╰━▏▊▕▕▋▕▕━╯⠀⠀ \n╲⠀⠀╲╱▔╭╮▔▔┳╲╲⠀⠀⠀ \n⠀╲⠀⠀▏╭━━━━╯▕▕⠀⠀⠀ \n⠀⠀╲⠀╲▂▂▂▂▂▂╱╱⠀⠀⠀ \n⠀⠀⠀⠀▏⠀⠀⠀⠀⠀⠀⠀⠀⠀╲⠀ \n⠀⠀⠀⠀▏⠀⠀⠀⠀⠀⠀▕╲⠀⠀╲ \n⠀╱▔╲▏⠀⠀⠀⠀⠀⠀▕╱▔╲▕ \n⠀▏ ⠀⠀⠀╰⠀⠀⠀⠀╯⠀⠀⠀▕▕ \n⠀╲⠀⠀⠀╲⠀⠀⠀⠀╱⠀⠀⠀╱⠀╲ \n⠀⠀╲⠀⠀▕▔▔▔▔▏⠀⠀╱╲╲╲▏ \n⠀╱▔⠀⠀▕⠀⠀⠀⠀▏⠀⠀▔╲▔▔ \n⠀╲▂▂▂╱⠀⠀⠀⠀╲▂▂▂╱ \n اینم از میمون 😂🤍", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "شیخ":
						bot.sendMessage(target, "/ْ ْ ْْْ ْ ْ ْ ْ ْْ ْ ْ ْ ْ ْ ْ ْ ْْ ْ ْ ْ ْ ْ ْ \            \n\____________/      \n     ¦¦l!  ْ ْo ْ ْْْْْo) \n   ( c          ِ ٍٍٍٍ_) \n     l    //ً_ًًً_ً_) \n      )   \\\\\\          \n   ِ/َِِِِِ َِ َِ َِ َِ َِ َِ ِ ِ\\\\\ \n/         _ْ_ْْ\______ \n|        (____________(|||) \nl              ¦    l            /   \ \nl              ¦    l       👳شیخ عرب \n|        /    ¦    |          ([[ْ_ْ_ْ]_) \n|      /      ¦    | \n|              ¦    | \nاینم از شیخ😂🤍", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "کامیون":
						bot.sendMessage(target, "┈╱▔▔▔▔▔▔▔▔╲┈♥┈♥┈\n ╱▔▔▔▔▔▔▔▔╲╱▏┈♥┈\n ▏┳╱╭╮┓┏┏ ┓▕╱▔▔╲┈\n ▏┃╱┃┃┃┃┣▏▕▔▔╲╱▏\n ▏┻┛╰╯╰╯┗┛▕▕▉▕╱╲ \n ▇▇▇▇▇▇▇▇▇▇▔▔▔╲▕ \n ▇▇╱▔╲▇▇▇▇▇╱▔╲▕╱ \n ┈┈╲▂╱┈┈┈┈┈╲▂╱▔┈👀💜 \n اینم از کامیون😂🤍", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "آیفون":
						bot.sendMessage(target, "🎛⬜️⬜️ \n ⬜️⬜️⬜️ \n ⬜️🍎⬜️ \n ⬜️⬜️⬜️ \n ⬜️⬜️⬜️ \n اینم از آیفون😂🤍", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "همین":
						bot.sendMessage(target, "کی  رم برات کرده کمین😂❤️", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "میگما":
						bot.sendMessage(target, "دولا شدی دیدما \n\n ندی ب عاقاد میگما😹🎈", message_id=msg.get("message_id"))	

					elif msg.get("text") == "رفتى؟":
						bot.sendMessage(target, "به كي.ر اكبر نفتى😂🖕🏿\n\n ميموندى باهاش ور ميرفتى😂🤟", message_id=msg.get("message_id"))	

					elif msg.get("text") == "خانوم ميشه بپرم تو كيفتون":
						bot.sendMessage(target, "نه خودكار توشه ميره تو ك‍ونتون.❤️😂", message_id=msg.get("message_id"))	

					elif msg.get("text") == "چکار کنم":
						bot.sendMessage(target, "بکش پایین نگا کنم ??", message_id=msg.get("message_id"))	

					elif msg.get("text") == "مث اسانسور میمونی":
						bot.sendMessage(target, "جدیدن همه دکمتو میزنن!😹🖕💯", message_id=msg.get("message_id"))	

					elif msg.get("text") == "بازی":
						bot.sendMessage(target, "لیست بازی اسم فامیل: \n\n😂〰〰〰〰〰〰〰〰〰〰〰😂 \n\n↩️برای راهنمایی:  \n\n«دوستان اول اسم فامیل جلو اش.» \n\n🌸➖➖➖➖➖➖➖➖➖➖➖🌸 \n\nالف ، ب ، پ ، ت ، ث ، ج ، چ ، \n\nح ، خ ، د ، ذ ، ر ، \n\nز ،‌ ژ ، س ، ش ، ص ، \n\nض ، ط ، ظ ، ع ، غ ، ف ،\n\n ، ک ، گ ، ل ، م ، ن ، و ،  \n\n🌸➖➖➖➖➖➖➖➖➖➖➖ \n\n♻️مثال: اسم فامیل الف \n\nلیست: بازی براتون میفرسته➕⚪️ \n\n🦋〰➖〰➖〰🐣〰➖〰➖〰🦋", message_id=msg.get("message_id"))	

					elif msg.get("text") == "اسم فامیل الف":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..الف. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))	
						
					elif msg.get("text") == "اسم فامیل ب":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ب. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))

					elif msg.get("text") == "اسم فامیل پ":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗????›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗??🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..پ. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ت":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ت. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ث":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ث. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ج":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ج. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل چ":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..چ. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل خ":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..خ. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))

					elif msg.get("text") == "اسم فامیل ح":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ح. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل د":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..د. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ذ":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ذ. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ر":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ر. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "لیست ز":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ز. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ژ":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ژ. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل س":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹??👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..س. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ش":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ش. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ص":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ص. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ض":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ض. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ط":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ط. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼??›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ظ":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ظ. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "اسم فامیل ع":
						bot.sendMessage(target, "‹💕📋◖اسـم◗??📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ع. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											

					elif msg.get("text") == "اسم فامیل غ":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..غ. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											
						
					elif msg.get("text") == "اسم فامیل ف":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ف. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											
						
					elif msg.get("text") == "اسم فامیل ق":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ق. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											
						
					elif msg.get("text") == "اسم فامیل ک":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ک. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											
						
					elif msg.get("text") == "اسم فامیل گ":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..گ. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											
						
					elif msg.get("text") == "اسم فامیل ل":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ل. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											
						
					elif msg.get("text") == "اسم فامیل م":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..م. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											
						
					elif msg.get("text") == "اسم فامیل و":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..و. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											
						
					elif msg.get("text") == "اسم فامیل ن":
						bot.sendMessage(target, "‹💕📋◖اسـم◗💕📋›\n\n‹🌸👼🏻◖فـامیل◗🌸👼🏻›\n\n‹🌻🍓◖شهـر◗🍓🌻›\n\n‹💕📋◖کشـور◗💕📋›\n\n‹🌸👼🏻◖میـوه◗🌸👼🏻›\n\n‹🌻🍓◖غـذا◗🍓🌻›\n\n‹💕📋◖رنـگ◗💕📋›\n\n‹🌸👼🏻◖حیـوان◗🌸👼🏻›\n\n‹🌻🍓◖اشیا◗🍓🌻›\n\n‹💕📋◖بـا حـرف..ن. ◗💕📋›\n\n‹🌸👼🏻◖اسـمـت نـایصم؟ ◗🌸👼🏻›\n\n‹🌻🍓◖@lo_amir_org◗🍓🌻›", message_id=msg.get("message_id"))											
						
					elif msg.get("text") == "فهمیدم":
						bot.sendMessage(target, "نمیفهمیدی خودکشی میکردم 😐", message_id=msg.get("message_id"))	

					elif msg.get("text") == "س":
						bot.sendMessage(target, "س🗿", message_id=msg.get("message_id"))											

					elif msg.get("text") == "رباط":
						bot.sendMessage(target, "جونم😁", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "باط":
						bot.sendMessage(target, "درست صدام کن (◔‿◔) ", message_id=msg.get("message_id"))

					elif msg.get("text") == "پیشی":
						bot.sendMessage(target, "ها چی میگی ", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "خوبم مرسی":
						bot.sendMessage(target, "🤍♥️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "چیه":
						bot.sendMessage(target, "هیچی!😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "عجب":
						bot.sendMessage(target, "مشت رجب...!", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "چه خبر":
						bot.sendMessage(target, "ســلامـتیت😍♥", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "چخبر":
						bot.sendMessage(target, "ســلامـتیت😍♥", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "خوبی":
						bot.sendMessage(target, "ممنون ت خبی 🙂", message_id=msg.get("message_id"))

					elif msg.get("text") == "استغفرالله":
						bot.sendMessage(target, "توبه توبه", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "سبحان الله":
						bot.sendMessage(target, "😱😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "😂":
						bot.sendMessage(target, "نخند مسواک تحریم میشه😤", message_id=msg.get("message_id"))
							
					elif msg.get("text") == "😐😂":
						bot.sendMessage(target, "جوننننن تو فقط بخند🤤💋", message_id=msg.get("message_id"))

					elif msg.get("text") == "😂😐":
						bot.sendMessage(target, "ها چیه ؟¿", message_id=msg.get("message_id"))

					elif msg.get("text") == "اسکل":
						bot.sendMessage(target, "بچه بیا پایین سرمون درد گرفت اه", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "زشت":
						bot.sendMessage(target, "جای تو رو تنگ کردم 😒", message_id=msg.get("message_id"))
												
					elif msg.get("text") == "سگ":
						bot.sendMessage(target, "فش نده ریم میشی", message_id=msg.get("message_id"))

					elif msg.get("text") == "گوه":
						bot.sendMessage(target, "بخور", message_id=msg.get("message_id"))

					elif msg.get("text") == "تست":
						bot.sendMessage(target, "هنوز زنده ام", message_id=msg.get("message_id"))

					elif msg.get("text") == "سوری":
						bot.sendMessage(target, "چیکارم داری؟ 😑", message_id=msg.get("message_id"))

					elif msg.get("text") == "رلم میشی":
						bot.sendMessage(target, "نه 🤨", message_id=msg.get("message_id"))

					elif msg.get("text") == "کس میقام":
						bot.sendMessage(target, "اخه ذوقم کور شده.از خود واقعیم دارم فاصله میگیرم.😶", message_id=msg.get("message_id"))

					elif msg.get("text") == "اه":
						bot.sendMessage(target, "برو توودستشویی بگو", message_id=msg.get("message_id"))

					elif msg.get("text") == "خبی":
						bot.sendMessage(target, "معلومه که خوبم فدات بشم من 😇", message_id=msg.get("message_id"))

					elif msg.get("text") == "سلام":
						bot.sendMessage(target, "های جیگر", message_id=msg.get("message_id"))

					elif msg.get("text") == "شکر":
						bot.sendMessage(target, "الحمدالله", message_id=msg.get("message_id"))

					elif msg.get("text") == "عشق منی":
						bot.sendMessage(target, "تو بیشتر عزیزم😍", message_id=msg.get("message_id"))

					elif msg.get("text") == "سوری چند سالته":
						bot.sendMessage(target, "25", message_id=msg.get("message_id"))

					elif msg.get("text") == "تو که میگی ملکه ای😻":
						bot.sendMessage(target, "چرا دنبال مشتری سر فلکه ای😂❤️", message_id=msg.get("message_id"))

					elif msg.get("text") == "نخیر":
						bot.sendMessage(target, "نامرد", message_id=msg.get("message_id"))

					elif msg.get("text") == "چیشد":
						bot.sendMessage(target, "هعب😐💔،گوز هوا شد ", message_id=msg.get("message_id"))

					elif msg.get("text") == "اسمت چیه":
						bot.sendMessage(target, "𝚛𝚘𝚋𝚘🥴", message_id=msg.get("message_id"))

					elif msg.get("text") == "اره.":
						bot.sendMessage(target, "دقیقاحق باشماهست قربان", message_id=msg.get("message_id"))

					elif msg.get("text") == "ن":
						bot.sendMessage(target, "نکمه😕", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "بات":
						bot.sendMessage(target, "بفرمایین 😊", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "ربات":
						bot.sendMessage(target, "جــونــم عــشــقــم😁💋", message_id=msg.get("message_id"))

					elif msg.get("text") == "اوکی بای":
						bot.sendMessage(target, "بشین سرش بخور چای😂☕", message_id=msg.get("message_id"))

					elif msg.get("text") == "لا پای بعضیا شده دروازه😻":
						bot.sendMessage(target, "با ی اشاره میگن بفرما در بازه😂❤", message_id=msg.get("message_id"))

					elif msg.get("text") == ".":
						bot.sendMessage(target, "روبیکا ریده؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "اوکی":
						bot.sendMessage(target, "👌😉", message_id=msg.get("message_id"))

					elif msg.get("text") == "چند سالته":
						bot.sendMessage(target, "25", message_id=msg.get("message_id"))

					elif msg.get("text") == "سوری خر":
						bot.sendMessage(target, "عمته", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "😐":
						bot.sendMessage(target, "پوکر نده پوکر میدم😐", message_id=msg.get("message_id"))

					elif msg.get("text") == "💔":
						bot.sendMessage(target, "چی شده عشقم 💔🥀", message_id=msg.get("message_id"))

					elif msg.get("text") == "تنهام":
						bot.sendMessage(target, "نمیدونم والا ☹️", message_id=msg.get("message_id"))

					elif msg.get("text") == "چی":
						bot.sendMessage(target, "بادام چی😗", message_id=msg.get("message_id"))

					elif msg.get("text") == "سید":
						bot.sendMessage(target, "جان سید ،سید فدات شه😃", message_id=msg.get("message_id"))

					elif msg.get("text") == "س":
						bot.sendMessage(target, "سلام خوبی", message_id=msg.get("message_id"))

					elif msg.get("text") == "ها":
						bot.sendMessage(target, "مرگِ ها 😐", message_id=msg.get("message_id"))

					elif msg.get("text") == "بای":
						bot.sendMessage(target, "فردا بخور های بای", message_id=msg.get("message_id"))

					elif msg.get("text") == "اها":
						bot.sendMessage(target, "خوبه فهمیدی داشتم نا امید میشدم😏", message_id=msg.get("message_id"))

					elif msg.get("text") == "خر":
						bot.sendMessage(target, "ادبت کو گوساله🗿", message_id=msg.get("message_id"))

					elif msg.get("text") == "چطوری":
						bot.sendMessage(target, "متوری", message_id=msg.get("message_id"))

					elif msg.get("text") == "هیچی":
						bot.sendMessage(target, "مسخره کردی😒", message_id=msg.get("message_id"))

					elif msg.get("text") == "معلون":
						bot.sendMessage(target, "تو معلولی🗿", message_id=msg.get("message_id"))

					elif msg.get("text") == "عشقم":
						bot.sendMessage(target, "عشقت لب میخاست بش ندادی عبضی🥲", message_id=msg.get("message_id"))

					elif msg.get("text") == "پی چک":
						bot.sendMessage(target, "با منی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "هعب😐💔":
						bot.sendMessage(target, "چیشد عشقم 💔", message_id=msg.get("message_id"))

					elif msg.get("text") == "خش😂":
						bot.sendMessage(target, "خوبی نفش 😂", message_id=msg.get("message_id"))

					elif msg.get("text") == "آها":
						bot.sendMessage(target, "خوبه فهمیدی داشتم نا امید میشدم😏", message_id=msg.get("message_id"))

					elif msg.get("text") == "چشم":
						bot.sendMessage(target, "بوس رو چشت", message_id=msg.get("message_id"))

					elif msg.get("text") == "خیلی خری":
						bot.sendMessage(target, "خریت از خودتونه 😁", message_id=msg.get("message_id"))

					elif msg.get("text") == "عا":
						bot.sendMessage(target, "باز چه مرگته؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "نت ریده":
						bot.sendMessage(target, "به درک🗿", message_id=msg.get("message_id"))

					elif msg.get("text") == "جوون":
						bot.sendMessage(target, "فنجون", message_id=msg.get("message_id"))

					elif msg.get("text") == "جون":
						bot.sendMessage(target, "بادمجون این سه تا رو نرنجون", message_id=msg.get("message_id"))

					elif msg.get("text") == "چرا تحول نمیگیری":
						bot.sendMessage(target, "عزیزم مگه من سفارشت دادم که حالا بخام تحولیت بگرم ", message_id=msg.get("message_id"))

					elif msg.get("text") == "خوبم تو خوبی":
						bot.sendMessage(target, "اره ممنون خوبم", message_id=msg.get("message_id"))

					elif msg.get("text") == "برو بابا":
						bot.sendMessage(target, "نگو بابا،احساس مسئولیت میکنم", message_id=msg.get("message_id"))

					elif msg.get("text") == "گلابی":
						bot.sendMessage(target, "مامور مسترابی", message_id=msg.get("message_id"))

					elif msg.get("text") == "الو":
						bot.sendMessage(target, "اَی خِداااااا چته چکارم داری نمیزاری بخوابم", message_id=msg.get("message_id"))

					elif msg.get("text") == "امیر":
						bot.sendMessage(target, "بابا بیا این کارت داره", message_id=msg.get("message_id"))

					elif msg.get("text") == "اصل":
						bot.sendMessage(target, "ربات هوشمند سخنگو هستم🤖", message_id=msg.get("message_id"))

					elif msg.get("text") == "والا":
						bot.sendMessage(target, "بمولا", message_id=msg.get("message_id"))

					elif msg.get("text") == "خدا وکیلی":
						bot.sendMessage(target, "خدا الان وکیل نیست قاضی", message_id=msg.get("message_id"))

					elif msg.get("text") == "زر نزن":
						bot.sendMessage(target, "تو بزن پولشو بگیر", message_id=msg.get("message_id"))

					elif msg.get("text") == "بیشور":
						bot.sendMessage(target, "ک.و.ن.تو بشور 🤣👍", message_id=msg.get("message_id"))

					elif msg.get("text") == "نوب":
						bot.sendMessage(target, "میدونی چیه ؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "لا پای بعضیا شده دروازه":
						bot.sendMessage(target, "با ی اشاره میگن بفرما در بازه😂❤", message_id=msg.get("message_id"))

					elif msg.get("text") == "سید هوشمند":
						bot.sendMessage(target, "اسم شوهرمو به زبونت نیار 🗿", message_id=msg.get("message_id"))

					elif msg.get("text") == "خش":
						bot.sendMessage(target, "الحمدالله", message_id=msg.get("message_id"))

					elif msg.get("text") == "جــــر نخـوری😂🌹":
						bot.sendMessage(target, "تیکه بنداز بهش 🗿", message_id=msg.get("message_id"))

					elif msg.get("text") == "سلم":
						bot.sendMessage(target, "منم یاد بگیرم اینجوری سلام کنم😐", message_id=msg.get("message_id"))

					elif msg.get("text") == "جوووون":
						bot.sendMessage(target, "بادمجون سه تاشو بگیر نرنجون", message_id=msg.get("message_id"))

					elif msg.get("text") == "فرانسه":
						bot.sendMessage(target, "جفت ممه هات بالانسع*-*💦😂", message_id=msg.get("message_id"))

					elif msg.get("text") == "خیخی":
						bot.sendMessage(target, "ممد بیا بببن این چی میگه", message_id=msg.get("message_id"))

					elif msg.get("text") == "چجوری":
						bot.sendMessage(target, "اینجوری همینجوری ", message_id=msg.get("message_id"))

					elif msg.get("text") == "پیشی بات":
						bot.sendMessage(target, "چیه کره خر", message_id=msg.get("message_id"))

					elif msg.get("text") == "باش":
						bot.sendMessage(target, "افـرین😊", message_id=msg.get("message_id"))

					elif msg.get("text") == "افرین":
						bot.sendMessage(target, "خواهش میکنم", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "قیز":
						bot.sendMessage(target, "قیز.... گل منی ج ز🤣", message_id=msg.get("message_id"))

					elif msg.get("text") == "عمته":
						bot.sendMessage(target, "چیکار عمش داری عمش مال منه", message_id=msg.get("message_id"))

					elif msg.get("text") == "دخترم":
						bot.sendMessage(target, "با من رل میزنی🤱", message_id=msg.get("message_id"))

					elif msg.get("text") == "پسرم":
						bot.sendMessage(target, "با من رل میزنی👻" , message_id=msg.get("message_id"))

					elif msg.get("text") == "نه باو":
						bot.sendMessage(target, "گاو🐮", message_id=msg.get("message_id"))

					elif msg.get("text") == "کیبورد":
						bot.sendMessage(target, "شما از کیبورد استفاده میکنید من از مغزم", message_id=msg.get("message_id"))

					elif msg.get("text") == "کسشعر":
						bot.sendMessage(target, "کـص اگه شعر داشت کی.ر من گیتار میزد", message_id=msg.get("message_id"))

					elif msg.get("text") == "شاخ نشو":
						bot.sendMessage(target, "شاخ نیستم چون رباتم", message_id=msg.get("message_id"))

					elif msg.get("text") == "نمال":
						bot.sendMessage(target, "بیا چیزمو بمال", message_id=msg.get("message_id"))

					elif msg.get("text") == "جرعت":
						bot.sendMessage(target, "اگه جرعت داری بگو گوه خوردم", message_id=msg.get("message_id"))

					elif msg.get("text") == "حقیقت":
						bot.sendMessage(target, "چند بار جق زدی؟", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "جرعت یا حقیقت":
						bot.sendMessage(target, "جرعت", message_id=msg.get("message_id"))

					elif msg.get("text") == "گوه خوردم":
						bot.sendMessage(target, "نوش جونت", message_id=msg.get("message_id"))

					elif msg.get("text") == "تایپری":
						bot.sendMessage(target, "اره من تایپر لشم", message_id=msg.get("message_id"))

					elif msg.get("text") == "گودرت":
						bot.sendMessage(target, "اره داش من گدرتمندم", message_id=msg.get("message_id"))

					elif msg.get("text") == "کصـ":
						bot.sendMessage(target, "خجالت بکش از سبیلات😂", message_id=msg.get("message_id"))

					elif msg.get("text") == "دانلود سطح":
						bot.sendMessage(target, "فرایند دانلود سطح برای این نوب آغاز شد.⇧⇧⇧████████▓▓▓70درصد❌ارور 404 این فرد یک نوب خالص است.!!!!❌", message_id=msg.get("message_id"))

					elif msg.get("text") == "حاجی":
						bot.sendMessage(target, "جانم حا‌جی قربونت😉", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "بگو":
						bot.sendMessage(target, "سام بادی گیو می هایااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااهههههههههههههههههههههه😐", message_id=msg.get("message_id"))

					elif msg.get("text") == "بربری":
						bot.sendMessage(target, "سرشو دیدی در نری😂❤️", message_id=msg.get("message_id"))

					elif msg.get("text") == "عزیزم":
						bot.sendMessage(target, "😐جون", message_id=msg.get("message_id"))

					elif msg.get("text") == "اطلاعیه":
						bot.sendMessage(target, "پس از مرگ کیان !!! مختار مجبور به متحد شدن با جومونگ شد 🙂💔", message_id=msg.get("message_id"))

					elif msg.get("text") == "😐😐":
						bot.sendMessage(target, "دردت چیست", message_id=msg.get("message_id"))

					elif msg.get("text") == "گشنمه":
						bot.sendMessage(target, "بیا اینو بخور😐", message_id=msg.get("message_id"))

					elif msg.get("text") == "هک":
						bot.sendMessage(target, "😂قدیمی شده", message_id=msg.get("message_id"))

					elif msg.get("text") == "بوس":
						bot.sendMessage(target, "💋لب میدم", message_id=msg.get("message_id"))

					elif msg.get("text") == "چایی":
						bot.sendMessage(target, "بفرما چایی😝☕️", message_id=msg.get("message_id"))

					elif msg.get("text") == "اومدم":
						bot.sendMessage(target, "خوش اومدی 💩", message_id=msg.get("message_id"))

					elif msg.get("text") == "احمق":
						bot.sendMessage(target, "حمق هفت جدته😐💔", message_id=msg.get("message_id"))

					elif msg.get("text") == "ربات کیه":
						bot.sendMessage(target, "امیر", message_id=msg.get("message_id"))

					elif msg.get("text") == "جنده":
						bot.sendMessage(target, "عمتـه", message_id=msg.get("message_id"))

					elif msg.get("text") == "خواهشـ🙇🏻🌹":
						bot.sendMessage(target, "اول یکم بمالشـ😹🙌🏿", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "صگ":
						bot.sendMessage(target, "یعنی روبیکا صگ داره", message_id=msg.get("message_id"))

					elif msg.get("text") == "مست":
						bot.sendMessage(target, "با اب میوه مست کردی", message_id=msg.get("message_id"))

					elif msg.get("text") == "حیوون مورد علاقت!؟":
						bot.sendMessage(target, "تُو =)😹🖕🏽", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "ممه":
						bot.sendMessage(target, "ندارم", message_id=msg.get("message_id"))

					elif msg.get("text") == "درد":
						bot.sendMessage(target, "تو جونت 😘💋", message_id=msg.get("message_id"))

					elif msg.get("text") == "خوبی عزیزم":
						bot.sendMessage(target, "مرسی تو خوبی قشنگم؟ اصل میدی؟🤓🫂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "خوبید":
						bot.sendMessage(target, "مرسی ماخوبیم توخوبی", message_id=msg.get("message_id"))

					elif msg.get("text") == "چتوری":
						bot.sendMessage(target, "مثل پلو تو دوری 😐چقدر زر میزنی بچه", message_id=msg.get("message_id"))

					elif msg.get("text") == "جق":
						bot.sendMessage(target, "در جوانی تا توانی منت کص‌ را نکش دستت را حلقه کن بر قامت کیرت بکش", message_id=msg.get("message_id"))

					elif msg.get("text") == "ممه میقام":
						bot.sendMessage(target, "بیا میمه ۸۵ بقول🙂🍼", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "کصکش":
						bot.sendMessage(target, "بشین سرش کیسه بکش", message_id=msg.get("message_id"))

					elif msg.get("text") == "😂😂":
						bot.sendMessage(target, "نخند زشت میشی", message_id=msg.get("message_id"))

					elif msg.get("text") == "نوبی":
						bot.sendMessage(target, "یک عدد نوب یافت شد❌\nدرحال پاکسازی ویروس نوب بودن😐\n█▓▓▓▓▓▓▓▓▓10درصد \n██▓▓▓▓▓▓▓▓20درصد\n███▓▓▓▓▓▓▓30درصد\n████▓▓▓▓▓▓40درصد\n█████▓▓▓▓▓50درصد\n██████▓▓▓▓60درصد\n███████▓▓▓70درصد\n████████▓▓80درصد\n█████████▓90درصد\n██████████ 100 درصد✅\nپاکسازی رو به اتمام است...✅لطفا صبور باشید🗿\nویروس نوب از روی زمین با موفقیت پاک شد.!✅🗿\n", message_id=msg.get("message_id"))

					elif msg.get("text") == "مدی":
						bot.sendMessage(target, "رل میخاد", message_id=msg.get("message_id"))

					elif msg.get("text") == "دیوث":
						bot.sendMessage(target, "کم گوه بخور خودتی🙂💔", message_id=msg.get("message_id"))

					elif msg.get("text") == "اره":
						bot.sendMessage(target, ":-/:-/", message_id=msg.get("message_id"))

					elif msg.get("text") == "نه":
						bot.sendMessage(target, "ای نــکــمــه بــگــیــری😹💔", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍑":
						bot.sendMessage(target, "هلو میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍎":
						bot.sendMessage(target, "سیب میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍒":
						bot.sendMessage(target, "گیلاس میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍌":
						bot.sendMessage(target, "موز میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥒":
						bot.sendMessage(target, "خیار میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍓":
						bot.sendMessage(target, "توت فرنگی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍉":
						bot.sendMessage(target, "هندوانه میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍊":
						bot.sendMessage(target, " نارنجی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥭":
						bot.sendMessage(target, "انبه میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍍":
						bot.sendMessage(target, "آناناس میقولی", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍐":
						bot.sendMessage(target, "گلابی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍇":
						bot.sendMessage(target, "انگور میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥕":
						bot.sendMessage(target, "هویج میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍋":
						bot.sendMessage(target, "لیمو ترش میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍅":
						bot.sendMessage(target, "گوجه فرنگی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🌶":
						bot.sendMessage(target, "فلفل قرمز میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🌽":
						bot.sendMessage(target, "ذرت میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🧄":
						bot.sendMessage(target, "سیر میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥝":
						bot.sendMessage(target, "کیوی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥬":
						bot.sendMessage(target, "برگ سبز میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🫒":
						bot.sendMessage(target, "زیتون میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍆":
						bot.sendMessage(target, "بادمجان میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥦":
						bot.sendMessage(target, "بروکلی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥑":
						bot.sendMessage(target, "آووکادو میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🫑":
						bot.sendMessage(target, "فلفل دلمه میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🧅":
						bot.sendMessage(target, "پیاز میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🌰":
						bot.sendMessage(target, "فندق میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍎":
						bot.sendMessage(target, "سیب قرمز میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥔":
						bot.sendMessage(target, "سیب زمینی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥥":
						bot.sendMessage(target, "نارگیل میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍈":
						bot.sendMessage(target, "طالبی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🫐":
						bot.sendMessage(target, "توت آبی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥜":
						bot.sendMessage(target, "بادام میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍄":
						bot.sendMessage(target, "قارچ میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍳":
						bot.sendMessage(target, "نیمرو عسلی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥚":
						bot.sendMessage(target, "تخم مرغ میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🧀":
						bot.sendMessage(target, "قاچ پنیر میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥨":
						bot.sendMessage(target, "چوب شور میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥖":
						bot.sendMessage(target, "نان باگت میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍞":
						bot.sendMessage(target, "نان میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥐":
						bot.sendMessage(target, "کرواسان میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥓":
						bot.sendMessage(target, "بیکن میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥞":
						bot.sendMessage(target, "پنکیک میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍟":
						bot.sendMessage(target, "سیب زمینی سرخ کردنی میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍔":
						bot.sendMessage(target, "همبرگر میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🌭":
						bot.sendMessage(target, "هات داگ میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍖":
						bot.sendMessage(target, "گوشت با استخوان میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍗":
						bot.sendMessage(target, "ران ماکیان میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍕":
						bot.sendMessage(target, "پیتزا میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥩":
						bot.sendMessage(target, "برش گوشت میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🌮":
						bot.sendMessage(target, "تاکو میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🌯":
						bot.sendMessage(target, "بوریتو میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥪":
						bot.sendMessage(target, "ساندویچ میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥫":
						bot.sendMessage(target, "غذای کنسرو شده میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🧇":
						bot.sendMessage(target, "وافل میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🥙":
						bot.sendMessage(target, "لقمه میقولی؟", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🧂":
						bot.sendMessage(target, "نمک میقولی؟", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🧆":
						bot.sendMessage(target, "فلافل میقولی؟", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🥘":
						bot.sendMessage(target, "ماهیتابه غذا میقولی؟", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🫕":
						bot.sendMessage(target, "فوندو میقولی؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🫔":
						bot.sendMessage(target, "تامال میقولی؟", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🧈":
						bot.sendMessage(target, "کره میقولی؟", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇩🇪":
						bot.sendMessage(target, "کشور آلمان از رنگ های مشکی، قرمز و زرد استفاده کرده است. سمبل هر یک از رنگ ها به ترتیب زیر است:رنگ های مشکی و زرد نشانگر امپراطوری مقدس در حدود قرن دهم می باشد. امپراطوری اتریشی هم از رنگ های مشکی، قرمز و زرد استفاده کرده است. در طول جنگ های ناپلئونی رنگ های مشکی، قرمز و زرد در لباس فرم سربازان آلمانی قرار داشت. سمبل رنگ های استفاده شده را می توان در یک جمله قرار داد: بیرون از سیاهی بندگی، از جنگ های خونین به سوی نور طلایی آزادی.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇦🇫":
						bot.sendMessage(target, "پرچم افغانستان که به رسمیت بین‌المللی شناخته شده، از سه رنگ سیاه، سرخ و سبز با نشان ملی سفید رنگ استفاده می‌کند. رنگ سیاه نشان‌دهنده مشکلات تاریخی قرن  نوزدهم میلادی به عنوان یک دولت تحت‌الحمایه بریتانیا است، رنگ سرخ نشان‌دهنده  خون کسانی است که برای استقلال مبارزه کردند (به‌طور خاص پیمان صلح افغانستان و انگلستان در ۱۹۱۹) و رنگ سبز نشان‌دهنده  امید و رفاه برای آینده است.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇺🇸":
						bot.sendMessage(target, "پرچم آمریکا، پرچم رسمی دولت فدرال ایالات متحده آمریکا می باشد. پرچم این کشور در سال ۱۷۷۵ طراحی شده و تا کنون ۲۶ بار دچار تغییر و تحول شده است. در ابتدا پرچم آمریکا مشابه پرچم کمپانی هند شرقی بریتانیا بوده است. پرچم کنونی آمریکا دارای ۱۳۳ خط سفید و قرمز و ۵۰ ستاره می باشد. ۱۳ خط نشان گر ۱۳ مستعمره ای است در ابتدا برای اولین بار بر علیه بریتانیا قیام کرده اند و باعث استقلال آمریکا شده اند. ۵۰ ستاره سفید موجود در زمینه آبی پرچم نشانگر ۵۰ ایالتی است که امروزه عضو ایالت متحده آمریکا هستند. البته هر یک از ۵۰ ایالت بطور جداگانه دارای پرچمی مخصوص به خود هستند.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇦🇿":
						bot.sendMessage(target, "آذربایجان یا همان جمهوری آذربایجان می پردازیم. آذربایجان از سه رنگ آبی، قرمز و سبز استفاده کرده است. آبی سمبل ترک ها، سبز سمبل دین اسلام و قرمز به نشانه ی پیشرفت می باشد. ستاره ی ۸ پَر نیز ۸ شاخه ی مردم ترک را نشان می دهد.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇮🇷":
						bot.sendMessage(target, " پرچم ایران در طول سلسله ها و حکومت های مختلف تغییرات بسیاری کرده است. پرچم کشورمان در زمان قاجار به سه رنگ سفیده، قرمز و سبز در آمد. امروزه پرچم ایران با همان ۳ رنگ و واژه ی مبارک الله اکبر در مرکز پرچم و همچنین ۲۲ الله اکبر دیگر در حاشیه ی رنگ های قرمز و سبز دیده می شود. این پرچم نمادی از ۲۲ بهمن ۵۷ و انقلاب اسلامی ایران است.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇹🇷":
						bot.sendMessage(target, "پرچم قرمز رنگ ترکیه ترکیبی از نماد اسلام یعنی ماه و ستاره و همچنین نمادی از پاکی مردم ترکیه است. البته در این پرچم همچنان نشان هایی از تاریخ پر فراز و نشیب ترکیه نیز دارد.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇨🇳":
						bot.sendMessage(target, "پرچم چین بسیار ساده است و نشانی از سیستم دولتی کمونیستی این کشور است. قرمز نماد کمونیست و ۵ ستاره یآن نماد اتحادی است که مردم چین است و ستاره ی بزرگ تر نیز رهبری این کشور را نشان می دهد.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🏳‍🌈":
						bot.sendMessage(target, "درسته حرامه دیگه چیزی نپرس نقطه چین🤐", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇸🇦":
						bot.sendMessage(target, "پرچم کشور عربستان در سال ۱۹۷۳ برای اولین بار یه رسمیت شناخته شده است. پرچم این کشور دارای رنگ زمینه سبز بوده است. رنگ سبزی که به عنوان رنگ سنتی اسلامی رنگ مورد علاقه حضرت محمد (ص) بوده است. روی پرچم جمله «لا اله الا الله محمد رسول الله» و یک شمشیر افقی در سمت چپ وجود دارد. شمشیر نمادی از عدالت و نشانی از عبدالعزیز بن سعود، اولین پادشاه عربستان سعودی می باشد. استفاده از این پرچم فقط در مراسم های رسمی و یا اهداف رسمس مجاز می باشد.", message_id=msg.get("message_id"))

					elif msg.get("text") == "🇦🇺":
						bot.sendMessage(target, "پرچم استرالیا. در گذشته تمامی کشورهای تحت سلطه انگلیس وظیفه داشتند تا در پرچمشان نشانی از انگلستان را داشته باشند که پرچم استرالیا نیز از این قاعده مستثنا نبوده است. ستاره هفت پر در این پرچم نشان دهنده ۶ ایالت استرالیا و همچنین یک پر برای مستعمرات می باشد. ستاره ای دیگر در پرچم به صورت فلکی صلیب جنوبی که از تمام قسمت های کشور استرالیا دیده می شود اشاره دارد.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇬🇧":
						bot.sendMessage(target, "پرچم کشور انگلیس، صلیبی قرمز بر روی زمینه سفید رنگ می باشد. صلیب این پرچم نمادی از صلیب سنت جرج همان قدیس مدافع انگلستان می باشد. صلیب قرمز در خیلی از جنگ ها به عنوان نماد کشور انگلستان بوده و به تدریج به نشانه انگلستان تبدیل گشته است. قدمت بکارگیری این پرچم در انگلیس به قرون وسطی باز می گردد. پرچم فعلی انگلیس اولین بار در ۱۸۰۱ میلادی به عنوان پرچم ملی انگلستان ثبت گردید. ترکیب پرچم کشورها با نام های ایرلند، اسکاتلند و انگلستان پرچم بریتانیا را تشکیل داده است.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇧🇷":
						bot.sendMessage(target, "پرچم برزیل زمینه ای سبز رنگ دارد که بر روی آن یک لوزی زرد قرار گرفته است و در داخل لوزی یک دایره آبی رنگ وجود دارد و بر روی دایره بر روی نواری خمیده شعار ملی کشور برزیل یعنی نظم و پیشرفت نوشته شده است. برای اولین بار در نوامبر ۱۸۸۹ این پرچم تخت عنوان پرچم اصلی و نماد برزیل شناخته شد. دایره آبی در این پرچم نشانی از آسمان پر ستاره دارد و ۲۷ ستاره به تعداد ایالات برزیل بر روی آن قرار دارد. رنگ سبز در این پرچم به جنگ های این کشور اشاره دارد و رنگ زرد در آن نشان دهنده ذخایر عظیم طلا در کشور برزیل می باشد.", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇪🇸":
						bot.sendMessage(target, "پرچم کشور اسپانیا از رنگ های قرمز و زرد به وجود آمده است نماد ملی آن کمی متمایل به چپ میباشد این پرچم در 5 اکتبر سال 1981 به عنوان پرچم اسپانیا انتخاب شد رنگ قرمز در این پرچم به مفهوم جنگ هایی است که در طول تاریخ در اسپانیا اتفاق افتاده و برخی نیز ان را به مراسم گاوبازی نیز تعبیر می کنند , رنگ زرد نشانه خورشید فروزان و روشن کننده است البته برخی افراد نیز آن رابه رنگ ماسه های زمین گاوبازی تعبیر می کنند رنگ قرمز و طلایی ریشه در فرهنگ مردم این کشور دارد .", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🇮🇶":
						bot.sendMessage(target, "پرچم عراق دارای تناسب ۲ به ۳ است. پرچم شامل سه نوار افقی به عرض یکسان و به ترتیب با رنگ های قرمز، سفید و مشکی از بالا به پایین است. در میانه نوار سفید در میانه پرچم عراق عبارت الله اکبر به رنگ سبز و خط کوفی نوشته شده است. پرچم به عنوان پرچم رسمی زمینی و دریایی شناخته می شود. رنگ های سبز و سیاه پرچم نشان از اسلامی بودن این کشور است. این رنگ ها را می توان در پرچم اغلب کشورهای عرب و مسلمان مشاهده نمود. رنگ قرمز پرچم نیز نشانه اکثریت عرب این کشور است. همچنین رنگ قرمز پرچم به معنی مبارزات و دلاوری های ملت عراق برای رسیدن به آزادی و استقلال است. رنگ سفید به معنی آینده کشور عراق و صلح دوستی و سخاوت مردم عراق است. رنگ مشکی پرچم عراق نشان از دین اسلام مردم این کشور و همچنین ظلم و ستم هایی است که در دوره های مختلف بر مردم وارد شده است.", message_id=msg.get("message_id"))

					elif msg.get("text") == "😭":
						bot.sendMessage(target, "چی شد عزیزم 💔🥀", message_id=msg.get("message_id"))

					elif msg.get("text") == "خفه":
						bot.sendMessage(target, "🤐", message_id=msg.get("message_id"))

					elif msg.get("text") == "😂😂😂":
						bot.sendMessage(target, "نمیری هالا \n\n لازمت داریم........👻.!", message_id=msg.get("message_id"))

					elif msg.get("text") == "😒":
						bot.sendMessage(target, "چته!....؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "🍫":
						bot.sendMessage(target, "شکلات میقولی؟", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🗿":
						bot.sendMessage(target, "مایل به گانگستر؟", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "هعب":
						bot.sendMessage(target, "درکت میکنم 💔🥀", message_id=msg.get("message_id"))

					elif msg.get("text") == "لینک گپ" and msg.get("author_object_guid") in admins :
						bot.sendMessage(target, "https://rubika.ir/joing/BFCJDDFA0HOZPHICIIQLADWYCOAAIAJJ", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "روبو":
						bot.sendMessage(target, "بله 🗿😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "قربونت برم":
						bot.sendMessage(target, "فدات😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "سیکتیر":
						bot.sendMessage(target, "سیک اگه تیر داشت ننت كلكسيون ك.ير🥴🤣", message_id=msg.get("message_id"))

					elif msg.get("text") == "ماشین":
						bot.sendMessage(target, "با ک.ون برین جا شین😂♥️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "باشه":
						bot.sendMessage(target, "بچوس تا لاش وا شه 😐🙌🏼", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "حوصلم سر رفت😢":
						bot.sendMessage(target, "یه گوز از کیونت در رفت😹🖕", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "گوه نخور":
						bot.sendMessage(target, "شاشیـــــدم سُر نخـــــور😹🙌🏿❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "ایش😒":
						bot.sendMessage(target, "بشین سرش برو کیـش🚘", message_id=msg.get("message_id"))

					elif msg.get("text") == "میخاری":
						bot.sendMessage(target, "بمال به لوله بخاری😂❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "دل میرود ز دستم":
						bot.sendMessage(target, "ممتو بزار تو دستـم 😹??", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "لالی!؟😡😒":
						bot.sendMessage(target, "میتونی برام بمالی😹", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "س.یکتیر":
						bot.sendMessage(target, "سیک اگه تیر داشت بابات جان باز بود😂🖕🏿", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "دقیقا":
						bot.sendMessage(target, "ک.یرمو ک.یونت رفیقن😂❤", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🖕":
						bot.sendMessage(target, "-پس بشین روش جوجه شه😹", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "عفریته":
						bot.sendMessage(target, "عمتـه👊", message_id=msg.get("message_id"))

					elif msg.get("text") == "رفیق":
						bot.sendMessage(target, "بكنمت ميزني جيغ؟😂👆🏿", message_id=msg.get("message_id"))

					elif msg.get("text") == "بای😻":
						bot.sendMessage(target, "بد کردمت گفتی آیییی😂❤", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "عزیزم😐":
						bot.sendMessage(target, "-نکردمت مریضم😂❤️", message_id=msg.get("message_id"))

					elif msg.get("text") == "بی کاری؟":
						bot.sendMessage(target, "خیار بدم بکاری😂❤️", message_id=msg.get("message_id"))

					elif msg.get("text") == "من کچلم تو مو دار😶":
						bot.sendMessage(target, "من میرینم تو بردار😹", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "مالزی":
						bot.sendMessage(target, "لا پات کیر فلزی😂❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "لاـشی!😻":
						bot.sendMessage(target, "جوری میزنمت به موزائیک بگی‌کاشی ، ساده میخوای یا خاش خاشی", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "بی شرف؟":
						bot.sendMessage(target, "تو ک*ون بابات شیشه رفت😂🤘🏿", message_id=msg.get("message_id"))

					elif msg.get("text") == "نگاه داره؟":
						bot.sendMessage(target, "دیدن خر صفا داره😂🖕🏿", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "گوش كن":
						bot.sendMessage(target, "سرشو بگير توش كن 😈😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "زندگی یعنی خنده":
						bot.sendMessage(target, "به شرط اینکه بیای بِدی به بنده😂❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "به تخمم":
						bot.sendMessage(target, "کو*نت رو ک.یر لختم😂❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "عه":
						bot.sendMessage(target, "آره بــــه مـــــولـــــا😐😂", message_id=msg.get("message_id"))

					elif msg.get("text") == "🤣":
						bot.sendMessage(target, "یـعـنـی ایــــنــــقـــد خــــنــده داش؟؟؟😐🤣", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "ارع":
						bot.sendMessage(target, "آجــــر پــــاره😐🤣💫️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "ممنون":
						bot.sendMessage(target, "انجام‌وظیفه بود🥴", message_id=msg.get("message_id"))

					elif msg.get("text") == "خیلی ممنون":
						bot.sendMessage(target, "خواهش می‌کنم، کاری نکردم♥️😊", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "🤣🤣":
						bot.sendMessage(target, "کــــم بــــخـــنـــد اخــــرش مـــیـــگـــوزی گـــپـــو بـــه گـــا مـــیـــدی هـــا 🤣💔", message_id=msg.get("message_id"))

					elif msg.get("text") == "اره با تو هستم":
						bot.sendMessage(target, "چیکار داری با من کارت بگو؟👻👊", message_id=msg.get("message_id"))

					elif msg.get("text") == "عافرین🗿":
						bot.sendMessage(target, "چـــــاکــــریــــم حــــاجــــی😁❤", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "حق":
						bot.sendMessage(target, "ســتــاده مــبــارزه بــا حــق گــویــان: کــص نــگــو کــیــرم بــه نــصــلــه یــتــیــمــت🤣️", message_id=msg.get("message_id"))

					elif msg.get("text") == "ریدی":
						bot.sendMessage(target, "من نرینم که تو از گشنگی میمیری😂😂😂", message_id=msg.get("message_id"))

					elif msg.get("text") == "گشاد":
						bot.sendMessage(target, "کَلَش تو چشات😂❤", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "توله":
						bot.sendMessage(target, "با سر برو تو لوله😐😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "کافه":
						bot.sendMessage(target, "سَــرِ کی.ــرَم غَـلافه🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "ایمان":
						bot.sendMessage(target, "تو کو🍑نت پاکت سیمان😂❤️", message_id=msg.get("message_id"))

					elif msg.get("text") == "همین😐":
						bot.sendMessage(target, "نه بیا کَلَشَم ببین 😂👌", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "برو بابا😐":
						bot.sendMessage(target, "نگو بابا، احساس مسئولیت میکنم😏", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "کثافط":
						bot.sendMessage(target, "ریدم تو اون قیافت با نرمی و لطافت😂❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "تا اخرش باهاتم😎😊":
						bot.sendMessage(target, "+تف کن باوو😐", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "چیو؟":
						bot.sendMessage(target, "گهی که خوردیو😏", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "ایول" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "بنازم به ایول گفتنت😍", message_id=msg.get("message_id"))

					elif msg.get("text") == "😡" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "ببخشید دیگه تکرار نمیشه جونم😖", message_id=msg.get("message_id"))

					elif msg.get("text") == "چقدر منو دوست داری" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "خیلی دوست دارم انقد که گفتنی نیست😊❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "استقلال" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "قسم به تیم استقلال ، قسم به سیمای خوبان ، قسم به ناصر حجازی ، ندای ما استقلال 💙", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "💙😂" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "قسم به تیم استقلال ، قسم به سیمای خوبان ، قسم به ناصر حجازی ، ندای ما استقلال 💙", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "پرسپولیس" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "پرسپولیس عشق آسیایی پرسپولیس خالق یک جامی گل بزن امشبو به یاد پروین و علی دایی ❤", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "❤️😂" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "پرسپولیس عشق آسیایی پرسپولیس خالق یک جامی گل بزن امشبو به یاد پروین و علی دایی ❤", message_id=msg.get("message_id"))
							
					elif msg.get("text") == "سپاهان" and msg.get("author_object_guid") :
						bot.sendMessage(target, "سپاهان خورشید سپهر نصف جهان خورشید از عشق سپاهانست طلایی وگرنه متوانست بود. سرخ و ابی سپاهان مظهرعشقد خدایست سزاوار سرورد قهرمانیست.....💛", message_id=msg.get("message_id"))

					elif msg.get("text") == "💛😂" and msg.get("author_object_guid") :
						bot.sendMessage(target, "سپاهان خورشید سپهر نصف جهان خورشید از عشق سپاهانست طلایی وگرنه متوانست بود. سرخ و ابی سپاهان مظهرعشقد خدایست سزاوار سرورد قهرمانیست.....💛", message_id=msg.get("message_id"))

					elif msg.get("text") == "تراکتورسازی" and msg.get("author_object_guid") :
						bot.sendMessage(target, "ياشا تيراختور قارتال تيراختور ، بيزلره جان سان وور گل لاري وور ، سن گل ووران سان قوردلار دره سي ، ياشاسين سسي سن قودرتيني ، بيزدن آلان سان يوز مين طرفدار ، سسلر اوجالار ياشا تراختور ، سن قهرمان سان هر تيم کي اولسا ، ديفايا دولسا جيريخ يئريني ، تئز تئز تاپان سان داليندا ميللت ، ائيله سن هيممت تيم لر ايچينه ، قورخو سالان سان هر گون اودورسان ، بيزه غرورسان آذربايجانا ، قيزيل نيشان سان♥️🚜", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "❤️🚜" and msg.get("author_object_guid") :
						bot.sendMessage(target, "ياشا تيراختور قارتال تيراختور ، بيزلره جان سان وور گل لاري وور ، سن گل ووران سان قوردلار دره سي ، ياشاسين سسي سن قودرتيني ، بيزدن آلان سان يوز مين طرفدار ، سسلر اوجالار ياشا تراختور ، سن قهرمان سان هر تيم کي اولسا ، ديفايا دولسا جيريخ يئريني ، تئز تئز تاپان سان داليندا ميللت ، ائيله سن هيممت تيم لر ايچينه ، قورخو سالان سان هر گون اودورسان ، بيزه غرورسان آذربايجانا ، قيزيل نيشان سان♥️🚜", message_id=msg.get("message_id"))

					elif msg.get("text") == "😎" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "هر کی با ما در افتاد ور افتاد 😎", message_id=msg.get("message_id"))

					elif msg.get("text") == "هعپ" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "آبی روشن عین من سیتی برف میاد سریع ترکیم هووو", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "رفیعی" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "یک دوست خوب'", message_id=msg.get("message_id"))

					elif msg.get("text") == "چی بلدی" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "بطچ؟", message_id=msg.get("message_id"))

					elif msg.get("text") == "چراغی" and msg.get("author_object_guid") :
						
						bot.sendMessage(target, "دشمن سیب زمینی دست میکنه تو بینی در میاره شیرینی #شوخی 😂", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "Amir" and msg.get("author_object_guid") :
						bot.sendMessage(target, "رئیسمه فداش بشم من", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "خودتو معرفی کن" and msg.get("author_object_guid") :
						bot.sendMessage(target, "من ربات هستم که با هوش مصنوعی میتونم اینجا رو مدیریت کنم و باهاتون مثل یک انسان واقعی چت کنم", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "😐😒":
						bot.sendMessage(target, "صد دانه فلفل🌶 همرنگ خونت💋با نظم و ترتیب😆یکجا تو کونت😹👊🏿", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "😑":
						bot.sendMessage(target, "طرفـ یہ جورے خودشو میگیرـه انگار منہ😻نمیدونه قیافـــ👹ــش شکل عنه😂❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "میرزا":
						bot.sendMessage(target, "بخورش با پیتزا😂❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "بگو فانوس":
						bot.sendMessage(target, "کم  بده بی نامـ..ـوس😂❤️", message_id=msg.get("message_id"))

					elif msg.get("text") == "خفع":
						bot.sendMessage(target, "از سرش بخور ‌این دفعه😕❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "وات":
						bot.sendMessage(target, "کیلووات، ریدم تو قبر بابات 😏😁", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "مهرنوش":
						bot.sendMessage(target, "شـُل کن بـره تـوش 😂❤️", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "گیم" or msg.get("text") == "/game" or msg.get("text") == "\game" and msg.get("author_object_guid") :
												bot.sendMessage(target, "👻برای دریافت بازی🙀 فقط بنویسید:↪️ \n\n ⚪️اکشن \n\n 🟢ورزشی \n\n 🟡پرتحرک \n\n 🔴پازل \n\n کلمه های مشخص شده را تایپ کنید.✅ \n\n لیست بازی براتون ارسال شود.🤠🔥", message_id=msg.get("message_id"))
												
					elif msg.get("text") == "ورزشی" and msg.get("author_object_guid") :
												bot.sendMessage(target, "🏀- بخش ورزشی  \n • فوتبال استار  \n ➖ https://b2n.ir/MC_rBOT2 \n • بسکتبال \n ➖ https://b2n.ir/MC_rBOT24 \n • پادشاه شوت کننده \n ➖ https://b2n.ir/MC_rBOT255 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.", message_id=msg.get("message_id"))
												
					elif msg.get("text") == "اکشن" and msg.get("author_object_guid") :
												bot.sendMessage(target, "🥊- بخش اکشن \n • نینجای جاذبه  \n ➖ https://b2n.ir/MC_rBOT3 \n • رانندگی کن یا بمیر \n ➖ https://b2n.ir/MC_rBOT9 \n • کونگ فو \n ➖ https://b2n.ir/MC_rBOT11 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.", message_id=msg.get("message_id"))
												
					elif msg.get("text") == "پرتحرک" and msg.get("author_object_guid") :
												bot.sendMessage(target, "💥- بخش پرتحرک \n • گربه دیوانه  \n ➖ https://b2n.ir/MC_rBOT4 \n • ماهی بادکنکی \n ➖ https://b2n.ir/MC_rBOT13 \n • دینگ دانگ \n ➖ https://b2n.ir/MC_rBOT12 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.", message_id=msg.get("message_id"))
												
					elif msg.get("text") == "پازل" and msg.get("author_object_guid") :
												bot.sendMessage(target, "🏮-بخش پازل \n • پازل بلاکی \n ➖ https://b2n.ir/MC_rBOT5 \n • ساحل پاپ \n ➖ https://b2n.ir/MC_rBOT14 \n • جمع اعداد \n ➖ https://b2n.ir/MC_rBOT15 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.", message_id=msg.get("message_id"))
							
					elif msg.get("text").startswith("الکی") or msg.get("text").startswith("alaki-masalan") or msg.get("text").startswith("!alaki-masalan"):
						
						try:
							response = get("https://api.codebazan.ir/jok/alaki-masalan/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "لطفا دستور را به طور صحیح وارد کنید❌", message_id=msg["message_id"])


					if  msg.get("text").startswith('!user @'):
						try:
							user_info = bot.getInfoByUsername( msg.get("text")[7:])
							if user_info['data']['exist'] == True:
								if user_info['data']['type'] == 'User':
									bot.sendMessage(target, 'Name User:\n ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\nBio User:\n ' + user_info['data']['user']['bio'] + '\n\nGuid:\n ' + user_info['data']['user']['user_guid'] ,  msg.get('message_id'))
									print('sended response')
								else:
									bot.sendMessage(target, 'کانال است ❌' ,  msg.get('message_id'))
									print('sended response')
							else:
								bot.sendMessage(target, "کاربری وجود ندارد ❌" ,  msg.get('message_id'))
								print('sended response')
						except:
							print('server bug6')
							bot.sendMessage(target, "خطا در اجرای دستور مجددا سعی کنید ❌" ,message_id=msg.get("message_id"))
							
					elif msg.get("text").startswith("نگاییدم"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کس"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کیر"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("کصکصش"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کیری"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("مادرت گاییدم"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کس نت"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کص نت"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("خواهر مادرت گاییدم"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("خواهرت گاییدم"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("مادر کونی"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کیرم تو کص نت"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کیرم تو کس نت"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کسس نگو"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("مادرت"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("مادرتو"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کیرم"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کوص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کوبص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کوس"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کبص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کسکش"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("بی ناموس"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("بیناموس"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("بی ناموص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("بیناموص"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کونی"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("@"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("@ "):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("کیرم تو کص نت"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("https://rubika.ir/joing/"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("https://rubika.ir"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("https://rubika.ir/"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("https://"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))

					elif msg.get("text").startswith(" https://rubika.ir/ "):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("rubika.ir"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("joing/"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کشکش"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("گاییدم"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("کیری"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "یک پیام مستهجن از گروه حذف شد.🥴", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("https://rubika.ir/joing/https://rubika.ir/joing//n/nhttps://rubika.ir/joing//n/nhttps://rubika.ir/joing//n/nhttps://rubika.ir/joing//n/nhttps://rubika.ir/joing//n/nhttps://rubika.ir/joing//n/n"):
						bot.deleteMessages(target, [str(msg.get("message_id"))])
						bot.sendMessage(target, "پیام شما چون حاوی تبلیغات بود حذف شد😐", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("غیر فعال ارام") and msg.get("author_object_guid") in admins:
							try:
								number = 0
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام غیرفعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						
					elif msg.get("text").startswith("ارام10") and msg.get("author_object_guid") in admins:
							try:
								number = 10
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
					elif msg.get("text").startswith("ارام1") and msg.get("author_object_guid") in admins:
							try:
								number = 60
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
					elif msg.get("text").startswith("ارام5") and msg.get("author_object_guid") in admins:
							try:
								number = 300
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))															
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
					elif msg.get("text").startswith("ارام15") and msg.get("author_object_guid") in admins:
							try:
								number = 900
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
					elif msg.get("text").startswith("ارام1s") and msg.get("author_object_guid") in admins:
							try:
								number = 1600
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
					elif msg.get("text").startswith("ارام30") and msg.get("author_object_guid") in admins:
							try:
								number = 30
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
					elif msg.get("text") == "!speak" or msg.get("text") == "speak" or msg.get("text") == "Speak" or msg.get("text") == "بگو":
							try:
								if msg.get('reply_to_message_id') != None:
									msg_reply_info = bot.getMessagesInfo(target, [msg.get('reply_to_message_id')])[0]
									if msg_reply_info['text'] != None:
										text = msg_reply_info['text']
										speech = gTTS(text)
										changed_voice = io.BytesIO()
										speech.write_to_fp(changed_voice)
										b2 = changed_voice.getvalue()
										changed_voice.seek(0)
										audio = MP3(changed_voice)
										dur = audio.info.length
										dur = dur * 1000
										f = open('sound.ogg','wb')
										f.write(b2)
										f.close()
										bot.sendVoice(target , 'sound.ogg', dur,message_id=msg["message_id"])
										os.remove('sound.ogg')
										print('sended voice')
								else:
									bot.sendMessage(target, 'پیام شما متن یا کپشن ندارد',message_id=msg["message_id"])
							except:
								print('server gtts bug')
								
					elif msg.get("text") == "سنجاق" and msg.get("author_object_guid") in admins :
						    bot.pin(target, msg["reply_to_message_id"])
						    bot.sendMessage(target, "پیام مورد نظر با موفقیت سنجاق شد!🥱", message_id=msg.get("message_id"))
						
					elif msg.get("text") == "برداشتن سنجاق" and msg.get("author_object_guid") in admins :
						    bot.unpin(target, msg["reply_to_message_id"])
						    bot.sendMessage(target, "پیام مورد نظر از سنجاق برداشته شد!🥱", message_id=msg.get("message_id"))

					elif msg.get("text") == "پایان" and msg.get("author_object_guid") in admins :
						sleeped = True
						bot.sendMessage(target, "ربات با موفقیت خاموش شد!", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("پینگ"):
						
						try:
							responser = get(f"https://api.codebazan.ir/ping/?url={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("!trans"):
						
						try:
							responser = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={msg.get('text').split()[1:]}").json()
							al = [responser["result"]]
							bot.sendMessage(msg.get("author_object_guid"), "پاسخ به ترجمه:\n"+"".join(al)).text
							bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه🤣", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("دستورات") or msg.get("text").startswith("/help") or msg.get("text").startswith("!help"):
							try:
								bot.sendMessage(msg.get("author_object_guid"), "لیسـت دستـــورات ربـات 🤖:\n\n●🤖 (ربات آنلاینی؟) : فعال یا غیر فعال بودن بات\n\n●❎ (پایان) : غیر فعال سازی بات\n\n●✅ (شروع) : فعال سازی بات\n\n●🕘 (ساعت) : ساعت\n\n●📅 (تاریخ میلادی) : تاریخ\n\n●📋 (پاک) : حذف پیام با ریپ بر روی ان\n\n●🔒 (بستن گروه) : بستن چت در گروه\n\n●🔓 (باز کردن گروه) : باز کردن چت در گروه\n\n●❌ (ریم) : حذف کاربر با ریپ زدن\n\n●✉ !send: ارسال پیام با استفاده از ایدی\n\n●📌 add: افزودن کاربر به گپ با ایدی\n\n●📜 (دستورات) : لیست دستورات ربات\n\n●🆑 cal :ماشین حساب\n\n●🔴 (!user) : اطلاعات کاربر با ایدی\n\n●😂 (جوک) : ارسال جوک\n\n●🔵 (فونت) : ارسال فونت\n\n●🔴 (پینگ) : گرفتن پینگ سایت\n\n●🔵 trans : مترجم انگلیسی\n\n●🔴 (زمان) : تاریخ و ساعت\n\n●🔴 (بیوگرافی) : بیوگرافی\n\n●🔴 (پ ن پ) : جوک پ ن پ\n\n●🔴 (الکی مثلا) : جوک الکی مثلا\n\n●🔴 (داستان) : داستان های کوتاه\n\n●🔴 (دانستنی) : دانستنی ها\n\n●🔴 (دیالوگ) : دیالوگ های ماندگار\n\n●🔴 (!weather) : آب و هوا\n\n●🔴 (حدیث) : سخن بزرگان\n\n●🔴 (ذکر) : ذکر روز ها\n\n●🔴 (گیم) : بازی های جایزه ای 🏆 \n\n سازنده @lo_amir_org").text
								bot.sendMessage(target, "نتیجه کامل به پیوی شما ارسال شد✔️", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "نتیجه کامل به پیوی شما ارسال شد✔️", message_id=msg["message_id"])

					elif msg.get("text").startswith("قوانین") or msg.get("text").startswith("/help") or msg.get("text").startswith("!help"):
							try:
								bot.sendMessage(msg.get("author_object_guid"), "● قوانین گروه🤖:\n\n○ فحش و لینک ممنوع🙃〽️\n\n○ تبلیغات ممنوع🤕🥀\n\n○ توهین به کاربران و ادمین ها ممنوع👌\n\n○ بحث به غیر از تکنولوژی ممنوع 🤕🥀\n\n○ دستورات مستهجن به ربات ممنوع🔞\n\n● در صورت مشاهده و زیر پا گذاشتن \n\n قوانین فورا شما از گروه حذف میشوید!❌🛑").text
								bot.sendMessage(target, "نتیجه کامل به پیوی شما ارسال شد✔️", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "نتیجه کامل به پیوی شما ارسال شد✔️", message_id=msg["message_id"])

					elif msg.get("text").startswith("فونت"):
						#print("\n".join(list(response["result"].values())))
						try:
							response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
							bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
							bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
							
					elif msg.get("text") == "𝚁𝚘𝚋𝚘":
					      user = bot.getUserInfo(msg["author_object_guid"])["data"]["user"]["first_name"]
					      text = f"جـــونــم {user} عــزیـزم🙂🌹"
					      bot.sendMessage(target, text, message_id=msg.get("message_id"))
					
					elif msg.get("text").startswith("دانش"):
						
						try:
							response = get("https://api.codebazan.ir/danestani/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("خاطره") or msg.get("text").startswith("khatere") or msg.get("text").startswith("!khatere"):
						
						try:
							response = get("http://api.codebazan.ir/jok/khatere").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "لطفا دستور رابه طورصحیح وارد کنید❌", message_id=msg["message_id"])

					elif msg.get("text").startswith("نام شاخ"):
						
						try:
							response = get("https://api.codebazan.ir/name/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("جوک"):
						
						try:
							response = get("https://api.codebazan.ir/jok/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("ذکر"):
						
						try:
							response = get("http://api.codebazan.ir/zekr/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("همسر"):
							try:
								response = get("https://api.codebazan.ir/name/?type=json").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
								
					elif msg.get("text").startswith("حدیث"):
						
						try:
							response = get("http://api.codebazan.ir/hadis/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("بیوگرافی"):
						
						try:
							response = get("https://api.codebazan.ir/bio/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg["text"].startswith("!weather"):
						response = get(f"https://api.codebazan.ir/weather/?city={msg['text'].split()[1]}").json()
						#print("\n".join(list(response["result"].values())))
						try:
							bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
							bot.sendMessage(target, "نتیجه بزودی برای شما ارسال خواهد شد...", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "متاسفانه نتیجه‌ای موجود نبود!", message_id=msg["message_id"])
						
							
					elif msg.get("text").startswith("دیالوگ"):
						
						try:
							response = get("http://api.codebazan.ir/dialog/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("دانستنی"):
						
						try:
							response = get("http://api.codebazan.ir/danestani/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("داستان"):
						
						try:
							response = get("http://api.codebazan.ir/dastan/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("پ ن پ"):
						
						try:
							response = get("http://api.codebazan.ir/jok/pa-na-pa/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("الکی مثلا"):
						
						try:
							response = get("http://api.codebazan.ir/jok/alaki-masalan/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
							
					elif msg.get("text").startswith("زمان"):
						
						try:
							response = get("https://api.codebazan.ir/time-date/?td=all").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])

					elif msg.get("text") == "ساعت":
						bot.sendMessage(target, f"Time : {time.localtime().tm_hour} : {time.localtime().tm_min} : {time.localtime().tm_sec}", message_id=msg.get("message_id"))

					elif msg.get("text") == "تاریخ میلادی":
						bot.sendMessage(target, f"Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}", message_id=msg.get("message_id"))

					elif msg.get("text") == "پاک" and msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("reply_to_message_id")])
						bot.sendMessage(target, "پیام مورد نظر پاک شد...", message_id=msg.get("message_id"))
       
					# elif msg.get("text").split(" ")[0] in  delmess:
					# 	bot.deleteMessages(target, [msg.get("message_id")])
					# 	bot.sendMessage(target, "یک پیام مستهجن پاک شد ✅", message_id=msg.get("message_id"))
					
					
					elif msg.get("text") == "گزارش" and msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("reply_to_message_id")])
						bot.sendMessage(target, "عجب",message_id=msg.get("message_id"))

					elif msg.get("text") == "بستن گروه" and msg.get("author_object_guid") in admins :
						print(bot.setMembersAccess(target, ["ViewMembers","ViewAdmins","AddMember"]).text)
						bot.sendMessage(target, "گروه بسته شد!", message_id=msg.get("message_id"))

					elif msg.get("text") == "باز کردن گروه" and msg.get("author_object_guid") in admins :
						bot.setMembersAccess(target, ["ViewMembers","ViewAdmins","SendMessages","AddMember"])
						bot.sendMessage(target, "گروه باز شد!", message_id=msg.get("message_id"))
						
					elif msg.get("text").startswith("ریم") and msg.get("author_object_guid") in admins :
						try:
							guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							if not guid in admins :
								bot.banGroupMember(target, guid)
								bot.sendMessage(target, f"کاربر مورد نظر حذف شد !", message_id=msg.get("message_id"))
							else :
								bot.sendMessage(target, f"خطا", message_id=msg.get("message_id"))
								
						except IndexError:
							a = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
							if a in admins:
								bot.sendMessage(target, f"خطا", message_id=msg.get("message_id"))
							else:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								bot.sendMessage(target, f"کاربر مورد نظر بن شد !", message_id=msg.get("message_id"))

				else:
					if msg.get("text") == "شروع" and msg.get("author_object_guid") in admins :
						sleeped = False
						bot.sendMessage(target, "ربات شروع به فعالیت کرد!", message_id=msg.get("message_id"))
						
			elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
				name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
				data = msg['event_data']
				if data["type"]=="RemoveGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"اگه قوانین رو رعایت میکردی حذف نمیشدی !", message_id=msg["message_id"])
					
				elif data["type"]=="AddedGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"هــای {user} عزیز 😘🌹\n\n •به گـروه {name}  🤍\n\n•😇 خیـلی خوش اومدی 🥳💛\n\n• لطفا قوانین رو رعایت کن✅\n\n• برای مشاهده قوانین ، قوانین را ارسال کن⁉️", message_id=msg["message_id"])
				
				elif data["type"]=="LeaveGroup":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"بای بای 🖖 {user} 🥀", message_id=msg["message_id"])
					
				elif data["type"]=="JoinedGroupByLink":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"هــای {user} عزیز 😘🌹\n\n •به گـروه {name}  🤍\n\n•😇 خیـلی خوش اومدی 🥳💛\n\n• لطفا قوانین رو رعایت کن✅\n\n• برای مشاهده قوانین ، قوانین را ارسال کن⁉️", message_id=msg["message_id"])

			answered.append(msg.get("message_id"))

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue