#! /usr/bin/python
# coding: utf-8
# TODO: add docstrings to all classes and defs 
"""
:synopsis: Classes and methods of people and objects on the playing board are
contained in this file. The Background contains other classes' objects and
is responsible for interactions between them.

"""

import json
import os
from random import randint


class Maze:
    WIDTH = 15
    HEIGHT = 15
    SPRITE_WIDTH = 1
    SPRITE_HEIGHT = 1
    FILE_LEVELS = "macgyver/assets/levels.json"
    BOARD = []
    ITEMS = []
    HEROS = []
    VILLAINS = []
    SAFE_EXIT = []

    def __init__(self, level):
        """ Creates the level and objects for the board """
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

    def display_maze(self):
        """ Show the board to the player """
        for line in self.BOARD:
            print(line)
        for item in self.ITEMS:
            item.display_item()

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
        """ Set a random position for Items MacGyver needs to find """
        row = -1
        column = -1
        while self.is_colliding(Position(row, column)) != "free":
            row = randint(0, 14)
            column = randint(0, 14)
        else:
            return Position(row, column)

    def ready_to_play(self):
        """ Check conditions for playing are met """
        if (self.macgyver.position_row != self.SAFE_EXIT['main_exit'][
          'position_row'] or self.macgyver.position_col != self.SAFE_EXIT[
          'main_exit']['position_col']) and self.macgyver.is_alive_and_kicking:
            return True
        else:
            return False

    def is_colliding(self, position=None):
        """ Verify what's in this position and return a string """

        row = position.row
        col = position.col
        if self.BOARD[row][col] == 'w':
            return "wall"
        elif row == self.macgyver.position_row \
                and col == self.macgyver.position_col:
            return "hero"
        elif row == self.guardian.position_row \
                and col == self.guardian.position_col:
            return "villain"
        else:
            for item in self.ITEMS:
                if item.position_col == col and item.position_row == row \
                        and item.is_displayed:
                    return "item"
            if self.BOARD[row][col] == 'f':
                return "free"
            else:
                return "invalid"

    def manage_collision(self, new_position):
        """ Changes parameters depending on collision type """
        if new_position is not None:
            collision_type = self.is_colliding(new_position)

            if collision_type == 'wall':
                print("Sorry, you can't go there.")
            elif collision_type == 'villain':
                self.macgyver.position_row = new_position.row
                self.macgyver.position_col = new_position.col
                if self.macgyver.items < 3:
                    self.macgyver.is_alive_and_kicking = False
                else:
                    self.guardian.is_alive_and_kicking = False
                    print("This guy felt like a nap.")
                    self.macgyver.moves += 1
            else:
                self.macgyver.position_row = new_position.row
                self.macgyver.position_col = new_position.col
                self.macgyver.moves += 1
                if collision_type == 'item':
                    self.macgyver.items += 1
                    print("You now have", self.macgyver.items, "item(s).")
                    for item in self.ITEMS:
                        if item.position_row == self.macgyver.position_row and \
                                item.position_col == self.macgyver.position_col:
                            item.is_displayed = False
                    if self.macgyver.items == 3:
                        print("Mac, hurry, time is running out! Use the items"
                              " you collected to get rid of the guard!")

    def ending(self):
        """ Show the end depending on hero status """
        if self.macgyver.is_alive_and_kicking:
            print(self.macgyver.victory_phrase)
            print("Congrats! You were out in", self.macgyver.moves, "moves :)")
        else:
            print(self.macgyver.failure_phrase)
            print("Ooops. You died.")
        self.reset_lists()

    def reset_lists(self):
        """ Empty lists to avoid doubling if player starts again """
        self.BOARD.clear()
        self.ITEMS.clear()
        self.HEROS.clear()
        self.VILLAINS.clear()
        self.SAFE_EXIT.clear()


class Human:
    """ Hero and villain are both humans with positions and status """

    def __init__(self, position,
                 image="https://avatars.dicebear.com/v2/male/joe.svg"):
        self.is_alive_and_kicking = True
        self.victory_phrase = "Yay"
        self.failure_phrase = "Argh..."
        self.position_row = position.row
        self.position_col = position.col
        self.image = image


class Hero(Human):
    """ Hero collects items and moves on the board """

    def __init__(self, position, image):
        super().__init__(position, image)
        self.items = 0
        self.moves = 0

    def print_position(self):
        print("You are now in position:", self.position_row, "(row),",
              self.position_col, "(column).")

    def travels(self, direction):
        """ Call a function depending on player direction choice """
        switcher = {
            "l": self.left,
            "r": self.right,
            "u": self.up,
            "d": self.down,
            "exit": self.exit
        }
        func = switcher.get(direction, self.other)
        return func()

    def up(self):
        print("You plan to go up at row", self.position_row - 1,
              "and column", self.position_col)
        planned_direction = Position(self.position_row - 1, self.position_col)
        return planned_direction

    def down(self):
        print("You plan to go down at row", self.position_row + 1,
              "and column", self.position_col)
        planned_direction = Position(self.position_row + 1, self.position_col)
        return planned_direction

    def left(self):
        print("You plan to go left at row", self.position_row, "and column",
              self.position_col - 1)
        planned_direction = Position(self.position_row, self.position_col - 1)
        return planned_direction

    def right(self):
        print("You plan to go right at row", self.position_row, "and column",
              self.position_col + 1)
        planned_direction = Position(self.position_row, self.position_col + 1)
        return planned_direction

    @staticmethod
    def exit():
        print("Sorry to see you go.")
        exit()

    @staticmethod
    def other():
        print("No known direction. Try again.")


class Item:
    """ Create item with position and display status """
    def __init__(self, position,
                 image="https://freeiconshop.com/wp-content/uploads/edd/gift-flat.png"):
        self.position_row = position.row
        self.position_col = position.col
        self.image = image
        self.is_displayed = True
        self.display_item()

    def display_item(self):
        if self.is_displayed:
            print("Item position:", self.position_row, self.position_col)


class Position:
    """ Every object on the board and tentative direction has a Position """
    def __init__(self, row, column):
        self.row = row
        self.col = column
