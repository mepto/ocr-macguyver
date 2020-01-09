#! /usr/bin/python
# coding: utf-8


import macgyver.data as data


def main():
    current_level = 0

    while current_level == 0:
        user_says = input("Ready Player 1 - Please enter 'y' to start playing")
        if user_says == "y":
            current_level += 1
        else:
            print("ok, no play for you then")
            exit()

    player_board = data.Maze(current_level)
    hero = player_board.macgyver
    villain = player_board.guardian

    while hero.position != player_board.SAFE_EXIT[0]:
        user_move = input("So, Mac, where would you like to go? (l, r, u, d)")
        if player_board.is_colliding(hero.goes(user_move)):
            print("Sorry, you can't go there.")
        else:
            hero.position = hero.goes(user_move)
            for item in data.Maze.ITEMS:
                print(item.position)
                if item.position == hero.position and item.is_displayed:
                    hero.items += 1
                    item.is_displayed = False
                    print("Mac now has", hero.items, "item(s).")
            print("Your position is now", hero.position)
            if villain.position == hero.position:
                hero.is_alive_and_kicking = False
                print("Ooops. You died.")
    else:
        print("Congrats! You're out!")


if __name__ == '__main__':
    main()
