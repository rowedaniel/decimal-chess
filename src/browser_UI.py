
#from flask import Flask, render_template, session, copy_current_request_context
#from flask_socketio import SocketIO, emit, disconnect
from threading import Thread, Event
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

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
        self.won = False
        self.winning_color = 0

        self.turn_color = Pawn.WHITE
        self.enable_move = False
        self.move_action = None
        self.quit_action = False

        self.update_board_event = Event()
        self.has_acted_event = Event()
        self.win_event = Event()

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

        @socket.on("q_move")
        def handle_move(message):
            self.handle_move(message)

        @socket.on("q_quit")
        def handle_quit(message):
            self.handle_quit()

        @socket.on("q_restart")
        def handle_restart(message):
            self.handle_restart()

        @socket.on("disconnect")
        def handle_disconnect():
            pass
            #self.handle_quit()


        self.website_thread = Thread(target=lambda: socket.run(app, debug=False, use_reloader=False, port=port))
        self.website_thread.setDaemon(True)
        self.website_thread.start()


    def handle_connect(self, auth):
        """ handles socket connections """
        self.send_board()

    def handle_view(self, message):
        """
        handles user requests to view a piece's moves/attacks
        """
        loc = self.get_client_pos(message)
        if loc is None:
            return

        locs = self.board.get_piece_movement(loc) + \
               self.board.get_piece_attack(loc)
        emit('r_view', [[l.row, l.col, l.index] for l in locs])

    def handle_move(self, message):
        """
        handles user requests to move
        """
        if not self.enable_move:
            return

        if 'from' not in message or 'to' not in message:
            return

        loc1 = self.get_client_pos(message['from'])
        loc2 = self.get_client_pos(message['to'])
        if loc1 is None or loc2 is None:
            return


        if self.turn_color != self.board.get_piece_color_at(loc1):
            return


        locs = self.board.get_piece_movement(loc1) + \
               self.board.get_piece_attack(loc1)
        if loc2 not in locs:
            return

        self.move_action = (loc1, loc2)
        self.has_acted_event.set()

        self.update_board_event.clear()
        self.update_board_event.wait()
        self.send_board()

    def handle_quit(self):
        """
        when a client quits, call this to notify the game manager
        """
        self.quit_action = True
        self.has_acted_event.set()
        self.win_event.set()

    def handle_restart(self):
        """
        when client requests a reset, this is called.
        """
        self.quit_action = False
        self.win_event.set()

    def alert_won(self, color : int):
        """
        alerts client that someone has won
        """
        self.won = True
        self.winning_color = color

        print('alerting win!')
        self.update_board_event.set()

        self.win_event.clear()
        self.win_event.wait(timeout=60)

        self.won = False

        return not self.quit_action

    def send_board(self):
        """
        sends the current board state to the client
        alternatively, if the board is won, then send that information.
        """

        # TODO: make this a method in board
        # NOTE: this currently doesn't allow for removing pieces (only adding)
        updated_pieces = {}
        for irow,row in enumerate(self.board.state):
            for icol,cell in enumerate(row):
                for i,piece in enumerate(cell):
                    updated_pieces[f'{irow},{icol},{i}'] = {
                            'color' : self.colors[piece.color],
                            'name'  : self.names[piece.__class__],
                            'hp'    : piece.hitpoints
                            }

        data = {}
        data["pieces"] = updated_pieces
        data["color"] = self.colors[self.turn_color]
        data["won"] = self.won
        data["winner"] = self.colors[self.winning_color]
        data["turnnum"] = self.board.turn_number

        emit("r_update_pieces", data)


    def get_client_pos(self, message):
        """
        converts the javascript-style messages from socket
        to normal PieceLocations.
        @param<map> message: incoming socket message
        returns: <PieceLocation>
        """
        if 'row' not in message or \
                'col' not in message or \
                'index' not in message:
            return None
        try:
            row = int(message['row'])
            col = int(message['col'])
            index = int(message['index'])
            return PieceLocation(row, col, index)
        except:
            # note: this broadcasts error; unideal
            return None




    def get_user_action(self, player_turn_color : int):
        """
        queries user for a move.
        Does not return until the user selects their move.
        """

        self.update_board_event.set()

        self.turn_color = player_turn_color
        self.enable_move = True

        self.has_acted_event.clear()
        self.has_acted_event.wait()

        self.enable_move = False
        if self.quit_action:
            return 'quit', None, None
        if self.move_action:
            return "move", self.move_action[0], self.move_action[1]
        return "", None, None
