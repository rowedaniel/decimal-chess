
from Board import Board

from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King
from Pawn import Pawn


# display stuff
# TODO: move this to a different file
names = {
        Rook : 'R',
        Knight : 'N',
        Bishop : 'B',
        Queen : "Q",
        King : "K",
        Pawn : "*",
        "EMPTY" : ".",
        "MARK" : "#",
        }
row_names = ("8", "7", "6", "5", "4", "3", "2", "1")
col_names = ("A", "B", "C", "D", "E", "F", "G", "H")

def is_valid_board_loc(locstr : str) -> bool:
    """
    checks if the specified location string is a valid location the board
    """
    if len(locstr) != 2:
        return False
    if locstr[0] not in col_names:
        return False
    if locstr[1] not in row_names:
        return False
    return True

def get_board_loc(locstr : str) -> tuple:
    """
    gets the piece at specified board location string
    @param {str} locstr: the stringified location of the space
    returns {tuple<int, int>}: row, col location of the space
    """
    return row_names.index(locstr[1]), col_names.index(locstr[0])


def print_board(board : Board, marked : list = []):
    """
    display the board (rudimentary print display.
    Uses the following notation
        R = rook
        N = knight
        B = bishop
        K = king
        Q = queen
        * = pawn
        . = empty space
        # = marked space
    @param {Board} board: the board to display
    @param {list<int, int>} marked: list of marked spaces to display
    """


    print("     " + "  ".join(col_names))
    print("  +=" + "=" * len(col_names)*3 + "=+")

    for irow, row in enumerate(board.state):
        print("  | " + " "*len(col_names)*3 + " |")
        print(row_names[irow], end=" | ")
        for icol, space in enumerate(row):

            character = " "
            if len(space) == 0:
                character += names["EMPTY"]
            for piece in space:
                character += names[piece.__class__]

            character += " "

            if (irow, icol) in marked:
                character = names["MARK"] + character.rstrip().lstrip() + names["MARK"]

            print(character, end="")
        print(" |", row_names[irow])

    print("  +=" + "=" * len(col_names)*3 + "=+")
    print("     " + "  ".join(col_names))


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
        ##Pawn    (10, 1, 2, 0, 1),
        ##Pawn    (10, 1, 2, 2, 1),
        ]

    for piece in pieces:
        board.place_piece(piece.row, piece.col, piece)


    cmd_message = "enter a command (h for help) "
    options = {
            'h' : "this menu",
            'p' : "display a piece's possible movements and attacks",
            'm' : "move a piece",
            "a" : "attack with a piece",
            "q" : "quit"
            }
    option = ''
    marked = []
    while option != 'q':
        print_board(board, marked)

        option = input(cmd_message)
        while option not in options or option == 'h':
            print('help:')
            print('commands:')
            for cmd in options:
                print(f"  {cmd}  -  {options[cmd]}")
            option = input(cmd_message)

        if option == 'p':
            location = input("enter the piece's location: ")
            if not is_valid_board_loc(location):
                print("invalid location.")
                continue
            loc = get_board_loc(location)
            if len(board.state[loc[0]][loc[1]]) == 0: 
                print("location has no piece to view.")
                continue
            print(loc)
            piece = board.state[loc[0]][loc[1]][0]
            marked = piece.get_movement_spaces(board.size, board.get_piece_at)
            marked.extend(piece.get_attack_spaces(board.size, board.check_opposing_piece_at))

        elif option == 'm':
            location1 = input("enter the piece's location: ")
            if not is_valid_board_loc(location1):
                print("invalid location.")
                continue
            row1, col1 = get_board_loc(location1)
            if len(board.state[row1][col1]) == 0:
                print("no piece there")
                continue

            location2 = input("enter the location you want to move the piece to: ")
            if not is_valid_board_loc(location2):
                print("invalid location.")
                continue
            row2, col2 = get_board_loc(location2)

            piece = board.state[row1][col1][0]
            possible_locs = piece.get_movement_spaces(board.size, board.get_piece_at)

            print(possible_locs)
            if (row2, col2) not in possible_locs:
                print(f"That {names[piece.__class__]} can't move there!")
                continue

            board.move_piece(row1, col1, row2, col2)
            marked = []









if __name__ == '__main__':
    main()
