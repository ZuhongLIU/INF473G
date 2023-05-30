import json

file_path="institute.txt"
target_path="./cleaned_data/institut_ranking.json"

data=[]
with open(file_path, "r",encoding="utf-8") as f:
    lines=f.readlines()
    for line in lines:
        name=line[7:].split("closed")[0].strip(" ")
        tmp=line.split("chart")[-1].split("\t")
        score=float(tmp[1])
        faculty=int(tmp[2].strip("\n"))
        print(name,score,faculty)
        data.append({"name":name,"score":score,"faculty":faculty})
        
    with open(target_path,'w',encoding='utf8') as f2:
        json.dump(data,f2,ensure_ascii=False,indent=2)