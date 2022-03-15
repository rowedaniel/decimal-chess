from Piece import Piece

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
        @param {Piece} piece: the piece to place
        """
        self.state[row][col].append(piece)

    def get_piece_at(self, row : int, col : int) -> bool:
        """
        decides if there is a piece at the desired location
        @param {int} row: the row to check
        @param {int} col: the column to check
        """
        return len(self.state[row][col]) > 0

    def get_piece_color_at(self, row : int, col : int) -> list:
        """
        decides if there is a piece at the desired location
        @param {int} row: the row to check
        @param {int} col: the column to check
        returns: list<int>: list of piece colors at that space

        """
        return (cell.color for cell in self.state[row][col])

    def check_opposing_piece_at(self, row : int, col : int, color : int) -> bool:
        """
        decides if there is a piece of the opposing color at the desired location
        @param {int} row: the row to check
        @param {int} col: the column to check
        @param {int} color: the color to check
        """
        return any((c != color for c in self.get_piece_color_at(row, col)))

    def move_piece(self, row1 : int, col1 : int,
                         row2 : int, col2 : int):
        """
        moves piece at designated row, col to new designated row, col
        """

        piece = self.state[row1][col1].pop()
        # TODO: make this better. Currently very bad practice
        piece.row = row2
        piece.col = col2
        self.state[row2][col2].append(piece)
