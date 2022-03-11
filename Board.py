from Piece import Piece

class Board:

    def __init__(self, size : int):
        """
        inits the board state to nothing
        @param {int} size: the width and height of the board
        """
        self.size = size
        self.reset_board()

    def reset_board(self):
        """
        resets the board to nothing (no pieces)
        """
        self.state = [[[] for i in range(self.size)] for j in range(self.size)]


    def place_piece(self, row : int, col : int, piece : Piece):
        """
        places a single piece on the board at the given location
        @param {int} row: the row to place the piece
        @param {int} col: the column to place the piece
        @param {Piece} piece: 
        """
        self.state[row][col].append(piece)

    def get_piece_at(self, row : int, col : int) -> bool:
        """
        decides if there is a piece at the desired location
        @param {int} row: the row to check
        @param {int} col: the column to check
        """
        return len(self.state[row][col]) > 0





