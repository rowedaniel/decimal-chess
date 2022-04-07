# Chess Project built for Yonas, using python

Current packages required:

flask
flask-socketio


to do list:
1. Add logging system
    - logging should save:
        [DONE] 1. game id
        [DONE] 2. turn #
        [DONE] 3. loc from
        [DONE] 4. loc to
        [DONE] 5. piece moved
        6. piece attacked (if any)
        8. health of old attacker
        9. health of new attacker
        10. health of defender
        11. total # of pieces on the board
2. detect if king is checkmated
    1. detect if a player has any kings on board
    2. detect if a piece is threatened
    3. detect if king is in check
3. Add the more obscure rules
    1. Castling
    2. Promotion
    3. En Passant
        - Currently works, but doesn't check if the piece moved last turn
4. Testing?
