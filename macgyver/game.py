#! /usr/bin/python
# coding: utf-8

from macgyver import data as data
import pygame
import sys


FPS = 9

pygame.init()
# pygame.mixer.init()

clock = pygame.time.Clock()


# Game!
def main():
    """ User interaction main loop """
    playing = True
    current_level = 0

    def make_maze(new_level):
        return data.Maze(new_level)

    player_board = make_maze(current_level)

    while playing:

        for event in pygame.event.get():
            # check for window closing
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                quit()
            if current_level < 1:
                player_board.display_maze()
                player_board.write_on_screen("READY PLAYER 1?", 50, "top")
                player_board.write_on_screen("Use SPACE to start, ARROWS to "
                                             "move", 45, "bottom")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    current_level += 1
            else:
                if "level" + str(current_level) != player_board.level:
                    player_board = make_maze(current_level)
                hero = player_board.macgyver
                if player_board.ready_to_play():
                    if event.type == pygame.KEYDOWN:
                        new_position = hero.travels(event.key)
                        player_board.manage_collision(new_position)
                        player_board.display_maze()
                else:
                    playing = False
                    player_board.ending()
                    user_says = input("Would you like to try again? (y/n)")
                    if user_says.lower() == 'y':
                        main()
                    else:
                        print("ok, no play for you then. Bye-bye now!")
                        exit()

        clock.tick(FPS)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
