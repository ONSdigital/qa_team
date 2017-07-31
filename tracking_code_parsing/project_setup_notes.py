""" Author Ian Edward
-- Extract notes and corresponding tracking code --
- Input and Output files passed in as arguments -
"""

from functools import reduce
import operator
import copy
import sys
import csv
import json



jsonfilepath = sys.argv[1] # Path to json file

with open(jsonfilepath, encoding="utf8") as data_file:
    data_202 = json.load(data_file)


def traverse(d, path = []):
    if isinstance(d, dict):
        iterator = d.items()
    else:
        iterator = enumerate(d) # Add count to the path

    for k, v in iterator:
        yield path + [k], v
        if isinstance(v, (dict, list)):

            for k, v in traverse(v, path + [k]):

                yield k, v

full_list = []

for pat, nods in traverse(data_202):

    full_list.append(pat)

print("_____________")



question_list = []
stored_paths = []

for line in full_list:
     if 'tracking_code' in line:
         print(line)
         thistuple = []
         thistuple.append(line)
         newlist = copy.deepcopy(line)
         for element in range(0, len(line)-0):
             newlist.pop()
             print(newlist)
             thistuple.append(copy.copy(newlist))
         stored_paths.append(thistuple)



def getFromDict(dataDict, *mapList):
    global store_row, store_ind
    tempInfo = []
    # notesList = []

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
                        if x == "note_ID":
                            note_val = res[x]
                        if x == "notes":
                            notesList = res[x]
                            try:
                                search_notes_track = next((item for item in notesList if item["note_ID"] == note_val))
                                tempInfo.append((note_val, search_notes_track))
                            except:
                                print(" No notes here ")




            print(tempInfo)
            note_val = None
            output_csv = sys.argv[3]  # csv output argument
            output_folder = sys.argv[2]  # csv directory argument
            with open(output_folder + output_csv, 'a') as out:
                csv_out = csv.writer(out)
            for row in tempInfo:
                csv_out.writerow(row)
            csv_out.writerow([])
            tempInfo[:] = []

getFromDict(data_202, stored_paths)