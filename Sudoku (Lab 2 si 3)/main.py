import time

# Funcția de inițializare
def initialize(input_state):
    state = [[0] * 3 for _ in range(3)]
    empty_cell = None
    for i in range(3):
        for j in range(3):
            state[i][j] = input_state[i * 3 + j]
            if input_state[i * 3 + j] == 0:
                empty_cell = (i, j)
    return state, empty_cell

# Funcția de verificare a stării finale
def is_final(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] != i * 3 + j + 1 and state[i][j] != 0:
                return False
    return True

# Funcțiile de tranziție
last_empty_cell = None

# Funcția de tranziție
def move(state, empty_cell, direction):
    global last_empty_cell
    x, y = empty_cell
    if direction == 'up' and x > 0 and (x - 1, y) != last_empty_cell:
        state[x][y], state[x - 1][y] = state[x - 1][y], state[x][y]
        last_empty_cell = (x, y)
        return state, (x - 1, y)
    elif direction == 'down' and x < 2 and (x + 1, y) != last_empty_cell:
        state[x][y], state[x + 1][y] = state[x + 1][y], state[x][y]
        last_empty_cell = (x, y)
        return state, (x + 1, y)
    elif direction == 'left' and y > 0 and (x, y - 1) != last_empty_cell:
        state[x][y], state[x][y - 1] = state[x][y - 1], state[x][y]
        last_empty_cell = (x, y)
        return state, (x, y - 1)
    elif direction == 'right' and y < 2 and (x, y + 1) != last_empty_cell:
        state[x][y], state[x][y + 1] = state[x][y + 1], state[x][y]
        last_empty_cell = (x, y)
        return state, (x, y + 1)
    return None, empty_cell

# Funcția de căutare IDDFS
def iddfs(state, empty_cell, depth):
    if is_final(state):
        return state
    if depth == 0:
        return None
    for direction in ['up', 'down', 'left', 'right']:
        next_state, next_empty_cell = move(state, empty_cell, direction)
        if next_state is not None:
            result = iddfs(next_state, next_empty_cell, depth - 1)
            if result is not None:
                return result
    return None

def main():
    input_state = [8, 6, 3, 2, 5, 4, 0, 7, 1]
    state, empty_cell = initialize(input_state)
    print('Starea inițială:')
    for row in state:
        print(row)
    print('Celula goală inițială:')
    print(empty_cell)
    start_time = time.time()
    solution = iddfs(state, empty_cell, 30)  # Limita la adancime sa nu ruleze la infinit fara sa-mi dau seama
    execution_time = time.time() - start_time
    print('Soluția:')
    if solution is not None:
        for row in solution:
            print(row)
    else:
        print('Nu există soluție.')
    print('Timpul de execuție:')
    print(execution_time)


main()
