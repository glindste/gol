#!/usr/bin/env python3

from drawille import Canvas
import time
import curses
import locale
import random

locale.setlocale(locale.LC_ALL, "")

stdscr = curses.initscr()
stdscr.refresh()

rows = 100
columns = 100

def neighbour_count(state, x, y):
    nburs = 0

    #print(" x=" + str(x) + " y=" + str(y) + " " + str(len(state)) + " " + str(len(state[0])))
    #if x >= 98:
        #time.sleep(3)

    # Left
    if x > 0:
        if state[x-1][y]:
            #if x == 20 and y == 20:
                #print("left")
            nburs += 1
        # Top
        if y > 0:
            if state[x-1][y-1]:
                #if x == 20 and y == 20:
                    #print("topleft")
                nburs += 1
        # Bottom
        if y < rows-1:
            if state[x-1][y+1]:
                #if x == 20 and y == 20:
                    #print("bottomleft")
                nburs += 1

    # Right
    if x < columns-1:
        if state[x+1][y]:
            #if x == 20 and y == 20:
                #print("right")
            nburs += 1
        # Top
        if y > 0:
            if state[x+1][y-1]:
                #if x == 20 and y == 20:
                    #print("topright")
                nburs += 1
        # Bottom
        if y < rows-1:
            if state[x+1][y+1]:
                #if x == 20 and y == 20:
                    #print("bottomright")
                nburs += 1

    # Top
    if y > 0:
        if state[x][y-1]:
            #if x == 20 and y == 20:
                #print("top")
            nburs += 1
    # Bottom
    if y < rows-1:
        if state[x][y+1]:
            #if x == 20 and y == 20:
                #print("bottom")
            nburs += 1

    return nburs


def __main__(stdsrc):

    state = [[bool(random.getrandbits(1)) for y in range(rows)] for x in range(columns)]

    c = Canvas()

    f = c.frame(0,0,columns,rows)
    stdscr.addstr(0, 0, '{0}\n'.format(f))
    stdscr.refresh()

    while True:

        next_gen = [[False for y in range(rows)] for x in range(columns)]

        for y in range(rows):
            for x in range(columns):
                nburs = neighbour_count(state, x, y)
                if state[x][y]:
                    #print("" + str(x) + " " + str(y) + " is alive, nburs = " + str(nburs))
                    # Alive
                    if nburs > 1 and nburs < 4:
                        c.set(x,y)
                        next_gen[x][y] = True
                    else:
                        next_gen[x][y] = False
                else:
                    # Dead
                    if nburs == 3:
                        c.set(x,y)
                        next_gen[x][y] = True
                    else:
                        next_gen[x][y] = False

        f = c.frame(0,0,columns,rows)
        stdscr.addstr(0, 0, '{0}\n'.format(f))
        stdscr.refresh()

        c.clear()

        state = next_gen
        #time.sleep(0.3)


def printState(state):
        s = ' '
        for i in range(len(state[0])):
              s += ' '+str(i)
        for i, row in enumerate(state):
              s += '\n\r'
              s += str(i)
              for col in state[i]:
                  s += ' '
                  if col:
                      s+='A'
                  else:
                      s+='D'

        s+='\n\r'

        print(s)


if __name__ == "__main__":
    curses.wrapper(__main__)
