import json
import urllib.request
import hashlib
from datetime import datetime, timedelta

SENDER = "zach.mcneilly@gmail.com"
SMTP = "smtp.google.com"
PASS = "SOME PASS"


class EmailAlerts(object):
    '''This class will track the variables neccesary for alerting an end user
    about new website updates.'''

    def __init__(self, recipient):
        '''The basic constructor method.'''
        self.recp = recipient
        self.sender = SENDER
        self.notifications = []

    def add_notify(self, site):
        '''This adds a site to the list of notifications to be sent.'''
        self.notifications.append(site)

    def can_notify(self):
        '''This method will check if any sites in the notifications variable
        are viable for sending a notification.'''
        result = False
        for site in self.notifications:
            cut_off = datetime.now() - timedelta(hours=23)
            if 'last' in site and \
                datetime.strptime(site['last'], "%Y%m%dT%H:%M") < cut_off:
                result = True
            else:
                self.notifications.remove(site)
        return result

    def send_notifications(self):
        '''This method will create an email and send it with links to the
        updated content.'''



    

def main():
    try:
        json_file = open('sites.json', 'r')
        sites = json.load(json_file)
        json_file.close()
    except IOError:
        print("No sites.json file!")
        print("See README for the format of the sites.json file")
        return 1
    for site in sites:
        site_resp = urllib.request.urlopen(sites[site]['rss_feed'])
        site_html = site_resp.read()
        site_md5 = hashlib.md5(site_html).hexdigest()
        if 'md5' in sites[site] and site_md5 == sites[site]['md5']:
            pass
        else:
            add_notify(sites[site])
            sites[site]['last'] = datetime.now().strftime("%Y%m%dT%H:%M")
        sites[site]['md5'] = md5
        json_file = open('sites.json', 'w')
        json_file.write(json.dump(sites, sort_keys=True,
                        indent=4, separators=(',', ': ')))
        json_file.close()

