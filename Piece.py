

class Piece:

    WHITE = 0
    BLACK = 1

    def __init__(self,
            hitpoints : float,
            attack : float,
            row: int,
            col: int,
            color : int):
        """
        generic chess piece class
        @param {float} hitpoints: the number of hitpoints this piece has
        @param {float} attack: the base damage this piece has
        @param {int} row: the row that this piece is in
        @param {int} col: the column that this piece is in
        @param {int} color: the color of this piece (0=white, 1=black)
        """
        self.hitpoints = hitpoints
        self.maxhitpoints = hitpoints
        self.attack = attack
        self.row = row
        self.col = col
        self.color = color

    def calculate_damage(self) -> float:
        """
        returns the damage expected, given this piece's hp and attack stats.
        """
        return self.attack * self.hitpoints / self.maxhitpoints

    def get_movement_spaces(self, boardSize : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space specified by (row, col) has a piece occupying it.
        returns: {list<tuple<int,int>>} of tuple coords
        """
        
        return []

    def get_attack_spaces(self, boardSize : int, check_piece_at, check_piece_color_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space specified by (row, col) has a piece occupying it.
        @param {Callable(int,int)} check_piece_color_at: function that returns the color of the piece at specified (row, col) coords
        returns: {list<tuple<int,int>>} of tuple coords
        """

        return []
