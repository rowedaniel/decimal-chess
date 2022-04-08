
from browser_UI import BrowserUI
from ClassicBoard import ClassicBoard

from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from Pawn import Pawn




def main():

    with open("game_info.txt", "r", encoding="utf-8") as file:
        game_id = int(file.read()) + 1


    board = ClassicBoard(
            10, # base hp is 10
            { # now set the attack stat for each piece
                Pawn : 1,
                King : 10,
                Queen : 8,
                Bishop : 3,
                Knight : 3,
                Rook : 5,
            },
            game_id
            )

    ui = BrowserUI(board)
    player_turn_color = 1

    while 1:
        player_turn_color = (player_turn_color + 1) % 2

        cmd, loc1, loc2 = ui.get_user_action(player_turn_color)
        if cmd == "move":
            board.move_piece(loc1, loc2)
        elif cmd == "quit":
            print('Quitting!')
            break

        if board.check_win():
            if ui.alert_won(board.get_winner()):
                board.reset_board()
                board.game_id += 1
            else:
                break

    with open("game_info.txt", "w", encoding="utf-8") as file:
        file.write(str(game_id))



if __name__ == '__main__':
    main()
