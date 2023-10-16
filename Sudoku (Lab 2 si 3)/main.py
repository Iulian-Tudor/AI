

# Funcția de inițializare
def initialize(input_state):
    state = [[0]*3 for _ in range(3)]
    empty_cell = None
    for i in range(9):
        state[i//3][i%3] = input_state[i]
        if input_state[i] == 0:
            empty_cell = (i//3, i%3)
    return state, empty_cell


# Funcția de verificare a stării finale
def is_final(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] != i*3 + j + 1 and state[i][j] != 0:
                return False
    return True

# Funcțiile de tranziție
def move(state, empty_cell, direction, history):
    x, y = empty_cell
    if direction == 'up':
        x -= 1
    elif direction == 'down':
        x += 1
    elif direction == 'left':
        y -= 1
    elif direction == 'right':
        y += 1
    if 0 <= x < 3 and 0 <= y < 3:
        if (x, y) not in history:
            state[empty_cell[0]][empty_cell[1]], state[x][y] = state[x][y], state[empty_cell[0]][empty_cell[1]]
            return state, (x, y), history + [(x, y)]
    return None, None, history

# Funcția de căutare IDDFS
def iddfs(state, empty_cell, depth, history):
    if is_final(state):
        return state
    if depth == 0:
        return None
    for direction in ['up', 'down', 'left', 'right']:
        next_state, next_empty_cell, next_history = move(state, empty_cell, direction, history)
        if next_state is not None:
            result = iddfs(next_state, next_empty_cell, depth - 1, next_history)
            if result is not None:
                return result
    return None

# Testarea funcțiilor
state, empty_cell = initialize([2, 5, 3, 1, 0, 6, 4, 7, 8])
print('Starea inițială:')
print(state)
print('Celula goală inițială:')
print(empty_cell)
solution = iddfs(state, empty_cell, 10, [empty_cell])
print('Soluția:')
print(solution)
