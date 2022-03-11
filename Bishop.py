from Piece import Piece

class Bishop(Piece):
    def get_movement_spaces(self, boardSize : int, check_piece_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space specified by (row, col) has a piece occupying it.
        returns: {list<tuple<int,int>>} of tuple coords
        """
        
        spaces = []

        # bottom-right diagonal
        row = self.row + 1
        col = self.col + 1
        while row < boardSize and col < boardSize and not check_piece_at(row, col):
            spaces.append((row, col))
            row += 1
            col += 1

        # bottom-left diagonal
        row = self.row + 1
        col = self.col - 1
        while row < boardSize and col >= 0 and not check_piece_at(row, col):
            spaces.append((row, col))
            row += 1
            col -= 1

        # top-right diagonal
        row = self.row - 1
        col = self.col + 1
        while row >= 0 and col < boardSize and not check_piece_at(row, col):
            spaces.append((row, col))
            row -= 1
            col += 1

        # top-left diagonal
        row = self.row - 1
        col = self.col - 1
        while row >= 0 and col >= 0 and not check_piece_at(row, col):
            spaces.append((row, col))
            row -= 1
            col -= 1

        return spaces



    def get_attack_spaces(self, boardSize : int, check_piece_at, check_piece_color_at) -> list:
        """
        returns an array of all possible locations to move to (not including attacking)
        @param {int} boardSize: the size of the board
        @param {Callable(int,int)} check_piece_at: function that checks if the space specified by (row, col) has a piece occupying it.
        @param {Callable(int,int)} check_piece_color_at: function that returns the color of the piece at specified (row, col) coords
        returns: {list<tuple<int,int>>} of tuple coords
        """

        spaces = []

        # bottom-right diagonal
        row = self.row + 1
        col = self.col + 1
        while row < boardSize and col < boardSize:
            if check_piece_at(row, col) and check_piece_color_at(row, col) != self.color:
                spaces.append((row, col))
                break
            row += 1
            col += 1

        # bottom-left diagonal
        row = self.row + 1
        col = self.col - 1
        while row < boardSize and col >= 0:
            if check_piece_at(row, col) and check_piece_color_at(row, col) != self.color:
                spaces.append((row, col))
                break
            row += 1
            col -= 1

        # top-right diagonal
        row = self.row - 1
        col = self.col + 1
        while row >= 0 and col < boardSize:
            if check_piece_at(row, col) and check_piece_color_at(row, col) != self.color:
                spaces.append((row, col))
                break
            row -= 1
            col += 1

        # top-left diagonal
        row = self.row - 1
        col = self.col - 1
        while row >= 0 and col >= 0:
            if check_piece_at(row, col) and check_piece_color_at(row, col) != self.color:
                spaces.append((row, col))
                break
            row -= 1
            col -= 1

        return spaces

