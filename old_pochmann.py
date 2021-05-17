#!/usr/bin/env python3

__author__ = 'Felix D'
__title__ = 'Rubik’s Cube Solver (old pochmann)'
__date__ = '09/03/2021'

"""
Rubik's Cube Solver
Copyright (C) 2021  Felix Drees

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

How to contact me by electronic and/or paper mail:
  https://github.com/felix-drees
"""


from Cube import CubeObj as Cube, POSSIBLE_MOVES
from typing import Union
from time import time
import random as rm


"""
PERMS USED:
I.   | Y-Perm   / Ecken-Algorithmus     |  => (F) R U' R' U' R U R' F' R U R' U' R' F R (F')
II.  | R-Perm   / Parity                |  => R U' R' U' R U R D R' U' R D' R' U2 R' U'
III. | T-Perm   / Kanten-Algorithmus 1  |  => R U R' U' R' F R2 U' R' U' R U R' F'
IV.  | J-Perm a / Kanten-Algorithmus 2  |  => R U R' F' R U R' U' R' F R2 U' R' U'
V.   | J-Perm b / Kanten-Algorithmus 3  |  => U' R' U L' U2 R U' R' U2 L R
"""

# PERMS
Y_PERM = "F R U' R' U' R U R' F' R U R' U' R' F R F'"
R_PERM = "R U' R' U' R U R D R' U' R D' R' U2 R' U'"  # Parity Fixing algorithm
T_PERM = "R U R' U' R' F R2 U' R' U' R U R' F'"
J_PERM_DOWN = "R U R' F' R U R' U' R' F R2 U' R' U'"
J_PERM_UP = "U' R' U L' U2 R U' R' U2 L R"


NAME_OF_BUFFER_PIC_CENTER = {
    ('w', 'g'): 'a',
    ('w', 'o'): 'b',
    ('w', 'b'): 'c',
    ('w', 'r'): 'd',
    ('r', 'w'): 'e',
    ('r', 'b'): 'f',
    ('r', 'y'): 'g',
    ('r', 'g'): 'h',
    ('b', 'w'): 'i',
    ('b', 'o'): 'j',
    ('b', 'y'): 'k',
    ('b', 'r'): 'l',
    ('o', 'w'): 'm',
    ('o', 'g'): 'n',
    ('o', 'y'): 'o',
    ('o', 'b'): 'p',
    ('g', 'w'): 'q',
    ('g', 'o'): 'r',
    ('g', 'y'): 's',
    ('g', 'r'): 't',
    ('y', 'b'): 'u',
    ('y', 'o'): 'v',
    ('y', 'g'): 'w',
    ('y', 'r'): 'x'
}

MOVE_FOR_SWAPPING_BUFFER_WITH_TARGET_CENTER = {
    'a': f"{J_PERM_UP}",
    # 'b': f"",
    'c': f"{J_PERM_DOWN}",
    'd': f"{T_PERM}",
    'e': f"R L F R' {J_PERM_DOWN} R F' L' R'",
    'f': f"R F R' {J_PERM_DOWN} R F' R'",
    'g': f"L' R F R' {J_PERM_DOWN} R F' R' L",
    'h': f"U B' U' {T_PERM} U B U'",
    'i': f"R2 U' R' F' R' {J_PERM_DOWN} R F R U R2",
    'j': f"U2 R U2 {T_PERM} U2 R' U2",
    'k': f"R F R' L' {T_PERM} L R F' R'",
    'l': f"L' {T_PERM} L",
    # 'm': f"",
    'n': f"U B U' {T_PERM} U B' U'",
    'o': f"D' R F R' L' {T_PERM} L R F' R' D",
    'p': f"U' F' U {T_PERM} U' F U",
    'q': f"R2 U R' F' R' {J_PERM_DOWN} R F R U' R2",
    'r': f"U2 R' U2 {T_PERM} U2 R U2",
    's': f"D L R' B' R {J_PERM_UP} R' B L' R D'",
    't': f"L {T_PERM} L'",
    'u': f"R F2 R' {J_PERM_DOWN} R F2 R'",
    'v': f"D' R F2 R' {J_PERM_DOWN} R F2 R' D",
    'w': f"R' B2 R {J_PERM_UP} R' B2 R",
    'x': f"D R F2 R' {J_PERM_DOWN} R F2 R' D'"
}

INDEX_TO_NAME_CENTER = {
    # TOP
    (0, 0, 1): 'a',
    (0, 1, 2): 'b',
    (0, 2, 1): 'c',
    (0, 1, 0): 'd',
    # LEFT
    (1, 0, 1): 'e',
    (1, 1, 2): 'f',
    (1, 2, 1): 'g',
    (1, 1, 0): 'h',
    # FRONT
    (2, 0, 1): 'i',
    (2, 1, 2): 'j',
    (2, 2, 1): 'k',
    (2, 1, 0): 'l',
    # RIGHT
    (3, 0, 1): 'm',
    (3, 1, 2): 'n',
    (3, 2, 1): 'o',
    (3, 1, 0): 'p',
    # BACK
    (4, 0, 1): 'q',
    (4, 1, 2): 'r',
    (4, 2, 1): 's',
    (4, 1, 0): 't',
    # BOTTOM
    (5, 0, 1): 'u',
    (5, 1, 2): 'v',
    (5, 2, 1): 'w',
    (5, 1, 0): 'x'
}

# read buffer from -> (top, left side, back)
NAME_OF_BUFFER_PIC_CORNER = {
    # TOP LEFT BACK
    ('w', 'r', 'g'): 'A',
    ('r', 'g', 'w'): 'E',
    ('g', 'w', 'r'): 'Q',
    # TOP RIGHT BACK
    ('w', 'g', 'o'): 'B',
    ('o', 'w', 'g'): 'N',
    ('g', 'o', 'w'): 'R',
    # TOP RIGHT FRONT
    ('w', 'o', 'b'): 'C',
    ('b', 'w', 'o'): 'J',
    ('o', 'b', 'w'): 'M',
    # TOP LEFT FRONT
    ('w', 'b', 'r'): 'D',
    ('r', 'w', 'b'): 'F',
    ('b', 'r', 'w'): 'I',
    # BOTTOM LEFT BACK
    ('r', 'y', 'g'): 'H',
    ('g', 'r', 'y'): 'T',
    ('y', 'g', 'r'): 'X',
    # BOTTOM RIGHT BACK
    ('o', 'g', 'y'): 'O',
    ('g', 'y', 'o'): 'S',
    ('y', 'o', 'g'): 'W',
    # BOTTOM RIGHT FRONT
    ('b', 'o', 'y'): 'K',
    ('o', 'y', 'b'): 'P',
    ('y', 'b', 'o'): 'V',
    # BOTTOM LEFT FRONT
    ('r', 'b', 'y'): 'G',
    ('b', 'y', 'r'): 'L',
    ('y', 'r', 'b'): 'U'
}

MOVE_FOR_SWAPPING_BUFFER_WITH_TARGET_CORNER = {
    # 'A': f"",
    'B': f"U {J_PERM_UP} U'",
    'C': f"{Y_PERM}",
    'D': f"U2 {J_PERM_DOWN} U2",
    # 'E': f"",
    'F': f"F {Y_PERM} F'",
    'G': f"D R {Y_PERM} R' D'",
    'H': f"D2 F' {Y_PERM} F D2",
    'I': f"F R U {J_PERM_UP} U' R' F'",
    'J': f"R U {J_PERM_UP} U' R'",
    'K': f"R {Y_PERM} R'",
    'L': f"D F' {Y_PERM} F D'",
    'M': f"F' U2 {J_PERM_DOWN} U2 F",
    'N': f"R' F' U2 {J_PERM_DOWN} U2 F R",
    'O': f"D' R {Y_PERM} R' D",
    'P': f"F' {Y_PERM} F",
    # 'Q': f"",
    'R': f"R' {Y_PERM} R",
    'S': f"D' F' {Y_PERM} F D",
    'T': f"D2 R {Y_PERM} R' D2",
    'U': f"F2 {Y_PERM} F2",
    'V': f"D' F2 {Y_PERM} F2 D",
    'W': f"R2 {Y_PERM} R2",
    'X': f"D' F2 {Y_PERM} F2 D"
}


def timer(func):
    def inner(*args, **kwargs):
        s_time = time()
        rv = func(*args, **kwargs)
        t_time = time() - s_time
        print(f'Total Time in s: {t_time}.')
        return rv
    return inner


def create_random_scrambled_cube() -> Cube:
    """
    Create a random Rubik’s Cube
    :return: the cube as an object
    """
    my_cube = Cube(3, True)
    random_moves = " ".join(rm.choices(POSSIBLE_MOVES, k=rm.randint(5, 15)))
    print(f'\nrandom scramble perms: {random_moves}\n')
    my_cube.translate(random_moves)
    return my_cube


def create_scrambled_cube(scramble) -> Cube:
    """
    create a cube with the given scramble
    :param scramble: string in which the moves are stored
    :return: the cube as an object
    """
    if not isinstance(scramble, str):
        raise ValueError('Scramble has to be str.')

    for element in scramble.upper().replace("'", "’").replace('(', '').replace('(', '').split():
        if element not in POSSIBLE_MOVES:
            raise ValueError(f'Scramble move unknown. [UNKNOWN MOVE >>{element}<<]')

    my_cube = Cube(3, True)
    my_cube.translate(scramble)
    return my_cube


@timer
def solve_old_pochmann(my_cube: Cube) -> list:
    moves = []

    def find_not_set_center() -> Union[str, None]:
        """
        if the buffer pic is at its target location, check if all center pieces are also at its target locations
        :return: name of first not set center pic which the function found, if there is none return None
        """
        for index in range(len(my_cube)):
            color_of_face = my_cube.board[index][1][1]

            if my_cube.board[index][0][1] != color_of_face:
                if INDEX_TO_NAME_CENTER[(index, 0, 1)] != 'm':
                    return INDEX_TO_NAME_CENTER[(index, 0, 1)]

            if my_cube.board[index][1][0] != color_of_face:
                return INDEX_TO_NAME_CENTER[(index, 1, 0)]

            if my_cube.board[index][1][2] != color_of_face:
                if INDEX_TO_NAME_CENTER[(index, 1, 2)] != 'b':
                    return INDEX_TO_NAME_CENTER[(index, 1, 2)]

            if my_cube.board[index][2][1] != color_of_face:
                return INDEX_TO_NAME_CENTER[(index, 2, 1)]
        return None

    def move_center_buffer_to_target_location() -> None:
        buffer_letter = NAME_OF_BUFFER_PIC_CENTER[(my_cube.board[0][1][2], my_cube.board[3][0][1])]

        if buffer_letter in 'bm':
            new_buffer = find_not_set_center()
            if new_buffer is not None:
                buffer_letter = new_buffer
            else:
                return
        moves.append(buffer_letter)
        move = MOVE_FOR_SWAPPING_BUFFER_WITH_TARGET_CENTER[buffer_letter]
        my_cube.translate(move)

        move_center_buffer_to_target_location()

    def find_not_set_corners() -> Union[str, None]:
        # TOP
        if my_cube.board[0][0][2] != 'w': return 'B'
        if my_cube.board[0][2][2] != 'w': return 'C'
        if my_cube.board[0][2][0] != 'w': return 'D'
        # LEFT
        if my_cube.board[1][0][2] != 'r': return 'F'
        if my_cube.board[1][2][2] != 'r': return 'G'
        if my_cube.board[1][2][0] != 'r': return 'H'
        # FRONT
        if my_cube.board[2][0][0] != 'b': return 'I'
        if my_cube.board[2][0][2] != 'b': return 'J'
        if my_cube.board[2][2][0] != 'b': return 'K'
        if my_cube.board[2][2][2] != 'b': return 'L'
        # RIGHT
        if my_cube.board[3][0][0] != 'o': return 'M'
        if my_cube.board[3][0][2] != 'o': return 'N'
        if my_cube.board[3][2][0] != 'o': return 'O'
        if my_cube.board[3][2][2] != 'o': return 'P'
        # BACK
        if my_cube.board[4][0][2] != 'g': return 'R'
        if my_cube.board[4][2][2] != 'g': return 'S'
        if my_cube.board[4][2][0] != 'g': return 'T'
        # BOTTOM
        if my_cube.board[5][0][0] != 'y': return 'U'
        if my_cube.board[5][0][2] != 'y': return 'V'
        if my_cube.board[5][2][2] != 'y': return 'W'
        if my_cube.board[5][2][0] != 'y': return 'X'

        return None

    def move_corner_buffer_to_target_location() -> None:
        buffer = NAME_OF_BUFFER_PIC_CORNER[(my_cube.board[0][0][0], my_cube.board[1][0][0], my_cube.board[4][0][0])]
        if buffer in 'AEQ':
            new_buffer = find_not_set_corners()
            if new_buffer is not None:
                buffer = new_buffer
            else:
                return

        moves.append(buffer)
        move = MOVE_FOR_SWAPPING_BUFFER_WITH_TARGET_CORNER[buffer]
        my_cube.translate(move)

        move_corner_buffer_to_target_location()

    move_center_buffer_to_target_location()

    if len(moves) % 2 != 0:
        my_cube.translate(R_PERM)
        moves.append('Parity')

    move_corner_buffer_to_target_location()

    return moves


def solution_schedule() -> None:
    user_input = input('Do you wont to create a cube with a RANDOM SCRAMBLE or use your OWN SCRAMBLE? [r/o]').lower()
    if user_input not in 'ro': raise ValueError('INVALID INPUT')

    if user_input == 'r': my_cool_cube = create_random_scrambled_cube()

    else:
        scramble = input('Enter your scramble: ').upper().replace("'", "’").replace('(', '').replace('(', '')
        for char in scramble:
            if char not in POSSIBLE_MOVES:
                raise ValueError('Неизвестная манипуляция.')  # f'Scramble move unknown. [UNKNOWN MOVE >>{element}<<]'
        my_cool_cube = create_scrambled_cube(scramble)

    print(f'\nScrambled Cube:\n\n{str(my_cool_cube)}\n')
    print(f'Solution:{solve_old_pochmann(my_cool_cube)}\n')
    print(f'\nSolved Cube:\n\n{str(my_cool_cube)}\n')


if __name__ == '__main__':
    solution_schedule()
