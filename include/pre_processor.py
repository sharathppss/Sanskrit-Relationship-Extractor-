# -*- coding: utf-8 -*-
from include import root_extractor as rx
#from sets import Set
import string

def reverse_dictionary(dic): 
    """Function to reverse a dictionary.

    Parameters
    ----------
    dic : An input dictionary of the format {key: [value_1, value_2, ...], ...}

    Returns
    -------
    result : Dictionary with the format {value_1: key, value_2: key, ...}
    """ 
    
    result = {}
    root_keys = dic.keys()
    for element in root_keys:
        name_keys = dic[element]
        for name in name_keys:
            result[name]=element
    return result

def find_relation_tuples(shloka, names_dict, relation_dict, data_type): 
    """Function that extracts the features(words in the shloka) for a name pair 
    if they are related. 

    Parameters
    ----------
    shloka : A segment of Sanskrit text.
    names_dict : A dictionary that contains synonym as key and the 
                corresponding name as value.
    relation_dict: A dictionary that contains 'name_1|name_2' as key and the 
                    relation between name_1 and name_2 as value.
    data_type : A string that specifies whether data is of type 'train' or 
                'test'.

    Returns
    -------
    result : A list of the format [name pair, relationship, features] if 
            data_type is 'train'.
            A lsit of the format [name_pair, features] if data_type is 'test'.
    """
    
    # strip punctuations and replace with space
    shloka = shloka.translate(string.maketrans(",:", "  ")).strip() 
    tokens = shloka.split()
    names = set()
    result = []
    relation = set()
    for token in tokens:
        root = token
        names_dict_keys = names_dict.keys()
        if root in names_dict_keys:
            names.add(names_dict[root])
    encountered_name_list = []
    for name_1 in names:
        encountered_name_list.append(name_1)
        for name_2 in [x for x in names if x not in encountered_name_list]:
            if data_type == "train":
                key = name_1 + "|" + name_2
                key_reverse = name_2 + "|" + name_1
                if key in relation_dict:
                    relation = relation_dict[key]
                elif key_reverse in relation_dict:
                    relation = relation_dict[key_reverse]
                else:
                    return result
                features = [x for x in tokens]
                #first arg is name pair, second in relationship between them, 
                #final is the list of all tokes in the sentence
                result.append([[name_1, name_2], relation, features]) 
            else:
                if name_1 in tokens and name_2 in tokens:
                    features = [x for x in tokens]
                    print name_1, name_2
                    for xx in tokens:
                        print xx
                    print "\n"
                    result.append([[name_1, name_2], features])
    return result

if __name__ == "__main__":
    d = {"ram":["ram","shriram","shrihari","hareram"],"sita":["sita","lela",
        "lelavati"]}
    x = reverse_dictionary(d)
    print(x)
    print(find_relation_tuples("ram and sita sitting in a tree", x, 
        {"sita|ram":"married"}))
# We can segment the input text file with "|" symbol as a list of sentences 
# and each is passed to find_relation_tuples
#Use find list to generate names_all argument mentioned.

