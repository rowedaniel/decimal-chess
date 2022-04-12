
from Piece import Piece

from Queen import Queen
#from Rook import Rook
#from Bishop import Bishop
#from Knight import Knight

from PieceLocation import PieceLocation

class Pawn(Piece):
    """ Pawn Chess piece """

    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:
        spaces = []

        # bottom-right diagonal
        for i in range(2 - (self.move_count > 0)):
            row = self.location.row + ( -1 if self.color == Piece.BLACK else 1 ) * (i+1)
            col = self.location.col
            loc = PieceLocation(row, col)
            if 0 <= row < board_size and not check_piece_at(loc):
                spaces.append(loc)

        return spaces

    def get_attack_spaces(self, board_size : int, check_piece_at, check_opposing_piece_at) -> list:
        spaces = []

        # bottom-right/left diagonal
        row = self.location.row + ( -1 if self.color == Piece.BLACK else 1 )
        for col in (self.location.col-1, self.location.col+1):
            loc = PieceLocation(row, col)
            if 0 <= row < board_size and \
                    0 <= col < board_size:
                spaces.extend(check_opposing_piece_at(loc, self.color))

        return spaces

    def get_special_attack_spaces(self, board_size : int,
                                  check_piece_at,
                                  check_opposing_piece_at,
                                  get_piece_at):
        """
        Pawn's special movement: En Passant
        """
        spaces = {}


        # promotion is considered a special attack, so deal with that now.
        if self.location.row == (self.color == Piece.WHITE) * (board_size-3) + 1:
            loc = PieceLocation(
                    self.location.row+ (-1 if self.color == Piece.BLACK else 1),
                    self.location.col)
            print('promotion op! ==================================================')
            print(loc.row, loc.col)
            spaces[loc] = loc

        side_row = (board_size-1) * (self.color == Piece.WHITE) + \
                3 * (-1 if self.color == Piece.WHITE else 1)
        if self.location.row != side_row:
            # en passant can only happen on 2nd row from the opponent
            return spaces

        # bottom-right/left diagonal
        row = self.location.row + ( -1 if self.color == Piece.BLACK else 1 )
        for col in (self.location.col-1, self.location.col+1):
            loc = PieceLocation(row, col) # location this pawn would move to
            side_tile = PieceLocation(side_row, col) # location of piece attacked

            if 0 <= row < board_size and \
               0 <= col < board_size and \
               not check_piece_at(loc):


                side_locs = check_opposing_piece_at(side_tile, self.color)
                for side_loc in side_locs:
                    # space to move is clear, and opposing piece is to the side.
                    # next, make sure that the opposing piece:
                    #  1. is in fact a pawn
                    #  2. moved 2 spaces in one turn (turn count is 1)
                    #  3. moved last turn
                    attacking_piece = get_piece_at(side_loc)
                    if attacking_piece.__class__ == self.__class__ and \
                            attacking_piece.move_count == 1 and \
                            True: #attacking_piece.just_moved:
                        spaces[loc] = side_loc

        return spaces

    def calculate_damage(self, other):
        if other is self:
            return self.maxhitpoints
        return super().calculate_damage(other)

    def attack(self, loc : PieceLocation, piece, get_total_hp):
        print('attacking!', loc.row, loc.col)
        # NOTE: constant board size of 8 assumed here
        if loc.row == (self.color == Piece.WHITE) * 7:
            # promoting!
            # TODO: implement promotion other than queen

            if piece:
                piece.damage(self.calculate_damage(piece))

            damage_moved = self.damage(self.maxhitpoints - get_total_hp(loc))
            return Queen(damage_moved,
                    self.maxhitpoints,
                    self.attack_points, # NOTE: is this what we want?
                    loc,
                    self.color,
                    self.move_count)

        return super().attack(loc, piece, get_total_hp)


    def __str__(self):
        return 'pawn'
