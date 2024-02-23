import tkinter as tk

CELL_SIZE = 28
CELL_PAD = 2


class Floorer:
    def __init__(self):
        self.root: tk.Tk | None = None
        self.w = 0
        self.h = 0
        self.c: tk.Canvas | None = None

    def reset(self, w, h):
        self.w = w
        self.h = h
        if self.root:
            self.root.destroy()
        self.root = tk.Tk('Floorer')
        xl = w*(CELL_SIZE + CELL_PAD) + CELL_PAD + 2
        yl = h*(CELL_SIZE + CELL_PAD) + CELL_PAD + 2
        self.c = tk.Canvas(self.root, width=xl, height=yl, background='black')
        self.c.pack()
        for y in range(CELL_PAD, yl, CELL_SIZE + CELL_PAD):
            for x in range(CELL_PAD + 2, xl, CELL_SIZE + CELL_PAD):
                self.c.create_rectangle(x, yl - y, x + CELL_SIZE, yl - (y + CELL_SIZE), fill='gray')

    def main_loop(self):
        self.root.mainloop()


if __name__ == '__main__':
    f = Floorer()
    f.reset(10, 10)
    f.main_loop()
