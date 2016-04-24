# -*- coding: utf-8 -*-

import requests
import bs4
import time
import codecs as cs
start = time.time()

def root_ext(word):
    """Function to extract the root/stem of a given word using the 
    morphological analyzer tool at http://sanskrit.uohyd.ac.in.

    Parameters
    ----------
    word : a string whose root has to be extracted. 

    Returns
    -------
    The root(type string) of the word.  
    """

    print ("word:" + word)
    word = word.decode("utf-8")
    response = requests.post("http://sanskrit.uohyd.ac.in/cgi-bin/scl/morph/morph.cgi", data={'morfword':word, "encoding":"Unicode"})
    t = response.text
    t = t.encode("utf-8")
    try:
        tree = bs4.BeautifulSoup(t,"lxml")
        td = tree.find("td")
        if td == None:
            return word
        a = td.find("a")
        if a == None:
            x = tree.find("td").string.split()[0]
        else:
            x = a.string.split()[0]
        r = "".join([i for i in x if not i.isdigit()])
        return r
    except:
        return word

if __name__ == "__main__":
    out = cs.open("output.txt","w","utf-8-sig")
    with open("../data/input.txt","r") as f:
        shlokas = f.readlines()
        for shloka in shlokas:
            segments = shloka.split("|")
            for segment in segments:
                line = segment.split()
                for word in line:
                    out.write("root:" + root_ext(word))

    end = time.time()
    print(str(end-start))
    #print finder("विश्वामित्रम्")
