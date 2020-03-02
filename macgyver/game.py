#! /usr/bin/python
# coding: utf-8

import os
from macgyver import data as data
import pygame
import sys

FPS = 15

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
# pygame.mixer.init()

clock = pygame.time.Clock()

current_level = 0
player_board = None


# Game!
def main():
    """ User interaction main loop """
    global current_level
    global player_board
    playing = True

    def start():
        global current_level
        global player_board
        current_level = 0
        player_board = make_maze(current_level)

    def make_maze(new_level):
        return data.Maze(new_level)

    start()

    while playing:

        for event in pygame.event.get():
            if event.type != pygame.MOUSEMOTION:
                # check for window closing
                if event.type == pygame.QUIT:
                    playing = False
                    pygame.quit()
                    quit()
                if current_level < 1:
                    player_board.display_maze()
                    player_board.write_on_screen("READY PLAYER 1?", 50, "top")
                    player_board.write_on_screen(
                        "Use SPACE to start, ARROWS to move", 50, "bottom")
                    if event.type == pygame.KEYDOWN and event.key == \
                            pygame.K_SPACE:
                        current_level += 1
                else:
                    if "level" + str(current_level) != player_board.level:
                        player_board = make_maze(current_level)
                        player_board.display_maze()
                    hero = player_board.macgyver
                    if player_board.ready_to_play():
                        if event.type == pygame.KEYDOWN:
                            new_position = hero.travels(event.key)
                            player_board.manage_collision(new_position)
                            player_board.display_maze()
                    else:
                        player_board.ending()
                        start()

        clock.tick(FPS)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
