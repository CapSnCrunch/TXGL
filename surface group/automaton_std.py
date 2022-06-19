from os import path
import re

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "graphStr.txt"))

with open(filepath, 'r') as f:
    newGraph = {}
    lines = f.readlines()
    lines = lines[1:-1]
    for line in lines:
        num = int(line[:line.find(':')])

        line = line.strip('\n')
        line = line[line.find('{')+1: line.find('}')]
        line = line.split(',')

        newNode = {}
        for pair in line:
            pair = pair.replace(' ', '').split(':')
            if len(pair) != 2:
                continue
            pair[0] = pair[0][1:-1]
            pair[1] = int(pair[1])
            newNode[pair[1]-1] = pair[0] 


        if len(newNode.keys()) > 0:
            newGraph[num-1] = newNode
    
    print('{')
    for key, value in newGraph.items():
        print(f'    {key}: {value}{"," if key < len(newGraph.keys())-1 else ""}')
    print('}')