import json, urllib.request, xml.etree.ElementTree as ET, datetime
FEEDS=[("https://www.aljazeera.com/xml/rss/all.xml","Al Jazeera"),("https://www.aljazeera.net/feed/rss","الجزيرة")]
lists=[]
for url,src in FEEDS:
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        root=ET.fromstring(urllib.request.urlopen(req,timeout=20).read())
        lists.append([{"t":i.findtext("title").strip(),"s":src} for i in root.iter("item") if i.findtext("title")][:10])
    except Exception as e: print("skip",url,e)
items=[x for pair in zip(*lists) for x in pair] if len(lists)==2 else (lists[0] if lists else [])
if items:
    now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=4))).strftime("%Y-%m-%dT%H:%M+04:00")
    json.dump({"updated":now,"items":items},open("headlines.json","w"),ensure_ascii=False)
    print(len(items),"headlines")
