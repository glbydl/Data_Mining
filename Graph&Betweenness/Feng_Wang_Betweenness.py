import networkx as nx
import sys
import json

def betweenness(inputdata):
    G = nx.Graph()
    dict_betweenness = {}

    # build graph G by input file
    for line in inputdata:
        edge = json.loads(line)
        G.add_edge(edge[0], edge[1])

    # initialize "edge - betweenness" pair with 0
    for edge in G.edges():
        dict_betweenness[edge] = 0

    # compute the betweenness for each edge
    for node in G.nodes():
        # build DAG using current node as source node
        DAG = get_DAG(node, G)
        # number of shortest paths to the current node
        px = {}
        px[node] = 1
        # compute px by top-down traversing DAG
        top_down(node, DAG, px)
        # compute betweenness by bottom-up traversing DAG
        bottom_up(node, DAG, px, dict_betweenness)

    # format the output
    for key in dict_betweenness:
        # de-duplicate
        dict_betweenness[key] /= 2
        # output by alphabetical order
        if key[0] > key[1]:
            print str(json.dumps([key[1], key[0]])) + ":", dict_betweenness[key]
        else:
            print str(json.dumps([key[0], key[1]])) + ":", dict_betweenness[key]

def get_DAG(node, G):
    DAG = nx.DiGraph()
    dict_nodes_level = {}
    dict_nodes_level[node] = 1
    nodes_list = list()
    nodes_visited = list()
    nodes_list.append(node)
    nodes_visited.append(node)
    while nodes_list:
        curr_node = nodes_list.pop(0)
        for next_node in G[curr_node]:
            if next_node not in nodes_visited:
                dict_nodes_level[next_node] = dict_nodes_level[curr_node] + 1
                nodes_list.append(next_node)
                nodes_visited.append(next_node)
                DAG.add_edge(curr_node, next_node)
            else:
                if dict_nodes_level[curr_node] == dict_nodes_level[next_node] - 1:
                    DAG.add_edge(curr_node, next_node)

    return DAG

def top_down(node, DAG, px):
    nodes_list = list()
    nodes_list.append(node)
    while nodes_list:
        curr_node = nodes_list.pop(0)
        for next_node in DAG[curr_node]:
            if next_node not in px.keys():
                px[next_node] = 1
                nodes_list.append(next_node)
            else:
                px[next_node] += 1

def bottom_up(node, DAG, px, dict_betweenness):
    if not DAG[node]:
        return 1

    fx = px[node]
    for child in DAG[node]:
        fx_child = bottom_up(child, DAG, px, dict_betweenness)
        fx_child = float(fx_child) / px[child] * px[node]
        forward_edge = (node, child)
        backward_edge = (child, node)
        if forward_edge in dict_betweenness.keys():
            dict_betweenness[forward_edge] += fx_child
            fx += fx_child
        else:
            dict_betweenness[backward_edge] += fx_child
            fx += fx_child

    return fx

if __name__ == '__main__':
    inputdata = open(sys.argv[0])
    betweenness(inputdata)