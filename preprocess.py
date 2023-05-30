import json
import ijson
import os
import csv
import spacy
from utils import *
import numpy as np
from eval import val


def filter(json_path,target_path,conf):
    '''
    record: [id,title,doi,issue,keywords,lang,venue,year,n_citation,
        page_start', 'page_end', 'volume', 'issn', 'isbn', 
        'url', 'abstract', 'authors', 'doc_type', 'fos', 'indexed_abstract']
    '''
    cnt=0
    data=[]
    with open(json_path, "r") as f:
        for record in ijson.items(f, "item"):
            #print(type(record))
            if "references" in record.keys()and record["year"]>2010 and record["lang"]=="en" and record["venue"]["raw"] in conf and len(record["references"])>0:
                if "fos" in record.keys():
                    for word in record["fos"]:
                        word["w"]=str(word["w"])
                data.append(record)
                cnt+=1
                #print(record["year"])
            #if cnt==5:
            #    break    
            
            
        with open(target_path,'w',encoding='utf8') as f2:
            json.dump(data,f2,ensure_ascii=False,indent=2)
    
    print(cnt)


def extract_edges(json_path,root_path):
    """
    Extract Paper-Paper Edge and Author-Paper Edge
    """
    nlp = spacy.load('en_core_web_lg')
    data=load_json(json_path)
    #print(data)
    paper_nodes=[]
    author_nodes=[]
    institute_nodes=[]
    for article in data:
        paper_nodes.append(article["id"])
    paper_edges=[]
    author_edges=[]
    
    for article in data:
        for ref in article["references"]:
            if ref in paper_nodes and {"Source":article["id"],"Target":ref} not in paper_edges:
                #similarity=nlp(article["abstract"]).similarity(nlp(ref))
                paper_edges.append({"Source":article["id"],"Target":ref})
        for author in article["authors"]:
            if author["id"] not in author_nodes:
                author_nodes.append(author["id"])
            if author["org"] not in institute_nodes:
                institute_nodes.append(author["org"])
            author_edges.append({"Source":article["id"],"Target":author["id"]})
    
    write_csv(paper_edges,os.path.join(root_path,"ai_paper_edges.csv"),paper_edges[0].keys())
    write_csv(author_edges,os.path.join(root_path,"ai_author_edges.csv"),author_edges[0].keys())
                
    print("paper_nodes:",len(paper_nodes))
    #print("institute_nodes",len(institute_nodes))
    print("author_nodes:",len(author_nodes))
    print("paper_edges:",len(paper_edges))
    print("author_edges:",len(author_edges))
            

def extract_nodes(json_path,root_path):
    """
    Extract paper and author nodes
    """
    
    data=load_json(json_path)
    #print(data)
    paper_nodes=[]
    author_nodes=[]
    for article in data:
        #print(article["id"])
        #print(article["title"])
        #print(article["keywords"])
        #print(article["abstract"].strip(""))
        #print(article["doc_type"])
        paper_nodes.append({
            "id":article["id"],
            "title":article["title"],
            "keywords":article["keywords"],
            "venue":article["venue"]["raw"],
            "year":article["year"],
            "n_citation":article["n_citation"],
            "abstract":article["abstract"].replace('"',''),
            "doc_type":article["doc_type"]
        }
        )
    author_ids=[]
    for article in data:
        for author in article["authors"]:
            if author["id"] not in author_ids:
                author_ids.append(author["id"])
                author_nodes.append({"id":author["id"],"name":author["name"]})
                
    print("paper_nodes:",len(paper_nodes))
    print("author_nodes:",len(author_nodes))

    write_csv(paper_nodes,os.path.join(root_path,"ai_paper_nodes.csv"),paper_nodes[0].keys())
    write_csv(author_nodes,os.path.join(root_path,"ai_author_nodes.csv"),author_nodes[0].keys())

def instit_matching(instit1,institut_path):
    """
    Entity Matching between two datasets
    """
    
    
    instituts=load_json(institut_path)
    instituts_=[]
    for institut in instituts:
        instituts_.append(institut["name"])
    
    if instit1=="":
        return None,100
    min_dist=1000
    current_len=0
    for word in instituts_:
        #similarity = nlp(normalize(instit1)).similarity(nlp(normalize(word)))
        #print(word)
        #print(instit1)
        index,dist=matching(instit1,word)
        if dist<=min_dist:
            if dist==min_dist and current_len>len(normalize(instit1)[index]):
                #print(word) 
                continue  
            min_dist=dist
            relation=[instit1,word]
            current_len=len(normalize(instit1)[index])
    if "berkeley" in normalize(instit1):
        relation[1]="Univ. of California - Berkeley"
    if " " not in normalize(relation[1])[0] and min_dist!=0:  ###saarland maryland
        #print(min_dist,normalize(relation[1]),normalize(instit1))
        return None,100
    return relation,min_dist

def extract_affiliation(json_path,root_path,institut_path):
    
    #nlp = spacy.load('en_core_web_lg')
    
    data=load_json(json_path)
    
    author_nodes=[]
    affiliation=[]    
    cnt=0
    for article in data:
        for author in article["authors"]:
            #if author["id"]!="54409dc7dabfae805a6deff1":
            #    continue
                #print(333333333333333333)
            #print(111111111111)
            if author["id"] not in author_nodes:
                author_nodes.append(author["id"]) 
                instit1=author["org"]
                relation,min_dist=instit_matching(instit1,institut_path)
                if min_dist<=5 and relation is not None:
                    if {"Author":author["id"],"Institut":relation[1]} not in affiliation:
                        print({"Author":author["id"],"Institut":relation[1]})
                        affiliation.append({"Source":author["id"],"Target":relation[1]})
    print(len(affiliation))
    
    #print(cnt)
    write_csv(affiliation,os.path.join(root_path,"affiliation_.csv"),affiliation[0].keys())

def institut2community(json_path,community_path,root_path,institut_path):
    data=load_json(json_path)
    instituts=load_json(institut_path)
    
    community_reader=read_csv(community_path)
        
    instituts_={}
    for institut in instituts:
        instituts_[institut["name"]]={"oth":0} ## count for the community "other"
    instituts_["others"]={"oth":0}
    
    
    for i in range(len(data)):
        #print(article["id"])
        article=data[i]
        line=community_reader[i+1][0]
        #print(line)
        id,com_id,method,problem=line.split("; ")[0],line.split("; ")[1],line.split("; ")[2],line.split("; ")[3]
        #print("com_id:",com_id)
        #print(problem)
        authors=article["authors"]
        affliation=[]
        for author in authors:
            #print(author["org"])

            relation,min_dit=instit_matching(author["org"],institut_path)
            if min_dit<=5 and relation is not None:
                affliation.append(relation[1])       
            else:
                affliation.append("others")
        print(affliation)
        if problem=="other":
            for inst in set(affliation):
                instituts_[inst]['oth']+=1
        else:
            for inst in set(affliation):
                if com_id in instituts_[inst].keys():
                    instituts_[inst][com_id]+=1
                else:
                    instituts_[inst][com_id]=1
        #break
    
    with open(os.path.join(root_path,"inst_comm.json"),'w',encoding='utf8') as f2:
        json.dump(instituts_,f2,ensure_ascii=False,indent=2)
    

def author2author(paper_edge_path,json_path,root_path,institut_path):
    """
    Generate Edges for hyper-nodes (authors). 
    For each paper-paper edge, finding authors and establish the connection
    """
    
    data=load_json(json_path)
    
    reader=read_csv(paper_edge_path)
    
    references={}
    
    weight={}
    
    author_edges=[]
    author_ids=[]
    author_nodes=[]
    
    for article in data:
        id=article["id"]
        references[id]=article["authors"]
        
    for edge in reader[1:]:
        
        source=edge[0]
        target=edge[1]
        #print(source,target)
        source_authors=references[source]
        target_authors=references[target]
        #print(source_authors)
        #print(target_authors)
        for au_s in source_authors:
            for au_t in target_authors:
                author_edge=au_s["id"]+"-"+au_t["id"]
                if au_s["id"]=="" or au_t["id"]=="" or au_t["id"]==au_s["id"]:
                    continue
                elif author_edge not in weight.keys():
                    weight[author_edge]=1
                    if au_s["id"] not in author_ids:
                        relation,min_dist=instit_matching(au_s["org"],institut_path)
                        if min_dist<=5 and relation is not None:
                            au_s["org"]=relation[1]
                        else:
                            au_s["org"]="None"
                        author_nodes.append(au_s)
                        author_ids.append(au_s["id"])
                    if au_t["id"] not in author_ids:
                        relation,min_dist=instit_matching(au_t["org"],institut_path)
                        if min_dist<=5 and relation is not None:
                            au_t["org"]=relation[1]
                        else:
                            au_t["org"]="None"
                        author_nodes.append(au_t)
                        author_ids.append(au_t["id"])    
                else:
                    weight[author_edge]+=1
    for key,value in weight.items():
        author_edges.append({"Source":key.split("-")[0],"Target":key.split("-")[1],"Weight":value})
    
    print(len(author_nodes))
    print(len(author_edges))
        
    write_csv(author_edges,os.path.join(root_path,"author2author_edges.csv"),author_edges[0].keys())
    write_csv(author_nodes,os.path.join(root_path,"author2author_nodes.csv"),author_nodes[0].keys())
    


if __name__=="__main__":
    json_path="dblp_v14.json"
    root_path="./cleaned_data"
    cleaned_path=os.path.join(root_path,"ai_conference.json")
    institut_path=os.path.join(root_path,"institut_ranking.json")
    conf=["ACL","EMNLP","AAAI","IJCAI","ICML","CVPR","ICCV","ECCV",'ACCV',"NIPS"]
    #conf=["CVPR","ICCV","ECCV",'ACCV',"WACV"]
    #filter(json_path,cleaned_path,conf)    
    print("Filter Process Done !")
    #extract_edges(cleaned_path,root_path)
    #extract_nodes(cleaned_path,root_path)
    
    #author2author("cleaned_data/ai_paper_edges.csv",cleaned_path,root_path,institut_path)
    #extract_affiliation(cleaned_path,root_path,institut_path)
    institut2community(cleaned_path,os.path.join(root_path,"community.csv"),root_path,institut_path)
    
    
    
    
    
    
    
    
    
    
    
    #gen_val(cleaned_path,root_path)
    #val(os.path.join(root_path,"validation.csv"),os.path.join(root_path,"affiliation_.csv"))
    

    
    
    #=======================================================================================
    #                               Just For Test
    #word="Xi An Jiao Tong Univ, Sch Math & Stat, Xian, Peoples R China"
    #instit1="Xi'an Jiaotong University"
    #word="Western Michigan University"
    #instit1="KTH Royal Inst Technol, CVAP, Stockholm, Sweden"
    #index,dst=matching(instit1,word)
    #print(index,dst)
    #if " " not in normalize(instit1_norm)[0] and dist!=0:
    #    print(True)
    #print(dist)
    #=======================================================================================
