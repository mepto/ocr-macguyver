#! /usr/bin/python
# coding: utf-8


from macgyver import data as data


def main():
    current_level = 0
    while current_level == 0:
        user_says = input("Ready Player 1 - Please enter 'y' to start playing")
        if user_says.lower() == 'y':
            current_level += 1
        else:
            print("ok, no play for you then")
            exit()

    player_board = data.Maze(current_level)
    hero = player_board.macgyver

    while player_board.ready_to_play():
        player_board.display_maze()
        hero.print_position()
        user_move = input("So, Mac, where would you like to go? (l, r, u, d)")
        new_position = hero.travels(user_move.lower())
        if new_position is not None:
            player_board.manage_collision(new_position)
            hero.print_position()
    else:
        if hero.is_alive_and_kicking:
            print("Congrats! You were out in", hero.moves, "moves :)")
            player_board.reset_lists()
        else:
            print("Ooops. You died.")
            player_board.reset_lists()
            user_says = input("Would you like to try again? (y/n)")
            if user_says.lower() == 'y':
                main()
            else:
                print("ok, no play for you then. Bye-bye now!")
                exit()


if __name__ == '__main__':
    main()
