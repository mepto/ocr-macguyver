#! /usr/bin/python
# coding: utf-8

"""
:synopsis: Game loop for macgyver game.

"""

import os
from macgyver import data as data
import pygame

FPS = 15

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

clock = pygame.time.Clock()


def make_maze(new_level):
    """ Initialise level """
    return data.Maze(new_level)


# Game!
def main():
    """ User interaction main loop """
    current_level = 0
    player_board = make_maze(current_level)
    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type != pygame.MOUSEMOTION:
                # check for window closing
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    playing = False
                    pygame.quit()
                    quit()
                # check for level update
                if "level" + str(current_level) != player_board.level:
                    player_board = make_maze(current_level)
                    player_board.display_maze()
                # manage start level
                if current_level < 1:
                    player_board.display_maze()
                    player_board.write_on_screen("READY PLAYER 1?", 50, "top")
                    player_board.write_on_screen(
                        "Use SPACE to start, ARROWS to move", 50, "bottom")
                    if event.type == pygame.KEYDOWN and event.key == \
                            pygame.K_SPACE:
                        current_level += 1
                # actual playing by user
                else:
                    hero = player_board.macgyver
                    if player_board.ready_to_play():
                        # key listener
                        if event.type == pygame.KEYDOWN:
                            new_position = hero.travels(event.key)
                            player_board.manage_collision(new_position)
                            player_board.display_maze()
                    # game end
                    else:
                        player_board.ending()
                        current_level = 0
                        make_maze(0)
        clock.tick(FPS)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
