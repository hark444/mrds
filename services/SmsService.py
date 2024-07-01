import urllib.request
import urllib.parse
from django.conf import settings

class SmsService:
    def __init__(self):
        self.sender = settings.SMS['sender']
        self.apikey = settings.SMS['apikey']
        self.apiurl = settings.SMS['apiurl']

    def send(self, numbers,  message, sender=None):
        if sender is None:
            sender = self.sender
        data = urllib.parse.urlencode({'apikey': self.apikey, 'numbers': numbers,
                                       'message': message, 'sender': sender})
        data = data.encode('utf-8')
        request = urllib.request.Request(self.apiurl)
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        return (fr)