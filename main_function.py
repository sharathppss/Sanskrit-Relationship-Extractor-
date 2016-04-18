# -*- coding: utf-8 -*-
from include import pre_processor as p
import glob
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import json
import codecs as cd
from collections import Set
from sklearn.svm import SVC

out=open("features.txt","w")
corpus = []
classes = []
relation_dict = {}
name_syn = {}
relation_syn = {}

def file_extract(file,n_dict,n_rel,data_type):
    res=[]
    with open(file,"r") as f:
        lines=f.readlines()
        #segments=lines.rstrip().split("|")
        #print(segments)
        for s in lines:
            res=res+p.find_relation_tuples(s.rstrip(),n_dict,n_rel,data_type)
    return res

def extract_relationships():
    global relation_syn, relation_dict, name_syn
    with open('Relation.txt') as fd:
        for line in fd:
            tokens = [x.rstrip() for x in line.split('\t')]
            relation_dict[tokens[0] + '|' + tokens[2]] = tokens[1]
            name_syn[tokens[0]] = [tokens[0]]
            name_syn[tokens[2]] = [tokens[2]] #to do
    with open('RelationshipSynonyms.txt') as fd:
        for line in fd:
            tokens = [x.rstrip() for x in line.split("\t")]
            relation_syn[tokens[0]] = tokens[1:]

def vectorize(training_data,test_data):
    global corpus, classes
    test_corpus=[]
    tr=relation_dict
    tr_k=tr.keys()
    for data in training_data:
        named_pair = data[0]
        rel_class = data[1]
        tokens = data[2]
        if rel_class=="पुत्र":
            classes.append(rel_class)
        else:
            classes.append("NR")
        corpus.append(' '.join(tokens))
        #corpus.append(' '.join(tokens))
    vectorizer = TfidfVectorizer(min_df=0,sublinear_tf=True,use_idf=True)
    X = vectorizer.fit_transform(corpus)
    print(X.toarray()) 
    svm = SVC(C=10, gamma=0.0, kernel='linear')
    svm.fit(X, classes)
    r_s=relation_syn
    relationship_reverse_dict = p.find_list(relation_syn)
    g=relationship_reverse_dict.keys()
    for data in test_data:
        named_pair = data[0]
        tokens = data[2]
        test_corpus.append(' '.join(tokens))
        dict_key = named_pair[0] + '|' + named_pair[1]
        #dict_key=dict_key.decode("utf-8")
        #dict_key_r=dict_key_r.decode("utf-8")
        st=""
        #if dict_key in relation_dict:
        #    st=relation_dict[dict_key]
         #   rv=relation_dict[dict_key_r]
        #print "break"+"\n"
        #if st!="" and st in tokens:
        #    print named_pair,st

        #for word in tokens:
        #    if word in relationship_reverse_dict and (relationship_reverse_dict[word] == st or relationship_reverse_dict[word] == rv):
         #       print named_pair[0],named_pair[1],st
          #      break

    #for data in test_data:
    #    named_pair = data[0]
    #    tokens = data[1]
    #    test_corpus.append(' '.join(tokens))
        dict_key_r = named_pair[1] + '|' + named_pair[0]
        #if relation_dict[dict_key] in tokens or relation_dict[dict_key_r] in tokens:
         #   print named_pair, relation_dict[dict_key]
#    test_corpus = open('test','r').readline().rstrip()
#    t = []
#    t.append(test_corpus)
        
    Xtest = vectorizer.transform(test_corpus)
    pred = svm.predict(Xtest)
    print "break"+"\n"
    corr1=0
    corr2=0
    total=0
    for i in range(len(pred)):
        if pred[i]==test_data[i][1]:
            corr1+=1
        elif pred[i]=="NR" and test_data[i][1]!="पुत्र":
            corr2+=1
        total+=1
        print test_data[i][0][0],test_data[i][0][1],pred[i],test_data[i][1]," ".join(test_data[i][2])
    print float(corr1+corr2)/total,corr1,corr2,total

def split_data(data,train,test):
    train_res=[]
    test_res=[]
    for d in data:
        if [d[0][0],d[0][1]] in train:
            train_res.append(d)
        elif[d[0][0],d[0][1]] in test:
            test_res.append(d)
    return train_res,test_res

if __name__=="__main__":
#    d={'राम':['राम'], 'सीता':['सीता']}
#    r={'राम|सीता':'पतिः'}
    train_l=[["भरत","कैकेयी"],["कैकेयी","भरत"],["राम","भरत"],["भरत","राम"]]
    test_l=[["राम","कौसल्या"],["कौसल्या","राम"],["राम","सीता"],["सीता","राम"]]
    extract_relationships()
    name_dict=p.find_list(name_syn)
    data=[]
    files=glob.glob("data/corpus/processed/*/*")
    for f in files:
        if os.path.isfile(f):
            data=data+file_extract(f,name_dict,relation_dict, "train")
    files=glob.glob("data/corpus/processed/test_data/*")
    for t in data:
        out.write(t[0][0]+":"+t[0][1]+":"+t[1]+":")
        for d in t[2]:
            out.write(d+":")
        out.write("\n")
    out.close()
    out=cd.open("features.txt","r","UTF-8")
    lines=out.readlines()
    data=[]
    for l in lines:
        l=l.encode("UTF-8")
        x=l.split(":")
        data.append([[x[0],x[1]],x[2],x[3:]])
    train_data,test_data=split_data(data,train_l,test_l)
    vectorize(train_data,test_data)
#train_data is a list of training data with each element having [[name1,name2],relationship,[<list of words in sentence>]]
