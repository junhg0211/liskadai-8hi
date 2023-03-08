from math import log2, inf
from random import choice
from pickle import dump, load
from pprint import pprint
from os.path import isfile

qtable = None

board = [[0 for _ in range(10)] for _ in range(10)]
nemas = 0

ACENTEM_TABLE = {
    (4, 4): 1,
    (4, 5): 2,
    (5, 4): 3,
    (5, 5): 4
}


def get_status_code(x, y):
    acentem = ACENTEM_TABLE.get((x, y), 0)

    top_wall = y == 0
    bottom_wall = y == 9
    left_wall = x == 0
    right_wall = x == 9
    wall = 0
    if top_wall:
        if left_wall:
            wall = 1
        elif right_wall:
            wall = 3
        else:
            wall = 2
    elif bottom_wall:
        if left_wall:
            wall = 6
        elif right_wall:
            wall = 8
        else:
            wall = 7
    else:
        if left_wall:
            wall = 4
        elif right_wall:
            wall = 5

    now = board[y][x]

    if (x + y) % 2 == 0:
        x, y = y, x

    neighbor = 0
    if y != 0:
        if x != 0:
            neighbor += board[y-1][x-1] * 3**0
        if x != 9:
            neighbor += board[y-1][x+1] * 3**2
        neighbor += board[y-1][x] * 3**1
    if y != 9:
        if x != 0:
            neighbor += board[y+1][x-1] * 3**5
        if x != 9:
            neighbor += board[y+1][x+1] * 3**7
        neighbor += board[y+1][x] * 3**6
    if x != 0:
        neighbor += board[y][x-1] * 3**3
    if x != 9:
        neighbor += board[y][x+1] * 3**4

    return (acentem, neighbor, wall, int(log2(nemas + 1)), now)


FILENAME = 'qtable.pickle'

learning_rate = 0.5


def main():
    global qtable

    if isfile(FILENAME):
        with open(FILENAME, 'rb') as file:
            qtable = load(file)
    else:
        qtable = dict()

    while True:
        print(qtable)

        pprint(board)

        maxs = list()
        max_value = -inf
        for y in range(10):
            for x in range(10):
                position_code = get_status_code(x, y)
                expect = qtable.get(position_code, 0.0)

                if expect > max_value:
                    max_value = expect
                    maxs.clear()
                    maxs.append((x, y))
                elif expect == max_value:
                    maxs.append((x, y))

        print(maxs)

        chosen = choice(maxs)

        position_code = get_status_code(*chosen)

        print('AI\'s choice:', chosen, position_code, max_value)

        if board[chosen[1]][chosen[0]] == 0:
            fitness = eval(input('fitness: '))
        else:
            fitness = -inf

        board[chosen[1]][chosen[0]] = 1

        qtable[position_code] = fitness * learning_rate + max_value * (1-learning_rate)

        with open(FILENAME, 'wb') as file:
            dump(qtable, file)

        if fitness == -inf:
            return

        pprint(board)
        x, y = map(int, input('your nema position (x y): ').split())
        board[y][x] = 2


if __name__ == '__main__':
    main()
