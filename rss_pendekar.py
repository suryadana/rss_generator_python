#!/usr/bin/python
import PyRSS2Gen
import requests
from datetime import datetime
from HTMLParser import HTMLParser
import time
class DataRSS():
def __init__(self):
self.items = []
def set_items(self, title, url, desc):
self.items.append((title, url, desc, datetime.now(),))
class MyHTMLParser(HTMLParser):
def __init__(self):
HTMLParser.__init__(self)
self.triger_title = 0
self.triger_desc = 0
self.triger_title_item = 0
self.triger_desc_item = 0
self.data = {
'title' : "",
'items' : {
'title' : "",
'desc' : [],
},
}
self.urls = []
def handle_starttag(self, tag, attrs):
if tag == "title":
self.triger_title += 1
elif tag == "a":
for attr in attrs:
if attr[0] == "href":
self.urls.append(attr[1])
elif tag == "h1" or tag == "h2" or tag == "h3" or tag == "h4":
self.triger_title_item = 1
elif tag == "p":
self.triger_desc_item = 1
def handle_endtag(self, tag):
if tag == "title" and self.triger_title:
self.triger_title -= 1
elif tag == "h1" or tag == "h2" or tag == "h3" or tag == "h4":
self.triger_title_item = 0
elif tag == "p":
self.triger_desc_item = 0
def handle_data(self, data):
if self.triger_title:
self.data['title'] = data
elif self.triger_title_item:
self.data['items']['title'] = data
elif self.triger_desc_item and len(self.data['items']['desc']) < 4:
self.data['items']['desc'].append(data)

def gen_rss(data, title, url):
def list_to_str(data):
r = ""
for t in data:
r = r+t
return r
def get_second():
date = datetime.now()
return str(date.second)
rss = PyRSS2Gen.RSS2(
title = title,
link = url,
description = "New RSS for "+title+" (Generate by Pendekar Langit)",
lastBuildDate= datetime.now(),
items = [PyRSS2Gen.RSSItem(title = d[0],link = d[1],description = list_to_str(d[2]),pubDate = d[3]) for d in data],
)
rss.write_xml(open(url.replace("http://", "").split(".", 1)[0]+".xml", "w"))
return url.replace("http://", "").split(".", 1)[0]+".xml"
def fix_url_list(url, urls):
fix_list_first = []
fix_list_second = []
for uri in urls:
if uri.split("/", 1)[0] == url:
fix_list_first.append(uri)
elif uri[:4] != "http" and uri[:1] == "?" :
fix_list_first.append(uri)
elif uri[:4] != "http" and uri[:1] != "?":
fix_list_first.append(uri)
fix_list_first = list(set(fix_list_first)) 
for uri in fix_list_first:
if uri[:4] != "http" and uri[:1] == "?":
fix_list_second.append(url+"/index.php"+uri)
elif uri[:4] != "http" and uri[:1] != "?":
fix_list_second.append(url+"/"+uri)
else:
fix_list_second.append(uri)
return fix_list_second
def get_html(url):
headers = {
'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
}
data = requests.get(url, headers=headers)
html = data.content
return html
def auto_ping(title, url, url_rss):
url = "http://pingomatic.com/ping/?"
for x in range(1,10):
requests.get(url+"title="+title+"&blogurl="+url+"&rssurl="+url_rss+"&chk_weblogscom=on&chk_blogs=on&chk_feedburner=on&chk_newsgator=on&chk_myyahoo=on&chk_pubsubcom=on&chk_blogdigger=on&chk_weblogalot=on&chk_newsisfree=on&chk_topicexchange=on&chk_google=on&chk_tailrank=on&chk_skygrid=on&chk_collecta=on&chk_superfeedr=on")
time.sleep(900)
def main():
parser = MyHTMLParser()
data_rss = DataRSS()
print "RSS is running, status OK !!"
while True:
urls = None
url = 'YOU_URL'
parser.feed(get_html(url))
title = parser.data['title']
urls = parser.urls
urls = fix_url_list(url, urls)
if len(urls) > 0:
for url in urls:
parser.feed(get_html(url))
data = parser.data 
data_rss.set_items(data['items']['title'], url, data['items']['desc'])
f_name = gen_rss(data_rss.items, title, url)
# Change folder name rss to your folder
url_rss = url+"/rss/"+f_name
auto_ping(title, url, url_rss)
time.sleep(7200)
main()
# RSS Generator and auto ping to pingomatic, if you went service running in backgroud you can use cron job.
# Create by Pendekar Langit
