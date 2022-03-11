
from Board import Board

from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from Pawn import Pawn

def main():
    board = Board(8)

    pieces = [
        Rook    (10, 5, 0, 0, 0),
        Knight  (10, 3, 0, 1, 0),
        Bishop  (10, 3, 0, 2, 0),
        Queen   (10, 8, 0, 3, 0),
        King    (10,10, 0, 4, 0),
        Bishop  (10, 3, 0, 5, 0),
        Knight  (10, 3, 0, 6, 0),
        Rook    (10, 5, 0, 7, 0),

        Pawn    (10, 1, 1, 0, 0),
        Pawn    (10, 1, 1, 1, 0),
        Pawn    (10, 1, 1, 2, 0),
        Pawn    (10, 1, 1, 3, 0),
        Pawn    (10, 1, 1, 4, 0),
        Pawn    (10, 1, 1, 5, 0),
        Pawn    (10, 1, 1, 6, 0),
        Pawn    (10, 1, 1, 7, 0),

        # opposing pieces for testing
        Pawn    (10, 1, 2, 0, 1),
        Pawn    (10, 1, 2, 2, 1),
        ]

    for piece in pieces:
        board.place_piece(piece.row, piece.col, piece)



    print('A-file pawn movement:',
            pieces[9].get_movement_spaces(board.size, board.get_piece_at)
            )
    print('B-file Knight movement:',
            pieces[1].get_movement_spaces(board.size, board.get_piece_at)
            )

    print('A-file pawn attack:',
            pieces[9].get_attack_spaces(board.size, board.check_opposing_piece_at)
            )



if __name__ == '__main__':
    main()
