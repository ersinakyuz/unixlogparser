#!/usr/bin/env python3
__version__ = "1.0.0"
__author__ = "Ersin Akyuz"
__email__ = "eakyuz@gmx.net"
__description__ = "Python parser for syslog files"

import re
import sys

def clean(item):  
    """ clean non-numeric chars"""
    item = re.sub("[^0-9]", "", item)
    return item

def find_pos(line, item):
    """find position of the item in the given line"""
    liste = re.sub("=.*?[\s|\n]", " ", line).split(" ")
    pos = (liste.index(item))
    return pos

def get_dicts(log_file, element):
    """ dictionaries"""
    get_dict = {}
    linenum = 0
    for line in log_file:
        linenum = linenum+1
        if "application_end" in line:
            item = int(clean(line.split(" ")[find_pos(line, element)].split("=")[1])) #cleaning = and " chars
            application = (line.split(" ")[find_pos(line, "application")].split("=")[1])  #cleaning = and " chars
            if application not in get_dict:
                get_dict[application] = [item,]
            else:
                get_dict[application].append(item)           
    return get_dict

def print_table(lines):
    """printing the result"""
    widths = []
    for line in lines:
        for i, size in enumerate([len(x) for x in line]):
            while i >= len(widths):
                widths.append(0)
            if size > widths[i]:
                widths[i] = size
    print_string = ""
    for i, width in enumerate(widths):
        if not i:
            print_string += "{" + str(i)+":<" + str(width) +"} "+" "  # first value will be left aligned 
        else:
            print_string += "{" + str(i)+":>" + str(width) +"} "+" "  # right aligned values
    if not print_string: # if len(print_string) == 0
        return
    print_string = print_string[:-1]
    for i, line in enumerate(lines):
        print(print_string.format(*line))    
        if i == 0:
            print("-"*widths[0], "", "-"*widths[1], "", "-"*widths[2]) #draw the -- line

# main code 
# Command line argument check
if len(sys.argv) > 1:
    LOGFILE = sys.argv[1]
else:
    print("Usage: parse.py targetfile")
    LOGFILE = "syslog.txt"
print("Default file", LOGFILE, "selected.\n")

with open(LOGFILE, 'r') as f:
    TERM_DICT = (get_dicts(f, "termsent"))
with open(LOGFILE, 'r') as f:
    ORIG_DICT = (get_dicts(f, "origsent"))

rows = []
rows.append(("Name", "Origsent", "Termsent"))
for key in sorted(ORIG_DICT.items()):
    app = key[0]
    orig = sum(key[1])
    orig_sent = ("{:,}".format(orig))
    term_sent = ("{:,}".format(sum(TERM_DICT[app])))
    rows.append((app, orig_sent, term_sent))
print_table(rows)
sys.exit()
