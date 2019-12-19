#! /usr/bin/venv python3
# coding: utf-8

import project3.data as p3


def main():
    current_level = 0

    while current_level == 0:
        user_says = input("Ready Player 1 - Please enter 'y' to start "
                          "playing")
        if user_says == "y":
            current_level += 1

    p3.Background(current_level)


if __name__ == '__main__':
    main()
