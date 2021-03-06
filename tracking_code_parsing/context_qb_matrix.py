""" Author - Ian Edward
 - Extract all tracking codes structured as matrix and all the relevant sections up to the root -
 - Input and Output file passed in as arguments -
"""

from functools import reduce
import operator
import os
import copy
import csv
import json
import logging
import sys


logging.basicConfig(filename='test_matrix.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s' )

jsonfiledir = sys.argv[1] # directory argument
jsonfile = sys.argv[2] # json file argument
os.chdir(jsonfiledir) # Json file directory Path
json_file = jsonfile # Selection of Json file passed in as an argument


with open(json_file,  encoding="utf8") as data_file:
    data_202 = json.load(data_file)

"""Traversing through json file collecting the json paths"""
def traverse(d, path = []):
    if isinstance(d, dict):
        iterator = d.items()
    else:
        iterator = enumerate(d) # Add count to the path

    # Seperate the keys and values
    for k, v in iterator:
        yield path + [k], v
        if isinstance(v, (dict, list)):
            for k, v in traverse(v, path + [k]):
                yield k, v
full_list = [] # List containing the paths
for pat, nods in traverse(data_202):
    full_list.append(pat)

stored_paths = []


# Select every path with tracking_code as key
for line in full_list:
     if ('tracking_code' in line) and ('cells' in line):
         thistuple = []
         #thistuple.append(line)
         for x in range(1):
             line.pop()
         logging.debug(line)
         thistuple.append(line)
         newlist = copy.deepcopy(line)

         # # For loop to remove the last element from the paths
         for element in range(0, len(line)-0):
             newlist.pop()
             logging.debug(newlist)
             thistuple.append(copy.copy(newlist))
         stored_paths.append(thistuple)

no_ext = os.path.splitext(json_file)[0]



""" Append data to keys """
def getFromDict(dataDict, *mapList):
    global store_row, store_ind
    tempInfo = []

    for arg in mapList:
        for mapper in arg:
            for maped in mapper:
                res = reduce(operator.getitem, maped, dataDict)
                if type(res) == dict:
                    for x in res.keys():
                        skipLevels = ("segment", "question", "notes", "validation", "cells", "rows", "cols")
                        if x not in skipLevels:
                            tempInfo.append((x, res[x]))
                            if x == 'col_index':
                                store_ind = res[x]
                            if x == 'row_index':
                                store_row = res[x]
                        if x == "cols":
                            col_val = res[x]
                            col_dict = next((item for item in col_val if item["col_index"] == store_ind))
                            tempInfo.append((x, col_dict))
                        if x == "rows":
                            row_val = res[x]
                            row_dict = next((item for item in row_val if item["row_index"] == store_row))
                            tempInfo.append((x, row_dict))


            logging.debug(tempInfo)
            output_csv = sys.argv[4] # csv output argument
            output_folder = sys.argv[3] # csv directory argument
            with open(output_folder + output_csv, 'a') as out:
                csv_out = csv.writer(out)
            for row in tempInfo:
                csv_out.writerow(row)
            csv_out.writerow([])
            tempInfo[:] = []

getFromDict(data_202, stored_paths)