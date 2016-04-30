from collections import defaultdict
import operator
'''
This file reads the features.txt entries and splits the name pairs into test and train based on the percent provided as input
Output is written to data/split_data.txt,this has to be read for getting the dictonary of split.
'''
def run():
    print("data spliter has been run")
    ratio=0.75
    out = open("features.txt", "r")
    split_dict=defaultdict(lambda:defaultdict(list))
    split_dict_count=defaultdict(lambda:defaultdict(int))
    lines = out.readlines()
    data = []
    for l in lines:
        temp=[]
        x = l.split(":")
        temp.append([[x[0], x[1]], x[2], x[3:]])
        split_dict[x[2]][x[0]+"|"+x[1]]+=temp
        split_dict_count[x[2]][x[0]+"|"+x[1]]+=1
    total=0
    '''
    for x in split_dict_count.keys():
        print "Relationship:"+x
        c=0
        for y in split_dict_count[x].keys():
            print "Pair:"+y+" count:"+str(split_dict_count[x][y])
            c+=split_dict_count[x][y]
        print "Count for relationship:"+str(c)
        print "\n"
        total+=c
    print "Total:"+str(total)
    '''
    out1=open("data/split_data.txt","w")
    for rel in split_dict_count.keys():
        total=0
        count_list=sorted(split_dict_count[rel].items(), key=operator.itemgetter(1),reverse=True)
        for names in count_list:
            total+=names[1]
        train_count=int(ratio*total)
        count=0
        for names in count_list:
            if count>train_count or len(count_list)==1:
                kind="test"
            else:
                kind="train"
            name_list=names[0].split("|")
            out1.write(kind+"|"+name_list[0]+"|"+name_list[1]+"|"+rel+"\n")
            count+=names[1]
    out.close()

