import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.header import Header

from email.MIMEText import MIMEText
from email.utils import formataddr
import json

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

url = ("https://financialmodelingprep.com/api/v3/quote/%5EDJI?apikey=a9a0e2e937837eb7414a9dee88b2f09a")

name = get_jsonparsed_data(url)[0]['name']
price = get_jsonparsed_data(url)[0]['price']
changesPercentage = get_jsonparsed_data(url)[0]['changesPercentage']
change = get_jsonparsed_data(url)[0]['change']

data = "Name: {}\nPrice: {}\nChange: {}\nChanges Percentage: {}".format(name, price, change, changesPercentage)


 
#Enter email information
fromaddr = "lynlynlynt@gmail.com"
password = ""
toaddr = ['mingxin.ou@gmail.com','centuryib100@gmail.com']
# fakeCcList = ['fakecc@gmail.com']
# bccList = ['bcc@gmail.com']
displayName = 'Stock Master'


msg = MIMEMultipart()
msg['From'] = formataddr((str(Header(displayName, 'utf-8')), fromaddr))


#Edit subject, message, and reply-to information here
msg['Subject'] = "Daily Stock Update"
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
