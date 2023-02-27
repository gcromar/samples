# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 16:04:49 2020

@author: Graham

The purpose of this program is to detect cycles in a directed graph
of ontology terms.

This program is an implementation of a depth first traversal (DFT) algorithm
for directed graphs found at:
https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
"""

import os
from collections import defaultdict

backEdges = {}
returnFlag = False

# =============================================================================
# Class definitions
# =============================================================================


class Graph():
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def vPrint(self, v):
        print(v, self.graph[v])

    def gPrint(self):
        for v in self.graph:
            print(v, self.graph[v])

    def isCyclicUtil(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True
        global returnFlag

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        for neighbour in self.graph[v]:
            if visited[neighbour] is False:
                if self.isCyclicUtil(neighbour, visited, recStack) is True:
                    i = 0
                    for item in recStack:
                        if item is True:
                            elements = (str(v), str(i), str(item))
                            vkey = " = ".join(elements)
                            backEdges[vkey] = "dummy"
                        i += 1
                    #  elements = (str(v), str(visited))
                    #  vkey = " = ".join(elements)
                    #  backEdges[vkey] = "dummy"
                    #  return True
                    returnFlag = True

            elif recStack[neighbour] is True:
                i = 0
                elements = (str(v), )
                for item in recStack:
                    if item is True:
                        elements = (str(v), str(i), str(item))
                        vkey = " = ".join(elements)
                        backEdges[vkey] = "dummy"
                    i += 1
                #  elements = (str(v), str(visited))
                #  vkey = " = ".join(elements)
                #  backEdges[vkey] = "dummy"
                # return True
                returnFlag = True

        # The node needs to be poped from
        # recursion stack before function ends
        recStack[v] = False
        return False  # hopefully forces full search

    # Returns true if graph is cyclic else false
    def isCyclic(self):
        visited = [False] * self.V
        recStack = [False] * self.V
        for node in range(self.V):
            if visited[node] is False:
                if self.isCyclicUtil(node, visited, recStack) is True:
                    return True
        return False

# =============================================================================
# Main line
# =============================================================================


# Check file path
inPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                          '\\ReactomeMMURelationsNumeric')
outPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                           '\\reactome_annotation_descriptions.txt')

exists = os.path.isfile(inPath)

if exists:
    # Open file handles

    IF = open(inPath, 'r')
    OF = open(outPath, 'w')

    g = Graph(90000000)  # Max depth = max neighbours per node
    # g.vPrint

    print("Loading graph data")
    for record in IF:

        fields = record.split('\t')

        # Map the fields

        parentTerm = fields[0]
        childTerm = fields[1]

        # Data cleanup

        childTerm = childTerm.rstrip("\n")
        # print(childTerm)

        g.addEdge(childTerm, parentTerm)
        # elements = (childTerm, " = ", parentTerm)
        # separator = ''
        # output = separator.join(elements)
        # OF.write(output)
        # OF.write('\n')
        # print(output)

    IF.close()
    OF.close()

#    g.addEdge(50, 10)
#    g.addEdge(10, 30)
#    g.addEdge(40, 40)
#    g.addEdge(20, 50)
#    g.addEdge(30, 10)
#    g.addEdge(40, 50)
#    g.addEdge(30, 50)
    # g.vPrint(0)
    g.gPrint()

    # Look for back edges

    print("Looking for back edges")

    if g.isCyclic() == 1:
        print("Graph has a cycle")
    else:
        if returnFlag is True:
            print("Graph has a cycle")
            for keys in backEdges:
                print(keys)
        else:
            print("Graph has no cycle")

else:
    print('file not found')
