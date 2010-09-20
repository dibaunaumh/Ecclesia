import urllib
import urllib2
import sys

def send_mail(sender, to, subject, body):
    gateway_send_mail(sender, to, subject, body)
    
def gateway_send_mail(sender, to, subject, body):
    url = 'http://ekkli-gateway.appspot.com/send_notification/'
    params = {'sender' : sender,
              'to' : to,
              'subject' : subject,
              'body': body }
    
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data)
    try:
        response = urllib2.urlopen(req)
    except:
        print sys.exc_info()[1]
    #the_page = response.read()