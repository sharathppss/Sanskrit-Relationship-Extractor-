from include import pre_processor as p
import glob

def file_extract(file,n_dict,n_rel):
    res=[]
    with open(file,"r") as f:
        lines=f.read()
        segments=lines.split("|")
        for s in segments:
            res=res+p.find_relation_tuples(s,n_dict,n_rel)
    return res

if __name__=="__main__":
    d={"ram":["ram","shriram","shrihari","hareram"],"sita":["sita","lela","lelavati"]}
    r={"sita|ram":"married"}
    name_dict=p.find_list(d)
    train_data=[]
    files=glob.glob("data/*")
    for f in files:
        train_data=train_data+file_extract(f,name_dict,r)

#train_data is a list of training data with each element having [[name1,name2],relationship,[<list of words in sentence>]]
