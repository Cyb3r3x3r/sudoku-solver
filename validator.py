# validator.py

def is_valid_solution(board, m, n):
    size = m * n

    # Check rows
    for row in board:
        if sorted(row) != list(range(1, size + 1)):
            return False

    # Check columns
    for col in range(size):
        col_vals = [board[row][col] for row in range(size)]
        if sorted(col_vals) != list(range(1, size + 1)):
            return False

    # Check boxes
    for box_row in range(0, size, m):
        for box_col in range(0, size, n):
            box_vals = []
            for i in range(m):
                for j in range(n):
                    box_vals.append(board[box_row + i][box_col + j])
            if sorted(box_vals) != list(range(1, size + 1)):
                return False

    return True
