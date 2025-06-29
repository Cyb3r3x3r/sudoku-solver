def is_valid(board, row, col, num, size, m, n):
    box_row = (row // m) * m
    box_col = (col // n) * n

    for i in range(size):
        if board[row][i] == num or board[i][col] == num:
            return False

    for i in range(m):
        for j in range(n):
            if board[box_row + i][box_col + j] == num:
                return False

    return True


def find_empty(board, size):
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return i, j
    return None


def solve_backtracking(board, m, n):
    size = m * n
    empty = find_empty(board, size)
    if not empty:
        return True  # solved

    row, col = empty
    for num in range(1, size + 1):
        if is_valid(board, row, col, num, size, m, n):
            board[row][col] = num
            if solve_backtracking(board, m, n):
                return True
            board[row][col] = 0

    return False
