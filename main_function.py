# -*- coding: utf-8 -*-
from include import pre_processor as p
from sklearn.metrics import metrics
import glob
import os
from include import data_splitter as ds
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import SVC

corpus = []
classes = []
relation_dict = {}
name_synonyms = {}
relation_synonyms = {}

def extract_features(input_file, name_dict, data_type):
    """Function to extract features from the shlokas in a file. Extracts only the 
    shlokas that have a name pair in them. 

    Parameters
    ----------
    input_file : The file name of the input file from which the features have 
                to be extracted.
    name_dict : The dictionary that contains the various synonyms of a given
                name. The format is {synonym_1: name, synonym_2: name, ...}. 
    data_type: A string parameter that specifies whether the data in the file is for 
            for training or testing. 
    
    Returns
    -------
    A list of the format [name_pair, relationship, list of features]
    """
    result = []
    with open(input_file, "r") as f:
        lines = f.readlines()
        for shloka in lines:
            result = result + p.find_relation_tuples(shloka.rstrip(), name_dict,
                     relation_dict, data_type)
    return result

def extract_relationships():
    """Function that extracts the relationships and also synonyms for names and
    relationships from the files Relaion.txt and RelationshipSynonyms.txt.
    Populates the global variables relation_synonyms, relation_dict and
    name_synonyms.
    """

    global relation_synonyms, relation_dict, name_synonyms

    with open('Relation.txt') as fd:
        for line in fd:
            tokens = [x.rstrip() for x in line.split('\t')]
            relation_dict[tokens[0] + '|' + tokens[2]] = tokens[1]
            name_synonyms[tokens[0]] = [tokens[0]]
            name_synonyms[tokens[2]] = [tokens[2]] #to do
    with open('RelationshipSynonyms.txt') as fd:
        for line in fd:
            tokens = [x.rstrip() for x in line.split("\t")]
            relation_synonyms[tokens[0]] = tokens

def baseline(test_data): # baseline method implementation
    correct=0
    total=0
    actual=[]
    pred=[]
    v = ""
    for pt in test_data:
        syn_list=[]
        if pt[0][0]+"|"+pt[0][1] in relation_dict:
            v=relation_dict[pt[0][0]+"|"+pt[0][1]]
            if v in relation_synonyms:
                    syn_list=relation_synonyms[v]
            else:
                    syn_list=[v]
        else:
            v="NA"
        made=False
        if v=="NA":
            continue
        for x in syn_list:
            if x in pt[2]:
                pred.append(v)
                correct+=1
                made=True
        if made==False:
            pred.append("NA")
        actual.append(v)
        total+=1
    res=open("Result_approach2.txt","a")
    res.write("Technique:Baseline\n")
    res.write(metrics.classification_report(actual, pred))
    res.write("Baseline evaluation: "+str(float(correct)/total)+"\n")
    res.write("Total: "+str(total)+"Correct:"+str(correct)+"\n")

def vectorize(training_data, test_data,approach):
    """Function that creates vectors from the training and test data for the SVM,
    trains the SVM and makes predictions on the test data.
    Uses the svm module from scikit.

    Parameters
    ----------
    training_data : A list of lists of the format
                    [named_pair, relationship, list of features].
    test_data : A list of lists of the format [named_pair, list of features].
    """
    global corpus, classes
    test_corpus = []
    for data in training_data:
        named_pair = data[0]
        rel_class = data[1]
        tokens = data[2]
        classes.append(rel_class)
        corpus.append(' '.join(tokens).decode("UTF-8",errors="ignore").encode("UTF-8"))
    u_clases=set(classes)
    class_list=list(u_clases)
    vectorizer = TfidfVectorizer(min_df=3, sublinear_tf=True, use_idf=True)
    X = vectorizer.fit_transform(corpus)
    svm = SVC(C=10, gamma=0.0, kernel='linear')
    svm.fit(X, classes)
    for data in test_data:
        named_pair = data[0]
        tokens = data[2]    #change index to 2 if approach 2
        test_corpus.append(' '.join(tokens).decode("UTF-8",errors="ignore").encode("UTF-8"))
    Xtest = vectorizer.transform(test_corpus)
    prediction = svm.predict(Xtest)
    corr1 = 0
    corr2 = 0
    total = 0
    actual=[]
    predict=[]
    for i in range(len(prediction)):
        if test_data[i][0][0]+"|"+test_data[i][0][1] in relation_dict:
            v=relation_dict[test_data[i][0][0]+"|"+test_data[i][0][1]]
        else:
            v="NA"
        if v=="NA":
            continue
        if prediction[i] == v and prediction[i] in class_list:
            corr1 += 1
        elif prediction[i] == v:
            corr2 += 1
        total += 1
        actual.append(v)
        predict.append(prediction[i])
        print str(i)+":"+test_data[i][0][0]+":"+test_data[i][0][1]+":"+prediction[i]+":"+v
    res=open("Result_approach2.txt","w")
    res.write("Technique Approach"+str(approach)+"\n")
    res.write(metrics.classification_report(actual, predict))
    res.write("Accuracy:"+str(float(corr1+corr2)/total)+"\n")

def read_split_dict():
    '''
    Reads from split_data.txt which has the seperation of relationship into training pairs and test pairs.

    Returns
    -------
    train : A list of name pairs that the SVM should be trained upon.
    test : A list of name pairs that the SVM should be tested upon.
    '''
    train=[]
    test=[]
    lines=open("data/split_data.txt","r").readlines()
    for l in lines:
        tokens=l.split("|")
        if tokens[0]=="train":
            train.append([tokens[1],tokens[2]])
        else:
            test.append([tokens[1],tokens[2]])
    return train,test

def split_data(data):
    """Function to split data into two parts one for training and the other for
    testing based on the named pairs contained in the data.
    The SVM is trained on a few name pairs and then tested upon name pairs with
    erlationships similar to the ones in training.

    Parameters
    ----------
    data : A list of list containing named pairs and the corresponding features.

    Returns
    -------
    Two lists, one containing the data for training and the other containing data
    for testing.
    """
    train,test=read_split_dict()
    train_result = []
    test_result = []
    for d in data:
        if [d[0][0], d[0][1]] in train:
            train_result.append(d)
        else:
            test_result.append(d)
    return train_result, test_result

def approach_1(name_dict):# split at corpus class level approach.
    corpus_used=["aranyakhanda","ayodyakhanda","sundarakhanda","kishkindhasans","balakhanda"]
    data=[]
    files=[]
    for c in corpus_used:
        files+= glob.glob("data/corpus/processed/training/"+c+"/*")
    for f in files:
        if os.path.isfile(f):
            data = data + extract_features(f, name_dict, "train")
    data_t=[]
    files=[]
    for c in corpus_used:
        files+= glob.glob("data/corpus/processed/test/"+c+"/*")
    for f in files:
        if os.path.isfile(f):
            data_t = data_t + extract_features(f, name_dict, "test")
    return data,data_t

def approach_2(name_dict): # split at relation class level approach.
    corpus_used=["aranyakhanda","ayodyakhanda","sundarakhanda","balakhanda"]
    files=[]
    for c in corpus_used:
        files+= glob.glob("data/corpus/processed/training/"+c+"/*")
    for c in corpus_used:
        files+= glob.glob("data/corpus/processed/test/"+c+"/*")
    data=[]
    for f in files:
        if os.path.isfile(f):
            data = data + extract_features(f, name_dict, "train")
    out1=open("features.txt","w")
    for t in data:
        out1.write(t[0][0] + ":" + t[0][1] + ":" + t[1] + ":")
        for d in t[2]:
            out1.write(d + ":")
        out1.write("\n")
    out1.close()
    out2 = open("features.txt", "r")
    lines = out2.readlines()
    out2.close()
    data = []
    for l in lines:
        x = l.split(":")
        data.append([[x[0], x[1]], x[2], x[3:]])
    ds.run()
    train_data,test_data = split_data(data)
    return train_data,test_data

if __name__=="__main__":
    extract_relationships()
    name_dict = p.reverse_dictionary(name_synonyms)
    approach=2
    if approach==2:
        data,data_t=approach_2(name_dict)
    else:
        data,data_t=approach_1(name_dict)
    vectorize(data,data_t,approach)
    baseline(data_t)
