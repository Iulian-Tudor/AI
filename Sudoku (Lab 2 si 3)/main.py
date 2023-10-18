import time


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

    return False



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

    # Map directions to their logic
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
def cautare_iddfs(puzzle, empty_cell, depth):
    if este_starea_finala(puzzle):
        return puzzle
    if depth == 0:
        return None
    for directie in ['sus', 'jos', 'stanga', 'dreapta']:
        next_puzzle, next_empty_cell = move(puzzle, empty_cell, directie)
        if next_puzzle is not None:
            rezultat = cautare_iddfs(next_puzzle, next_empty_cell, depth - 1)
            if rezultat is not None:
                return rezultat
    return None


def main():
    lst = []
    for i in range(0, 9):           # Citire de instanta de la tastatura
        element = int(input())
        lst.append(element)

    # stare_initiala = [8, 6, 3, 2, 5, 4, 0, 7, 1]
    puzzle, empty_cell = initializeaza_puzzle(lst)
    print('Starea Initiala a Puzzle-ului:')
    for i in puzzle:
        print(i)

    print('Celula Goala Initiala:')
    print(empty_cell)
    moment_de_start = time.time()
    solutie = cautare_iddfs(puzzle, empty_cell, 30)  # Limita adancimii pentru a evita executia infinita
    timp_de_executie = time.time() - moment_de_start

    print('Solutia:')
    if solutie is not None:
        for i in solutie:
            print(i)
    else:
        print('Nu exista solutie.')
    print('Timpul de Executie:')
    print(timp_de_executie)


if __name__ == '__main__':
    main()
