import time
from copy import deepcopy
from queue import PriorityQueue


# Inițializează puzzle-ul
def initializeaza_puzzle(stare_initiala):
    puzzle = [[0] * 3 for _ in range(3)]
    empty_cell = None
    for i in range(3):
        for j in range(3):
            puzzle[i][j] = stare_initiala[i * 3 + j]
            if stare_initiala[i * 3 + j] == 0:
                empty_cell = (i, j)
    return puzzle, empty_cell


# Verifica daca este starea finala
def este_starea_finala(puzzle):

    puzzle_flattened = [item for sublist in puzzle for item in sublist]

    # Este 0 primul element si restul listei este sortat?
    if puzzle_flattened[0] == 0 and puzzle_flattened[1:] == sorted(puzzle_flattened[1:]):
        return True

    # Este 0 ultimul element si restul listei este sortat?
    if puzzle_flattened[-1] == 0 and puzzle_flattened[:-1] == sorted(puzzle_flattened[:-1]):
        return True

    # take 0 out of the list and check if it's sorted (the rest of the list)
    puzzle_without_0 = [i for i in puzzle_flattened if i != 0]
    if puzzle_without_0 == sorted(puzzle_without_0):
        return True

    return False


def manhattan_distance(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0:
                goal_i = (puzzle[i][j] - 1) // 3
                goal_j = (puzzle[i][j] - 1) % 3
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


def hamming_distance(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0 and puzzle[i][j] != (i * 3 + j + 1):
                distance += 1
    return distance


def linear_conflict(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0:
                goal_i = (puzzle[i][j] - 1) // 3
                goal_j = (puzzle[i][j] - 1) % 3
                if i < goal_i:
                    distance += sum(1 for k in range(i + 1, goal_i + 1) if puzzle[k][j] != 0)
                elif i > goal_i:
                    distance += sum(1 for k in range(goal_i, i) if puzzle[k][j] != 0)
                if j < goal_j:
                    distance += sum(1 for k in range(j + 1, goal_j + 1) if puzzle[i][k] != 0)
                elif j > goal_j:
                    distance += sum(1 for k in range(goal_j, j) if puzzle[i][k] != 0)
    return distance


# Functie pentru mutare
last_empty_cell = None  # Variabila globala pentru a evita mutarea inversa


def swap_cells(puzzle, current_cell, new_cell):
    x1, y1 = current_cell
    x2, y2 = new_cell
    puzzle[x1][y1], puzzle[x2][y2] = puzzle[x2][y2], puzzle[x1][y1]
    return puzzle, new_cell


def move(puzzle, empty_cell, direction):
    global last_empty_cell
    x, y = empty_cell

    # Dictionar
    directions = {
        'sus': ((x > 0, (x - 1, y))),
        'jos': ((x < 2, (x + 1, y))),
        'stanga': ((y > 0, (x, y - 1))),
        'dreapta': ((y < 2, (x, y + 1)))
    }

    if direction in directions:
        condition, new_cell = directions[direction]
        if condition and new_cell != last_empty_cell:
            last_empty_cell = empty_cell
            return swap_cells(puzzle, empty_cell, new_cell)

    return None, empty_cell


# Functie pentru cautare IDDFS
def iddfs(puzzle, empty_cell, depth, steps=0):
    if este_starea_finala(puzzle):
        return puzzle, steps
    if depth == 0:
        return None, steps
    for directie in ['sus', 'jos', 'stanga', 'dreapta']:
        next_puzzle, next_empty_cell = move(puzzle, empty_cell, directie)
        if next_puzzle is not None:
            solutie, steps = iddfs(next_puzzle, next_empty_cell, depth - 1, steps + 1)
            if solutie is not None:
                return solutie, steps
    return None, steps

def greedy_best_first(puzzle, empty_cell, heuristic, steps=0):

    queue = PriorityQueue()
    queue.put((heuristic(puzzle), steps, puzzle, empty_cell))

    visited_states = set()

    while not queue.empty():
        _, steps, puzzle, empty_cell = queue.get()
        state = tuple(map(tuple, puzzle))

        if state in visited_states:
            continue
        visited_states.add(state)

        if este_starea_finala(puzzle):
            return puzzle, steps

        for directie in ['sus', 'jos', 'stanga', 'dreapta']:
            next_puzzle, next_empty_cell = move(deepcopy(puzzle), empty_cell, directie)
            if next_puzzle is not None:
                h = heuristic(next_puzzle)
                queue.put((h, steps + 1, next_puzzle, next_empty_cell))

    return None, steps


def a_star(puzzle, empty_cell, heuristic, steps=0):
    queue = PriorityQueue()
    queue.put((0, steps, puzzle, empty_cell))

    while not queue.empty():
        _, steps, puzzle, empty_cell = queue.get()

        if este_starea_finala(puzzle):
            return puzzle, steps

        for directie in ['sus', 'jos', 'stanga', 'dreapta']:
            next_puzzle, next_empty_cell = move(puzzle, empty_cell, directie)
            if next_puzzle is not None:
                g = steps + 1
                h = heuristic(next_puzzle)
                f = g + h
                queue.put((f, g, next_puzzle, next_empty_cell))


    return None, steps


def main():
    stare_initiala = [[8, 6, 7, 2, 5, 4, 0, 3, 1], [2, 5, 3, 1, 0, 6, 4, 7, 8], [2, 7, 5, 0, 8, 4, 3, 1, 6]]

    strategies = ['IDDFS', 'Greedy Manhattan', 'Greedy Hamming', 'Greedy Linear Conflict']
    heuristics = [None, manhattan_distance, hamming_distance, linear_conflict]

    for stare in stare_initiala:
        puzzle, empty_cell = initializeaza_puzzle(stare)
        for strategy, heuristic in zip(strategies, heuristics):
            print(f'Running {strategy} with starting position {stare}...')
            moment_de_start = time.time()
            if strategy == 'IDDFS':
                solutie, steps = iddfs(deepcopy(puzzle), empty_cell, 30)
            else:
                solutie, steps = greedy_best_first(deepcopy(puzzle), empty_cell, heuristic)
            timp_de_executie = time.time() - moment_de_start

            if solutie is not None:
                print('Solutia:')
                for i in solutie:
                    print(i)
                print('Lungimea solutiei:', steps)
            else:
                print('Nu exista solutie.')
            print('Timpul de Executie:', timp_de_executie)

        puzzle, empty_cell = initializeaza_puzzle(stare)
        moment_de_start = time.time()
        bonus_solutie, steps = a_star(deepcopy(puzzle), empty_cell, manhattan_distance)
        timp_de_executie = time.time() - moment_de_start
        print('Running A* with starting position', stare, '...')
        if bonus_solutie is not None:
            print('Solutia:')
            for i in bonus_solutie:
                print(i)
            print('Lungimea solutiei:', steps)
        else:
            print('Nu exista solutie.')
        print('Timpul de Executie:', timp_de_executie)


if __name__ == '__main__':
    main()
