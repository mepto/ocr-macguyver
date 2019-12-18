#! /usr/bin/venv python3
# coding: utf-8

import pygame as pg

import json
from random import randint


class Human:

    def __init__(self, position=(1, 1), image="https://avatars.dicebear.com/v2/male/joe.svg"):
        self.is_alive = True
        self.victory_phrase = "Yay"
        self.failure_phrase = "Argh..."
        self.position = position
        self.image = image


class Hero(Human):
    def __init__(self, position, image):
        super().__init__(position, image)
        self.items = 0


class Background:

    WIDTH = 15
    HEIGHT = 15
    FILE_LEVELS = "assets/levels.json"
    VALUES = []

    def __init__(self, level):
        self.level = "level" + str(level)
        self.display_background(self.level)
        self.aiguille = NewItem(self.randomize_position(),
                                "https://cdn0.iconfinder.com/data/icons/world-issues/500/needle_and_thread-256.png")
        self.tube = NewItem(self.randomize_position(),
                            "https://cdn3.iconfinder.com/data/icons/medical-205/32/Artboard_10-256.png")
        self.ether = NewItem(self.randomize_position(),
                             "https://cdn3.iconfinder.com/data/icons/glypho-free/64/flask-256.png")
        self.macguyver = Hero((0, 13), "https://user.oc-static.com/upload/2017/04/21/14927753100739_macgyver-32-43.png")
        self.villain = Human((14, 6), "https://user.oc-static.com/upload/2017/04/21/14927753225921_murdoc-32.png")
        self.moves = 0

    def display_background(self, values):
        # values_pd = pd.DataFrame(self.read_values_from_json(values))
        values = self.read_values_from_json(values)
        # print(values_pd)
        print(values)

    def read_values_from_json(self, level_nb):

        # check if file exists
        try:
            open(self.FILE_LEVELS)
        except (OSError, IOError) as e:
            # print("error no.: " + str(e.errno))
            self.VALUES = "Cannot create background: no file found to create levels."
        else:
            # open a json file with my objects
            with open(self.FILE_LEVELS) as level:
                # load all the data contained in this file. data = entries
                # data = json.load(level)
                # self.VALUES.append(data[level_nb])
                self.VALUES.append(json.load(level)[level_nb])

        return self.VALUES

    def randomize_position(self):
        column = randint(1, 15)
        row = randint(1, 15)
        while self.is_colliding(self.__class__.__name__, (column, row)):
            column = randint(1, 15)
            row = randint(1, 15)
        else:
            return column, row

    def is_colliding(self, class_name, instance_position):
        # print(instance_position)
        if instance_position == "(1, 1)":
            return True
        else:
            return False


class NewItem:

    def __init__(self, position, image):
        self.position = position
        self.image = image
        self.display_item()

    def display_item(self):
        print(self.position)


class Position:

    SPRITE_WIDTH = 1
    SPRITE_HEIGHT = 1

    def __init__(self, position_x, position_y):
        self.position_x = position_x * self.SPRITE_WIDTH
        self.position_y = position_y * self.SPRITE_HEIGHT
