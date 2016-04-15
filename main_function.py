# -*- coding: utf-8 -*-
from include import pre_processor as p
import glob
import os
from sklearn.feature_extraction.text import CountVectorizer
import json
from sklearn.svm import SVC

corpus = []
classes = ['NR']

def file_extract(file,n_dict,n_rel):
    res=[]
    with open(file,"r") as f:
        lines=f.read()
        segments=lines.rstrip().split("|")
        print(segments)
        for s in segments:
            res=res+p.find_relation_tuples(s.rstrip(),n_dict,n_rel)
    return res


def vectorize(training_data):
    global corpus, classes
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
    svm = SVC(C=1000000.0, gamma=0.0, kernel='rbf')
    svm.fit(X, classes)
#    test_corpus = open('test','r').readline().rstrip()
#    t = []
#    t.append(test_corpus)
#    Xtest = vectorizer.transform(t)
#    pred = svm.predict(Xtest)
#    print(pred)

if __name__=="__main__":
    d={'राम':['राम'], 'सीता':['सीता']}
    r={'राम|सीता':'पतिः'}
    name_dict=p.find_list(d)
    train_data=[]
    files=glob.glob("data/*")
    for f in files:
        if os.path.isfile(f):
            train_data=train_data+file_extract(f,name_dict,r)
#    with open('x','w') as fd:
#        fd.write(json.dumps(train_data))
    vectorize(train_data)
#train_data is a list of training data with each element having [[name1,name2],relationship,[<list of words in sentence>]]
