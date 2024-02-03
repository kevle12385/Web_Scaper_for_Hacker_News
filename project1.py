import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import ssl

now = datetime.now()

# email content placeholder
content = ''


def extract_news(url):
    print('Extracting hacker news stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories:<b>\n' + '<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', ' valign': ''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text != 'More' else '')
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>---------<br>')
content += ('<br>---------<br>')

print('Composing Email')

SERVER = 'smtp.gmail.com'
PORT = 587  # PORT NUMBER FOR GMAIL
FROM = '#'  # Email
TO = '#'  # Email
PASS = '#'  # Google App Password, not regular password


msg = MIMEMultipart()

msg['Subject'] = ('Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' +
                  str(now.year))
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
context = ssl.create_default_context()

print('Initializing Server...')
server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP('smtp.gmail.com', 465)
server.set_debuglevel(1)  # 1 to see error meesages if bugs
server.ehlo()
server.starttls(context=context)
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email sent!')

server.quit()



































