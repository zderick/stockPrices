import requests
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.header import Header

from email.MIMEText import MIMEText
from email.utils import formataddr
import json
from datetime import date





def get_data(response, name):
   return response.json()[0][name] 


headers = {
                'Content-Type': 'application/json'
                        }
response = requests.get("https://api.tiingo.com/tiingo/daily/DIA/prices?token=12d898a99f0a48f6c3483cd1f30e8c53dbb854e0",
                                            headers=headers)





name = "DIA ETF"
price = get_data(response, 'close')

change = get_data(response, 'close') - get_data(response, 'open')
changesPercentage = (change / get_data(response, 'open'))



data = "Name: {}\nPrice: {}\nChange: {}\nChanges Percentage: {:.2%}".format(name, price, change, changesPercentage)


today = date.today()
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
