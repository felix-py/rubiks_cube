#!/usr/bin/env python3

__author__ = 'Felix D'
__title__ = 'Rubik’s Cube Solver'
__date__ = '09/03/2021'

from Cube import CubeObj as Cube
from time import time
import random as rm


def timer(func):
    def inner(*args, **kwargs):
        s_time = time()
        rv = func(*args, **kwargs)
        t_time = time() - s_time
        print(f'Total Time: {t_time}.')
        return rv
    return inner


@timer
def create_cube() -> object:
    """
    Create a random Rubik’s Cube
    """
    list_of_possible_moves = [
        'F', 'B', 'U', 'D', 'L', 'R',
        'F2', 'B2', 'U2', 'D2', 'L2', 'R2',
        "F’", "B’", "U’", "D’", "L’", "R’"
    ]
    # create object
    cube_ = Cube(3, True)
    # create random move string
    random_moves = " ".join(rm.choices(list_of_possible_moves, k=rm.randint(1, 15)))
    # apply the moves
    cube_.translate(random_moves)
    return cube_


@timer
def solve(cube_: object) -> None:
    """
    Solve the Rubik’s Cube
    """
    pass


if __name__ == '__main__':
    cube = create_cube()
    print(f'Mixed Cube:\n\n{str(cube)}')
    solve(cube)
