from maze import Maze
from graphics import Window
import random
import sys

def main():
    sys.setrecursionlimit(10000)
    num_rows = 20
    num_cols = 20
    win_width = 800
    win_height = 800
    margin = 25

    cell_size_x = (win_width - 2 * margin) / num_cols
    cell_size_y = (win_height - 2 * margin) / num_rows

    win = Window(win_width, win_height)
    
    # Draw things here
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    maze.solve()
    
    win.wait_for_close()


main()