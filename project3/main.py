#! /usr/bin/venv python3
# coding: utf-8

import project3.data as p3


def main():
    current_level = 0

    while current_level == 0:
        user_says = input("Ready Player 1 - Please enter 'y' to start playing")
        if user_says == "y":
            current_level += 1
        else:
            print("ok, no play for you then")
            exit()

    p3.Maze(current_level)

    # while p3.Maze.macgyver.is_alive_and_kicking:
    #     direction = input("Where would you like to go? (u, d, l, r")
    #     is_colliding()


if __name__ == '__main__':
    main()
