class Board:
    """Класс, реализующий шахматную или шашечную доску, а также историю ходов."""

    def __init__(self, game_type='chess'):
        """Инициализирует доску, историю ходов и историю отменённых действий.

        Args:
            game_type (str): Тип игры ('chess' для шахмат, 'checkers' для шашек).
        """
        self.game_type = game_type
        self.board = self._init_board()
        self.move_history = []
        self.redo_history = []

    def _init_board(self):
        """Создаёт начальное расположение фигур для выбранной игры."""
        if self.game_type == 'chess':
            return [
                ['r', 'w', 'a', 'q', 'k', 'a', 'w', 'r'],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['R', 'W', 'A', 'Q', 'K', 'A', 'W', 'R']
            ]
        elif self.game_type == 'checkers':
            board = [['.' for _ in range(8)] for _ in range(8)]
            for row in range(3):
                for col in range(8):
                    if (row + col) % 2 == 1:
                        board[row][col] = 'b'
            for row in range(5, 8):
                for col in range(8):
                    if (row + col) % 2 == 1:
                        board[row][col] = 'W'
            return board

    def print_board(self, highlight=None):
        """Выводит текущее состояние доски с опциональной подсветкой выбранных клеток.

        Args:
            highlight (list): Список кортежей (строка, столбец) для выделения.
        """
        if highlight is None:
            highlight = []
        print("    Black")
        print("    A B C D E F G H\n")
        for i in range(8):
            print(8 - i, end='   ')
            for j in range(8):
                cell = self.board[i][j]
                if (i, j) in highlight:
                    print(f"\033[46m{cell}\033[0m", end=' ')
                else:
                    print(cell, end=' ')
            print(' ', 8 - i)
        print("\n    A B C D E F G H")
        print("    White")
        print('-----------------------------')

    def parse_position(self, pos):
        """Преобразует позицию в шахматной нотации (например, 'e2') в координаты (строка, столбец).

        Args:
            pos (str): Позиция в нотации.

        Returns:
            tuple: Индексы строки и столбца.
        """
        col = ord(pos[0].lower()) - ord('a')
        row = 8 - int(pos[1])
        return row, col

    def make_move(self, start, end):
        """Выполняет ход, обновляя доску и историю ходов.

        Args:
            start (str): Начальная позиция (например, 'e2').
            end (str): Конечная позиция (например, 'e4').
        """
        s_row, s_col = self.parse_position(start)
        e_row, e_col = self.parse_position(end)
        moving_piece = self.board[s_row][s_col]
        captured_piece = self.board[e_row][e_col]

        if abs(s_row - e_row) == 2:
            mid_row = (s_row + e_row) // 2
            mid_col = (s_col + e_col) // 2
            captured_piece = self.board[mid_row][mid_col]
            self.board[mid_row][mid_col] = '.'

        self.move_history.append((start, end, moving_piece, captured_piece))
        self.board[e_row][e_col] = moving_piece
        self.board[s_row][s_col] = '.'
        self.redo_history.clear()

        if self.game_type == 'checkers':
            if (moving_piece == 'W' and e_row == 0) or (moving_piece == 'b' and e_row == 7):
                self.board[e_row][e_col] = 'K' if moving_piece.isupper() else 'k'

    def undo_move(self):
        """Отменяет последний совершённый ход."""
        if self.move_history:
            start, end, piece, captured = self.move_history.pop()
            s_row, s_col = self.parse_position(start)
            e_row, e_col = self.parse_position(end)

            if abs(s_row - e_row) == 2:
                mid_row = (s_row + e_row) // 2
                mid_col = (s_col + e_col) // 2
                self.board[mid_row][mid_col] = captured

            self.board[s_row][s_col] = piece
            self.board[e_row][e_col] = captured
            self.redo_history.append((start, end, piece, captured))

    def redo_move(self):
        """Повторяет последний отменённый ход."""
        if self.redo_history:
            start, end, piece, captured = self.redo_history.pop()
            s_row, s_col = self.parse_position(start)
            e_row, e_col = self.parse_position(end)

            if abs(s_row - e_row) == 2:
                mid_row = (s_row + e_row) // 2
                mid_col = (s_col + e_col) // 2
                self.board[mid_row][mid_col] = '.'

            self.board[e_row][e_col] = piece
            self.board[s_row][s_col] = '.'
            self.move_history.append((start, end, piece, captured))


class Piece:
    """Базовый класс для всех фигур."""

    def __init__(self, color, position):
        """Устанавливает цвет и позицию фигуры.

        Args:
            color (str): 'white' или 'black'.
            position (str): Позиция в нотации (например, 'e2').
        """
        self.color = color
        self.position = position

    def is_valid_move(self, board, end):
        """Проверяет корректность хода. Метод для переопределения."""
        pass

    def get_possible_moves(self, board):
        """Возвращает список допустимых ходов. Метод для переопределения."""
        pass


class Checker(Piece):
    """Обычная шашка для игры в шашки."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        direction = -1 if self.color == 'white' else 1

        if abs(s_col - e_col) == 1 and (e_row - s_row) == direction:
            return board.board[e_row][e_col] == '.'

        if abs(s_col - e_col) == 2 and (e_row - s_row) == 2 * direction:
            mid_row = (s_row + e_row) // 2
            mid_col = (s_col + e_col) // 2
            return board.board[mid_row][mid_col] != '.' and board.board[e_row][e_col] == '.'

        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        direction = -1 if self.color == 'white' else 1

        for dc in [-1, 1]:
            n_row, n_col = s_row + direction, s_col + dc
            if 0 <= n_row < 8 and 0 <= n_col < 8 and board.board[n_row][n_col] == '.':
                moves.append(f"{chr(n_col + ord('a'))}{8 - n_row}")

        for dc in [-2, 2]:
            n_row, n_col = s_row + 2 * direction, s_col + dc
            if 0 <= n_row < 8 and 0 <= n_col < 8:
                mid_row, mid_col = s_row + direction, s_col + dc // 2
                if (board.board[mid_row][mid_col] != '.' and
                        board.board[mid_row][mid_col].islower() != (self.color == 'white') and
                        board.board[n_row][n_col] == '.'):
                    moves.append(f"{chr(n_col + ord('a'))}{8 - n_row}")
        return moves


class KingChecker(Piece):
    """Дамка в шашках."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        if abs(s_row - e_row) != abs(s_col - e_col):
            return False

        step_row = 1 if e_row > s_row else -1
        step_col = 1 if e_col > s_col else -1
        r, c = s_row + step_row, s_col + step_col
        captured = 0
        while r != e_row:
            if board.board[r][c] != '.':
                if captured or board.board[r][c].islower() == (self.color == 'white'):
                    return False
                captured += 1
            r += step_row
            c += step_col
        return board.board[e_row][e_col] == '.' and captured <= 1

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = s_row + dr, s_col + dc
            captured = 0
            while 0 <= r < 8 and 0 <= c < 8:
                if board.board[r][c] != '.':
                    if captured or board.board[r][c].islower() == (self.color == 'white'):
                        break
                    captured += 1
                    r += dr
                    c += dc
                    if 0 <= r < 8 and 0 <= c < 8 and board.board[r][c] == '.':
                        moves.append(f"{chr(c + ord('a'))}{8 - r}")
                    break
                moves.append(f"{chr(c + ord('a'))}{8 - r}")
                r += dr
                c += dc
        return moves


class Pawn(Piece):
    """Пешка для шахматной игры."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        direction = -1 if self.color == 'white' else 1

        if s_col == e_col:
            if s_row + direction == e_row and board.board[e_row][e_col] == '.':
                return True
            if s_row in [1, 6] and s_row + 2 * direction == e_row and board.board[e_row][e_col] == '.' and board.board[s_row + direction][s_col] == '.':
                return True
        elif abs(s_col - e_col) == 1 and s_row + direction == e_row:
            target = board.board[e_row][e_col]
            if target != '.':
                if (self.color == 'white' and target.islower()) or (self.color == 'black' and target.isupper()):
                    return True
        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        direction = -1 if self.color == 'white' else 1

        if 0 <= s_row + direction < 8 and board.board[s_row + direction][s_col] == '.':
            moves.append(f"{chr(s_col + ord('a'))}{8 - (s_row + direction)}")
            if s_row in [1, 6] and board.board[s_row + 2 * direction][s_col] == '.':
                moves.append(f"{chr(s_col + ord('a'))}{8 - (s_row + 2 * direction)}")
        for dc in [-1, 1]:
            n_row, n_col = s_row + direction, s_col + dc
            if 0 <= n_row < 8 and 0 <= n_col < 8:
                target = board.board[n_row][n_col]
                if target != '.' and (target.islower() != (self.color == 'white')):
                    moves.append(f"{chr(n_col + ord('a'))}{8 - n_row}")
        return moves


class Knight(Piece):
    """Конь в шахматах."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        if ((abs(s_row - e_row) == 2 and abs(s_col - e_col) == 1) or
                (abs(s_row - e_row) == 1 and abs(s_col - e_col) == 2)):
            target = board.board[e_row][e_col]
            return target == '.' or (target.islower() != (self.color == 'white'))
        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        for dr in [-2, -1, 1, 2]:
            for dc in [-2, -1, 1, 2]:
                if abs(dr) != abs(dc):
                    n_row, n_col = s_row + dr, s_col + dc
                    if 0 <= n_row < 8 and 0 <= n_col < 8:
                        pos = f"{chr(n_col + ord('a'))}{8 - n_row}"
                        if self.is_valid_move(board, pos):
                            moves.append(pos)
        return moves


class Bishop(Piece):
    """Слон в шахматах."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        if abs(s_row - e_row) == abs(s_col - e_col):
            dr = 1 if e_row > s_row else -1
            dc = 1 if e_col > s_col else -1
            r, c = s_row + dr, s_col + dc
            while (r, c) != (e_row, e_col):
                if board.board[r][c] != '.':
                    return False
                r += dr
                c += dc
            target = board.board[e_row][e_col]
            return target == '.' or (target.islower() != (self.color == 'white'))
        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = s_row + dr, s_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                pos = f"{chr(c + ord('a'))}{8 - r}"
                if board.board[r][c] == '.':
                    moves.append(pos)
                else:
                    if board.board[r][c].islower() != (self.color == 'white'):
                        moves.append(pos)
                    break
                r += dr
                c += dc
        return moves


class Rook(Piece):
    """Ладья в шахматах."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        if s_row == e_row:
            for col in range(min(s_col, e_col) + 1, max(s_col, e_col)):
                if board.board[s_row][col] != '.':
                    return False
            target = board.board[e_row][e_col]
            return target == '.' or (target.islower() != (self.color == 'white'))
        elif s_col == e_col:
            for row in range(min(s_row, e_row) + 1, max(s_row, e_row)):
                if board.board[row][s_col] != '.':
                    return False
            target = board.board[e_row][e_col]
            return target == '.' or (target.islower() != (self.color == 'white'))
        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        for row in range(8):
            if row != s_row:
                pos = f"{chr(s_col + ord('a'))}{8 - row}"
                if self.is_valid_move(board, pos):
                    moves.append(pos)
        for col in range(8):
            if col != s_col:
                pos = f"{chr(col + ord('a'))}{8 - s_row}"
                if self.is_valid_move(board, pos):
                    moves.append(pos)
        return moves


class Queen(Piece):
    """Ферзь в шахматах."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        if (s_row == e_row or s_col == e_col or abs(s_row - e_row) == abs(s_col - e_col)):
            return Rook.is_valid_move(self, board, end) or Bishop.is_valid_move(self, board, end)
        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        for row in range(8):
            if row != s_row:
                pos = f"{chr(s_col + ord('a'))}{8 - row}"
                if self.is_valid_move(board, pos):
                    moves.append(pos)
        for col in range(8):
            if col != s_col:
                pos = f"{chr(col + ord('a'))}{8 - s_row}"
                if self.is_valid_move(board, pos):
                    moves.append(pos)
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = s_row + dr, s_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                pos = f"{chr(c + ord('a'))}{8 - r}"
                if self.is_valid_move(board, pos):
                    moves.append(pos)
                r += dr
                c += dc
        return moves


class King(Piece):
    """Король в шахматах."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        if abs(s_row - e_row) <= 1 and abs(s_col - e_col) <= 1:
            target = board.board[e_row][e_col]
            return target == '.' or (target.islower() != (self.color == 'white'))
        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                n_row, n_col = s_row + dr, s_col + dc
                if 0 <= n_row < 8 and 0 <= n_col < 8:
                    pos = f"{chr(n_col + ord('a'))}{8 - n_row}"
                    if self.is_valid_move(board, pos):
                        moves.append(pos)
        return moves


class Wizard(Piece):
    """Волшебник, комбинирующий ходы коня и короля."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        if ((abs(s_row - e_row) == 2 and abs(s_col - e_col) == 1) or
                (abs(s_row - e_row) == 1 and abs(s_col - e_col) == 2)):
            target = board.board[e_row][e_col]
            return target == '.' or (target.islower() != (self.color == 'white'))
        if abs(s_row - e_row) <= 1 and abs(s_col - e_col) <= 1:
            target = board.board[e_row][e_col]
            return target == '.' or (target.islower() != (self.color == 'white'))
        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        for dr in [-2, -1, 1, 2]:
            for dc in [-2, -1, 1, 2]:
                if abs(dr) != abs(dc):
                    n_row, n_col = s_row + dr, s_col + dc
                    pos = f"{chr(n_col + ord('a'))}{8 - n_row}"
                    if 0 <= n_row < 8 and 0 <= n_col < 8 and self.is_valid_move(board, pos):
                        moves.append(pos)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                n_row, n_col = s_row + dr, s_col + dc
                pos = f"{chr(n_col + ord('a'))}{8 - n_row}"
                if 0 <= n_row < 8 and 0 <= n_col < 8 and self.is_valid_move(board, pos):
                    moves.append(pos)
        return moves


class Dragon(Piece):
    """Дракон: сочетает возможности ладьи и коня."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        if s_row == e_row or s_col == e_col:
            return Rook.is_valid_move(self, board, end)
        if ((abs(s_row - e_row) == 2 and abs(s_col - e_col) == 1) or
                (abs(s_row - e_row) == 1 and abs(s_col - e_col) == 2)):
            target = board.board[e_row][e_col]
            return target == '.' or (target.islower() != (self.color == 'white'))
        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        for row in range(8):
            if row != s_row:
                pos = f"{chr(s_col + ord('a'))}{8 - row}"
                if self.is_valid_move(board, pos):
                    moves.append(pos)
        for col in range(8):
            if col != s_col:
                pos = f"{chr(col + ord('a'))}{8 - s_row}"
                if self.is_valid_move(board, pos):
                    moves.append(pos)
        for dr in [-2, -1, 1, 2]:
            for dc in [-2, -1, 1, 2]:
                if abs(dr) != abs(dc):
                    n_row, n_col = s_row + dr, s_col + dc
                    pos = f"{chr(n_col + ord('a'))}{8 - n_row}"
                    if 0 <= n_row < 8 and 0 <= n_col < 8 and self.is_valid_move(board, pos):
                        moves.append(pos)
        return moves


class Archer(Piece):
    """Стрелок, способный двигаться как слон или совершать 'выстрел' на две клетки по диагонали."""

    def is_valid_move(self, board, end):
        s_row, s_col = board.parse_position(self.position)
        e_row, e_col = board.parse_position(end)
        if abs(s_row - e_row) == abs(s_col - e_col):
            return Bishop.is_valid_move(self, board, end)
        if abs(s_row - e_row) == 2 and abs(s_col - e_col) == 2:
            target = board.board[e_row][e_col]
            return target != '.' and (target.islower() != (self.color == 'white'))
        return False

    def get_possible_moves(self, board):
        moves = []
        s_row, s_col = board.parse_position(self.position)
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = s_row + dr, s_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                pos = f"{chr(c + ord('a'))}{8 - r}"
                if self.is_valid_move(board, pos):
                    moves.append(pos)
                r += dr
                c += dc
        for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            r, c = s_row + dr, s_col + dc
            pos = f"{chr(c + ord('a'))}{8 - r}"
            if 0 <= r < 8 and 0 <= c < 8 and self.is_valid_move(board, pos):
                moves.append(pos)
        return moves


class Game:
    """Класс, управляющий процессом шахматной игры."""

    def __init__(self):
        self.board = Board()
        self.turn = 'white'
        self.move_count = 0

    def play(self):
        """Основной цикл игры."""
        while True:
            self.board.print_board()
            print(f"Ход {'белых' if self.turn == 'white' else 'черных'}. Введите ход (например, e2 e4) или команду (back, next, hint, threats, save, load, exit):")
            user_input = input().strip().lower()

            if user_input == 'exit':
                break
            elif user_input == 'back':
                self.board.undo_move()
                self.move_count -= 1
                self.turn = 'black' if self.turn == 'white' else 'white'
            elif user_input == 'next':
                self.board.redo_move()
                self.move_count += 1
                self.turn = 'black' if self.turn == 'white' else 'white'
            elif user_input.startswith('hint'):
                pos = user_input.split()[1]
                self.hint(pos)
            elif user_input.startswith('threats'):
                pos = user_input.split()[1]
                self.threats(pos)
            elif user_input.startswith('save'):
                filename = user_input.split()[1]
                self.save_game(filename)
            elif user_input.startswith('load'):
                filename = user_input.split()[1]
                self.load_game(filename)
            else:
                try:
                    start, end = user_input.split()
                    if self.is_valid_move(start, end):
                        self.board.make_move(start, end)
                        self.move_count += 1
                        self.turn = 'black' if self.turn == 'white' else 'white'
                    else:
                        print("Неверный ход. Повторите попытку.")
                except ValueError:
                    print("Неверный формат ввода. Повторите попытку.")

    def is_valid_move(self, start, end):
        """Проверяет корректность хода на основе типа фигуры.

        Args:
            start (str): Начальная позиция.
            end (str): Конечная позиция.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        s_row, s_col = self.board.parse_position(start)
        piece = self.board.board[s_row][s_col]

        if piece == '.':
            return False

        if piece.lower() == 'p':
            return Pawn('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'h':
            return Knight('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'r':
            return Rook('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'b':
            return Bishop('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'q':
            return Queen('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'k':
            return King('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'w':
            return Wizard('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'd':
            return Dragon('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'a':
            return Archer('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        return False

    def hint(self, pos):
        """Выводит все возможные ходы для фигуры на указанной позиции.

        Args:
            pos (str): Позиция фигуры (например, 'e2').
        """
        row, col = self.board.parse_position(pos)
        piece = self.board.board[row][col]

        if piece == '.':
            print("На этой клетке нет фигуры.")
            return

        if (self.turn == 'white' and piece.islower()) or (self.turn == 'black' and piece.isupper()):
            print("Нельзя получить подсказку для фигуры противника.")
            return

        moves = []
        if piece.lower() == 'p':
            moves = Pawn('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'h':
            moves = Knight('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'r':
            moves = Rook('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'b':
            moves = Bishop('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'q':
            moves = Queen('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'k':
            moves = King('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'w':
            moves = Wizard('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'd':
            moves = Dragon('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'a':
            moves = Archer('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)

        if moves:
            print(f"Возможные ходы для фигуры на {pos}: {', '.join(moves)}")
            hl = [self.board.parse_position(mv) for mv in moves]
            self.board.print_board(hl)
        else:
            print(f"Нет возможных ходов для фигуры на {pos}.")

    def threats(self, pos):
        """Отображает фигуры, которые угрожают указанной клетке.

        Args:
            pos (str): Позиция клетки (например, 'e4').
        """
        row, col = self.board.parse_position(pos)
        threats_list = []

        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece != '.' and (piece.islower() != self.board.board[row][col].islower()):
                    if piece.lower() == 'p':
                        moves = Pawn('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'h':
                        moves = Knight('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'r':
                        moves = Rook('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'b':
                        moves = Bishop('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'q':
                        moves = Queen('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'k':
                        moves = King('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'w':
                        moves = Wizard('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'd':
                        moves = Dragon('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)
                    elif piece.lower() == 'a':
                        moves = Archer('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}").get_possible_moves(self.board)

                    for mv in moves:
                        if self.board.parse_position(mv) == (row, col):
                            threats_list.append((i, j))

        self.board.print_board(threats_list)
        if threats_list:
            print(f"Фигура на {pos} под угрозой следующих фигур:")
            for i, j in threats_list:
                print(f"{self.board.board[i][j]} на {chr(j + ord('a'))}{8 - i}")
        else:
            print(f"Фигура на {pos} не находится под угрозой.")

    def save_game(self, filename):
        """Сохраняет историю ходов в указанный файл.

        Args:
            filename (str): Имя файла для сохранения.
        """
        with open(filename, 'w') as f:
            for move in self.board.move_history:
                start, end, piece, captured = move
                s_row, s_col = self.board.parse_position(start)
                e_row, e_col = self.board.parse_position(end)
                start_notation = f"{chr(s_col + ord('a'))}{8 - s_row}"
                end_notation = f"{chr(e_col + ord('a'))}{8 - e_row}"
                full_move = f"{piece}{start_notation}{end_notation}"
                f.write(f"{full_move}\n")
        print(f"Партия сохранена в файл {filename}")

    def load_game(self, filename):
        """Загружает партию из файла, воспроизводя все ходы.

        Args:
            filename (str): Имя файла для загрузки.
        """
        self.board = Board()
        self.turn = 'white'
        self.move_count = 0

        with open(filename, 'r') as f:
            for line in f:
                move = line.strip()
                piece = move[0]
                start_pos = move[1:3]
                end_pos = move[3:5]
                self.board.make_move(start_pos, end_pos)
        print(f"Партия загружена из файла {filename}")


class CheckersGame(Game):
    """Класс для управления игрой в шашки."""

    def __init__(self):
        self.board = Board(game_type='checkers')
        self.turn = 'white'
        self.move_count = 0

    def is_valid_move(self, start, end):
        s_row, s_col = self.board.parse_position(start)
        piece = self.board.board[s_row][s_col]
        if piece == '.' or (self.turn == 'white' and piece.islower()) or (self.turn == 'black' and piece.isupper()):
            return False

        checker = Checker('white' if piece.isupper() else 'black', start) if piece in 'Wb' else KingChecker('white' if piece.isupper() else 'black', start)
        return checker.is_valid_move(self.board, end)

    def make_move(self, start, end):
        print(f"\n=== Попытка хода {start} -> {end} ===")
        s_row, s_col = self.board.parse_position(start)
        e_row, e_col = self.board.parse_position(end)
        piece = self.board.board[s_row][s_col]
        print(f"Фигура: {piece}, цвет: {'белый' if piece.isupper() else 'черный'}")

        if abs(s_row - e_row) == 2:
            mid_row = (s_row + e_row) // 2
            mid_col = (s_col + e_col) // 2
            print(f"Удаляем шашку на {chr(mid_col + ord('a'))}{8 - mid_row}")
            self.board.board[mid_row][mid_col] = '.'

        if abs(s_row - e_row) == 2:
            mid_row = (s_row + e_row) // 2
            mid_col = (s_col + e_col) // 2
            captured = self.board.board[mid_row][mid_col]
            self.board.board[mid_row][mid_col] = '.'
            self.board.move_history.append((start, end, piece, captured))
        else:
            self.board.move_history.append((start, end, piece, None))

        self.board.board[s_row][s_col] = '.'
        self.board.board[e_row][e_col] = piece

        if (piece == 'W' and e_row == 0) or (piece == 'b' and e_row == 7):
            self.board.board[e_row][e_col] = piece.upper() if self.turn == 'white' else piece.lower()

        self.turn = 'black' if self.turn == 'white' else 'white'

    def hint(self, pos):
        row, col = self.board.parse_position(pos)
        piece = self.board.board[row][col]

        if piece == '.':
            print("На этой клетке нет шашки.")
            return
        if (self.turn == 'white' and piece.islower()) or (self.turn == 'black' and piece.isupper()):
            print("Подсказка для шашки противника недоступна.")
            return

        checker = Checker('white' if piece.isupper() else 'black', pos) if piece in 'Wb' else KingChecker('white' if piece.isupper() else 'black', pos)
        moves = checker.get_possible_moves(self.board)

        if moves:
            print(f"Возможные ходы для шашки на {pos}: {', '.join(moves)}")
            hl = [self.board.parse_position(mv) for mv in moves]
            self.board.print_board(hl)
        else:
            print(f"Нет возможных ходов для шашки на {pos}.")

    def threats(self, pos):
        row, col = self.board.parse_position(pos)
        threats_list = []
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece != '.' and (piece.islower() != self.board.board[row][col].islower()):
                    checker = Checker('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}") if piece in 'Wb' else KingChecker('white' if piece.isupper() else 'black', f"{chr(j + ord('a'))}{8 - i}")
                    moves = checker.get_possible_moves(self.board)
                    if pos in moves:
                        threats_list.append((i, j))

        self.board.print_board(threats_list)
        if threats_list:
            print(f"Клетка {pos} под угрозой следующих шашек:")
            for i, j in threats_list:
                print(f"{self.board.board[i][j]} на {chr(j + ord('a'))}{8 - i}")
        else:
            print(f"Клетка {pos} не находится под угрозой.")


if __name__ == "__main__":
    print("Выберите игру: 1 - Шахматы, 2 - Шашки")
    choice = input().strip()
    if choice == '1':
        game = Game()
    elif choice == '2':
        game = CheckersGame()
    else:
        print("Неверный выбор, по умолчанию запускаются шахматы.")
        game = Game()
    game.play()
