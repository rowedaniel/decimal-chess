from Piece import Piece

class Rook(Piece):
    def get_movement_spaces(self, boardSize : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space specified by (row, col) has a piece occupying it.
        returns: {list<tuple<int,int>>} of tuple coords
        """
        
        spaces = []

        # right line 
        row = self.row + 1
        col = self.col
        while row < boardSize:
            if check_piece_at(row, col) and check_piece_color_at(row, col) != self.color:
                spaces.append((row, col))
                break
            row += 1

        # bottom line
        row = self.row
        col = self.col + 1
        while col < boardSize:
            if check_piece_at(row, col) and check_piece_color_at(row, col) != self.color:
                spaces.append((row, col))
                break
            col += 1

        # left line
        row = self.row - 1
        col = self.col
        while row >= 0:
            if check_piece_at(row, col) and check_piece_color_at(row, col) != self.color:
                spaces.append((row, col))
                break
            row -= 1

        # left line
        row = self.row
        col = self.col - 1
        while col >= 0:
            if check_piece_at(row, col) and check_piece_color_at(row, col) != self.color:
                spaces.append((row, col))
                break
            col -= 1

        return spaces



