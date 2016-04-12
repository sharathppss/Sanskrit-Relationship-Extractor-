# -*- coding: utf-8 -*-
import requests
import re
import bs4
import xml.etree.ElementTree as ET
import sys
import time
start=time.time()
sys.stdout = open('output.txt', 'w')
def finder(inp):
    print "word:"+inp
    response = requests.post("http://sanskrit.uohyd.ac.in/cgi-bin/scl/morph/morph.cgi", data={'morfword':inp, "encoding":"Unicode"})
    t=response.text
    t=t.encode("utf-8")
    try:
        #t=t.replace("\n","")
        #t=re.sub(r"(<script>).*(</script>)","",t)
        tree=bs4.BeautifulSoup(t,"lxml")
        td=tree.find("td")
        if td==None:
            return tree.find("tr").string.rstrip()
        a=td.find("a")
        if a==None:
            x=tree.find("td").string.split()[0]
        else:
            x=a.string.split()[0]
        #td=re.findall("(<td.*>)(.*)(<\/td>)",t)
        #s=re.findall("<a.*<\/a>",td[0][1])
        #if s==[]:
        #    res=td[0][1]
        #else:
        #    res=re.findall("(>)(.*[^<])(<\/a)",s[0])[0][1]
        return x
    except:
        print "Error:"+t
        return inp


with open("input.txt","r") as f:
    s=f.readlines()
    for i in s:
        q=i.split("|")
        for u in q:
            a=u.split()
            for d in a:
                print("root:"+finder(d).encode("utf-8"))
end=time.time()
print(str(end-start))
#print finder("विश्वामित्रम्")
