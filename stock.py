import requests
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.header import Header
from email.MIMEText import MIMEText
from email.utils import formataddr
import json
import datetime






# def get_data(response, name, index):
#    return response.json()[index][name] 

def isHoliday(today):
	list = [
	'2020-09-07',
	'2020-11-26',
	'2020-12-25',
	'2021-01-01',
	'2021-01-18',
	'2021-02-15',
	'2021-04-02',
	'2021-05-31',
	'2021-07-05',
	'2021-09-06',
	'2021-11-25',
	'2021-12-24'
	]

	return today in list


# OFFSET = 6


today = datetime.date.today()
todayString = today.strftime("%Y-%m-%d")
# lastWeek = today - datetime.timedelta(days=OFFSET)
# lastWeekString = lastWeek.strftime("%Y-%m-%d")







# url = "https://api.tiingo.com/tiingo/daily/DIA/prices?startDate=LASTWEEK&endDate=TODAY&token=12d898a99f0a48f6c3483cd1f30e8c53dbb854e0"
# url = url.replace("LASTWEEK", lastWeekString).replace("TODAY", todayString)

# headers = {'Content-Type': 'application/json'}
# response = requests.get(url,headers=headers)




# TODAY_INDEX = len(response.json()) - 1
# YESTERDAY_INDEX = len(response.json()) - 2



# price = get_data(response, 'close', TODAY_INDEX)

# change = get_data(response, 'close', TODAY_INDEX) - get_data(response, 'close', YESTERDAY_INDEX)
# changesPercentage = (change / get_data(response, 'close', YESTERDAY_INDEX))

nameDIA = "DIA ETF"
responseDIA = requests.get('https://finnhub.io/api/v1/quote?symbol=DIA&token=bsn0ifnrh5ret9gkabfg')
priceDIA = responseDIA.json()['c']
changeDIA = responseDIA.json()['c'] - responseDIA.json()['pc']
changesPercentageDIA = (changeDIA / responseDIA.json()['pc'])

nameSPY = "SPY ETF"
responseSPY = requests.get('https://finnhub.io/api/v1/quote?symbol=SPY&token=bsn0ifnrh5ret9gkabfg')
priceSPY = responseSPY.json()['c']
changeSPY = responseSPY.json()['c'] - responseSPY.json()['pc']
changesPercentageSPY = (changeSPY / responseSPY.json()['pc'])



today_formatted = today.strftime("%m/%d/%y")
if isHoliday(todayString):
	data = "The market is actually closed on {} \n\nPlease enjoy your holiday! :)".format(today_formatted)
else:
	data = "Name: {}\nPrice: {}\nChange: {}\nChanges Percentage: {:.2%}\n\nName: {}\nPrice: {}\nChange: {}\nChanges Percentage: {:.2%}".format(nameDIA, priceDIA, changeDIA, changesPercentageDIA, nameSPY, priceSPY, changeSPY, changesPercentageSPY)



today_formatted = today.strftime("%m/%d/%y")



 
#Enter email information
fromaddr = "lynlynlynt@gmail.com"
password = "lynlynlyn"
toaddr = ['mingxin.ou@gmail.com', 'centuryib100@gmail.com']

# fakeCcList = ['fakecc@gmail.com']
# bccList = ['bcc@gmail.com']
displayName = 'Stock Master'


msg = MIMEMultipart('alternative')
msg['From'] = formataddr((str(Header(displayName, 'utf-8')), fromaddr))


#Edit subject, message, and reply-to information here
msg['Subject'] = today_formatted + " Daily Stock Update"
stockInfo = "The stock market has just closed\n\n"
stockInfo = stockInfo + data
# msg.add_header('reply-to', "replyto@gmail.com")



## News Module


import requests
r = requests.get('https://finnhub.io/api/v1/news?category=general&token=bsn0ifnrh5ret9gkabfg')
news = "\n\n\nNews\n" + json.dumps(r.json(), indent=4)


msg['To'] = ",".join(toaddr)
# msg['Cc'] = ",".join(fakeCcList)
msg.attach(MIMEText(stockInfo + news, 'plain'))




## Formatting with HTML
newsHtmlText = news
newsHtmlText = newsHtmlText.replace("\n", "<br>")
newsHtmlText = newsHtmlText.replace("\"headline\"", "<b>\"Headline\"</b>")
htmlBegin = """\
<html>
  <head></head>
  <body>
  <pre>
  <code>
"""
htmlEnd = """\
	</code>
	</pre>
  </body>
</html>
"""

html = MIMEText(stockInfo.replace("\n", "<br>") + htmlBegin + newsHtmlText + htmlEnd, 'html')
msg.attach(html)



server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
