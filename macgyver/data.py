#! /usr/bin/python
# coding: utf-8

"""
:synopsis: Classes and methods of people and objects on the playing board are
contained in this file. The Background contains other classes' objects and
is responsible for interactions between them.

"""

# Standard lib imports
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
    LEVEL_DATA = []
    BOARD = []
    ITEMS = []
    # HEROS = []
    # VILLAINS = []
    SAFE_EXIT = []

    def __init__(self, level):
        self.level = "level" + str(level)
        self.read_values_from_json(self.level)
        self.macgyver = Hero(
            self.LEVEL_DATA["heros"][0],
            """https://user.oc-static.com/upload/2017
            /04/21/14927753100739_macgyver-32-43.png"""
        )
        self.guardian = Human(self.LEVEL_DATA["villains"][0],
                             "https://user.oc-static.com/upload/2017/04/21/14927753225921_murdoc-32.png")
        self.needle = Item(self.randomize_position(),
                           "https://cdn0.iconfinder.com/data/icons/world-issues/500/needle_and_thread-256.png")
        self.ITEMS.append(self.needle)
        self.tube = Item(self.randomize_position(),
                         "https://cdn3.iconfinder.com/data/icons/medical-205/32/Artboard_10-256.png")
        self.ITEMS.append(self.tube)
        self.ether = Item(self.randomize_position(),
                          "https://cdn3.iconfinder.com/data/icons/glypho-free/64/flask-256.png")
        self.ITEMS.append(self.ether)
        self.display_maze()

    def display_maze(self):  # , level_nb):
        print("MacGyver is currently located in row", self.macgyver.position[0],
              "and col", self.macgyver.position[1])
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
        else:
            # open a json file with my objects
            with open(self.FILE_LEVELS) as level:
                # load all the data contained in this file
                self.LEVEL_DATA = json.load(level)[level_nb]
                self.BOARD = self.LEVEL_DATA["background"]
                self.SAFE_EXIT = self.LEVEL_DATA["exit"]

    def randomize_position(self):
        """ Sets a random position for Items MacGyver needs to find """
        row = -1
        column = -1
        while self.BOARD[row][column] != "f" \
                and (row != self.macgyver.position[0]
                     or column != self.macgyver.position[1]) \
                and (row != self.guardian.position[0]
                     or column != self.guardian.position[1]):
            row = randint(0, 14)
            column = randint(0, 14)
        else:
            return [row, column]

    def is_colliding(self, planned_direction):
        """ Verifies if position of objects are relevant relative
        to each other and Maze elements """
        # print(planned_direction)
        row = planned_direction[0]
        col = planned_direction[1]
        zone_type = self.BOARD[row][col]
        while row != -1 and col != -1:
            if zone_type == "f":
                return False
            else:
                return True
        else:
            return True


class Human:

    def __init__(self, position=[-1, -1],
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
        func = switcher.get(direction, self.other)
        return func()

    def up(self):
        planned_direction = [self.position[0]-1, self.position[1]]
        print("You plan to go up at", planned_direction, Maze.BOARD[
            planned_direction[0]][planned_direction[1]])
        return planned_direction

    def down(self):
        planned_direction = [self.position[0]+1, self.position[1]]
        print("You plan to go down at", planned_direction, Maze.BOARD[
            planned_direction[0]][planned_direction[1]])
        return planned_direction

    def left(self):
        planned_direction = [self.position[0], self.position[1]-1]
        print(Maze.BOARD)
        print("You plan to go left at", planned_direction, Maze.BOARD[planned_direction[0]][planned_direction[1]])
        return planned_direction

    def right(self):
        planned_direction = [self.position[0], self.position[1]+1]
        print("You plan to go right at", planned_direction, Maze.BOARD[
            planned_direction[0]][planned_direction[1]])
        return planned_direction

    def other(self):
        planned_direction = self.position
        print("No know direction. Try again.")
        return planned_direction


class Item:

    def __init__(self, position, image):
        self.position = position
        self.image = image
        self.is_displayed = True
        self.display_item()

    def display_item(self):
        print(self.position)
