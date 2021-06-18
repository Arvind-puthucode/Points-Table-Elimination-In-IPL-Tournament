# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 16:42:59 2020

@author: 91908
"""
import numpy as np
class Edge(object):
    def __init__(self, u, v, capacity):
        # initializing a new edge object
        self.source = u
        self.destination = v
        self.capacity = capacity
    
    def __repr__(self):
        return "%s-->%s:%s" % (self.source, self.destination, self.capacity)
      
class FlowGraph(object):
    def __init__(self):
        # using an adjacency list representation of for a graph
        self.adjMat = {}
        # map to track the flow (much easier than using an array)
        self.flow = {}

    def add_node(self, node):
        # adds a node with an empty list as it has no edges
        self.adjMat[node] = []

    def get_edges(self, node):
        # returns the edges that originate from the desired node
        return self.adjMat[node]

    def add_edge(self, u, v, capacity=0):
        # we cannot have self loops in this graph
        if u == v:
            raise ValueError("u == v : no self loops allowed!")
        edge = Edge(u, v, capacity)
        backEdge = Edge(v, u, 0)
        # not that the peer attribute need not be defined in the edge class
        # for every edge we have a backEdge --> simpler way to implement
        # the residual graph
        edge.peer = backEdge
        backEdge.peer = edge
        # for an edge u-v, the edge originates from u and the backEdge from v
        self.adjMat[u].append(edge)
        self.adjMat[v].append(backEdge)
        # initailly the flow in both of them is 0
        self.flow[edge] = 0
        self.flow[backEdge] = 0
    
    def get_adjmat(self):
        return self.adjMat
        
    
    def get_augmenting_path(self, s, t, path, set_path):
  # this method uses DFS to find an augmenting path
      
      if s == t:
          return path
      for edge in self.get_edges(s):
          # find the capacity remaining in the edge
          leftover = edge.capacity - self.flow[edge]
          if leftover > 0 and (edge, leftover) not in set_path:
              set_path.add((edge, leftover))
              result = self.get_augmenting_path(
              edge.destination, t, path + [(edge, leftover)], set_path)
              if result != None:
                  return result

    def ford_fulkerson(self, s, t):
        aug_path = self.get_augmenting_path(s, t, [], set())
  # ford-fulkerson runs while there exists and s-t path
        while aug_path != None:
      # calculating the bottleneck capacity
          flow = min(lftvr for edge, lftvr in aug_path)
          for edge, lftvr in aug_path:
          # increasing flow on edge
              self.flow[edge] += flow
          # decreasing flow on peer
              self.flow[edge.peer] -= flow
              aug_path = self.get_augmenting_path(s, t, [], set())
  # calculating the maxflow - as the sum of flow on edges leaving 's'
        maxflow = sum(self.flow[edge] for edge in self.get_edges(s))
        return maxflow
        
        
        
def main():
    g = FlowGraph()
    # adding all the nodes to the graph
    nodes_list = ['s', 'CSK-DC', 'CSK-KKR', 'KKR-DC', 'CSK', 'DC', 'KKR', 't']
    [g.add_node(node) for node in nodes_list]

    # adding the first set of edges
    g.add_edge('s', 'CSK-DC', 2)
    g.add_edge('s', 'CSK-KKR', 0)
    g.add_edge('s', 'KKR-DC', 0)

    # adding the second set of edges
    g.add_edge('CSK-DC', 'CSK', float('inf'))
    g.add_edge('CSK-DC', 'DC', float('inf'))
    g.add_edge('CSK-KKR', 'CSK', float('inf'))
    g.add_edge('CSK-KKR', 'KKR', float('inf'))
    g.add_edge('KKR-DC', 'KKR', float('inf'))
    g.add_edge('KKR-DC', 'DC', float('inf'))

    # adding the third set of edges
    g.add_edge('CSK', 't', 11)
    g.add_edge('DC', 't', 14)
    g.add_edge('KKR', 't', 13)

    # this prints the maxflow from source s to sink t
    maxflow1=g.ford_fulkerson('s', 't')
    print('Max Flow for MI: ' + str(g.ford_fulkerson('s', 't')))
    set1=g.get_edges('s')
    sum1=0
    for i in set1:
        sum1=sum1+i.capacity
    if(sum1==maxflow1):
        print("There is no guarantee Mi is disqualified")
    
    g2 = FlowGraph()
    nodes_list2 = ['s', 'MI-DC', 'MI-KKR', 'KKR-DC', 'MI', 'DC', 'KKR', 't']
    [g2.add_node(node) for node in nodes_list2]

    # adding the first set of edges
    g2.add_edge('s', 'MI-DC', 1)
    g2.add_edge('s', 'MI-KKR', 6)
    g2.add_edge('s', 'KKR-DC', 0)

    # adding the second set of edges
    g2.add_edge('MI-DC', 'MI', float('inf'))
    g2.add_edge('MI-DC', 'DC', float('inf'))
    g2.add_edge('MI-KKR', 'MI', float('inf'))
    g2.add_edge('MI-KKR', 'KKR', float('inf'))
    g2.add_edge('KKR-DC', 'KKR', float('inf'))
    g2.add_edge('KKR-DC', 'DC', float('inf'))

    # adding the third set of edges
    g2.add_edge('MI', 't', 0)
    g2.add_edge('DC', 't', 6)
    g2.add_edge('KKR', 't', 5)

    # running the Ford-Fulkerson algorithm
    maxflow2=g2.ford_fulkerson('s', 't')
    print('Max Flow for CSK: ' + str(g2.ford_fulkerson('s', 't')))
    set2=g.get_edges('s')
    sum1=0
    for i in set2:
        sum1=sum1+i.capacity
    if(sum1==maxflow2):
        print("There is no guarantee Csk is disqualified")
    
    else:
        print("Csk is disqualified:")
    
    g3 = FlowGraph()
    nodes_list3 = ['s', 'MI-DC', 'MI-CSK', 'CSK-DC', 'MI', 'CSK', 'DC', 't']
    [g3.add_node(node) for node in nodes_list3]

    # adding the first set of edges
    g3.add_edge('s', 'MI-DC', 1)
    g3.add_edge('s', 'MI-CSK', 1)
    g3.add_edge('s', 'CSK-DC', 2)

    # adding the second set of edges
    g3.add_edge('MI-DC', 'MI', float('inf'))
    g3.add_edge('MI-DC', 'DC', float('inf'))
    g3.add_edge('MI-CSK', 'MI', float('inf'))
    g3.add_edge('MI-CSK', 'CSK', float('inf'))
    g3.add_edge('CSK-DC', 'CSK', float('inf'))
    g3.add_edge('CSK-DC', 'DC', float('inf'))

    # adding the third set of edges
    g3.add_edge('MI', 't', 1)
    g3.add_edge('DC', 't', 7)
    g3.add_edge('CSK', 't', 4)

    # running the Ford-Fulkerson algorithm
    maxflow3=g3.ford_fulkerson('s', 't')
    print('Max Flow for KKR: ' + str(g3.ford_fulkerson('s', 't')))
    set3=g3.get_edges('s')
    sum1=0
    for i in set3:
        sum1=sum1+i.capacity
    if(sum1==maxflow3):
        print("There is no guarantee KKR is disqualified")
    
    else:
        print("KKR is disqualified:")
    
    g4 = FlowGraph()
    nodes_list4 = ['s', 'MI-CSK', 'MI-KKR', 'MI', 'CSK', 'KKR', 't']
    [g4.add_node(node) for node in nodes_list4]

    # adding the first set of edges
    g4.add_edge('s', 'MI-CSK', 1)
    g4.add_edge('s', 'MI-KKR', 6)
    

    # adding the second set of edges
    g4.add_edge('MI-CSK', 'MI', float('inf'))
    g4.add_edge('MI-CSK', 'CSK', float('inf'))
    g4.add_edge('MI-KKR', 'MI', float('inf'))
    g4.add_edge('MI-KKR', 'KKR', float('inf'))
    # adding the third set of edges
    g4.add_edge('MI', 't', -3)
    g4.add_edge('KKR', 't', 2)
    g4.add_edge('CSK', 't', 0)

    # running the Ford-Fulkerson algorithm
    maxflow4=g4.ford_fulkerson('s', 't')
    print('Max Flow for DC: ' + str(g4.ford_fulkerson('s', 't')))
    set4=g4.get_edges('s')
    sum1=0
    for i in set4:
        sum1=sum1+i.capacity
    if(sum1==maxflow4):
        print("There is no guarantee DC is disqualified")
    
    else:
        print("DC is disqualified:")
    
    
    
    
    
    
    
    
main()
    