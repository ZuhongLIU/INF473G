from matplotlib import pyplot as plt
import numpy as np
import os
from utils import *

def draw_pie(data,labels):
    #x=[200,500,1200,7000,200,900]
    paper_counts={}
    for conf in labels:
        paper_counts[conf]=0
    for article in data:
        if article["venue"]["raw"] in labels:
            paper_counts[article["venue"]["raw"]]+=1
    
    plt.title("Distribution of papers by conference")
    explode = [0.03 for i in range(len(labels))]
    #colors=["#C4F2C8","#E6DAF7","#E7EBC3","#D8DDF0","#EDD1D1","#C6F1D6","#E0F5B9","#FFBA92","#FF8080"] 
    colors=["#B02B2C","#D15600","#C79810","#73880A","#6BBA70","#3F4C6B","#356AA0","#D01F3C","#FF8080"]
    plt.pie(paper_counts.values(),labels=labels,colors=colors,autopct='%.2f%%',explode=explode,labeldistance=10, pctdistance=1.15)
    plt.legend(bbox_to_anchor=(0,0.5))
    #plt.show()
    plt.savefig(os.path.join("./vis/","pie_conf.jpg"))
    #return

def draw_bar(data,labels):
    
    paper_counts={}
    for conf in labels:
        paper_counts[conf]=0
    for article in data:
        #print(str(article["year"]))
        if str(article["year"]) in labels:
            paper_counts[str(article["year"])]+=1
    print(paper_counts)
    x=range(len(labels))
    #plt.ylim(500, 2500)
    #fig = plt.figure(figsize=(10, 6.18))  # 设置画布大小
    #ax = fig.add_subplot(111)
    ax1 = plt.gca()  # 获取坐标轴
    ax1.bar(x=labels, height=paper_counts.values(), width=0.5, color="blue")
    #plt.xticks([index + 0.2 for index in x], labels)
    #ax2 = ax1.twinx()  # 设置次坐标轴
    plt.xlabel("Year")
    plt.xlabel("Number")
    ax1.plot(labels, paper_counts.values(), "c-", color='y')
    plt.title("Distribution of papers by year")
    plt.savefig(os.path.join("./vis/","bar_year.jpg"))
    #plt.show()
    #return

type_dict={"65":"(Chinese) Word Segmentation",
           "96":"Multi-Agent Reinforcement Learning",
           "159":"Retrieval",
           "331":"Semantic Comprehension",
           "416":"Inverse Reinforcement Learning",
           "433":"3D Reconstruction",
           "1862":"Sentiment Analysis",
           "1959":"Pose Estimation",
           "1779":"Domain Adaptation",
           "1974":"Action Recoginition",
           "1996":"Dictionary Learning",
           "2076":"Security Games",
           "2180":"Machine Translation",
           "2872":"Object/Saliency Detection",
           "2931":"Variational Inference"
           }

universities=["Carnegie Mellon University",
              "Tsinghua University",
              ]


if __name__=="__main__":
    json_path="dblp_v14.json"
    root_path="./cleaned_data"
    cleaned_path=os.path.join(root_path,"ai_conference.json")
    conference_labels=["ACL","EMNLP","AAAI","IJCAI","ICML","CVPR","ICCV","ECCV","NIPS"]
    years=[str(i) for i in range(2011,2020)]
    print(years)
    data=load_json(cleaned_path)
    draw_bar(data,years)   
    #draw_pie(data,conference_labels)