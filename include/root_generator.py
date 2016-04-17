# -*- coding: utf-8 -*-
import os
import root_extractor as rx
import codecs as cdec
import glob
import re
import time

start=time.time()
def read_file (root,filename):
    all = open (filename, "r").read()
    outname = root+filename.split("/")[-1] + "_processed.txt"
    fdw = open (outname, "w").close()
    fdw = open (outname, "a")
    shloka = ""
    root_shloka = ""
    sholkas=all.split("||")
    for sholk in sholkas:
        o_sholka=[]
        lines=sholk.split("\n")
        for line in lines:
            #m=re.search(".*([२४१३०७]).*",line)
            l=line.decode("utf-8")
            m=re.search(ur".*[\u0966-\u096F].*",l)
            if (m!=None) or line=="":
                #print m.group(0)
                continue
            for word in line.split():
                if word=="|":
                    continue
                temp=rx.root_ext(word)
                o_sholka.append(temp.encode("utf-8"))
        print(" ".join(o_sholka))
        fdw.write(" ".join(o_sholka)+"\n")
    fdw.close()
    #for line in fd:
    #    if line=="\n":
    #    shloka += line
    #    words = shloka.split()
    #    for word in words:
    #
    #        temp = rx.root_ext (word)
    #       root_shloka += temp
    #        root_shloka += " "
    #    if "||" in line:
    #        print "Sholka = ", shloka
     #       words = shloka.split()
      ##         temp = rx.root_ext (word)
        #        root_shloka += temp
         #       root_shloka += " "
          #  shloka = ""
           # fdw.write (root_shloka)
            #fdw.write ("||")
            #root_shloka = ""

if __name__ == "__main__":
    files=glob.glob("../data/corpus/raw/suhas/*")
    r_files=[f.split("/")[-1] for f in files]
    for f in files:
        if os.path.isfile(f):
            read_file ("../data/corpus/processed/suhas/",f)
    end=time.time()
    print(str(end-start))
