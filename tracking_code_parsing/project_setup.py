""" Author - Ian Edward
 -- Extract tracking code structured as matrix --
 Input and Output files passed in as arguments
"""
from functools import reduce
import operator
import os
import copy
import csv
import json
import sys
import logging

logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s' )

def parse_json_survey(filename, path):
    json_data = read_file_data(filename, path)
    paths = process_paths(json_data)
    e_track = extract_tracking(paths)
    all_info = getFromDict(json_data, e_track)
    write_to_csv(all_info)

""" Read json file and return json_data object """
def read_file_data(filename, path):
    os.chdir(path)
    with open(filename,  encoding="utf8") as data_file:
        json_data = json.load(data_file)
    return json_data

""" Append the paths and nods to list"""
def process_paths(json_data):
    full_list = []
    for pat, nods in traverse(json_data):
        full_list.append(pat)
    return full_list

""" Traverse through json object to separate keys from values """
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

""" Select every path with tracking code """
def extract_tracking(full_list):
    stored_paths = []
    for line in full_list:
         if ('tracking_code' in line) and ('cells' not in line):
             logging.debug(line)
             thistuple = []
             thistuple.append(line)
             newlist = copy.deepcopy(line)
             # For loop to remove the last element from the paths
             for element in range(0, len(line)-0):
                 newlist.pop()
                 thistuple.append(copy.copy(newlist))
             stored_paths.append(thistuple)

    return stored_paths

""" Using the paths append value to keys """
def getFromDict(dataDict, *mapList):
    tempInfo = []
    for arg in mapList:
        for mapper in arg:
            for maped in mapper:
                res = reduce(operator.getitem, maped, dataDict)
                if type(res) == dict:
                    print("\n")
                    for x in res.keys():
                        skipLevels = ("segment", "question", "notes")
                        if x not in skipLevels:
                            tempInfo.append((x, res[x]))

        return tempInfo
"""Write the parsed data to csv file"""
def write_to_csv(all_info):


    output_csv = sys.argv[4]
    output_folder = sys.argv[3]
    with open(output_folder + output_csv, 'a') as out:
        csv_out = csv.writer(out)
        for row in all_info:
            csv_out.writerow(row)
        csv_out.writerow([])

if __name__ == "__main__":
    parse_json_survey(sys.argv[2], sys.argv[1])
