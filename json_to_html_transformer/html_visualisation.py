""" Author Ian Edward
 -- HTML VISUALISATION --
 - convert json files to html -
 - Input and Output file passed in as arguments -
 - pip install json2html -
"""
import json
from json2html import *
from sys import argv

json_directory = argv[1]
json_in = argv[2]
html_directory = argv[3]
html_out = argv[4]


with open(json_directory + json_in, encoding="utf8") as data_file:
    data_202 = json.load(data_file)

raw_html = json2html.convert(json=data_202)

with open(html_directory + html_out, 'w') as f:
    f.write(raw_html)

print(raw_html)