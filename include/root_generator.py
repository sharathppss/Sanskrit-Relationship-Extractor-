# -*- coding: utf-8 -*-
import os
import root_extractor as rx
import codecs as cdec
import glob
import re
import time

start=time.time()
def read_file(root_directory, filename):
    """Function that extracts the root of all the words in a file
        and writes the output to a new file.

    Parameters
    ----------
    root_directory : path of the directory under which the processed file has 
                    to be written.
    filename : name of the file for which the root extraction has to be done. 
    """

    all = open (filename, "r").read()
    outname = root_directory + filename.split("/")[-1] + "_processed.txt"
    fdw = open (outname, "w").close()
    fdw = open (outname, "a")
    shloka = ""
    root_shloka = ""
    sholkas = all.split("||")
    for sholk in sholkas:
        o_sholka = []
        lines=sholk.split("\n")
        for line in lines:
            #m=re.search(".*([२४१३०७]).*",line)
            l = line.decode("utf-8")
            m = re.search(ur".*[\u0966-\u096F].*",l)
            if (m! = None) or line == "":
                #print m.group(0)
                continue
            for word in line.split():
                if word == "|":
                    continue
                temp=rx.root_ext(word)
                o_sholka.append(temp.encode("utf-8"))
        print(" ".join(o_sholka))
        fdw.write(" ".join(o_sholka)+"\n")
    fdw.close()

if __name__ == "__main__":
    files = glob.glob("../data/corpus/raw/aranyakhanda/shloka/6/*")
    r_files = [f.split("/")[-1] for f in files]
    for f in files:
        if os.path.isfile(f):
            read_file("../data/corpus/pr/aranyakhanda/6/",f)
    end = time.time()
    print(str(end-start))
