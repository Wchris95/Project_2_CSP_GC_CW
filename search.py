from datetime import timedelta
from time import time


def parse_file(filename):
    with open(filename,"r") as file:
        text = file.readlines()
    color = text[2].split()[-1]
    color

parse_file("text_file.txt")
