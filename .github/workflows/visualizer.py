from graphviz import Digraph
from  graphviz import Source
import copy
from collections import defaultdict
import yaml
from networkx import nx
from itertools import product
import sys


class node:
    def __init__(self,name):
        self.name = name
        self.matrix=[]
        self.needs=[]
        self.matrix_needs=[]
        self.successors=[]
        self.predecessors=[]
        self.group=dict()
    
    def name():
        return self.name
    
    def add_matrix(self,nodes):
        for i in list(product(*tuple(nodes.values()))):
            self.matrix.append('-'.join([self.name]+[str(j) for j in i]))        
    
    def add_needs(self,nodes):
        if type(nodes) == list:
            self.needs = self.needs+nodes
        else:
            self.needs = self.needs+[nodes]
            
    def add_successors(self,nodes):
        self.successors=nodes
    
    def add_predecessors(self,nodes):
        self.predecessors=nodes
    
    def has_matrix(self):
        return True if len(self.matrix)>0 else False
    
    def has_needs(self):
        return True if len(self.needs)>0 else False
    
    def add_group(self,name):
        self.group[name[0]]=name[1]
        
    def part_of_matrix(self):
        if "matrix" in self.group.keys():
            return True
        else:
            return False

def print_graph():
    #file_name,show_matrix_nodes=True,group_parallel_nodes=True
    file_name=sys.argv[1]
    show_matrix_nodes=sys.argv[2]
    group_parallel_nodes=sys.argv[3]

    with open(file_name) as file:
            pre_workflow = yaml.load(file, Loader=yaml.FullLoader)

    workflow=copy.deepcopy(pre_workflow)

    nodes=dict()
    for k,v in pre_workflow['jobs'].items():
        nodes[k] = node(k)
        if pre_workflow['jobs'][k] != None:
            if 'needs' in pre_workflow['jobs'][k]:
                nodes[k].add_needs(pre_workflow['jobs'][k]['needs'])
            if 'stage' in pre_workflow['jobs'][k]:
                nodes[k].add_group(('stage',pre_workflow['jobs'][k]['stage']))
            if 'strategy' in pre_workflow['jobs'][k]:
                    if 'matrix' in pre_workflow['jobs'][k]['strategy']:
                        nodes[k].add_matrix(pre_workflow['jobs'][k]['strategy']['matrix'])

    if show_matrix_nodes == True:
        temp=dict()
        nodes_to_del=list()

        for n in nodes.values():
            if n.has_matrix() == True:
                nodes_to_del.append(n)
                for matrix_node in n.matrix:
                    temp[matrix_node] = node(matrix_node)
                    temp[matrix_node].needs=nodes[n.name].needs
                    temp[matrix_node].add_group(('matrix',n.name))

        nodes = {**nodes,**temp}

        for n in nodes.values():
            if n.has_needs() == True:
                for needs_node in n.needs:
                    if nodes[needs_node].has_matrix() == True:
                        n.needs.remove(needs_node)
                        n.add_needs(nodes[needs_node].matrix)

        for n in nodes_to_del:
            del nodes[n.name]

    DG = nx.DiGraph()
    for n in nodes.values():
        DG.add_node(n.name)
        if n.has_needs() == True:
            for needs_node in n.needs:
                if (nodes[needs_node].has_matrix() == True) and (show_matrix_nodes == True):
                    for matrix_node in nodes[needs_node].matrix: 
                        DG.add_edges_from([(matrix_node,n.name)])
                else:
                    DG.add_edges_from([(needs_node,n.name)])

    for n in DG.nodes:
        nodes[n].add_successors(list(DG.successors(n)))
        nodes[n].add_predecessors(list(DG.predecessors(n)))

    dot = Digraph(
            comment='Graph',
            graph_attr={'rankdir':'LR','style':'filled'},
            node_attr={'shape':'rectangle',
                                'fixedsize': 'false',
                                'width': '1.2',
                                'height': '0.2',
                                'fontsize':'10'})
    dot.attr(compound='true')
    for n in DG.nodes:
        dot.node(n)

    j=0
    for n in nodes.values():
        t=[k for k in nodes.values() if (n.successors==k.successors) and (n.predecessors==k.predecessors)]
        if len(t)>1:
            for ns in t:
                if "matrix" not in ns.group.keys():
                    ns.add_group(('smart',str(j)))
            j=j+1

    cluster=defaultdict(list)
    stage=defaultdict(list)
    for n in nodes.values():
        if "matrix" in n.group.keys():
            cluster['cluster_'+ n.group["matrix"]].append(n.name)
        elif "stage" in n.group.keys():
            stage['cluster_'+ n.group["stage"]].append(n.name)
        elif "smart" in n.group.keys() and group_parallel_nodes == True:
            cluster['cluster_'+ n.group["smart"]].append(n.name)

    for cluster_name,ns in cluster.items():
        with dot.subgraph(name=cluster_name) as c:
            for n in ns:
                c.node(n)
    for cluster_name,ns in stage.items():
        with dot.subgraph(name=cluster_name) as c:
            for n in ns:
                c.node(n)

    smart_edges=list()
    for edges in DG.edges:
        start_cluster= [k for k,v in  cluster.items() if edges[0] in v]
        end_cluster=[k for k,v in  cluster.items() if edges[1] in v]
        if start_cluster != [] and end_cluster != []:
            smart_edges.append((start_cluster[0],end_cluster[0]))
        elif start_cluster != []:
            smart_edges.append((start_cluster[0],edges[1]))            
        elif end_cluster != []:
            smart_edges.append((edges[0],end_cluster[0]))
        else:
            smart_edges.append((edges[0],edges[1]))
    smart_edges=list(dict.fromkeys(smart_edges))

    for edges in smart_edges:
        if (edges[0] in cluster.keys()) and (edges[1] in cluster.keys()):
             dot.edge(cluster[edges[0]][0],
                      cluster[edges[1]][0],lhead=edges[1],ltail=edges[0])
        elif (edges[0] in cluster.keys()):
            dot.edge(cluster[edges[0]][0],
                     edges[1],ltail=edges[0])
        elif (edges[1] in cluster.keys()):
            dot.edge(edges[0],
                     cluster[edges[1]][0],lhead=edges[1])
        else:
            dot.edge(edges[0],edges[1])
    return dot


if __name__ == '__main__':
    print_graph()
