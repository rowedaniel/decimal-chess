import csv

from Piece import Piece
from PieceLocation import PieceLocation

FILENAME = "game_log.csv"



class Board:
    """
    Chess board, responsible for handling all of the pieces inside of it
    """

    def __init__(self, size : int, game_id):
        """
        inits the board state to nothing
        @param {int} size: the width and height of the board
        """
        self.size = size
        self.game_id = game_id
        self.reset_board()

    # private methods`
    def reset_board(self):
        """
        resets the board to nothing (no pieces)
        """
        self.state = [[[] for i in range(self.size)] for j in range(self.size)]
        self.turn_number = 0

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

    def get_pieces_at_tile(self, loc : PieceLocation) -> list:
        """
        gets the location of all pieces on the specified tile.
        index attr. of location input is ignored.
        returns {list<PieceLocation>} of locations
        """
        self.clean_dead_pieces()
        return [PieceLocation(loc.row, loc.col, i) \
                for i,_ in enumerate(self.state[loc.row][loc.col])]

    def get_piece_color_at(self, loc : PieceLocation) -> list:
        """
        gets the colors at a given location
        @param {PieceLocation} loc: where to place the piece
        returns: list<int>: list of piece colors at that space
        """
        return self.get_piece(loc).color

    def get_all_occupied_locs(self) -> iter:
        """
        returns generator that gets every occupied space in the board
        """
        for irow, row in enumerate(self.state):
            for icol, space in enumerate(row):
                for index, _ in enumerate(space):
                    yield PieceLocation(irow, icol, index)

    def clean_dead_pieces(self):
        """
        removes all pieces with 0 health from the board
        """
        for irow, row in enumerate(self.state):
            for icol, space in enumerate(row):
                index = 0
                while index < len(space):
                    loc = PieceLocation(irow, icol, index)
                    if self.get_piece(loc).is_dead():
                        self.remove_piece(loc)
                    else:
                        index += 1

    # public methods
    def check_piece_at_tile(self, loc : PieceLocation) -> bool:
        """
        decides if there is a piece at the desired location
        @param {PieceLocation} loc: where to place the piece
        """
        return len(self.state[loc.row][loc.col]) > 0


    def get_opposing_pieces_at_tile(self, loc : PieceLocation, color : int) -> bool:
        """
        returns the location of all pieces of the opposing color at the desired location
        @param {PieceLocation} loc: where to place the piece
        @param {int} color: the color to check
        returns {list<PieceLocation}: list of pieces
        """
        locs = []
        for t_loc in self.get_pieces_at_tile(loc):
            if self.get_piece_color_at(t_loc) != color:
                locs.append(t_loc)
        return locs


    def check_threatened(self, loc : PieceLocation, color : int):
        """
        Checks if the specified location is threatened by any opposing piece
        """
        return False

    def get_piece_movement(self, loc : PieceLocation) -> list:
        """
        returns {list<PieceLocation>}: the list of spaces that the piece at the given
            location can move to.

        """
        if self.check_piece_at_tile(loc):
            piece = self.get_piece(loc)
            normal = piece.get_movement_spaces(self.size, self.check_piece_at_tile)
            special = list(
                    piece.get_special_movement_spaces(
                        self.size,
                        self.check_piece_at_tile,
                        self.get_piece).keys()
                    )
            return normal + special

        return []

    def get_piece_attack(self, loc : PieceLocation) -> list:
        """
        returns {list<PieceLocation>}: the list of spaces that the piece at the given
            location can move to.

        """
        if self.check_piece_at_tile(loc):
            piece = self.get_piece(loc)
            normal = piece.get_attack_spaces(
                    self.size,
                    self.check_piece_at_tile,
                    self.get_opposing_pieces_at_tile)
            special = list(
                    piece.get_special_attack_spaces(
                       self.size,
                       self.check_piece_at_tile,
                       self.get_opposing_pieces_at_tile,
                       self.get_piece).keys()
                    )
            return normal + special
        return []


    def move_piece(self, loc1 : PieceLocation,
                         loc2 : PieceLocation,
                         ):
        """
        moves piece at designated row, col to new designated row, col
        """

        piece = self.get_piece(loc1)

        # first, check weird special movement and attacks
        special_attack_spaces = piece.get_special_attack_spaces(self.size,
                self.check_piece_at_tile, self.get_opposing_pieces_at_tile, self.get_piece)
        if loc2 in special_attack_spaces:
            self.place_piece(loc2, piece.attack(loc2, self.get_piece(special_attack_spaces[loc2])))
        # next, check for special movement
        # TODO: add special movement checks
        # if there's  an opposing piece there, you gotta attack it.
        elif self.get_opposing_pieces_at_tile(loc2, piece.color):
            # as per this chess variant, instead of moving, spawn a new piece at the
            # desired location
            self.place_piece(loc2, piece.attack(loc2, self.get_piece(loc2)))

        # if there's no opposing piece there, just move
        else:
            self.remove_piece(loc1)
            piece.move(loc2)
            self.place_piece(loc2, piece)
        self.clean_dead_pieces()

        self.turn_number += 1

        with open(FILENAME, 'a', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=' ',
                    quotechar = '|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow((
                    self.game_id,
                    self.turn_number,
                    loc1.row,
                    loc1.col,
                    loc1.index,
                    loc2.row,
                    loc2.col,
                    loc2.index,
                    str(piece)
                    ))

