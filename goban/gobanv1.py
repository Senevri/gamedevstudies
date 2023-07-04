import tkinter as tk

class GoBoard:
    def __init__(self, size):
        self.size = size
        self.board = [[None] * size for _ in range(size)]
        self.current_player = 'black'
        self.previous_moves = []

        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=570, height=600)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.handle_click)

        self.undo_button = tk.Button(self.window, text='Undo', command=self.undo_move)
        self.undo_button.pack()

        self.status_label = tk.Label(self.window, text='Black: 0 | White: 0', width=20)
        self.status_label.pack()

        self.captures = {"white":0, "black":0}

        self.draw_board()

    def draw_board(self):
        self.canvas.delete('all')
        cell_size = 570 // self.size

        for row in range(self.size + 1):
            y = row * cell_size + cell_size/2
            self.canvas.create_line(cell_size, y, self.size * cell_size, y)

        for col in range(self.size + 1):
            x = col * cell_size + cell_size/2
            self.canvas.create_line(x, cell_size, x, self.size * cell_size)

        black_count, white_count = 0, 0

        for row in range(self.size):
            for col in range(self.size):
                x1, y1 = col * cell_size, row * cell_size
                x2, y2 = (col + 1) * cell_size, (row + 1) * cell_size

                stone = self.board[row][col]
                if stone == 'black':
                    self.canvas.create_oval(x1, y1, x2, y2, fill='black')
                    black_count += 1
                elif stone == 'white':
                    self.canvas.create_oval(x1, y1, x2, y2, fill='white', outline='black')
                    white_count += 1

        self.status_label.config(text=f'Black: {self.captures["white"]} | White: {self.captures["black"]}')

    def handle_click(self, event):
        cell_size = 570 // self.size
        row = event.y // cell_size
        col = event.x // cell_size

        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.previous_moves.append((row, col))
            self.current_player = 'white' if self.current_player == 'black' else 'black'
        elif (row, col) in self.previous_moves:
            self.board[row][col] = None
            self.previous_moves.remove((row, col))
            self.captures[self.current_player] += 1

        self.draw_board()

    def undo_move(self):
        if self.previous_moves:
            row, col = self.previous_moves.pop()
            stone = self.board[row][col]
            self.board[row][col] = None
            self.current_player = 'white' if stone == 'black' else 'black'
        self.draw_board()

if __name__ == '__main__':
    board_size = 19
    game = GoBoard(board_size)
    game.window.mainloop()
