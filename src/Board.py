
from Piece import Piece
from PieceLocation import PieceLocation

class Board:
    """
    Chess board, responsible for handling all of the pieces inside of it
    """

    def __init__(self, size : int):
        """
        inits the board state to nothing
        @param {int} size: the width and height of the board
        """
        self.size = size
        self.reset_board()

    # private methods`
    def reset_board(self):
        """
        resets the board to nothing (no pieces)
        """
        self.state = [[[] for i in range(self.size)] for j in range(self.size)]

    def get_piece_colors_at(self, loc : PieceLocation) -> list:
        """
        gets the list of piece colors on a space
        @param {PieceLocation} loc: where to place the piece
        returns: list<int>: list of piece colors at that space

        """
        return (cell.color for cell in self.state[loc.row][loc.col])

    def place_piece(self, loc : PieceLocation, piece : Piece):
        """
        places a single piece on the board at the given location
        @param {PieceLocation} loc: where to place the piece
        @param {Piece} piece: the piece to place
        """
        self.state[loc.row][loc.col].insert(loc.index, piece)

    def remove_piece(self, loc : PieceLocation) -> Piece:
        """
        removes a single piece on the board from the given location
        @param {PieceLocation} loc: where to find the piece
        """
        # get the piece
        piece = self.state[loc.row][loc.col].pop(loc.index)
        # update the positions of other pieces in the same space to have the right location
        for i, move_piece in enumerate(self.state[loc.row][loc.col]):
            move_piece.move(PieceLocation(loc.row, loc.col, i))
        return piece

    def get_piece(self, loc : PieceLocation) -> Piece:
        """
        gets a single piece on the board from the given location
        @param {PieceLocation} loc: where to find the piece
        """
        return self.state[loc.row][loc.col][loc.index]

    def get_piece_color_at(self, loc : PieceLocation) -> list:
        """
        gets the list of piece colors at a given location
        @param {PieceLocation} loc: where to place the piece
        returns: list<int>: list of piece colors at that space
        """
        return (cell.color for cell in self.state[loc.row][loc.col])

    def clean_dead_pieces(self):
        """
        removes all pieces with 0 health from the board
        """
        print('cleaning!')
        for irow, row in enumerate(self.state):
            for icol, space in enumerate(row):
                index = 0
                while index < len(space):
                    loc = PieceLocation(irow, icol, index)
                    if self.get_piece(loc).is_dead():
                        print('aHA!')
                        self.remove_piece(loc)
                    else:
                        index += 1

    # public methods
    def check_piece_at(self, loc : PieceLocation) -> bool:
        """
        decides if there is a piece at the desired location
        @param {PieceLocation} loc: where to place the piece
        """
        return len(self.state[loc.row][loc.col]) > 0


    def check_opposing_piece_at(self, loc : PieceLocation, color : int) -> bool:
        """
        decides if there is a piece of the opposing color at the desired location
        @param {PieceLocation} loc: where to place the piece
        @param {int} color: the color to check
        """
        return any((c != color for c in self.get_piece_color_at(loc)))

    def get_piece_movement(self, loc : PieceLocation) -> list:
        """
        returns {list<PieceLocation>}: the list of spaces that the piece at the given
            location can move to.

        """
        if self.check_piece_at(loc):
            return self.get_piece(loc).get_movement_spaces(self.size, self.check_piece_at)
        return []

    def get_piece_attack(self, loc : PieceLocation) -> list:
        """
        returns {list<PieceLocation>}: the list of spaces that the piece at the given
            location can move to.

        """
        if self.check_piece_at(loc):
            return self.get_piece(loc).get_attack_spaces(
                    self.size,
                    self.check_piece_at,
                    self.check_opposing_piece_at
                    )
        return []


    def move_piece(self, loc1 : PieceLocation,
                         loc2 : PieceLocation,
                         ):
        """
        moves piece at designated row, col to new designated row, col
        """

        # if there's  an opposing piece there, you gotta attack it.
        piece = self.get_piece(loc1)
        if self.check_opposing_piece_at(loc2, piece.color):
            # as per this chess variant, instead of moving, spawn a new piece at the
            # desired location
            self.place_piece(loc2, piece.attack(loc2, self.get_piece(loc2)))
            self.clean_dead_pieces()

        # if there's no opposing piece there, just move
        else:
            self.remove_piece(loc1)
            piece.move(loc2)
            self.place_piece(loc2, piece)

