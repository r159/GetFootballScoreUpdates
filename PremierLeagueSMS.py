import time
import urllib2
import cookielib
from getpass import getpass
from bs4 import BeautifulSoup
import sys


def SMSDetails(DetailsOfMatch):
    if(len(DetailsOfMatch) > 1):
       strMessage = str(DetailsOfMatch[1])
       lenMsg =  len(strMessage)
       SendSMS(strMessage)
       if(lenMsg > 99):
        nLimit = 99
        for iMsg in range(0,len(strMessage),nLimit):
            SendSMS(strMessage[iMsg:iMsg+nLimit])
       else:
          SendSMS(strMessage)
    else:
        print "Not enough details to send SMS"

def SendSMS(Detail1):
    message = Detail1
    usernumber = "**********"
    passwrd = "****"
    ToNumber = "**********"
    #logging into SMS site
    url =  'http://site24.way2sms.com/Login1.action?'
    data = 'username='+usernumber+'&password='+passwrd+'&Submit=Sign+in'
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]
    try:
        usock = opener.open(url,data)

    except IOError:
        print "Error while logging In"
        sys.exit(1)

    jsessio_id = str(cj).split('~')[1].split(' ')[0]
    send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
    send_sms_data =  'ssaction=ss&Token='+jsessio_id+'&mobile='+ToNumber+'&message='+message+'&msgLen=136'
    opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jsessio_id)]

    try:
        sms_sent_page = opener.open(send_sms_url,send_sms_data)
    except IOError:
        print "Error while sending message"
        sys.exit(1)
    print "SMS has been sent."

#Method to get details from Site:
def GetScoreUpdate():
    url = "https://www.**********.com/football/live/2016/nov/05/manchester-city-v-middlesbrough-premier-league-live"
    content = urllib2.urlopen(url).read()
    removeTags =  ['a','b','strong','i'];
    contentList = []; # Append the contents to a list
    getDetailsSoup = BeautifulSoup(content,'html.parser')
    getData =  getDetailsSoup.find_all('div', attrs={'class':'block-elements block-elements--no-byline'})
    for Data in getData:
        DataInPara = Data.find('p')
        for tag in removeTags:
            for match in Data.findAll(tag):
                match.replaceWithChildren()
                contentList.append(DataInPara)


    if(len(contentList)> 0):
        SMSDetails(contentList)

#Run the App every 1 Min
count = 0
while(count < 120):
    print "Match Started, Mins Over" + str(count);
    GetScoreUpdate()
    count = count + 1
    time.sleep(60)


#End Of program