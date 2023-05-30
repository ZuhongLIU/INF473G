# Import the library
import networkx as nx
import json
from collections import Counter
import spacy

# create an empty graph
G = nx.Graph()

# read the node from the data
def load_json(json_path):

    with open(json_path, mode="r",encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_edges(json_path):
    data=load_json(json_path)
    #print(len(data))
    for article in data:
        G.add_nodes_from([(article["id"], {"Title": article["title"], 
                                           "Keywords": article["keywords"],
                                           "Abstracts": article["abstract"]})])
    nlp = spacy.load('en_core_web_md')
    
    for article in data:    
        for ref in article["references"]:
            if ref in G:
                doc1 = nlp(article["title"])
                doc2 = nlp(nx.get_node_attributes(G, "Title")[ref])
                G.add_edge(article["id"], ref, weight=doc1.similarity(doc2)) 

# open the csv file and read each row
json_path = './cleaned_data/ai_conference.json'
extract_edges(json_path)

# implementation of community detection algorithm
community = nx.community.louvain_communities(G, seed=123)

# function that print the list of 10 word combinations 
# (indicating method and problem) with highest frequency
def print_output(file, idx):
    method = []
    problem = []
    # for each article in a community
    for i in community[idx]:
        title = nx.get_node_attributes(G, "Title")[i]
        title = title[:-1]
        # finding the position of linking word in the title
        find_for = title.find(" for ")
        find_with = title.find(" with ")
        find_using = title.find(" using ")
        find_in = title.find(" in ")
        find_by = title.find(" by ")
        # adding the method and problem to a list
        if (title.find(" for ") != -1):
            method.append(title[:find_for])
            problem.append(title[find_for + 5:])
        elif (title.find(" with ") != -1):
            problem.append(title[:find_with])
            method.append(title[find_with + 6:])
        elif (title.find(" using ") != -1):
            problem.append(title[:find_using])
            method.append(title[find_using + 7:])
        elif (title.find(" in ") != -1):
            method.append(title[:find_in])
            problem.append(title[find_in + 4:])
        elif (title.find(" by ") != -1):
            problem.append(title[:find_by])
            method.append(title[find_by + 4:])
        # if the linking word is not finded, we add the all the title to the problem
        else: 
            problem.append(title)

    # extract the word combinations that the distance of each word is not greater
    # than 2
    token_method = []
    token_problem = []
    # for the method list
    for u in range(len(method)):
        doc = method[u].split()
        for i in range(len(doc)):
            for j in  range(len(doc)):
                if (i < j) and (j-i <= 2):
                    token_method.append((doc[i]+" "+doc[j]).lower())

    # for the problem list
    for u in range(len(problem)):
        doc = problem[u].split()
        for i in range(len(doc)):
            for j in range(len(doc)):
                if (i < j and j-i<=2):
                    token_problem.append((doc[i]+" "+doc[j]).lower())

    # counting the frequency
    counted_method = Counter(token_method)
    counted_problem = Counter(token_problem)

    # find the 10 combinations with highest frequency in each list
    top_10 = counted_method.most_common(10)
    for element, count in top_10:
        print(f"{element} appears {count} times")
    print("==============================================")


    top_10 = counted_problem.most_common(10)
    for element, count in top_10:
        print(f"{element} appears {count} times")
    print("==============================================")

# print for all the community of size bigger than 50
file = open("output.csv", 'w')
print("id; community id; method; problem", file=file)
for i in range(len(community)):
    if (len(community[i]) > 50):
        print_output(file, i)