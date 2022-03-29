from abc import abstractmethod
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
        self.attack_points = attack
        self.location = location
        self.color = color

        self.move_count = 0

    def move(self, loc : PieceLocation):
        """
        This is called whenever this piece is moved
        @param {PieceLocation} loc:  the location to move to.
        """

        if not self.location.same_space(loc):
            self.move_count += 1
        self.location = loc

    def attack(self, loc : PieceLocation, piece):
        """
        Attacks the given piece, dealing damage.
        NOTE: this method is NOT responsible for moving any pieces, only for damage calculation.
        @param {Piece} piece: the piece to deal damage to.
        returns {Piece}: new piece created after dealing damage to the old one.
        """

        # TODO: implement fancy version. For now, just make it normal chess.
        damage_dealt = piece.damage(self.calculate_damage())
        self.damage(damage_dealt)
        print("did", damage_dealt, "damage. Attacked piece is now at:", piece.hitpoints)
        return self.__class__(damage_dealt, self.attack_points, loc, self.color)

    def damage(self, damage : float) -> float:
        """
        Damages this piece, and returns the damage dealt
        @param {float} damage: the incoming damage
        returns {float}: the damage actually dealt
        """
        if damage > self.hitpoints:
            damage = self.hitpoints
        self.hitpoints -= damage
        return damage

    def calculate_damage(self) -> float:
        """
        returns the damage expected, given this piece's hp and attack stats.
        Currently rounds damage DOWN
        """

        # for testing purposes, using infinite (999) damage value here for now.
        return 999 #self.attack_points * self.hitpoints // self.maxhitpoints


    def is_dead(self) -> bool:
        """
        returns if this piece is dead (hp <= 0) or not
        """
        return self.hitpoints <= 0

    @abstractmethod
    def get_movement_spaces(self, board_size : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} board_size: the size of the board
        @param {Callable(PieceLocation)} check_piece_at: function that checks if the space
            specified by has a piece occupying it.
        returns: {list<PieceLocation>} of locations
        """
        return []

    @abstractmethod
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

    def get_special_movement_spaces(self, board_size : int, check_piece_at, get_piece_at):
        # TODO: this is gonna need more inputs. Rethink?
        """
        returns a dictionary of the possible movement spaces
            mapped to a dictionary of other pieces to be moved.
        @param {int} board_size: the size of the board
        @param {Callable(loc:PieceLocation, color:int)} check_piece_at: function that checks if
            a piece exists at the specified location
        @param {Callable(loc:PieceLocation)} get_piece_at: function
            that returns the pointer to the piece at the specified location
        returns: {dict<PieceLocation,dict<PieceLocation,PieceLocation>>} where the keys are the
            possible locations this piece could move to, and the values are dictionaries of
            the locations that other pieces would have to move to.
        """
        return {}

    def get_special_attack_spaces(self, board_size : int,
                                  check_piece_at,
                                  check_opposing_piece_at,
                                  get_piece_at):
        """
        returns a dictionary of possible spaces to move to, and the pieces attacked
        @param {int} board_size: the size of the board
        @param {Callable(loc:PieceLocation, color:int)} check_piece_at: function that checks if
            a piece exists at the specified location
        @param {Callable(loc:PieceLocation, color:int)} check_opposing_piece_at: function
            that checks if the space specified has a piece occupying it of the opposing color.
        @param {Callable(loc:PieceLocation)} get_piece_at: function
            that returns the pointer to the piece at the specified location
        returns: {dict<PieceLocation,PieceLocation>} where the keys are the spaces where
            this piece moves to, and the values are the locations of the attacked pieces
        """
        return {}
