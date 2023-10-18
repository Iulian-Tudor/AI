import time

# Inițializează puzzle-ul
def inițializează_puzzle(stare_inițială):
    puzzle = [[0] * 3 for _ in range(3)]
    celulă_goală = None
    for i in range(3):
        for j in range(3):
            puzzle[i][j] = stare_inițială[i * 3 + j]
            if stare_inițială[i * 3 + j] == 0:
                celulă_goală = (i, j)
    return puzzle, celulă_goală

# Verifică dacă este starea finală
def este_starea_finală(puzzle):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != i * 3 + j + 1 and puzzle[i][j] != 0:
                return False
    return True

# Funcție pentru mutare
ultima_celulă_goală = None  # Variabilă globală pentru a evita mutarea inversă

def mutare(puzzle, celulă_goală, direcție):
    global ultima_celulă_goală
    x, y = celulă_goală

    if direcție == 'sus' and x > 0 and (x - 1, y) != ultima_celulă_goală:
        puzzle[x][y], puzzle[x - 1][y] = puzzle[x - 1][y], puzzle[x][y]
        ultima_celulă_goală = (x, y)
        return puzzle, (x - 1, y)

    elif direcție == 'jos' and x < 2 and (x + 1, y) != ultima_celulă_goală:
        puzzle[x][y], puzzle[x + 1][y] = puzzle[x + 1][y], puzzle[x][y]
        ultima_celulă_goală = (x, y)
        return puzzle, (x + 1, y)

    elif direcție == 'stânga' and y > 0 and (x, y - 1) != ultima_celulă_goală:
        puzzle[x][y], puzzle[x][y - 1] = puzzle[x][y - 1], puzzle[x][y]
        ultima_celulă_goală = (x, y)
        return puzzle, (x, y - 1)

    elif direcție == 'dreapta' and y < 2 and (x, y + 1) != ultima_celulă_goală:
        puzzle[x][y], puzzle[x][y + 1] = puzzle[x][y + 1], puzzle[x][y]
        ultima_celulă_goală = (x, y)
        return puzzle, (x, y + 1)

    return None, celulă_goală

# Funcție pentru căutare IDDFS
def căutare_iddfs(puzzle, celulă_goală, adâncime):
    if este_starea_finală(puzzle):
        return puzzle
    if adâncime == 0:
        return None
    for direcție in ['sus', 'jos', 'stânga', 'dreapta']:
        următorul_puzzle, următoarea_celulă_goală = mutare(puzzle, celulă_goală, direcție)
        if următorul_puzzle is not None:
            rezultat = căutare_iddfs(următorul_puzzle, următoarea_celulă_goală, adâncime - 1)
            if rezultat is not None:
                return rezultat
    return None

def main():
    stare_inițială = [8, 6, 3, 2, 5, 4, 0, 7, 1]
    puzzle, celulă_goală = inițializează_puzzle(stare_inițială)
    print('Starea Inițială a Puzzle-ului:')
    for rând in puzzle:
        print(rând)
    print('Celula Goală Inițială:')
    print(celulă_goală)
    moment_de_start = time.time()
    soluție = căutare_iddfs(puzzle, celulă_goală, 30)  # Limita adâncimii pentru a evita execuția infinită
    timp_de_execuție = time.time() - moment_de_start
    print('Soluția:')
    if soluție is not None:
        for rând in soluție:
            print(rând)
    else:
        print('Nu există soluție.')
    print('Timpul de Execuție:')
    print(timp_de_execuție)

if __name__ == '__main__':
    main()
