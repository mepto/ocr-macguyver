#! /usr/bin/python
# coding: utf-8


# import macgyver.data as data
import data


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
                hero.is_alive_and_kicking = False
            elif collision_type == 'item':
                hero.position_row = new_direction.row
                hero.position_col = new_direction.col
                hero.items += 1
                # player_board.ITEMS[hero.position_row][
                # hero.position_col].is_displayed = False
                print("You now have", hero.items, "item(s).")
                print("Your position is now", hero.position_row,
                      hero.position_col)
    else:
        if hero.is_alive_and_kicking:
            print("Congrats! You're out!")
        else:
            print("Ooops. You died.")


if __name__ == '__main__':
    main()
