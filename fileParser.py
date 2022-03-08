#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
class file_parse:
    def __init__(self, filename: str)->None:
        self.filename = filename
        self.parsed_data = self.parse_file()
        
    def parse_file(self) -> dict:
        edges = []
        colors = 0
        vertices = list()
        neighbors = defaultdict(set)
        data_dict = {}
        with open(self.filename,"r") as file:
            for line in file:
                if line.split() == [] or line.split()[0] == '#':
                    continue
                if line.lower().split()[0] == 'colors':
                    colors = int(line.split()[-1].strip())
                #set a tempvar to parse the edges if the edge is already in the edges list ignore the edge
                else:
                    tempVar = tuple(sorted(int(b) for b in line.strip().split(",")))
                    if tempVar not in edges:                      
                        edges.append(tempVar)
                    else:
                        continue
                #else:
                 #   continue
        for edge in edges:
            neighbors[edge[0]].add(edge[1])
            neighbors[edge[1]].add(edge[0])
            if edge[0] not in vertices:
                vertices.append(edge[0])
            if edge[1] not in vertices:
                vertices.append(edge[1])
            else:
                continue
        data_dict["colors"] = colors
        data_dict["edges"] = edges
        data_dict["vertices"] = vertices
        data_dict["neighbors"] = neighbors
        return data_dict