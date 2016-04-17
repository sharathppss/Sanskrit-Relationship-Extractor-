# -*- coding: utf-8 -*-
from include import pre_processor as p
import glob
import os
from sklearn.feature_extraction.text import CountVectorizer
import json
from sklearn.svm import SVC

out=open("features.txt","w")
corpus = []
test_corpus = []
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
    global corpus, classes, test_corpus
    for data in training_data:
        named_pair = data[0]
        rel_class = data[1]
        tokens = data[2]
        classes.append(rel_class)
        corpus.append(' '.join(tokens))
        #corpus.append(' '.join(tokens))
    vectorizer = CountVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus)
    print(X.toarray()) 
    svm = SVC(C=1, gamma=0.0, kernel='rbf')
    svm.fit(X, classes)
    for data in test_data:
        named_pair = data[0]
        tokens = data[1]
        test_corpus.append(' '.join(tokens))
#    test_corpus = open('test','r').readline().rstrip()
#    t = []
#    t.append(test_corpus)
    Xtest = vectorizer.transform(test_corpus)
    pred = svm.predict(Xtest)
    for i in range(len(pred)):
        print training_data[i][0][0],training_data[i][0][1],pred[i]

if __name__=="__main__":
#    d={'राम':['राम'], 'सीता':['सीता']}
#    r={'राम|सीता':'पतिः'}
    extract_relationships()
    name_dict=p.find_list(name_syn)
    train_data=[]
    test_data=[]
    files=glob.glob("data/corpus/processed/suhas/*")
    files+=glob.glob("data/corpus/processed/sachin/*")
    files+=glob.glob("data/corpus/processed/sharath/*")
    #files=["data/input.txt"]
    for f in files:
        if os.path.isfile(f):
            train_data=train_data+file_extract(f,name_dict,relation_dict, "train")
    files=glob.glob("data/corpus/processed/sharath/*")
    for f in files:
        if os.path.isfile(f):
            test_data = test_data+file_extract(f,name_dict,relation_dict, "test")
#    with open('x','w') as fd:
#        fd.write(json.dumps(train_data))
    print("Train Data")
    for t in train_data:
        out.write(t[0][0]+":"+t[0][1]+":"+t[1]+":")
        for d in t[2]:
            out.write(d+":")
        out.write("\n")
    #print [x[1].encode("utf-8") for x in train_data]
    print(train_data)
    print("Test Data")
    print(test_data)
    #print [x.encode("utf-8") for x in test_data]
    vectorize(train_data,test_data)
#train_data is a list of training data with each element having [[name1,name2],relationship,[<list of words in sentence>]]
