import requests
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.header import Header
from email.MIMEText import MIMEText
from email.utils import formataddr
import json
import datetime






def get_data(response, name, index):
   return response.json()[index][name] 

TODAY = 1
YESTERDAY = 0




today = datetime.date.today()
todayString = today.strftime("%Y-%m-%d")
yesterday = today - datetime.timedelta(days=1)
yesterdayString = yesterday.strftime("%Y-%m-%d")


url = "https://api.tiingo.com/tiingo/daily/DIA/prices?startDate=YESTERDAY&endDate=TODAY&token=12d898a99f0a48f6c3483cd1f30e8c53dbb854e0"
url = url.replace("YESTERDAY", yesterdayString).replace("TODAY", todayString)

headers = {'Content-Type': 'application/json'}
response = requests.get(url,headers=headers)





name = "DIA ETF"
price = get_data(response, 'close', TODAY)

change = get_data(response, 'close', TODAY) - get_data(response, 'close', YESTERDAY)
changesPercentage = (change / get_data(response, 'close', YESTERDAY))



data = "Name: {}\nPrice: {}\nChange: {}\nChanges Percentage: {:.2%}".format(name, price, change, changesPercentage)


today_formatted = today.strftime("%m/%d/%y")



 
#Enter email information
fromaddr = "lynlynlynt@gmail.com"
password = "lynlynlyn"
toaddr = ['mingxin.ou@gmail.com','centuryib100@gmail.com']
# fakeCcList = ['fakecc@gmail.com']
# bccList = ['bcc@gmail.com']
displayName = 'Stock Master'


msg = MIMEMultipart()
msg['From'] = formataddr((str(Header(displayName, 'utf-8')), fromaddr))


#Edit subject, message, and reply-to information here
msg['Subject'] = today_formatted + " Daily Stock Update"
body = "The stock market has just closed\n\n"
body = body + data
# msg.add_header('reply-to', "replyto@gmail.com")


msg['To'] = ",".join(toaddr)
# msg['Cc'] = ",".join(fakeCcList)
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
