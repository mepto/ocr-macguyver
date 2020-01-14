#! /usr/bin/python
# coding: utf-8


# import macgyver.data as data
import data


def main():
    current_level = 0
    while current_level == 0:
        user_says = input("Ready Player 1 - Please enter 'y' to start playing")
        if user_says == "y" or user_says == "Y":
            current_level += 1
        else:
            print("ok, no play for you then")
            exit()

    player_board = data.Maze(current_level)
    hero = player_board.macgyver
    villain = player_board.guardian

    while hero.position_row != player_board.SAFE_EXIT["main_exit"][
          "position_row"] or hero.position_col != player_board.SAFE_EXIT[
          "main_exit"]["position_col"]:
        player_board.display_maze()
        user_move = input("So, Mac, where would you like to go? (l, r, u, d)")
        new_direction = hero.travels(user_move)
        print(new_direction)
        if player_board.is_colliding(data.Position(new_direction.row,
                                     new_direction.col)):
            print("Sorry, you can't go there.")
        else:
            hero.position_row = new_direction.row
            hero.position_col = new_direction.col
            for item in player_board.ITEMS:
                print(item.position_row, item.position_col)
                if item.position_col == hero.position_col and \
                        item.position_row == hero.position_row and \
                        item.is_displayed:
                    hero.items += 1
                    item.is_displayed = False
                    print("Mac now has", hero.items, "item(s).")
            print("Your position is now", hero.position_row, hero.position_col)
            if villain.position_row == hero.position_row and \
                    villain.position_col == hero.position_col:
                hero.is_alive_and_kicking = False
                print("Ooops. You died.")
    else:
        print("Congrats! You're out!")


if __name__ == '__main__':
    main()
