import copy
import timeit


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


def get_possible_values(board, row, col, even_cells):
    values = set(range(1, 10))
    if row and col in even_cells:
        values = {2, 4, 6, 8}
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


def solve_without_MRV(board, empty_cells, domain):
    if not empty_cells:
        return board
    cell = empty_cells[0]  # Select the first empty cell
    values = domain[cell]
    for value in values:
        new_board = copy.deepcopy(board)
        new_board[cell[0]][cell[1]] = value
        new_empty_cells = empty_cells.copy()
        new_empty_cells.remove(cell)
        new_domain = forward_checking(new_board, new_empty_cells, domain)
        if all(len(new_domain[cell]) > 0 for cell in new_empty_cells):
            result = solve_without_MRV(new_board, new_empty_cells, new_domain)
            if result:
                return result
    return False


def solve_with_MRV(board, empty_cells, domain):
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
            result = solve_with_MRV(new_board, new_empty_cells, new_domain)
            if result:
                return result
    return False


def check_even_numbers(board, num_evens):
    count = 0
    for row in board:
        for num in row:
            if num != 0 and num % 2 == 0:
                count += 1
    if count >= num_evens:
        return True
    else:
        return False


def sudoku_solver(board, solver, even_cells):
    # Initialize domain for each empty cell
    empty_cells = get_empty_cells(board)
    domain = {}
    for cell in empty_cells:
        domain[cell] = get_possible_values(board, cell[0], cell[1], even_cells)

    solved_board = solver(board, empty_cells, domain)

    return solved_board


def main():
    board = [
        [0, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    even_cells = {(0,0), (1,1), (2,2)}
    num_evens = 10
    if not check_even_numbers(board, num_evens):
        print(f"Error:Board should have at least {num_evens} even values on the board")
        return
    else:
        # with MRV
        start_time = timeit.default_timer()
        solved_board_with_MRV = sudoku_solver(board, solve_with_MRV, even_cells)
        end_time = timeit.default_timer()
        print("Time taken to solve with MRV: ", end_time - start_time, "seconds")
        if solved_board_with_MRV:
            for row in solved_board_with_MRV:
                print(row)
        else:
            print("No solution found")

        print("\n")

        # without MRV
        start_time = timeit.default_timer()
        solved_board_without_MRV = sudoku_solver(board, solve_without_MRV, even_cells)
        end_time = timeit.default_timer()
        print("Time taken to solve without MRV: ", end_time - start_time, "seconds")
        if solved_board_without_MRV:
            for row in solved_board_without_MRV:
                print(row)
        else:
            print("No solution found")


if __name__ == "__main__":
    main()
