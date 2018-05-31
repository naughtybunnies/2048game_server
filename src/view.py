import tkinter
from src.polygon import polygon

class View:
    def __init__(self, window, boardsize):
        self.window = window
        self.tile_padding = 10
        self.canvas_padding = 20
        self.tile_size = 80

        self.canvas_width = 2*self.canvas_padding + (boardsize-1)*self.tile_padding + (boardsize)*80
        self.canvas_height = 2*self.canvas_padding + (boardsize-1)*self.tile_padding + (boardsize)*80

        self.bgcolor = "#BBADA0"
        self.canvas = tkinter.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg=self.bgcolor)
        self.canvas.grid(row=0, column=0)

        score_width = 200
        score_height = self.canvas_height
        score_color = "#EDE0C8"
        self.score_canvas = tkinter.Canvas(self.window, width=score_width, height=score_height, bg=score_color)
        self.score_canvas.grid(row=0, column=1)


    def render(self, boardMatrix, score):
        for i in range(len(boardMatrix)):
            for j in range(len(boardMatrix)):
                xpos = self.canvas_padding + i*(self.tile_size) + i*(self.tile_padding)
                ypos = self.canvas_padding + j*(self.tile_size) + j*(self.tile_padding)
                polygon.drawtile(self.canvas, boardMatrix[j][i], self.tile_size, xpos, ypos)
        self.drawScore(score)

    def drawScore(self, score):
        text_xpos = 100
        text_ypos = 100
        self.score_canvas.delete('score')
        self.score_canvas.create_text(text_xpos, text_ypos, font=("Helvetica", 32), text=score, tags=('score'))
