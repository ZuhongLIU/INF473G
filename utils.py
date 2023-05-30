import json
import ijson
import os
import csv
import spacy
import re
import Levenshtein

def load_json(path):
    with open(path, mode="r",encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_csv(data,filename,headers):
    #fieldnames = ['Source', 'Target']
    # create and write to the CSV file
    with open(filename, 'w', newline='',encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def normalize(univ):
    
    univ=univ.lower()
    univ=univ.replace("the ","")
    
    abbre={
           "acad.":"academy",
           "acad":"academy",
           "technological":"technology",
           "technol.":"technology",
           "technol":"technology",
           "nat.":"national",
           "natl":"national",
           "nat":"national",
           "sci.":"science",
           "sci":"science",
           "calif":"california",
           "inst.":"institute",
           "inst":"institute",
           "informat":"informatics",
           "universite de":"university of ",
           "université":"university of ",
           "univ.":"university",
           "univ ":"university ",
           "univ":"university"
           }
    #pattern = r"\(.*?\)"  
    pattern=r"\((.*?)\)"
    #assert len(re.findall(pattern, univ))<2
    if len(re.findall(pattern, univ))>0:
        univ = re.findall(pattern, univ)[0]   
    for key,value in abbre.items():
        if key in univ and value not in univ:
            univ=univ.replace(key,value)
            #break
    #print(univ)    
    if ", " in univ:
        #print(111111111111111111)
        univ_l=univ.split(", ")
        #univ_l=[i for i in univ_l if " " in i]
    elif "," in univ:
        univ_l=univ.split(",")
    else:
        #print(univ)
        univ_l=[univ]
        #return [univ]
    for i in range(len(univ_l)): 
        if "university of " in univ_l[i]:
            univ_l[i]=univ_l[i].replace("university of ","")
        elif " university" in univ_l[i]:
            univ_l[i]=univ_l[i].replace(" university","")
        elif "university " in univ_l[i]:
            univ_l[i]=univ_l[i].replace("university ","")
        elif "of " in univ_l[i]:
            univ_l[i]=univ_l[i].replace("of ","")
    
    for i in range(len(univ_l)-1):
        univ_l.append(univ_l[i]+" - "+univ_l[i+1])
    
    return univ_l
    
    #univ=univ.strip(" ")

def matching(instit1,word):
    word_norm=normalize(word)[0]
    #print(word,word_norm)
    #dist=min([Levenshtein.distance(instit1_norm,word_norm) for instit1_norm in normalize(instit1)])
    instits_norm=normalize(instit1)
    similarity_list=[Levenshtein.distance(instit1_norm,word_norm) for instit1_norm in instits_norm]
    
    min_value=similarity_list[0]
    min_index=0
    for i in range(len(similarity_list)):
        if similarity_list[i]<=min_value:
            min_value=similarity_list[i]
            #if similarity_list[i]==min_value: #and len(instits_norm[i])<len(instits_norm[min_index]):
            #    continue
            min_index=i    
    
    return min_index,min_value

def similarity(nlp,instit1,word):
    flag=False
    #print(nlp(normalize(instit1)).ents)
    print(normalize(instit1))
    print(nlp(normalize(word)).ents)
    for i in nlp(normalize(instit1)).ents:
        
        for j in nlp(normalize(word)).ents:
            if i.text==j.text: 
                flag=True
        if flag:
            flag=False
        else:
            return False   
    return True                  


def read_csv(filename):
    with open(filename, 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        L=[]
        # Iterate over each row in the CSV file
        for row in reader:
            L.append(row)
    return L