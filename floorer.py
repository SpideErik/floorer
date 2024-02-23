import tkinter as tk
import time

CELL_SIZE = 28
CELL_PAD = 2


class FloorerError(Exception):
    pass


class Floorer:
    def __init__(self):
        self.root: tk.Tk | None = None
        self.w = 0
        self.h = 0
        self.x = 0
        self.y = 0
        self.c: tk.Canvas | None = None
        self._rect = []
        self._f = None
        self._yl = 0
        self.timeout = 0.1

    def __getitem__(self, xy):
        if xy[0] < 1 or xy[0] > self.w or xy[1] < 1 or xy[1] > self.h:
            return 'wall'
        i = xy[0] - 1 + (xy[1]-1)*self.w
        return self._rect[i][1]

    def __setitem__(self, xy, color):
        i = xy[0] - 1 + (xy[1]-1)*self.w
        self.c.itemconfig(self._rect[i][0], fill=color)
        self._rect[i][1] = color

    def reset(self, w, h):
        self.w = w
        self.h = h
        if self.root:
            self.root.destroy()
        self.root = tk.Tk()
        xl = w*(CELL_SIZE + CELL_PAD) + CELL_PAD + 2
        yl = h*(CELL_SIZE + CELL_PAD) + CELL_PAD + 2
        self._yl = yl
        self.c = tk.Canvas(self.root, width=xl, height=yl, background='black')
        self.c.pack()
        self._rect = []
        for y in range(CELL_PAD, yl, CELL_SIZE + CELL_PAD):
            for x in range(CELL_PAD + 2, xl, CELL_SIZE + CELL_PAD):
                r = self.c.create_rectangle(x, yl - y, x + CELL_SIZE, yl - (y + CELL_SIZE), fill='gray')
                self._rect.append([r, 'gray'])
        self._f = self.c.create_oval(0, 0, CELL_SIZE//2, CELL_SIZE//2, fill='cyan')
        self.move_to(1, 1)

    def main_loop(self):
        self.root.mainloop()

    def put(self, color):
        if self[self.x, self.y] != 'gray':
            raise FloorerError('Нельзя класть на занятую клетку')
        self[self.x, self.y] = color
        self.root.update()
        time.sleep(self.timeout)

    def remove(self):
        if self[self.x, self.y] == 'gray':
            raise FloorerError('Клетка пустая')
        self[self.x, self.y] = 'gray'

    def move(self, dx, dy):
        self.move_to(self.x + dx, self.y + dy)

    def move_to(self, x, y):
        if 0 < x <= self.w and 0 < y <= self.h:
            self.x = x
            self.y = y
            x = (x - 1)*(CELL_SIZE+CELL_PAD) + CELL_PAD + CELL_SIZE//4
            y = (y - 1)*(CELL_SIZE+CELL_PAD) + CELL_PAD + CELL_SIZE//4
            self.c.moveto(self._f, x + 2, self._yl - y - CELL_SIZE//2)
            self.root.update()
            time.sleep(self.timeout)
        else:
            raise FloorerError('Паркетчик разбился')

    def up(self):
        self.move(0, 1)

    def down(self):
        self.move(0, -1)

    def left(self):
        self.move(-1, 0)

    def right(self):
        self.move(1, 0)

    def get(self):
        return self[self.x, self.y]

    def get_up(self):
        return self[self.x, self.y + 1]

    def get_down(self):
        return self[self.x, self.y - 1]

    def get_left(self):
        return self[self.x - 1, self.y]

    def get_right(self):
        return self[self.x + 1, self.y]


f = Floorer()

if __name__ == '__main__':
    f.reset(30, 30)
    f.timeout = 0.01
    xl = 1
    while f.get_up() != 'wall':
        xl += 1
        f.up()
    print(xl)
    f.move_to(7, 7)
    for action in (f.up, f.right, f.down, f.left):
        cnt = xl - 13
        while cnt > 0:
            f.put('green')
            action()
            cnt -= 1
    f.main_loop()
