
from Board import Board

from PieceLocation import PieceLocation
from Piece import Piece

from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King
from Pawn import Pawn


class TextUI:
    """
    Basic text-based UI (mostly for testing)
    """
    def __init__(self):
        self.names = {
                Rook    : 'R',
                Knight  : 'N',
                Bishop  : 'B',
                Queen   : "Q",
                King    : "K",
                Pawn    : "*",
                "EMPTY" : ".",
                "MARK_MOVE"  : "#",
                "MARK_ATTACK"  : "x",
                }
        self.row_names = ("8", "7", "6", "5", "4", "3", "2", "1")
        self.col_names = ("A", "B", "C", "D", "E", "F", "G", "H")
        self.command_message = "enter a command (h for help) "
        self.options = {
                'h' : "this menu",
                'p' : "display a piece's possible movements and attacks",
                'm' : "move a piece",
                "q" : "quit"
                }

        self.marked = {}

    def is_valid_board_loc(self, locstr : str) -> bool:
        """
        checks if the specified location string is a valid location the board
        """
        if len(locstr) != 2:
            return False
        if locstr[0] not in self.col_names:
            return False
        if locstr[1] not in self.row_names:
            return False
        return True

    def get_board_loc(self, locstr : str) -> PieceLocation:
        """
        gets the piece at specified board location string
        @param {str} locstr: the stringified location of the space
        returns {tuple<int, int>}: row, col location of the space
        """
        return PieceLocation(self.row_names.index(locstr[1]), self.col_names.index(locstr[0]))


    def print_board(self, board : Board):
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
        @param {Board} board: the board to display
        """


        print("     " + "  ".join(self.col_names))
        print("  +=" + "=" * len(self.col_names)*3 + "=+")

        for irow, row in enumerate(board.state):
            print("  | " + " "*len(self.col_names)*3 + " |")
            print(self.row_names[irow], end=" | ")
            for icol, space in enumerate(row):

                character = " "
                if len(space) == 0:
                    character += self.names["EMPTY"]
                for piece in space:
                    character += self.names[piece.__class__]

                character += " "

                loc = PieceLocation(irow, icol)
                if loc in self.marked:
                    character = character.rstrip().lstrip()
                    character = self.names[self.marked[loc]] + \
                            character + \
                            self.names[self.marked[loc]]

                print(character, end="")
            print(" |", self.row_names[irow])

        print("  +=" + "=" * len(self.col_names)*3 + "=+")
        print("     " + "  ".join(self.col_names))


    def print_help(self):
        """
        display the help message to the screen
        """
        print('help:')
        print('commands:')
        for cmd, msg in self.options.items():
            print(f"  {cmd}  -  {msg}")

    def get_piece_location(self, board : Board) -> PieceLocation:
        """
        queries the user for a particular piece
        """
        user_loc = input("enter the piece's location: ")

        # convert user location to valid board location
        if not self.is_valid_board_loc(user_loc):
            print("invalid location.")
            return None
        loc = self.get_board_loc(user_loc)
        if not board.get_piece_color_at(loc):
            print("location has no piece to view.")
            return None
        return loc

    def get_user_move(self, board : Board, color : int):
        """
        queries user for a move
        """
        loc1 = self.get_piece_location(board)
        if not loc1:
            return None, None
        if color not in board.get_piece_color_at(loc1):
            print("no piece of your color there")
            return None, None
        possible_locs = board.get_piece_movement(loc1) + board.get_piece_attack(loc1)

        loc2 = self.get_piece_location(board)
        if not loc2:
            return None, None
        if loc2 not in possible_locs:
            print("That piece can't move there!")
            return None, None
        return loc1, loc2

    def set_piece_info(self, board : Board, loc : PieceLocation):
        """
        queries user for which space they want, then adds info about where the piece on that
        space can move to.
        """
        for mark_loc in board.get_piece_movement(loc):
            self.marked[mark_loc] = 'MARK_MOVE'
        for mark_loc in board.get_piece_attack(loc):
            self.marked[mark_loc] = 'MARK_ATTACK'




    def get_user_action(self, board : Board, color : int) -> tuple:
        """
        prompts the user until given a move command
        @param {Board} board: the board to display to the player
        @param {int} color: the color of the player whose turn it is
        returns: tuple<str, PieceLocation, PieceLocation> tuple of the desired command, and the
            locations for that command.
        """


        option = ''
        while 1:
            self.print_board(board)
            self.marked = {}

            option = input(self.command_message)

            if option == 'p':
                # fetch the desired piece and display everywhere it can move/attack
                piece = self.get_piece_location(board)
                if not piece:
                    continue
                self.set_piece_info(board, piece)

            elif option == 'm':
                # attempt to move desired piece
                loc1, loc2 = self.get_user_move(board, color)
                if loc1 is not None and loc2 is not None:
                    return "move", loc1, loc2

            elif option == 'q':
                # quit
                return "quit", None, None

            else:
                # by default, just print the help message
                self.print_help()
