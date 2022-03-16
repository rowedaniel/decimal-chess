
from text_UI import TextUI
from ClassicBoard import ClassicBoard

from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from Pawn import Pawn




def main():
    board = ClassicBoard(
            10, # base hp is 10
            { # now set the attack stat for each piece
                Pawn : 1,
                King : 10,
                Queen : 8,
                Bishop : 3,
                Knight : 3,
                Rook : 5,
            })

    ui = TextUI()
    player_turn_color = 1

    while 1:
        player_turn_color = (player_turn_color + 1) % 2

        cmd, loc1, loc2 = ui.get_user_action(board, player_turn_color)
        if cmd == "move":
            board.move_piece(loc1, loc2)
        elif cmd == "quit":
            return













if __name__ == '__main__':
    main()
