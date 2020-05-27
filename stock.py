import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.header import Header

from email.MIMEText import MIMEText
from email.utils import formataddr
 
 
#Enter email information
fromaddr = "yourEmail@gmail.com"
password = "password"
toaddr = ['to@gmail.com']
# fakeCcList = ['fakecc@gmail.com']
# bccList = ['bcc@gmail.com']
displayName = 'Stock Master'


msg = MIMEMultipart()
msg['From'] = formataddr((str(Header(displayName, 'utf-8')), fromaddr))


#Edit subject, message, and reply-to information here
msg['Subject'] = "Daily Stock Update"
body = "The stock has just closed"
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