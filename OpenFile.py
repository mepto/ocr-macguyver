#! /usr/bin/venv python3
# coding: utf-8

import json
from os import path

def read_values_from_json(level_nb):
    values = []
    file_levels = "Data/levels.json"
    # check if file exists
    if path.exists(file_levels):
        # open a json file with my objects
        with open(file_levels) as level:
            # load all the data contained in this file. data = entries
            data = json.load(level)
            for entry in data:
                values.append(entry[level_nb][0])
    else:
        values = "Cannot create background: no file found to create levels."
    return values
