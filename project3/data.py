#! /usr/bin/venv python3
# coding: utf-8

"""
:synopsis: Classes and methods of people and objects on the playing board are
contained in this file. The Background contains other classes' objects and
is responsible for interactions between them.

"""

# Standard lib imports
import os
import sys
import json
from random import randint

# Third-party imports
import pygame as pg


class Maze:

    WIDTH = 15
    HEIGHT = 15
    SPRITE_WIDTH = 1
    SPRITE_HEIGHT = 1
    FILE_LEVELS = "assets/levels.json"
    BOARD = []
    ITEMS = []
    HUMANS = []
    SAFE_EXIT = []

    def __init__(self, level):
        self.level = "level" + str(level)
        self.read_values_from_json(self.level)
        self.display_maze()
        self.macgyver = Hero(self.HUMANS[0],
                              "https://user.oc-static.com/upload/2017/04/21/14927753100739_macgyver-32-43.png")
        self.guardian = Human(self.HUMANS[1],
                             "https://user.oc-static.com/upload/2017/04/21/14927753225921_murdoc-32.png")
        self.needle = Item(self.randomize_position(),
                           "https://cdn0.iconfinder.com/data/icons/world-issues/500/needle_and_thread-256.png")
        self.tube = Item(self.randomize_position(),
                         "https://cdn3.iconfinder.com/data/icons/medical-205/32/Artboard_10-256.png")
        self.ether = Item(self.randomize_position(),
                          "https://cdn3.iconfinder.com/data/icons/glypho-free/64/flask-256.png")

    def display_maze(self):  # , level_nb):
        print("MacGyver is currently located in column ", self.HUMANS[0][0],
              "and row", self.HUMANS[0][1])
        for line in self.BOARD:
            print(line)

    def read_values_from_json(self, level_nb):
        """ Retrieve Maze data from json file"""
        # check if file exists
        try:
            open(self.FILE_LEVELS)
        except (OSError, IOError) as e:
            self.BOARD.append("Cannot create Maze: no file "
                              "found to create levels (error no.: " +
                              str(e.errno) + ").")
        except Exception:
            self.BOARD.append("Cannot create Maze, "
                              "an unexpected error occurred:"
                              + str(sys.exc_info()[0]))
        else:
            # open a json file with my objects
            with open(self.FILE_LEVELS) as level:
                # load all the data contained in this file
                data = json.load(level)
                for elem in data[level_nb]:
                    for r in data[level_nb][elem]:
                        if elem == "background":
                            self.BOARD.append(r)
                        elif elem == "humans":
                            self.HUMANS.append(r)
                        else:
                            self.SAFE_EXIT.append(r)

    # def position(self, thecolumn=randint(0, 14), therow=randint(0, 14)):
    #
    #     thecolumn = thecolumn * self.SPRITE_WIDTH
    #     therow = therow * self.SPRITE_HEIGHT
    #     return thecolumn, therow

    def randomize_position(self):
        """ Sets a random position for Items MacGyver needs to find """
        column = -1
        row = -1
        while self.BOARD[column][row] != "f" \
                and (column != self.macgyver.position[0]
                     or row != self.macgyver.position[1]) \
                and (column != self.guardian.position[0]
                     or row != self.guardian.position[1]):
            column = randint(0, 14)
            row = randint(0, 14)
        else:
            self.ITEMS.append([column, row])
            return [column, row]

    def is_colliding(self, instance, position):
        """ Verifies if position of objects are relevant relative
        to each other and Maze elements """
        col = position[0] - 1
        row = position[1] - 1
        print(instance)
        zone_type = self.BOARD[col][row]
        return False


class Human:

    def __init__(self, position=(-1, -1),
                 image="https://avatars.dicebear.com/v2/male/joe.svg"):
        self.is_alive_and_kicking = True
        self.victory_phrase = "Yay"
        self.failure_phrase = "Argh..."
        self.position = position
        self.image = image


class Hero(Human):

    def __init__(self, position, image):
        super().__init__(position, image)
        self.items = 0
        self.moves = 0

    def goes(self, direction):
        switcher = {
            "l": self.left,
            "r": self.right,
            "u": self.up,
            "d": self.down
        }
        func = switcher.get(direction, lambda: "Ce n'est pas une direction "
                                               "connue")
        return func()

    def left(self):
        planned_direction = [self.position[0]-1, self.position[1]]
        print(planned_direction, self.position)

    def right(self):
        planned_direction = [self.position[0]+1, self.position[1]]
        print(planned_direction, self.position)

    def up(self):
        planned_direction = [self.position[0], self.position[1]-1]
        print(planned_direction, self.position)

    def down(self):
        planned_direction = [self.position[0], self.position[1]+1]
        print(planned_direction, self.position)


class Item:

    def __init__(self, position, image):
        self.position = position
        self.image = image
        # self.display_item()

    def display_item(self):
        print(self.position)
