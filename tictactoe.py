# A game of tic-tac-toe

import random

g_display = '---------\n' \
            '| {0} {1} {2} |\n' \
            '| {3} {4} {5} |\n' \
            '| {6} {7} {8} |\n' \
            '---------'

winning_pos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
               (1, 4, 7), (2, 5, 8), (0, 4, 8), (6, 4, 2)]


def count(iterable, term):
    return sum([1 for x in iterable if x == term])


def easy_turn():
    while True:
        new_cell_coord = [random.randint(1, 3), random.randint(1, 3)]
        new_cell_loc = (new_cell_coord[0] - 1) * 3 + new_cell_coord[1] - 1
        if g_state[new_cell_loc] in ['X', 'O']:
            continue
        else:
            return new_cell_loc


def game_over():
    if win_check(g_state, 'X'):
        print('X wins')
        return True
    elif win_check(g_state, 'O'):
        print('O wins')
        return True
    elif all([pos in ['X', 'O'] for pos in g_state]):
        print('Draw')
        return True
    else:
        return False


def game_play(player1, player2):
    print(g_display.format(*g_state))
    while True:
        turn = turn_check(g_state)
        if turn == "X":
            turn_type(player1, turn)
        else:
            turn_type(player2, turn)
        print(g_display.format(*g_state))
        if game_over():
            return
        else:
            continue


def game_params():
    play_types = ['user', 'easy', 'medium', 'hard']
    while True:
        user_in = input("Input command: ")
        if user_in == "exit":
            return False, "", ""
        else:
            try:
                start, player1, player2 = user_in.split()
            except ValueError:
                print("Bad parameters!")
                continue
            if start == "start" and player1 in play_types and player2 in play_types:
                return True, player1, player2
            else:
                print("Bad parameters!")
                continue


def hard_turn(game, turn):

    move = 0
    maxvalue = -2

    if all(x == " " for x in game):
        return easy_turn()

    for pos in range(9):
        if game[pos] in ['X', 'O']:
            continue
        elif minimax(game, pos, turn) > maxvalue:
            maxvalue = minimax(game, pos, turn)
            move = pos

    return move


def minimax(game, pos, turn):
    if turn == "X":
        other_turn = "O"
    else:
        other_turn = "X"

    temp_game = game.copy()
    temp_game[pos] = turn

    if win_check(temp_game, turn):
        return 1
    elif win_check(temp_game, other_turn):
        return -1
    elif all([pos in ['X', 'O'] for pos in temp_game]):
        return 0
    else:
        maxval = -2
        move = 0
        for pos in range(9):
            if temp_game[pos] in ['X', 'O']:
                continue
            else:
                if minimax(temp_game, pos, other_turn) > maxval:
                    maxval = minimax(temp_game, pos, other_turn)
                    move = pos
        return minimax(temp_game, move, other_turn) * -1


def medium_turn(game, turn):
    for pos in winning_pos:
        row = [game[cell] for cell in pos]
        if count(row, turn) == 2 and count(row, " ") == 1:
            index = row.index(" ")
            cell_index = pos[index]
            return cell_index, True  # True indicates this is a winning position
    for pos in winning_pos:
        row = [game[cell] for cell in pos]
        if count(row, turn) == 0 and count(row, " ") == 1:
            index = row.index(" ")
            cell_index = pos[index]
            return cell_index, False
    return easy_turn(), False


def turn_type(play_type, turn):
    if play_type == "user":
        user_turn(turn)
    elif play_type == "easy":
        print('Making move level "easy"')
        g_state[easy_turn()] = turn
    elif play_type == "medium":
        print('Making move level "medium"')
        g_state[medium_turn(g_state, turn)[0]] = turn
    elif play_type == "hard":
        print('Making move level "hard"')
        g_state[hard_turn(g_state, turn)] = turn


def turn_check(game):
    if count(game, 'X') <= count(game, 'O'):
        return 'X'
    else:
        return 'O'


def user_turn(turn):
    while True:
        new_cell_coord = input('Enter the coordinates: ').split()
        try:
            new_cell_coord = [int(x) for x in new_cell_coord]
        except ValueError:
            print('You should enter numbers!')
            continue
        if 1 <= new_cell_coord[0] <= 3 and 1 <= new_cell_coord[1] <= 3:
            new_cell_loc = (new_cell_coord[0] - 1) * 3 + new_cell_coord[1] - 1
            if g_state[new_cell_loc] in ['X', 'O']:
                print('This cell is occupied! Choose another one!')
                continue
            else:
                g_state[new_cell_loc] = turn
                return
        else:
            print('Coordinates should be from 1 to 3!')
            continue


def win_check(game, team):
    for comb in winning_pos:
        if all([game[pos] == team for pos in comb]):
            return True


while True:
    playing, play1, play2 = game_params()
    if playing:
        g_state = [' '] * 9
        game_play(play1, play2)
    else:
        break
