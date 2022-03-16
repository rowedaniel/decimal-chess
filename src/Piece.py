
from PieceLocation import PieceLocation

class Piece:
    """ Basic Chess Piece superclass. All chess pieces should inherit from this. """

    WHITE = 0
    BLACK = 1


    def __init__(self,
            hitpoints : float,
            attack : float,
            location : PieceLocation,
            color : int):
        """
        generic chess piece class
        @param {float} hitpoints: the number of hitpoints this piece has
        @param {float} attack: the base damage this piece has
        @param {PieceLocation} location: the location to put the piece at


        """
        self.hitpoints = hitpoints
        self.maxhitpoints = hitpoints
        self.attack = attack
        self.location = location
        self.color = color

        self.has_moved = False

    def move(self, loc : PieceLocation):
        """
        This is called whenever this piece is moved
        @param {PieceLocation} loc:  the location to move to.
        """

        if not self.location.same_space(loc):
            self.has_moved = True
        self.location = loc

    def calculate_damage(self) -> float:
        """
        returns the damage expected, given this piece's hp and attack stats.
        """
        return self.attack * self.hitpoints / self.maxhitpoints

    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} board_size: the size of the board
        @param {Callable(PieceLocation)} check_piece_at: function that checks if the space
            specified by has a piece occupying it.
        returns: {list<PieceLocation>} of locations
        """
        return []

    def get_attack_spaces(self, board_size : int, check_piece_at, check_opposing_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} board_size: the size of the board
        @param {Callable(loc:PieceLocation, color:int)} check_piece_at: function that checks if
            a piece exists at the specified location
        @param {Callable(loc:PieceLocation, color:int)} check_opposing_piece_at: function
            that checks if the space specified has a piece occupying it of the opposing color.
        returns: {list<PieceLocation>} of locations
        """

        return []
