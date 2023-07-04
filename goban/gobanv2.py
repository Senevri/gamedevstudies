import tkinter as tk
from dataclasses import dataclass


class GobanException(Exception):
    ...

@dataclass
class Move:
    row: int
    col: int
    player: str
    color: str
    addition: bool

class GoBoard:
    def __init__(self, size):
        self.size = size
        self.board = [[None] * size for _ in range(size)]
        self.current_player = 'black'
        self.previous_moves = []
        self.captures = {"white": 0, "black": 0}

        self.margin = 30
        #self.cell_size = (570 - self.margin) // self.size
        self.board_size = 570
        self.cell_size = (self.board_size - self.margin) // self.size

        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=self.board_size + self.margin, height=self.board_size + self.margin*2)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.handle_click)


        self.undo_button = tk.Button(self.window, text='Undo', command=self.undo_move)
        self.undo_button.pack()

        self.status_label = tk.Label(self.window, text='Black: 0 | White: 0', width=20)
        self.status_label.pack()

        self.draw_board_ui()

    def draw_border(self):
        border_line_width = 2  # Width of the border lines

        self.canvas.create_line(self.margin, self.margin, self.board_size + self.margin, self.margin, width=border_line_width)

        self.canvas.create_line(self.margin, self.board_size + self.margin, self.board_size + self.margin, self.board_size + self.margin, width=border_line_width)

        self.canvas.create_line(self.margin, self.margin, self.margin, self.board_size + self.margin, width=border_line_width)

        self.canvas.create_line(self.board_size + self.margin, self.margin, self.board_size + self.margin, self.board_size + self.margin, width=border_line_width)


    def draw_lines(self):
        self.draw_border()
        for row in range(self.size):
            y = self.margin//2 + row * self.cell_size + self.margin + self.cell_size // 2
            self.canvas.create_line(self.margin, y, self.board_size + self.margin, y)

        for col in range(self.size):
            x = self.margin // 2 + col * self.cell_size + self.margin + self.cell_size // 2
            self.canvas.create_line(x, self.margin, x, self.board_size + self.margin)

    def draw_markings(self):
        cell_size = 570 // self.size

        for i in range(self.size):
            x = cell_size // 2
            y = self.margin + (self.size - i -1) * cell_size + cell_size // 2
            self.canvas.create_text(x, y, text=str(i + 1))

        for i in range(self.size):
            x = (i + 1) * cell_size + cell_size // 2
            y = 10+self.margin + self.size * cell_size + 5
            self.canvas.create_text(x, y, text=chr(65 + i))

    def draw_board(self):
        for row in range(self.size):
            for col in range(self.size):
                x1, y1 = self.margin//2 + col * self.cell_size + self.margin, self.margin//2 + row * self.cell_size + self.margin
                x2, y2 = self.margin//2 + (col + 1) * self.cell_size + self.margin, self.margin//2 + (row + 1) * self.cell_size + self.margin

                stone = self.board[row][col]

                if stone == 'black':
                    self.canvas.create_oval(x1, y1, x2, y2, fill='black')
                elif stone == 'white':
                    self.canvas.create_oval(x1, y1, x2, y2, fill='white', outline='black')

    def draw_ui(self):
        self.status_label.config(text=f'Black: {self.captures["white"]} | White: {self.captures["black"]}')

    def draw_board_ui(self):
        self.canvas.delete('all')
        self.draw_lines()
        self.draw_markings()
        self.draw_board()
        self.draw_ui()

    def handle_click(self, event):
        row = (event.y - int(self.margin*1.5)) // self.cell_size
        col = (event.x - int(self.margin*1.5)) // self.cell_size

        print(f"clicked position: row={row}, col={col}")

        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col] is None:
                move = Move(row, col, self.current_player, self.current_player, True)
                self.previous_moves.append(move)
                self.board[row][col] = self.current_player
                self.current_player = 'white' if self.current_player == 'black' else 'black'
            elif (row, col) in [(move.row, move.col) for move in self.previous_moves]:
                prev_move = None
                for prev_move in self.previous_moves:
                    if prev_move.row == row and prev_move.col == col:
                        break
                if prev_move:
                    move = Move(row, col, self.current_player, prev_move.color, False)
                else:
                    raise GobanException("Prev move but no prev move.")
                self.previous_moves.append(move)
                self.board[row][col] = None
                #self.current_player = 'white' if self.current_player == 'black' else 'black'
            else:
                self.board[row][col] = None
                self.captures[self.current_player] += 1

        self.draw_board_ui()


    def undo_move(self):
        if self.previous_moves:
            move = self.previous_moves.pop()
            row, col = move.row, move.col
            player = move.player
            addition = move.addition

            if addition:
                self.board[row][col] = None
                #if color != player:
                self.captures[player] -= 1
            elif self.board[row][col] is None:
                self.board[row][col] = move.color
                self.captures[player] += 1

            self.current_player = 'white' if move.player == 'black' else 'black'

        self.draw_board_ui()

if __name__ == '__main__':
    board_size = 19
    game = GoBoard(board_size)
    game.window.mainloop()
