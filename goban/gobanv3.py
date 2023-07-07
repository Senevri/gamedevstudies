import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from dataclasses import dataclass
import logging


logger = logging.getLogger(__name__)
logger.warn = logger.warning
logger.setLevel(logging.DEBUG)

class GobanException(Exception):
    pass


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


    def switch_current_player(self):
        self.current_player = 'white' if self.current_player == 'black' else 'black'

    def make_move(self, row, col):
        if self.board[row][col] is None:
            move = Move(row, col, self.current_player, self.current_player, True)
            self.previous_moves.append(move)
            self.board[row][col] = self.current_player
            self.switch_current_player()
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
        else:
            self.board[row][col] = None
            self.captures[self.current_player] += 1

    def undo_move(self):
        if not self.previous_moves:
            return
        move = self.previous_moves.pop()
        row, col = move.row, move.col
        player = move.player
        addition = move.addition

        if addition:
            self.board[row][col] = None
            self.captures[player] -= 1
        elif self.board[row][col] is None:
            self.board[row][col] = move.color
            self.captures[player] += 1
        self.captures[player] = max(self.captures[player], 0)
        self.switch_current_player()


class GoBoardUI:
    def __init__(self, size):
        self.size = size
        self.margin = 45 #30
        self.board_size = 855#570
        self.stone_margin = 2
        self.cell_size = (self.board_size) // self.size

        self.window = tk.Tk()
        frame = tk.Frame(self.window)

        self.canvas = tk.Canvas(self.window, width=self.board_size + self.margin, height=self.board_size + self.margin * 2)
        #self.canvas.grid(row=0, column=0)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.handle_click)



        self.undo_button = tk.Button(frame, text='Undo', command=self.undo_move)
        self.status_label = tk.Label(frame, text='Black: 0 | White: 0', width=20)

        self.go_board = GoBoard(size)
        self.player_button = tk.Button(frame, text=self.go_board.current_player, command=self.switch_player)
        self.player_label = tk.Label(frame, text="Turn:")

        self.undo_button.grid(row=1, column=2)
        self.player_label.grid(row=1, column=0)
        self.player_button.grid(row=1, column=1)
        self.status_label.grid(row=2, column=1)
        frame.pack()

        self.window.bind("<KeyPress-z>", self.undo_key)
        self.draw_board_ui()

        self.stone_images = []

    def undo_key(self, event):
        if event.keysym == 'z':
            self.undo_move()

    def switch_player(self):
        self.go_board.switch_current_player()
        self.player_button.configure(text=self.go_board.current_player)

    def draw_border(self):
        border_line_width = 2  # Width of the border lines

        right_edge = bottom_edge = self.board_size + self.margin
        #top
        self.canvas.create_line(self.margin, self.margin, right_edge, self.margin, width=border_line_width)
        #bottom
        self.canvas.create_line(self.margin, bottom_edge, right_edge, bottom_edge, width=border_line_width)
        #left
        self.canvas.create_line(self.margin, self.margin, self.margin, self.board_size + self.margin, width=border_line_width)
        #right
        self.canvas.create_line(right_edge, self.margin, right_edge, bottom_edge, width=border_line_width)

    def draw_lines(self):
        self.draw_border()
        for row in range(self.size):
            y = self.margin // 2 + row * self.cell_size + self.margin + self.cell_size // 2
            self.canvas.create_line(self.margin, y, self.board_size + self.margin, y)

        for col in range(self.size):
            x = self.margin // 2 + col * self.cell_size + self.margin + self.cell_size // 2
            self.canvas.create_line(x, self.margin, x, self.board_size + self.margin)

    def draw_markings(self):
        cell_size = self.board_size // self.size

        for i in range(self.size):
            x = cell_size // 2
            y = self.margin + (self.size - i - 1) * cell_size + cell_size // 2
            self.canvas.create_text(x, y, text=str(i + 1))

        for i in range(self.size):
            x = (i + 1) * cell_size + cell_size // 2
            y = 10 + self.margin + self.size * cell_size + 5
            self.canvas.create_text(x, y, text=chr(65 + i))

    def draw_stone(self, row, col, color):
        margin = self.stone_margin
        x1, y1 = self.margin // 2 + col * self.cell_size + self.margin, self.margin // 2 + row * self.cell_size + self.margin
        x2, y2 = self.margin // 2 + (col + 1) * self.cell_size + self.margin, self.margin // 2 + (row + 1) * self.cell_size + self.margin
        outline_width=1
        outline_color = "black"

        canvas = self.canvas
        # Create an image with RGBA mode
        image = Image.new("RGBA", (x2 - x1, y2 - y1))

        # Create a draw object
        draw = ImageDraw.Draw(image)

        # # Draw an anti-aliased oval on the image
        draw.ellipse(
            [(0, 0), (x2 - x1-margin, y2 - y1-margin)],
            fill=color, outline=outline_color, width=outline_width
            )

        # # Draw a slightly larger filled oval
        # draw.ellipse([(0, 0), (x2 - x1-margin + outline_width, y2 - y1-margin + outline_width)], fill=outline_color)

        # # Draw a slightly smaller filled oval in the center
        # draw.ellipse([(outline_width // 2 + margin // 2, outline_width // 2 + margin // 2),
        #               (x2 - x1 - outline_width-margin // 2, y2 - y1 - outline_width-margin // 2)
        #              ], fill=color)


        # Convert the image to Tkinter-compatible format
        photo_image = ImageTk.PhotoImage(image)

        self.stone_images.append(photo_image)
        # Display the image on the canvas
        canvas.create_image(x1+margin, y1+margin, image=photo_image, anchor=tk.NW)

    def draw_board(self):
        self.stone_images = []
        for row in range(self.size):
            for col in range(self.size):

                if stone := self.go_board.board[row][col]:
                    #self.canvas.create_oval(x1+margin, y1+margin, x2-margin, y2-margin, fill=stone, outline='black')
                    self.draw_stone(row, col, color=stone)

    def update_ui_data(self):
        self.status_label.config(text=f'Black: {self.go_board.captures["white"]} | White: {self.go_board.captures["black"]}')
        self.player_button.configure(text=self.go_board.current_player)

    def draw_board_ui(self):
        self.canvas.delete('all')
        self.draw_lines()
        self.draw_markings()
        self.draw_board()
        self.update_ui_data()

    def handle_click(self, event):
        row = (event.y - int(self.margin * 1.5)) // self.cell_size
        col = (event.x - int(self.margin * 1.5)) // self.cell_size

        if 0 <= row < self.size-1 and 0 <= col < self.size-1:
            self.go_board.make_move(row, col)
            self.draw_board_ui()

    def undo_move(self):
        self.go_board.undo_move()
        self.draw_board_ui()

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    board_size = 19
    game_ui = GoBoardUI(board_size)
    game_ui.run()
