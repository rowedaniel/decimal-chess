# Chess Project built for Yonas, using python

Current packages required:

flask
flask-socketio


to do list:
1. Make graphical interface. Consider options:
    - Tkinter
    - Browser
2. Add logging system
    - logging should save:
        1. game id
        2. turn #
        3. loc from
        4. loc to
        5. piece moved
        6. piece attacked (if any)
        8. health of old attacker
        9. health of new attacker
        10. health of defender
        11. total # of pieces on the board
3. detect if king is checkmated
    1. detect if a piece is threatened
    2. detect if king is in check
4. Add the more obscure rules
    1. Castling
    2. Promotion
5. Testing?
