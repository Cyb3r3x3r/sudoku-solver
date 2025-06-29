from flask import Flask, render_template, request
from solver import SudokuSolver
import time  # ⏱️ Import time
from validator import is_valid_solution
from backtracking import solve_backtracking
import copy

app = Flask(__name__)
#last_board = None

@app.route('/', methods=['GET', 'POST'])
def index():
    #global last_board

    if request.method == 'POST':
        m = int(request.form['m'])
        n = int(request.form['n'])
        size = m * n
        board = []

        for i in range(size):
            row = []
            for j in range(size):
                val = request.form.get(f'cell_{i}_{j}', '')
                row.append(int(val) if val.strip().isdigit() else 0)
            board.append(row)

        #last_board = (board, m, n)

        solver = SudokuSolver(board, m, n)

        start_time = time.time()
        solution = solver.solve()
        solve_time = round(time.time() - start_time, 4)

        if solution is None:
        # fallback to backtracking
            board_copy = copy.deepcopy(board)
            bt_start = time.time()
            if solve_backtracking(board_copy, m, n):
                solution = board_copy
                solve_time = round(time.time() - bt_start, 4)
                method = "Backtracking"
            else:
                return "<h3>❌ No valid solution found.</h3>"
        else:
            method = "Simulated Annealing"

        if solution:
            is_valid = is_valid_solution(solution, m, n)
            return render_template(
                'result.html',
                solution=solution,
                initial_board=board,
                m=m,
                n=n,
                is_valid=is_valid_solution(solution, m, n),
                solve_time=solve_time,
                method=method
            )
        else:
            return "<h3>❌ Failed to solve Sudoku. Try again.</h3>"

    return render_template('index.html')
if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)