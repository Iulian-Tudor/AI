import copy


def get_empty_cells(board):
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    return empty_cells


def check_values(board, values, row, col):
    # Check row
    for j in range(9):
        if board[row][j] in values:
            values.remove(board[row][j])
    # Check column
    for i in range(9):
        if board[i][col] in values:
            values.remove(board[i][col])
    # Check box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] in values:
                values.remove(board[i][j])
    return values

def get_possible_values(board, row, col):
    values = set(range(1, 10))
    return check_values(board, values, row, col)


def forward_checking(board, empty_cells, domain):
    new_domain = copy.deepcopy(domain)
    for cell in empty_cells:
        row, col = cell
        values = new_domain[(row, col)]
        new_domain[(row, col)] = check_values(board, values, row, col)
    return new_domain


def mrv(empty_cells, domain):
    min_cell = None
    min_values = float('inf')
    for cell in empty_cells:
        values = domain[cell]
        if len(values) < min_values:
            min_cell = cell
            min_values = len(values)
    return min_cell

def solve(board, empty_cells, domain):
    if not empty_cells:
        return board
    cell = mrv(empty_cells, domain)
    values = domain[cell]
    for value in values:
        new_board = copy.deepcopy(board)
        new_board[cell[0]][cell[1]] = value
        new_empty_cells = empty_cells.copy()
        new_empty_cells.remove(cell)
        new_domain = forward_checking(new_board, new_empty_cells, domain)
        if all(len(new_domain[cell]) > 0 for cell in new_empty_cells):
            result = solve(new_board, new_empty_cells, new_domain)
            if result:
                return result
    return None


def sudoku_solver(board):
    # Initialize domain for each empty cell
    empty_cells = get_empty_cells(board)
    domain = {}
    for cell in empty_cells:
        domain[cell] = get_possible_values(board, cell[0], cell[1])

    # Solve the board
    solved_board = solve(board, empty_cells, domain)

    return solved_board


def main():
    # Custom Sudoku initial state
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    # Solve the Sudoku board
    solved_board = sudoku_solver(board)

    # Print the solved Sudoku board
    for row in solved_board:
        print(row)


if __name__ == "__main__":
    main()
