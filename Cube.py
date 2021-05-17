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

"""
https://en.wikipedia.org/wiki/Rubik%27s_Cube

Move notation:

Many 3×3×3 Rubik's Cube enthusiasts use a notation developed by David Singmaster to denote a sequence of moves, referred
to as "Singmaster notation". Its relative nature allows algorithms to be written in such a way that they can be applied
regardless of which side is designated the top or how the colours are organised on a particular cube.

F (Front): the side currently facing the solver
B (Back): the side opposite the front
U (Up): the side above or on top of the front side
D (Down): the side opposite the top, underneath the Cube
L (Left): the side directly to the left of the front
R (Right): the side directly to the right of the front

When a prime symbol ( ′ ) follows a letter, it denotes an anticlockwise face turn; while a letter without a prime symbol
denotes a clockwise turn. These directions are as one is looking at the specified face. A letter followed by a 2
(occasionally a superscript ²) denotes two turns, or a 180-degree turn. R is right side clockwise, but R′ is right side
anticlockwise.
"""


"""
EXAMPLE OF USE:

my_cube = CubeObj(3, True)

print(f'before:\n\n { str(my_cube) } \n\n')

# do some moves ...
my_cube.translate("U F F' B D R2")

print(f'afterwards:\n\n { str(my_cube) } \n\n')
"""

import numpy as np

POSSIBLE_MOVES = [
    'F', 'B', 'U', 'D', 'L', 'R',
    'F2', 'B2', 'U2', 'D2', 'L2', 'R2',
    "F’", "B’", "U’", "D’", "L’", "R’"
]

COLOR_BOARD = [
    # TOP SIDE
    [['w', 'w', 'w'],
     ['w', 'w', 'w'],
     ['w', 'w', 'w']],
    # LEFT SIDE
    [['r', 'r', 'r'],
     ['r', 'r', 'r'],
     ['r', 'r', 'r']],
    # FRONT SIDE
    [['b', 'b', 'b'],
     ['b', 'b', 'b'],
     ['b', 'b', 'b']],
    # RIGHT SIDE
    [['o', 'o', 'o'],
     ['o', 'o', 'o'],
     ['o', 'o', 'o']],
    # BACK SIDE
    [['g', 'g', 'g'],
     ['g', 'g', 'g'],
     ['g', 'g', 'g']],
    # BOTTOM SIDE
    [['y', 'y', 'y'],
     ['y', 'y', 'y'],
     ['y', 'y', 'y']]
]

# TODO CHECK FI THE BACK SIDE IS CORRECT
#  MAYBE IT SHOULD BE COUNTERCLOCKWISE ?? => [['R', 'q', 'Q'], ...
LETTER_BOARD = [
    # TOP SIDE
    [['A', 'a', 'B'],
     ['d', '𝗪', 'b'],
     ['D', 'c', 'C']],
    # LEFT SIDE
    [['E', 'e', 'F'],
     ['h', '𝗥', 'f'],
     ['H', 'g', 'G']],
    # FRONT SIDE
    [['I', 'i', 'J'],
     ['l', '𝗕', 'j'],
     ['L', 'k', 'K']],
    # RIGHT SIDE
    [['M', 'm', 'N'],
     ['p', '𝗢', 'n'],
     ['P', 'o', 'O']],
    # BACK SIDE
    [['Q', 'q', 'R'],
     ['t', '𝗚', 'r'],
     ['T', 's', 'S']],
    # BOTTOM SIDE
    [['U', 'u', 'V'],
     ['x', '𝗬', 'v'],
     ['X', 'w', 'W']]
]

# translate cube notation in function name
TRANSLATION_DICTIONARY = {
    'F': 'F',
    'B': 'B',
    'U': 'U',
    'D': 'D',
    'L': 'L',
    'R': 'R',
    'F2': 'II_F',
    'B2': 'II_B',
    'U2': 'II_U',
    'D2': 'II_D',
    'L2': 'II_L',
    'R2': 'II_R',
    "F’": 'anti_F',
    "B’": 'anti_B',
    "U’": 'anti_U',
    "D’": 'anti_D',
    "L’": 'anti_L',
    "R’": 'anti_R'
}


class CubeObj:
    NxNxN: int
    colour: bool

    def __init__(self, NxNxN=3, colour=True) -> None:
        self._height = self._width = self._depth = NxNxN
        self._board = COLOR_BOARD if colour else LETTER_BOARD

    def __str__(self) -> str:
        return str(np.array(self._board))

    def __len__(self) -> int:
        return len(self._board)

    @property
    def board(self) -> list:
        return self._board

    @board.setter
    def board(self, input_board: list) -> None:
        if not isinstance(input_board, list): raise ValueError('Board has to be a list.')
        if len(input_board) != 6: raise ValueError('Len fo Board has to be 6.')

        for item in input_board:
            if len(item) != 3:
                raise ValueError('The length of the Items in board must be 3.')

        self._board = input_board

    # !!! THIS IS NOT A @staticmethod  OR FUNCTION IT IS A METHOD !!!!
    def translate(self, txt: str) -> None:
        """
        translate cube notation into function names, and call them
        """
        new_txt = txt.upper().replace("'", "’").replace('(', '').replace('(', '')  # (r') -> R’

        for instruction in new_txt.split():
            exec(f"self.{TRANSLATION_DICTIONARY[instruction]}()")

    def F(self) -> None:
        """
        Rotation of the front side by 90 ° clockwise. (blue side)
        """
        # get the current state of the cube
        white_row = self._board[0][self._depth - 1]
        orange_row = [item[0] for item in self._board[3]]
        yellow_row = self._board[5][0]
        red_row = [item[self._depth - 1] for item in self._board[1]]

        # update the cube by rotating the blue face clockwise by 90°
        self._board[0][2] = red_row[::-1]
        for index in range(len(white_row)): self._board[3][index][0] = white_row[index]
        self._board[5][0] = orange_row[::-1]
        for index in range(len(yellow_row)): self._board[1][index][self._depth - 1] = yellow_row[index]
        self._board[2] = np.rot90(np.array(self._board[2]), 3).tolist()

    def B(self) -> None:
        """
        Rotation of the back side by 90 ° clockwise. (green side)
        """
        # get the current state of the cube
        white_row = self._board[0][0][::-1]
        orange_row = [item[self._depth - 1] for item in self._board[3]]
        yellow_row = self._board[5][self._depth - 1][::-1]
        red_row = [item[0] for item in self._board[1]]

        # update the cube by rotating the green face clockwise by 90°
        self._board[0][0] = orange_row
        for index in range(len(yellow_row)): self._board[3][index][self._depth - 1] = yellow_row[index]
        self._board[5][self._depth - 1] = red_row
        for index in range(len(white_row)): self._board[1][index][0] = white_row[index]
        self._board[4] = np.rot90(np.array(self._board[4]), 1).tolist()

    def R(self) -> None:
        """
        Rotation of the right side by 90 ° clockwise. (orange side)
        """
        # get the current state of the cube
        white_row = [item[self._width - 1] for item in self._board[0]][::-1]
        green_row = [item[self._width - 1] for item in self._board[4]][::-1]
        yellow_row = [item[self._width - 1] for item in self._board[5]]
        blue_row = [item[self._width - 1] for item in self._board[2]]

        # update the cube by rotating the orange face clockwise by 90°
        for index in range(len(blue_row)): self._board[0][index][self._width - 1] = blue_row[index]
        for index in range(len(white_row)): self._board[4][index][self._width - 1] = white_row[index]
        for index in range(len(green_row)): self._board[5][index][self._width - 1] = green_row[index]
        for index in range(len(yellow_row)): self._board[2][index][self._width - 1] = yellow_row[index]
        self._board[3] = np.rot90(np.array(self._board[3]), 3).tolist()

    def L(self) -> None:
        """
        Rotating the left side by 90° clockwise. (red side)
        """
        # get the current state of the cube
        white_row = [item[0] for item in self._board[0]]
        blue_row = [item[0] for item in self._board[2]]
        yellow_row = [item[0] for item in self._board[5]][::-1]
        green_row = [item[0] for item in self._board[4]][::-1]

        # update the cube by rotating the red face clockwise by 90°
        for index in range(len(green_row)): self._board[0][index][0] = green_row[index]
        for index in range(len(white_row)): self._board[2][index][0] = white_row[index]
        for index in range(len(blue_row)): self._board[5][index][0] = blue_row[index]
        for index in range(len(yellow_row)): self._board[4][index][0] = yellow_row[index]
        self._board[1] = np.rot90(np.array(self._board[1]), 3).tolist()

    def U(self) -> None:
        """
        Rotating the top side by 90° clockwise. (white side)
        """
        # get the current state of the cube
        blue_row = self._board[2][0]
        red_row = self._board[1][0]
        green_row = self._board[4][0]
        orange_row = self._board[3][0]

        # update the cube by rotating the white face clockwise by 90°
        self._board[2][0] = orange_row
        self._board[1][0] = blue_row
        self._board[4][0] = red_row[::-1]
        self._board[3][0] = green_row[::-1]
        self._board[0] = np.rot90(np.array(self._board[0]), 3).tolist()

    def D(self) -> None:
        """
        Rotating the down side by 90° clockwise. (yellow side)
        """
        # get the current state of the cube
        blue_row = self._board[2][self._height - 1]
        red_row = self._board[1][self._height - 1]
        green_row = self._board[4][self._height - 1]
        orange_row = self._board[3][self._height - 1]

        # update the cube by rotating the yellow face clockwise by 90°
        self._board[2][self._height - 1] = red_row
        self._board[3][self._height - 1] = blue_row
        self._board[4][self._height - 1] = orange_row[::-1]
        self._board[1][self._height - 1] = green_row[::-1]
        self._board[5] = np.rot90(np.array(self._board[5]), 3).tolist()

    def II_F(self) -> None: [self.F() for _ in range(2)]
    def II_B(self) -> None: [self.B() for _ in range(2)]
    def II_R(self) -> None: [self.R() for _ in range(2)]
    def II_L(self) -> None: [self.L() for _ in range(2)]
    def II_U(self) -> None: [self.U() for _ in range(2)]
    def II_D(self) -> None: [self.D() for _ in range(2)]

    def anti_F(self) -> None: [self.F() for _ in range(3)]
    def anti_B(self) -> None: [self.B() for _ in range(3)]
    def anti_R(self) -> None: [self.R() for _ in range(3)]
    def anti_L(self) -> None: [self.L() for _ in range(3)]
    def anti_U(self) -> None: [self.U() for _ in range(3)]
    def anti_D(self) -> None: [self.D() for _ in range(3)]
