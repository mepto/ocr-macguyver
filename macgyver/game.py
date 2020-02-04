#! /usr/bin/python
# coding: utf-8

from macgyver import data as data
import pygame


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
FPS = 30

pygame.init()
pygame.mixer.init()

board = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Save MacGyver!!!")
clock = pygame.time.Clock()


# Game!
def main():
    """ User interaction main loop """
    playing = True
    while playing:
        # keep loop at same speed
        clock.tick(FPS)
        for event in pygame.event.get():
            # check for window closing
            if event.type == pygame.QUIT:
                playing = False
        
        current_level = 0
        while current_level == 0:
            user_says = input("Ready Player 1 - Please enter 'y' to start playing")
            if user_says.lower() == 'y':
                current_level += 1
            else:
                print("ok, no play for you then")
                playing = False
                exit()

        player_board = data.Maze(current_level)
        hero = player_board.macgyver

        while player_board.ready_to_play():
            player_board.display_maze()
            hero.print_position()
            user_move = input("So, Mac, where would you like to go? (l, r, u, d)")
            new_position = hero.travels(user_move.lower())
            player_board.manage_collision(new_position)
            hero.print_position()
        else:
            player_board.ending()
            user_says = input("Would you like to try again? (y/n)")
            if user_says.lower() == 'y':
                main()
            else:
                print("ok, no play for you then. Bye-bye now!")
                exit()
    pygame.quit()
        

if __name__ == '__main__':
    main()
