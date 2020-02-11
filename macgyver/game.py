#! /usr/bin/python
# coding: utf-8

from macgyver import data as data
import pygame
import sys


FPS = 30

pygame.init()
# pygame.mixer.init()

clock = pygame.time.Clock()


# Game!
def main():
    """ User interaction main loop """
    playing = True

    current_level = 1
    player_board = data.Maze(current_level)
    hero = player_board.macgyver
    player_board.display_maze()

    # while playing:
    while player_board.ready_to_play():
        # keep loop at same speed

        for event in pygame.event.get():
            # check for window closing
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                quit()


                # player_board.display_maze()
                # hero.print_position()
                # user_move = input("So, Mac,
                # where would you like to go? (l, r,
                # u, d)")

            if event.type == pygame.KEYDOWN:
                new_position = hero.travels(event.key)
                player_board.manage_collision(new_position)
                player_board.display_maze()
                # if event.key == pygame.K_UP:
                #     print(event.key)


        # current_level = 1
        # current_level = 0
        # while current_level == 0:
        #     user_says = input("Ready Player 1 -
        #     # Please enter 'y' to start playing")
        #     if user_says.lower() == 'y':
        #         current_level += 1
        #     else:
        #         print("ok, no play for you then")
        #         playing = False
        #         exit()

        # player_board = data.Maze(current_level)
        # hero = player_board.macgyver
        # player_board.display_maze()

        # while player_board.ready_to_play():
            # pass
            # player_board.display_maze()
            # hero.print_position()
            # user_move = input("So, Mac,
            # where would you like to go? (l, r,
            # u, d)")
            # new_position = hero.travels(user_move.lower())
            # print(event.key)

                # new_position = hero.travels(event.key)
                # cplayer_board.manage_collision(new_position)
                # player_board.display_maze()
            # hero.print_position()
        # else:
        #     playing = False
        #     player_board.ending()
        #     user_says = input("Would you like to try again? (y/n)")
        #     if user_says.lower() == 'y':
        #         main()
        #     else:
        #         print("ok, no play for you then. Bye-bye now!")
        #         exit()

        # pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    quit()
    # sys.exit()
        

if __name__ == '__main__':
    main()
