
class PieceLocation:
    """
    storage class for storing the location of a piece.
    Everything in this class should be read-only, so might as well be public.
    """

    def __init__(self, row : int, col : int, index : int=0):
        self.row = row
        self.col = col
        self.index = index

    def same_space(self, other):
        """
        checks to see if this location is in the same space as another location.
        @param {PieceLocation} other: other location to compare to.
        """
        return self.row == other.row and self.col == other.col

    def __eq__(self, other):
        """
        checks to see if this location is exactly the same as another location
        @param {PieceLocation} other: other location to compare to.
        """
        return self.row == other.row and self.col == other.col and self.index == other.index

    def __hash__(self):
        """
        hash to compare to other objects
        """
        return hash((self.row, self.col, self.index))
