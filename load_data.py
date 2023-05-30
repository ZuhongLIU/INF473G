import networkx as nx
import json

def load_json(path):
    with open(path, mode="r") as f:
        data = json.load(f)
    return data

def construct_graph_from_json(path):
    G = nx.Graph()
    
    data=load_json(path)
    
    with open(node_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print(reader)
        for line in reader:
            G.add_node(line["Id"],label=line["Label"],link=line["Link"])
    
    with open(edge_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print(reader)
        for line in reader:
            G.add_edge(line["Source"],line['Target'],weight=int(line["Weight"]))


    return G