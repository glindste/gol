#!/usr/bin/env python3

from drawille import Canvas, getTerminalSize
import time
import curses
import locale
import random
import sys

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
        self.can.clear()

    def put(self, matrix, x, y):
        for mx in range(len(matrix)):
            for my in range(len(matrix[0])):
                self.state[x+my][y+mx] = matrix[mx][my]


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

def __main__(stdsrc, argv=None):
    if argv == None:
        argv = sys.argv

    # Initialize putmatrix
    matrix = None
    if len(argv) > 1:
        # load specified file
        f = open( argv[1], 'r' )
        matrix = [ [ bool(int(val)) for val in  line.split(',')] for line in f ]
    else:
        matrix = [[True for i in range(20)] for j in range(20)]

    # Get terminal size
    term_x, term_y = getTerminalSize()

    # Set rows and columns
    columns = (term_x-1)*2
    rows = (term_y-1)*4

    g = GameOfLife(rows,columns)

    g.draw()

    c_x = 0
    c_y = 0
    stdscr.move(c_y,c_x)

    while True:

        g.tick()

        # Draw to curses
        g.draw()
        stdscr.move(c_y,c_x)

        stdscr.refresh()

        # Catch user input
        inp = stdscr.getch()
        if inp != curses.ERR:
            # Down
            if inp == 258:
                c_y = min(c_y + 1, term_y-1)
            # Up
            if inp == 259:
                c_y = max(c_y - 1, 0)
            # Left
            if inp == 260:
                c_x = max(c_x - 1, 0)
            # Right
            if inp == 261:
                c_x = min(c_x + 1, term_x-1)
            # Put
            if inp == ord(" "):
                g.put(matrix, c_x*2, c_y*4)
            # Quit
            if inp == 27:
                break

if __name__ == "__main__":
    curses.wrapper(__main__)
