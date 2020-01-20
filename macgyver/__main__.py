#! /usr/bin/python
# coding: utf-8


# import macgyver.data as data
from macgyver import data as data


def main():
    current_level = 0
    while current_level == 0:
        user_says = input("Ready Player 1 - Please enter 'y' to start playing")
        if user_says == 'y' or user_says == 'Y':
            current_level += 1
        else:
            print("ok, no play for you then")
            exit()

    player_board = data.Maze(current_level)
    hero = player_board.macgyver
    villain = player_board.guardian

    while (hero.position_row != player_board.SAFE_EXIT['main_exit'][
          'position_row'] or hero.position_col != player_board.SAFE_EXIT[
          'main_exit']['position_col']) and hero.is_alive_and_kicking:
        player_board.display_maze()
        user_move = input("So, Mac, where would you like to go? (l, r, u, d)")
        new_direction = hero.travels(user_move)
        if new_direction is not None:
            collision_type = player_board.is_colliding(data.Position(
                                                       new_direction.row,
                                                       new_direction.col))
            if collision_type == 'wall':
                print("Sorry, you can't go there.")
            elif collision_type == 'villain':
                hero.position_row = new_direction.row
                hero.position_col = new_direction.col
                if hero.items < 3:
                    hero.is_alive_and_kicking = False
                else:
                    villain.is_alive_and_kicking = False
                    print("This guy felt like a nap.")
                    hero.moves += 1
            else:
                hero.position_row = new_direction.row
                hero.position_col = new_direction.col
                hero.moves += 1
                if collision_type == 'item':
                    hero.items += 1
                    print("You now have", hero.items, "item(s).")
                    for item in player_board.ITEMS:
                        if item.position_row == hero.position_row and \
                                item.position_col == hero.position_col:
                            item.is_displayed = False
                    if hero.items == 3:
                        print("Mac, hurry, time is running out! Use the items"
                              " you collected to get rid of the guard!")
                print("Your position is now", hero.position_row,
                      hero.position_col)
    else:
        if hero.is_alive_and_kicking:
            print("Congrats! You were out in", hero.moves, "moves :)")
            player_board.reset_lists()
        else:
            print("Ooops. You died.")
            player_board.reset_lists()
            user_says = input(
                "Would you like to try again? (y/n)")
            if user_says == 'y' or user_says == 'Y':
                main()
            else:
                print("ok, no play for you then")
                exit()


if __name__ == '__main__':
    main()
