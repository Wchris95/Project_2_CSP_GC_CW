from datetime import timedelta
from time import time

def parse_file(filename):
    with open(filename,"r") as file:
        text = file.read()
    #Set up a temporary variable to split the file line by line
    tempVar = text.split("\n")
    #set the domain at line 3 grabbing the last value as this will be the number of colors
    domain = int(tempVar[2][-1])
    Variables = []
    constraint = []
    #Go through the pairs of each line
    for pairs in tempVar[4:-1]:
        #append to the constraint list where for every line we split the line by "," and convert it into an integer
        constraint.append(list(int(b) for b in pairs.split(",")))
        #go throug each variable in the line
        for variable in pairs.split(","):
            if int(variable) not in Variables:
                Variables.append(int(variable))
    print("colors:",domain,"\nVertices:",Variables,"\nConstraints",constraint)
    return domain, Variables, constraint

domain, Variables, constraint = parse_file("test file.txt")
