#! /usr/bin/python
# coding: utf-8

"""
:synopsis: Classes and methods of people and objects on the playing board are
contained in this file. The Background contains other classes' objects and
is responsible for interactions between them.

"""

import json
import os
from random import randint
import pygame
pygame.font.init()

class Maze:
    SCREEN_WIDTH = 720
    SCREEN_HEIGHT = 720
    SPRITE_SIZE = 48
    WIDTH = 15
    HEIGHT = 15
    FILE_LEVELS = "macgyver/assets/levels.json"
    BOARD = []
    ITEMS = []
    HEROS = []
    VILLAINS = []
    SAFE_EXIT = []

    def __init__(self, level):
        """ Creates the level and objects for the board """
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH,
                                               self.SCREEN_HEIGHT))
        self.wall = pygame.image.load(
            'macgyver/assets/wall1.png').convert_alpha()
        self.floor = pygame.image.load(
            'macgyver/assets/floor1.png').convert_alpha()
        self.door = pygame.image.load(
            'macgyver/assets/door.png').convert_alpha()
        self.title = pygame.display.set_caption("Save MacGyver!!!")
        self.level = "level" + str(level)
        self.read_values_from_json(self.level)

        if level > 0:
            self.macgyver = Hero(Position(
                self.HEROS["macgyver"]["position_row"],
                self.HEROS["macgyver"]["position_col"]), pygame.image.load(
                self.HEROS["macgyver"]["avatar"]).convert_alpha(),
                pygame.image.load(self.HEROS["macgyver"]["walk_right"][
                                      0]).convert_alpha(),
                pygame.image.load(self.HEROS["macgyver"]["walk_left"][
                                      0]).convert_alpha(),
                pygame.image.load(self.HEROS["macgyver"]["walk_up"][
                                      0]).convert_alpha(),
                pygame.image.load(self.HEROS["macgyver"]["walk_down"][
                                      0]).convert_alpha())
            self.guardian = Human(Position(
                self.VILLAINS["guardian"]["position_row"],
                self.VILLAINS["guardian"]["position_col"]), pygame.image.load(
                self.VILLAINS["guardian"]["avatar"]).convert_alpha())
            self.needle = Item(self.randomize_position(), pygame.image.load(
                'macgyver/assets/needle.png').convert_alpha())
            self.ITEMS.append(self.needle)
            self.tube = Item(self.randomize_position(), pygame.image.load(
                'macgyver/assets/tube.png').convert_alpha())
            self.ITEMS.append(self.tube)
            self.ether = Item(self.randomize_position(), pygame.image.load(
                'macgyver/assets/potion.png').convert_alpha())
            self.ITEMS.append(self.ether)

    def display_maze(self):
        """ Show the board to the player """
        # blank canvas first
        self.window.fill(pygame.Color(0, 0, 0))
        # loop over background maze data
        pos_row = 0
        for row in self.BOARD:
            pos_col = 0
            for location in row:
                if location == "w":
                    self.window.blit(self.wall, (pos_col * self.SPRITE_SIZE,
                                                 pos_row * self.SPRITE_SIZE))
                elif location == "f":
                    self.window.blit(self.floor, (pos_col * self.SPRITE_SIZE,
                                                  pos_row * self.SPRITE_SIZE))
                elif location == "d":
                    self.window.blit(self.door, (pos_col * self.SPRITE_SIZE,
                                                 pos_row * self.SPRITE_SIZE))
                pos_col += 1
            pos_row += 1

        # loop over collectible items
        if len(self.ITEMS) > 0:
            for item in self.ITEMS:
                if item.is_displayed:
                    self.window.blit(item.image, (item.position_col *
                                     self.SPRITE_SIZE, item.position_row *
                                     self.SPRITE_SIZE))
        # display humans
        if len(self.HEROS) > 0:
            self.window.blit(self.macgyver.image, (
                self.macgyver.position_col * self.SPRITE_SIZE,
                self.macgyver.position_row * self.SPRITE_SIZE))

        if len(self.VILLAINS) > 0:
            if self.guardian.is_alive_and_kicking:
                self.window.blit(self.guardian.image, (
                    self.guardian.position_col * self.SPRITE_SIZE,
                    self.guardian.position_row * self.SPRITE_SIZE))
            else:
                self.window.blit(self.guardian.image, (
                    self.guardian.position_col * self.SPRITE_SIZE,
                    self.guardian.position_row * self.SPRITE_SIZE + 12))
        pygame.display.update()

    def write_on_screen(self, message, size, location):
        """ Display text on start and end screen """
        font = pygame.font.Font("macgyver/assets/zcool.ttf", size)
        if location == "top":
            distance_from_top = 40
        elif location == "bottom":
            distance_from_top = 670
        elif location == "center":
            distance_from_top = self.SCREEN_HEIGHT / 2
        text = font.render(message, True, (235, 207, 52))
        self.window.blit(text, (360 - text.get_width() // 2,
                                distance_from_top - text.get_height() // 2))
        pygame.display.update()

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
                try:
                    self.SAFE_EXIT = playing_level["exit"]
                    self.HEROS = playing_level["heros"]
                    self.VILLAINS = playing_level["villains"]
                except KeyError:
                    pass

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
                    self.macgyver.is_dead()
                else:
                    self.guardian.is_alive_and_kicking = False
                    self.guardian.is_dead()
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
            victory = str(f"Congrats! You were out in {self.macgyver.moves} "
                          f"moves :)")
            self.write_on_screen(victory, 50, "top")
        else:
            self.write_on_screen("Ooops. You died.", 40, "top")
        self.write_on_screen("Press ENTER to go to main menu", 40, "center")
        self.reset_lists()

    def reset_lists(self):
        """ Empty lists to avoid doubling if player starts again """
        self.BOARD.clear()
        self.ITEMS.clear()
        self.HEROS.clear()
        self.VILLAINS.clear()
        self.SAFE_EXIT.clear()
        del self.guardian
        del self.macgyver


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

    def is_dead(self):
        if not self.is_alive_and_kicking:
            self.image = pygame.transform.rotate(self.image, 90)


class Hero(Human):
    """ Hero collects items and moves on the board """

    def __init__(self, position, image, right, left, up, down):
        super().__init__(position, image)
        self.items = 0
        self.moves = 0
        self.walk_right = right
        self.walk_left = left
        self.walk_up = up
        self.walk_down = down
        self.death = pygame.image.load(
            'macgyver/assets/dead.png').convert_alpha()

    def is_dead(self):
        self.image = self.death

    @staticmethod
    def print_position():
        print(pygame.key.get_pressed())

    def travels(self, direction):
        """ Call a function depending on player direction choice """
        switcher = {
            pygame.K_LEFT: self.left,
            pygame.K_RIGHT: self.right,
            pygame.K_UP: self.up,
            pygame.K_DOWN: self.down,
            pygame.K_q: self.exit,
            pygame.K_ESCAPE: self.exit
        }
        func = switcher.get(direction, self.other)
        return func()

    def up(self):
        self.image = self.walk_up
        planned_direction = Position(self.position_row - 1, self.position_col)
        return planned_direction

    def down(self):
        self.image = self.walk_down
        planned_direction = Position(self.position_row + 1, self.position_col)
        return planned_direction

    def left(self):
        self.image = self.walk_left
        planned_direction = Position(self.position_row, self.position_col - 1)
        return planned_direction

    def right(self):
        self.image = self.walk_right
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
    def __init__(self, position, image=None):
        self.position_row = position.row
        self.position_col = position.col
        self.image = image
        self.is_displayed = True


class Position:
    """ Every object on the board and tentative direction has a Position """
    def __init__(self, row, column):
        self.row = row
        self.col = column
