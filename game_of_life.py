#!/usr/bin/env python3

from drawille import Canvas, getTerminalSize
import time
import curses
import locale
import random

locale.setlocale(locale.LC_ALL, "")

stdscr = curses.initscr()
stdscr.nodelay(True)
stdscr.refresh()

class GameOfLife:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.can = Canvas()
        self.state = [[bool(random.getrandbits(1)) for y in range(rows)] for x in range(cols)]

    def tick(self):
        next_gen = [[False for y in range(self.rows)] for x in range(self.cols)]

        for y in range(self.rows):
            for x in range(self.cols):
                nburs = self._ncount(x, y)
                if self.state[x][y]:
                    # Alive
                    if nburs > 1 and nburs < 4:
                        self.can.set(x,y)
                        next_gen[x][y] = True
                    else:
                        next_gen[x][y] = False
                else:
                    # Dead
                    if nburs == 3:
                        self.can.set(x,y)
                        next_gen[x][y] = True
                    else:
                        next_gen[x][y] = False

        self.state = next_gen

    def draw(self):
        f = self.can.frame(0,0,self.cols,self.rows)
        stdscr.addstr(0, 0, '{0}\n'.format(f))
        stdscr.refresh()
        self.can.clear()


    def _ncount(self, x, y):
        nburs = 0

        # Left
        if x > 0:
            if self.state[x-1][y]:
                nburs += 1
            # Top
            if y > 0:
                if self.state[x-1][y-1]:
                    nburs += 1
            # Bottom
            if y < self.rows-1:
                if self.state[x-1][y+1]:
                    nburs += 1

        # Right
        if x < self.cols-1:
            if self.state[x+1][y]:
                nburs += 1
            # Top
            if y > 0:
                if self.state[x+1][y-1]:
                    nburs += 1
            # Bottom
            if y < self.rows-1:
                if self.state[x+1][y+1]:
                    nburs += 1

        # Top
        if y > 0:
            if self.state[x][y-1]:
                nburs += 1
        # Bottom
        if y < self.rows-1:
            if self.state[x][y+1]:
                nburs += 1

        return nburs

def __main__(stdsrc):

    # Get terminal size
    term_x, term_y = getTerminalSize()

    # Set rows and columns
    columns = (term_x-1)*2
    rows = (term_y-1)*4

    g = GameOfLife(rows,columns)

    g.draw()

    while True:

        g.tick()
        g.draw()

        # Catch user input
        inp = stdscr.getch()
        if inp != curses.ERR:
            break

if __name__ == "__main__":
    curses.wrapper(__main__)
