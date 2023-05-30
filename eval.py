import json
import ijson
import os
import csv
import spacy
from utils import *
import numpy as np


def gen_val(json_path,root_path):
    author_nodes=[]
    data=load_json(json_path)
    samples=[]
    cnt=0
    for article in data:
        for author in article["authors"]:
            #cnt+=1
            if author["id"] not in author_nodes:
                author_nodes.append(author["id"]) 
                
                if author["org"]!="":
                    samples.append({"id":author["id"],"Institut":author["org"]})
    #print(cnt)
    print(len(samples))        
    data_val=np.random.choice(samples, 200, replace=False)
    #print(data_val)
    write_csv(data_val,os.path.join(root_path,"validation1.csv"),data_val[0].keys())



def val(validation_path,affliation_path):
    val_reader=read_csv(validation_path)
    aff_reader=read_csv(affliation_path)
    sample_dict={}
    p=0
    for row in aff_reader[1:]:
        #print(row)
        sample_dict[row[0]]=row[1]
    
    for row in val_reader[1:]:
        #print(row)
        if row[0] not in sample_dict.keys() :
            if row[2]=="None":
                p+=1
            #else:
            #    print(row[1],row[2],None)
                #print(ld(normalize(row[1]),normalize("Univ. of California - Berkeley"))) 
            #    print(normalize(row[1]))
                #print(normalize("Univ. of California - Berkeley"))
                
        elif sample_dict[row[0]]==row[2]:
            p+=1
        else:
            print(row[1],row[2],sample_dict[row[0]])    
    print("Accuracy:",p/len(val_reader))
    
    
