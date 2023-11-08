from itertools import combinations


def initialize_game():
    game_state = [0] * 9
    player_A_choices = []
    player_B_choices = []
    return game_state, player_A_choices, player_B_choices


def check_final_state(player_A_choices, player_B_choices):
    # Check if either player has won
    for player_choices in [player_A_choices, player_B_choices]:
        if len(player_choices) >= 3:
            for combo in combinations(player_choices, 3):
                if sum(combo) == 15:
                    return True, combo
    # Check if the game is a draw
    if len(player_A_choices) + len(player_B_choices) == 9:
        return 'Draw', ()
    return False, ()


def choose_number(player, number, game_state, player_choices):
    if 1 <= number <= 9 and game_state[number - 1] == 0:
        game_state[number - 1] = player
        player_choices.append(number)
        return True
    else:
        return False


def heuristic(game_state):
    potential_triplets = [
        (1, 5, 9),
        (1, 6, 8),
        (2, 4, 9),
        (2, 5, 8),
        (2, 6, 7),
        (3, 4, 8),
        (3, 5, 7),
        (4, 2, 9),
        (4, 3, 8),
        (5, 1, 9),
        (5, 2, 8),
        (5, 3, 7),
        (6, 1, 8),
        (6, 2, 7),
    ]
    priority_numbers = [5, 6, 4, 2, 1, 3, 7, 8, 9]
    available_numbers = [num for num in priority_numbers if game_state[num - 1] == 0]
    # Prioritize numbers that block player A from forming a winning triplet
    for triplet in potential_triplets:
        if sum(game_state[num - 1] for num in triplet) == 2 and set(triplet).intersection(set(available_numbers)):
            return list(set(triplet).intersection(set(available_numbers)))
    # Prioritize numbers that are part of the most potential triplets
    return sorted(available_numbers, key=lambda num: sum(num in triplet for triplet in potential_triplets),
                  reverse=True)


def minmax(game_state, player_B_choices):
    min_score = float('inf')
    best_move = None
    for i in heuristic(game_state):
        if game_state[i - 1] == 0:
            # Simulate player B choosing number i
            player_B_choices.append(i)
            game_state[i - 1] = 2
            max_score = -float('inf')
            for j in range(9):
                if game_state[j] == 0:
                    # Simulate player A choosing number j+1
                    game_state[j] = 1
                    for k in range(9):
                        if game_state[k] == 0:
                            # Simulate player A choosing number k+1
                            game_state[k] = 1
                            # Calculate the maximum sum of any combination of 3 numbers that player B has chosen
                            score = max(sum(combo) for combo in combinations(player_B_choices, 3)) if len(
                                player_B_choices) >= 3 else 0
                            if score > max_score:
                                max_score = score
                            # Undo player A's choice
                            game_state[k] = 0
                    # Undo player A's choice
                    game_state[j] = 0
            # Undo player B's choice
            player_B_choices.remove(i)
            game_state[i - 1] = 0
            if max_score < min_score:
                min_score = max_score
                best_move = i
    return best_move


def main():
    game_state, player_A_choices, player_B_choices = initialize_game()
    while True:
        player_A_choice = int(input("Player A, choose a number: "))
        valid_choice = choose_number(1, player_A_choice, game_state, player_A_choices)
        while not valid_choice:
            player_A_choice = int(input("Invalid choice. Player A, choose a different number: "))
            valid_choice = choose_number(1, player_A_choice, game_state, player_A_choices)
        result, winning_combo = check_final_state(player_A_choices, player_B_choices)
        if result:
            if result == 'Draw':
                print("The game is a draw.")
            else:
                print("Player A wins with the combination ", winning_combo)
            break
        player_B_choice = minmax(game_state, player_B_choices)
        choose_number(2, player_B_choice, game_state, player_B_choices)
        print(f"Player B chose {player_B_choice}")
        result, winning_combo = check_final_state(player_A_choices, player_B_choices)
        if result:
            if result == 'Draw':
                print("The game is a draw.")
            else:
                print("Player B wins with the combination ", winning_combo)
            break


if __name__ == "__main__":
    main()
