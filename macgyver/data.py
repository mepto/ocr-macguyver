#! /usr/bin/python
# coding: utf-8

"""
:synopsis: Classes and methods of people and objects on the playing board are
contained in this file. The Background contains other classes' objects and
is responsible for interactions between them.

"""

# Standard lib imports
import os
import json
from random import randint

# Third-party imports
import pygame as game


class Maze:

    WIDTH = 15
    HEIGHT = 15
    SPRITE_WIDTH = 1
    SPRITE_HEIGHT = 1
    FILE_LEVELS = "assets/levels.json"
    BOARD = []
    ITEMS = []
    HEROS = []
    VILLAINS = []
    SAFE_EXIT = []

    def __init__(self, level):
        self.level = "level" + str(level)
        self.read_values_from_json(self.level)
        self.macgyver = Hero(Position(
            self.HEROS["macgyver"]["position_row"],
            self.HEROS["macgyver"]["position_col"]),
            """https://user.oc-static.com/upload/2017
            /04/21/14927753100739_macgyver-32-43.png"""
        )
        self.guardian = Human(Position(self.VILLAINS["guardian"][
                                           "position_row"],
                                       self.VILLAINS["guardian"]["position_col"]
                                       ),
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

    def display_maze(self):
        print("MacGyver is currently located in row",
              self.macgyver.position_row,
              "and col", self.macgyver.position_col)
        for line in self.BOARD:
            print(line)

    def read_values_from_json(self, level_nb):
        """ Retrieve Maze data from json file"""
        # check if file exists
        try:
            os.path.exists(self.FILE_LEVELS)
        except (OSError, IOError) as e:
            self.BOARD.append("Cannot create Maze: no file "
                              "found to create levels (error no.: " +
                              str(e.errno) + ").")
        else:
            # open json file with level elements
            with open(self.FILE_LEVELS) as level:
                # load the data contained in this file
                playing_level = json.load(level)[level_nb]
                self.BOARD = playing_level["background"]
                self.SAFE_EXIT = playing_level["exit"]
                self.HEROS = playing_level["heros"]
                self.VILLAINS = playing_level["villains"]

    def randomize_position(self):
        """ Sets a random position for Items MacGyver needs to find """
        row = -1
        column = -1
        while self.is_colliding(row, column):
            row = randint(0, 14)
            column = randint(0, 14)
        else:
            return Position(row, column)

    def is_colliding(self, planned_row=-1, planned_col=-1):
        """ Verifies if position of objects are relevant relative
        to each other and Maze elements """
        row = planned_row
        col = planned_col
        print(row, col)
        zone_type = self.BOARD[row][col]
        while row != -1 and col != -1:
            print("the self.board result is", self.BOARD[row][col])
            if zone_type != "f" \
                or (row == self.macgyver.position_row
                    and col == self.macgyver.position_col) \
                or (row == self.guardian.position_row
                    and col == self.guardian.position_col):
                return True
            else:
                return False
        else:
            return True


class Human:

    def __init__(self, position,
                 image="https://avatars.dicebear.com/v2/male/joe.svg"):
        self.is_alive_and_kicking = True
        self.victory_phrase = "Yay"
        self.failure_phrase = "Argh..."
        self.position_row = position.row
        self.position_col = position.column
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
        planned_direction = Position(self.position_row - 1, self.position_col),
        print("You plan to go up at row", planned_direction,
              "and column", self.position_col, Maze.is_colliding(
               self.position_row - 1, self.position_col))
        return planned_direction

    def down(self):
        planned_direction = Position(self.position_row + 1, self.position_col),
        print("You plan to go up at row", planned_direction,
              "and column", self.position_col, Maze.is_colliding(
              self.position_row + 1, self.position_col))
        return planned_direction

    def left(self):
        planned_direction = Position(self.position_row, self.position_col - 1)
        print("You plan to go left at row", self.position_row, "and column",
              planned_direction, Maze.is_colliding(self.position_row,
                                                   self.position_col - 1))
        return planned_direction

    def right(self):
        planned_direction = self.position_col + 1
        print("You plan to go left at row", self.position_row, "and column",
              planned_direction, Maze.is_colliding(self.position_row,
                                                   self.position_col + 1))
        return planned_direction
               
    def other(self):
        print("No known direction. Try again.")


class Item:

    def __init__(self, position,
                 image="https://freeiconshop.com/wp-content/uploads/edd/gift-flat.png"):
        self.position_row = position.row
        self.position_col = position.column
        self.image = image   
        self.is_displayed = True
        self.display_item()

    def display_item(self):
        pass
        print(self.position_row, self.position_col)


class Position:

    def __init__(self, row, column):
        self.row = row
        self.column = column
