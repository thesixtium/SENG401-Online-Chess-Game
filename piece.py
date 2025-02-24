import pygame
import os
import constants

b_bishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
b_king = pygame.image.load(os.path.join("img", "black_king.png"))
b_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
b_rook = pygame.image.load(os.path.join("img", "black_rook.png"))

w_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
w_king = pygame.image.load(os.path.join("img", "white_king.png"))
w_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img", "white_queen.png"))
w_rook = pygame.image.load(os.path.join("img", "white_rook.png"))

b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

B = []
W = []

for img in b:
    B.append(pygame.transform.scale(img, (55, 55)))

for img in w:
    W.append(pygame.transform.scale(img, (55, 55)))


def draw_math(x1, x2, y):
    draw_x = (4 - x1) + round(constants.rect[0] + (x2 * constants.rect[2] / constants.board_size))
    draw_y = 3 + round(constants.rect[1] + (y * constants.rect[3] / constants.board_size))
    return draw_x, draw_y


class Piece:
    img = -1
    rect = constants.rect
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False

    def isSelected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def draw(self, win, color):
        if self.color == "w":
            drawThis = W[self.img]
        else:
            drawThis = B[self.img]

        x, y = draw_math(self.col, self.col, self.row)

        if self.selected and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)

        win.blit(drawThis, (x, y))

    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def __str__(self):
        return str(self.col) + " " + str(self.row)

    def check_diagonals(self, i, j, board, moves):
        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break

            djL += 1

        for di in range(i - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        # TOP LEFT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break
            djL += 1
        for di in range(i + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break

            djR -= 1

    def check_laterals(self, i, j, board, moves):
        # UP
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # DOWN
        for x in range(i + 1, 8, 1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # LEFT
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break

        # RIGHT
        for x in range(j + 1, 8, 1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break

    def check_specific_square(self, i, j, i_offset, j_offset, board, moves):
        p = board[i + i_offset][j + j_offset]
        if p == 0:
            moves.append((j + j_offset, i + i_offset,))
        elif p.color != self.color:
            moves.append((j + j_offset, i + i_offset,))

class Bishop(Piece):
    img = 0

    def valid_moves(self, board):
        moves = []

        self.check_diagonals(self.row, self.col, board, moves)

        return moves


class King(Piece):
    img = 1

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        if i > 0:
            # TOP LEFT
            if j > 0:
                self.check_specific_square(i, j, -1, -1, board, moves)

            # TOP MIDDLE
            self.check_specific_square(i, j, -1, 0, board, moves)

            # TOP RIGHT
            if j < 7:
                self.check_specific_square(i, j, -1, 1, board, moves)

        if i < 7:
            # BOTTOM LEFT
            if j > 0:
                self.check_specific_square(i, j, -1, 1, board, moves)

            # BOTTOM MIDDLE
            self.check_specific_square(i, j, 1, 0, board, moves)

            # BOTTOM RIGHT
            if j < 7:
                self.check_specific_square(i, j, 1, 1, board, moves)

        # MIDDLE LEFT
        if j > 0:
            self.check_specific_square(i, j, 0, -1, board, moves)

        # MIDDLE RIGHT
        if j < 7:
            self.check_specific_square(i, j, 0, 1, board, moves)

        return moves


class Knight(Piece):
    img = 2

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        # DOWN LEFT
        if i < 6 and j > 0:
            self.check_specific_square(i, j, 2, -1, board, moves)

        # UP LEFT
        if i > 1 and j > 0:
            self.check_specific_square(i, j, -2, -1, board, moves)

        # DOWN RIGHT
        if i < 6 and j < 7:
            self.check_specific_square(i, j, 2, 1, board, moves)

        # UP RIGHT
        if i > 1 and j < 7:
            self.check_specific_square(i, j, -2, 1, board, moves)

        if i > 0 and j > 1:
            self.check_specific_square(i, j, -1, -2, board, moves)

        if i > 0 and j < 6:
            self.check_specific_square(i, j, -1, 2, board, moves)

        if i < 7 and j > 1:
            self.check_specific_square(i, j, 1, -2, board, moves)

        if i < 7 and j < 6:
            self.check_specific_square(i, j, 1, 2, board, moves)

        return moves


class Pawn(Piece):
    img = 3

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first = True
        self.queen = False
        self.pawn = True

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []
        try:
            if self.color == "b":
                if i < 7:
                    p = board[i + 1][j]
                    if p == 0:
                        moves.append((j, i + 1))

                    # DIAGONAL
                    if j < 7:
                        p = board[i + 1][j + 1]
                        if p != 0:
                            if p.color != self.color:
                                moves.append((j + 1, i + 1))

                    if j > 0:
                        p = board[i + 1][j - 1]
                        if p != 0:
                            if p.color != self.color:
                                moves.append((j - 1, i + 1))

                if self.first:
                    if i < 6:
                        p = board[i + 2][j]
                        if p == 0:
                            if board[i + 1][j] == 0:
                                moves.append((j, i + 2))
                        elif p.color != self.color:
                            moves.append((j, i + 2))
            # WHITE
            else:

                if i > 0:
                    p = board[i - 1][j]
                    if p == 0:
                        moves.append((j, i - 1))

                if j < 7:
                    p = board[i - 1][j + 1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((j + 1, i - 1))

                if j > 0:
                    p = board[i - 1][j - 1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((j - 1, i - 1))

                if self.first:
                    if i > 1:
                        p = board[i - 2][j]
                        if p == 0:
                            if board[i - 1][j] == 0:
                                moves.append((j, i - 2))
                        elif p.color != self.color:
                            moves.append((j, i - 2))
        except:
            pass

        return moves


class Queen(Piece):
    img = 4

    def valid_moves(self, board):
        moves = []
        self.check_diagonals(self.row, self.col, board, moves)
        self.check_laterals(self.row, self.col, board, moves)

        return moves


class Rook(Piece):
    img = 5

    def valid_moves(self, board):
        moves = []

        self.check_laterals(self.row, self.col, board, moves)

        return moves

