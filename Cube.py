import numpy as np

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

"""
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

    def II_F(self) -> None:
        [self.F() for _ in range(2)]

    def II_B(self) -> None:
        [self.B() for _ in range(2)]

    def II_R(self) -> None:
        [self.R() for _ in range(2)]

    def II_L(self) -> None:
        [self.L() for _ in range(2)]

    def II_U(self) -> None:
        [self.U() for _ in range(2)]

    def II_D(self) -> None:
        [self.D() for _ in range(2)]

    def anti_F(self) -> None:
        [self.F() for _ in range(3)]

    def anti_B(self) -> None:
        [self.B() for _ in range(3)]

    def anti_R(self) -> None:
        [self.R() for _ in range(3)]

    def anti_L(self) -> None:
        [self.L() for _ in range(3)]

    def anti_U(self) -> None:
        [self.U() for _ in range(3)]

    def anti_D(self) -> None:
        [self.D() for _ in range(3)]

    # ATTENTION (THIS IS NOT A @staticmethod  or function !!!!)
    def translate(self, txt: str) -> None:
        """
        ATTENTION THIS IS NOT A @staticmethod, IF YOU MAKE IT ONE IT WILL NO LONGER WORK !!!!
        IT USES THE SELF IN A EXEC

        translate cube notation into function calls
        """
        new_txt = txt.replace("'", "’").replace('(', '').replace('(', '')  # (R') -> R’

        for instruction in new_txt.split():
            exec(f"self.{TRANSLATION_DICTIONARY[instruction]}()")

    def a_perm_01(self) -> None:
        """
        Lw' U R' D2 R U' R' D2 R2
        y2 (L' B L') (F2 L B' L') (F2 L2)
        R' U2 R2 U' L' U R' U' L U R' U2 R
        x R' U R' D2 R U' R' D2 R2
        y2 z F2 R U2 R' U2 F2 L' U2 L U2
        """
        self.translate("R' U2 R2 U' L' U R' U' L U R' U2 R")

    # todo
    def a_perm_02(self) -> None:
        """
        Rw U' L D2 L' U L D2 L2, oder
        y x R2 D2 R U R' D2 R U' R, oder
        y R' U2 R U' L' U R U' L U R2 U2 R, oder
        y' z U2 L' U2 L F2 U2 R U2 R' F2, oder
        y2 z' F2 L' U2 L U2 F2 R U2 R' U2
        """
        self.translate("")

    # todo
    def e_perm(self) -> None:
        """
        x' R U' R' D R U R' D' R U R' D R U' R' D', oder
        x' R U' R' D R U R' Uw2 R' U R D R' U' R, oder
        x' R U' R' D R U R' D2 L' U L D L' U' L, oder
        z' R' F R2 U R' B' R U' R2 F' R z R B R', oder
        y x U R' U' L U R U' r2' U' R U L U' R' U, oder
        (r' R' U') (L D' L' U L) (R U' R' D R) U
        """
        self.translate("")

    # todo
    def z_perm(self) -> None:
        """
        M2 U M2 U M' U2 M2 U2 M' U2, oder
        y M2 U' M2 U' M' U2 M2 U2 M' U2, oder
        R2 U' R2 U R2 x' U2 R2 F U2 F' R2 U2, oder
        R' U L' E2 L U' R L' U R' E2 R U' L', oder
        U' l' U R U' D' R U D' R U' R' D2, oder
        y F2 M2 F2 M2 U M2 U M2 U2
        """
        self.translate("")

    def h_perm(self) -> None:
        """
        M2 U M2 U2 M2 U M2, oder
        M2 U' M2 U2 M2 U' M2, oder
        R2' r2 U' L2 l2' U2 R2' r2 U' L2 l2', oder
        F2 M2 F2 U' F2 M2 F2 U, oder
        x U2 M2 U2 B' U2 M2 U2 B, oder
        R U2 R' U' R' U' R2 U' R2 U2 R2 U2 R' U
        """
        self.translate("R U2 R' U' R' U' R2 U' R2 U2 R2 U2 R' U")

    def u_perm_01(self) -> None:
        """
        R U' R U R U R U' R' U' R2, oder
        M2 U M U2 M' U M2, oder
        y2 M2 U M' U2 M U M2, oder
        y' R2 U' y r U2 r' R U2 R' y' U R2
        """
        self.translate("R U' R U R U R U' R' U' R2")

    def u_perm_02(self) -> None:
        """
        R2 U R U R' U' R' U' R' U R', oder
        M2 U' M U2 M' U' M2, oder
        y2 M2 U' M' U2 M U' M2, oder
        y2 R' U R' U' R' U' R' U R U R2, oder
        y2 L' U' L U R U R' U2 L' U L U R U' R'
        """
        self.translate("R2 U R U R' U' R' U' R' U R'")

    def j_perm_01(self) -> None:
        """
        J-Perm auch L-Perm genannt

        L' U' L F L' U' L U L F' L2 U L U, oder
        R U' L' U R' U2 L U' L' U2' L, oder
        y2 R' U2 R U R' z R2 U R' D R U', oder
        y2 F2 L' U' r U2 l' U R' U' R2, oder
        y R' U L' U2 R U' R' U2 L R U'
        """
        self.translate("R U' L' U R' U2 L U' L' U2' L")

    def j_perm_02(self) -> None:
        """
        R U R' F' R U R' U' R' F R2 U' R' U', oder
        R U2 R' U' R U2 L' U R' U' L, oder
        y2 R L U2 L' U' L U2 R' U L' U', oder
        y2 r2 U' L' U r' U2 R B' R' U2
        """
        self.translate("R U2 R' U' R U2 L' U R' U' L")

    def t_perm(self) -> None:
        """
        R U R' U' R' F R2 U' R' U' R U R' F', oder
        F R U' R' U R U R2 F' R U R U' R', oder
        R2 U R2' U' R2 U' D R2' U' R2 U R2' D', oder
        y' U R2' u' R2 U R2' y R2 u R2' U' R2
        """
        self.translate("F R U' R' U R U R2 F' R U R U' R'")

    def r_perm_01(self) -> None:
        """
        R' U2 R U2 R' F R U R' U' R' F' R2 U', oder
        R' U2 R U' y' R' F R B' R' F' R z x' R' U R', oder
        y2 R' U2 l R U' R' U l' U2' R F R U' R' U' R U R' F', oder
        y R2 B2 U' R' U' R U R U B2 R U' R U
        """
        self.translate("R' U2 R U2 R' F R U R' U' R' F' R2 U'")

    def r_perm_02(self) -> None:
        """
        L U2 L' U2 L F' L' U' L U L F L2 U, oder
        z U R2 U' R2 U F' U' R' U R U F U2 R, oder
        y2 R U2 R' U2 R B' R' U' R U R B R2' U, oder
        y R U R' F' R U2 R' U2 R' F R U R U2 R' U', oder
        y2 R U2 R' U' (R' F' R) U2 R U2 R' F R U' R' U
        """
        self.translate("L U2 L' U2 L F' L' U' L U L F L2 U")

    # todo
    def f_perm(self) -> None:
        """
        R U' R' U R2 y R U R' U' F' Dw R2 F R F', oder
        y' R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R, oder
        y' U R U' R' U R2 y R U R' U' x U' R' U R U2, oder
        y z R U R' U' R U2 (z'y') R U R' U' (yx) L' U' L U L2, oder
        y2 R' U R U' R2' F' U' F U R U' x' R2 U' R' U, oder
        y' R U R' U R U2 R2 U' R U' R' U2 R U r U R' U' L' U R U'
        """
        self.translate("")

    # todo
    def v_perm(self) -> None:
        """
        R' U R' Dw' R' F' R2 U' R' U R' F R F, oder
        R' U R' Dw' x Lw' U R' U' Lw R U' R' U R U, oder
        R' U R' U' y R' F' R2 U' R' U R' F R F, oder
        y2 R U' L' U R' U' R U' L U R' U2 L' U2 L, oder
        y L' U R U' L U L' U R' U' L U2 R U2 R'
        """
        self.translate("")

    def n_perm_01(self) -> None:
        """
        R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R', oder
        R U' R' U Lw U F U' R' F' R U' R U Lw' U R', oder
        L U' L' U L F U F' L' U' L F' L F L' U L', oder
        F' R U R' U' R' F R2 F U' R' U' R U F' R', oder
        L U' R U2 L' U R' L U' R U2 L' U R' U', oder
        y' L U' R U2 L' U R' L U' R U2 L' U R' U
        """
        self.translate("L U' R U2 L' U R' L U' R U2 L' U R' U'")

    def n_perm_02(self) -> None:
        """
        (R' U L' U2 R U' L) (R' U L' U2 R U' L) (U), oder
        L' U L U' Rw' U' F' U L F L' U L' U' Rw U' L, oder
        z U' R D' R2' U R' (U' D) R D' R2 U R' D R, oder
        L' U R' U2' L U' L' R U R' U2' L U' R U, oder
        R' U R U' R' F' U' F R U R' F R' F' R U' R
        """
        self.translate("R' U L' U2 R U' L R' U L' U2 R U' L U")

    def y_perm(self) -> None:
        """
        F R U' R' U' R U R' F' R U R' U' R' F R F', oder
        R2 U' R' U R U' z' y' L' U' R U' R' U' L U, oder
        F R' F' R U R U' R2 U' R U l U' R' U F, oder
        R' F R F' y' U' R' U R2 U R' U' R' F R F' U', oder
        y z U2 R U R' U' R y R U L' U L U R' U'
        """
        self.translate("F R U' R' U' R U R' F' R U R' U' R' F R F'")

    # todo
    def g_perm_01(self) -> None:
        """
        R2 Uw' R U' R U R' Uw R2 y R U' R', oder
        y F2 D' L U' L U L' D F2 R U' R', oder
        y' L' R' U2 L R (y) L U' R U2 L' U R' U2
        """
        self.translate("")

    # todo
    def g_perm_02(self) -> None:
        """
        R2 Uw R' U R' U' R Uw' R2 y' R' U R, oder
        R2' u R' U R' U' R u' R2 y' R' U R, oder
        y' R L U2 R' L' (y') R' U L' U2 R U' L U2
        """
        self.translate("")

    # todo
    def g_perm_03(self) -> None:
        """
        R' U' R y R2 Uw R' U R U' R Uw' R2, oder
        R' U' R B2 D L' U L U' L D' B2, oder
        y2 L' U' L y' R2' u R' U R U' R u' R2
        """
        self.translate("")

    def g_perm_04(self) -> None:
        """
        R U R' y' R2 Uw' R U' R' U R' Uw R2, oder
        R U R' F2 D' L U' L' U L' D F2, oder
        y (R' F' R F') (U' L' U) (F R' F' L F2 R)
        """
        self.translate("R U R' F2 D' L U' L' U L' D F2")


if __name__ == '__main__':
    x = CubeObj(3, True)
    print('before:\n\n', str(x), '\n\n')
    # x.F()
    # x.anti_F()

    # x.II_B()
    # x.II_B()

    # x.r_perm_01()
    print('afterwards:\n\n', str(x), '\n\n')
