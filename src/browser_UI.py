
from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect

from PieceLocation import PieceLocation
from Board import Board
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King
from Pawn import Pawn


class BrowserUI:
    """
    Browser-based user interface.
    Uses http.server, and is thus NOT SECURE.
    """


    def __init__(self, board : Board, port : int = 8000):
        self.board = board
        self.names = {
                Rook    : 'rook',
                Knight  : 'knight',
                Bishop  : 'bishop',
                Queen   : "queen",
                King    : "king",
                Pawn    : "pawn"
                }
        self.colors = {
                Pawn.WHITE : 'white',
                Pawn.BLACK : 'black'
                }

        app = Flask(__name__)
        socket = SocketIO(app, async_mode=None)

        @app.route('/')
        def index():
            return render_template('index.html', sync_mode=socket.async_mode)

        @socket.on("connect")
        def handle_connect(auth):
            self.handle_connect(auth)

        @socket.on("q_view")
        def handle_view(message):
            self.handle_view(message)

        socket.run(app, debug=True, port=port)

    def handle_connect(self, auth):
        """ handles socket connections """
        # TODO: make this a method in board
        # NOTE: this currently doesn't allow for removing pieces (only adding)
        updated_pieces = {}
        for irow,row in enumerate(self.board.state):
            for icol,cell in enumerate(row):
                for i,piece in enumerate(cell):
                    updated_pieces[f'{irow},{icol},{i}'] = [
                            self.colors[piece.color],
                            self.names[piece.__class__]
                            ]


        emit("r_update_pieces", updated_pieces)

    def handle_view(self, message):
        """
        handles user requests to view a piece's moves/attacks
        """
        if 'row' not in message or \
                'col' not in message or \
                'index' not in message:
            return
        try:
            row = int(message['row'])
            col = int(message['col'])
            index = int(message['index'])
            loc = PieceLocation(row, col, index)
        except:
            # note: this broadcasts error; unideal
            return

        locs = self.board.get_piece_movement(loc) + \
               self.board.get_piece_attack(loc)
        emit('r_view', [[l.row, l.col, l.index] for l in locs])


    def get_user_action(self, player_turn_color : int):
        """
        queries user for a move.
        Does not return until the user selects their move.
        """
        return ("", None, None)


