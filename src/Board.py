
import csv

from Piece import Piece
from Pawn import Pawn
from King import King
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
        self.clean_pieces()
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

    def clean_pieces(self):
        """
        removes all pieces with 0 health from the board
        """
        for irow, row in enumerate(self.state):
            for icol, space in enumerate(row):
                index = 0
                while index < len(space):
                    loc = PieceLocation(irow, icol, index)
                    piece = self.get_piece(loc)

                    # merge pieces together
                    for i in range(0,index):
                        if self.get_piece(PieceLocation(irow,icol,i)).merge(piece):
                            break

                    if self.get_piece(loc).is_dead():
                        self.remove_piece(loc)
                    else:
                        index += 1

    # public methods
    def check_win(self):
        """
        checks if the board is in a win-state
        returns True or False.
        """
        kings = {
                Piece.WHITE : False,
                Piece.BLACK : False,
                }
        for loc in self.get_all_occupied_locs():
            piece = self.get_piece(loc)
            if piece.__class__ == King:
                kings[piece.color] = True
        print('checking for win, kings is:', kings)
        return not kings[Piece.WHITE] or not kings[Piece.BLACK]

    def get_winner(self):
        """
        returns the color of the winner
        """
        kings = {
                Piece.WHITE : None,
                Piece.BLACK : None,
                }
        for loc in self.get_all_occupied_locs():
            piece = self.get_piece(loc)
            if piece.__class__ == King:
                kings[piece.color] = piece.color
        for king in kings.values():
            if king is not None:
                return king
        return None



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
        orig_health = piece.hitpoints
        new_health = 0
        defender_orig_health = 0
        defender_final_health = 0
        piece_attacked = ""
        special = ""

        # first, check weird special movement and attacks
        special_attack_spaces = piece.get_special_attack_spaces(self.size,
                self.check_piece_at_tile, self.get_opposing_pieces_at_tile, self.get_piece)
        if loc2 in special_attack_spaces:
            print('special action possible!', loc2.row, loc2.col, loc2.index)

            special = "special attack"
            if piece.__class__ == Pawn:
                special = "En Passant"

            if self.check_piece_at_tile(special_attack_spaces[loc2]):
                defender = self.get_piece(special_attack_spaces[loc2])
                defender_orig_health = defender.hitpoints
                piece_attacked = str(defender)
            else:
                if piece.__class__ == Pawn:
                    special = "Promote"
                    print("promoting")
                defender = None

            new_piece = piece.attack(loc2, defender)
            new_health = new_piece.hitpoints
            if defender:
                defender_final_health = defender.hitpoints

            self.place_piece(loc2, new_piece)
        # next, check for special movement
        # TODO: add special movement checks
        # if there's  an opposing piece there, you gotta attack it.
        elif self.get_opposing_pieces_at_tile(loc2, piece.color):
            # as per this chess variant, instead of moving, spawn a new piece at the
            # desired location
            defender = self.get_piece(loc2)
            defender_orig_health = defender.hitpoints

            new_piece = piece.attack(loc2, defender)
            new_health = new_piece.hitpoints
            defender_final_health = defender.hitpoints
            piece_attacked = str(defender)

            self.place_piece(loc2, new_piece)

        # if there's no opposing piece there, just move
        else:
            self.remove_piece(loc1)
            piece.move(loc2)
            self.place_piece(loc2, piece)
        self.clean_pieces()

        self.turn_number += 1

        with open(FILENAME, 'a', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=',',
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
                    str(piece),
                    orig_health,
                    new_health,
                    defender_orig_health,
                    defender_final_health,
                    piece_attacked,
                    special
                    ))

