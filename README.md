# chessboard_path_finding
""" Rules on the original board
    1. Topology:
        a. The first column is the leftmost,
        b. the first row is the bottom row of the board.
            e.g. the_original_board[0, 3] = 55. We take the first column from the left and the fourth row from the bottom.
    2. Movements:
        a. The value of -1 means the wall, and you cannot go through it,
        b. the value of 0 means freedom, and you can go in any direction,
        c. values that are greater than 0 mean 'jumping off', you can jump when you step on those positions.
            e.g. the_original_board[col, row] = 37 means that you are now teleported to the cell [col = 3, row = 7]
    Requirement(s):
    Find the shortest path from start = (0, 0) to goal (8, 8)
"""
