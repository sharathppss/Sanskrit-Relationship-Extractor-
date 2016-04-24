# -*- coding: utf-8 -*-
from include import pre_processor as p
import glob
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import json
import codecs as cd
from collections import Set
from sklearn.svm import SVC

out = open("features.txt", "w")
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
            relation_synonyms[tokens[0]] = tokens[1:]

def vectorize(training_data, test_data):
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
        if rel_class == "पुत्र":
            classes.append(rel_class)
        else:
            classes.append("NR")
        corpus.append(' '.join(tokens))
    vectorizer = TfidfVectorizer(min_df=0, sublinear_tf=True, use_idf=True)
    X = vectorizer.fit_transform(corpus)
    print(X.toarray())
    svm = SVC(C=10, gamma=0.0, kernel='linear')
    svm.fit(X, classes)
    relationship_reverse_dict = p.reverse_dictionary(relation_synonyms)
    for data in test_data:
        named_pair = data[0]
        tokens = data[2]
        test_corpus.append(' '.join(tokens))
        dict_key = named_pair[0] + '|' + named_pair[1]
        dict_key_r = named_pair[1] + '|' + named_pair[0]
       
    Xtest = vectorizer.transform(test_corpus)
    prediction = svm.predict(Xtest)
    corr1 = 0
    corr2 = 0
    total = 0
    for i in range(len(prediction)):
        if prediction[i] == test_data[i][1]:
            corr1 += 1
        elif prediction[i] == "NR" and test_data[i][1] != "पुत्र":
            corr2 += 1
        total += 1
        print (test_data[i][0][0], test_data[i][0][1], prediction[i], 
            test_data[i][1])
    print float(corr1+corr2)/total#, corr1, corr2, total

def split_data(data, train, test):
    """Function to split data into two parts one for training and the other for 
    testing based on the named pairs contained in the data. 
    The SVM is trained on a few name pairs and then tested upon name pairs with
    erlationships similar to the ones in training. 

    Parameters
    ----------
    data : A list of list containing named pairs and the corresponding features.
    train : A list of name pairs that the SVM should be trained upon.
    test : A list of name pairs that the SVM should be tested upon.  
    
    Returns
    -------
    Two lists, one containing the data for training and the other containing data 
    for testing.
    """

    train_result = []
    test_result = []
    for d in data:
        if [d[0][0], d[0][1]] in train:
            train_result.append(d)
        elif[d[0][0], d[0][1]] in test:
            test_result.append(d)
    return train_result, test_result

if __name__=="__main__":
    train_l = [["भरत","कैकेयी"],["कैकेयी","भरत"],["राम","भरत"],["भरत","राम"]]
    test_l = [["राम","कौसल्या"],["कौसल्या","राम"],["राम","सीता"],["सीता","राम"]]
    extract_relationships()
    name_dict = p.reverse_dictionary(name_synonyms)
    data = []
    files = glob.glob("data/corpus/processed/*/*")
    for f in files:
        if os.path.isfile(f):
            data = data + extract_features(f, name_dict, "train")
    files = glob.glob("data/corpus/processed/test_data/*")
    for t in data:
        out.write(t[0][0] + ":" + t[0][1] + ":" + t[1] + ":")
        for d in t[2]:
            out.write(d + ":")
        out.write("\n")
    out.close()
    out = cd.open("features.txt","r","UTF-8")
    lines = out.readlines()
    data = []
    for l in lines:
        l = l.encode("UTF-8")
        x = l.split(":")
        data.append([[x[0], x[1]], x[2], x[3:]])
    train_data,test_data = split_data(data, train_l, test_l)
    vectorize(train_data, test_data)
# train_data is a list of training data with each element having 
# [[name1,name2],relationship,[<list of words in sentence>]]
