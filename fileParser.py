#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Generic, TypeVar, Dict, List, Optional, Tuple

class file_parse:
    def __init__(self, filename: str)->None:
        self.filename = filename
        self.parsed_data = self.parse_file()
        
    def parse_file(self):
        edges = set()
        colors = 0
        variables = list()
        data_dict = {}
        with open(filename,"r") as file:
            for line in file:
                if line.split()[0].strip() == '#':
                    continue
                if line.lower().split()[0].strip() == 'colors':
                    colors = int(line.split()[-1].strip())
                else:
                    edges.add(tuple(int(b) for b in line.split(",")))
        for edge in edges:
            if edge[0] not in variables:
                variables.append(edge[0])
            if edge[1] not in variables:
                variables.append(edge[1])
            else:
                continue
        data_dict["colors"] = colors
        data_dict["edges"] = edges
        data_dict["variables"] = variables
        return data_dict
    
if  __name__ == "__main__":
    filename = "test file.txt"
    fileData = file_parse(filename)
    print(fileData.parse_file())