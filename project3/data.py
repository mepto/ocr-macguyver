#! /usr/bin/venv python3
# coding: utf-8

import json
from os import path


class Human:

    def __init__(self):
        self.is_alive=True
        self.victory_phrase="Yay"
        self.failure_phrase="Argh..."
        self.position = Position(1, 1)
        self.image=image()

    def image(self):
        # error_if_none
        pass


class Hero:
    def __init__(self):
        self.items=0


class Background:
    print(of.read_values_from_json("level1"))


def read_values_from_json(level_nb):
    values = []
    file_levels = "assets/levels.json"
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


class Position:

    SPRITE_WIDTH=1
    SPRITE_HEIGHT=1

    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    @property
    def position_x(self):
        return self.position_x * self.SPRITE_WIDTH

    @property
    def position_y(self):
        return self.position_y * self.SPRITE_HEIGHT
