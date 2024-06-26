from tkinter import Tk, BOTH, Canvas
from graphics import Line, Point
from time import sleep
import random

class Cell:
    def __init__(self, win=None):
        self.win = win
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self.visited = False

    def __repr__(self) -> str:
        res = f"""
            ({self.x1}, {self.y1}) 
                         TTTTTT
                        L      R
                        L      R
                        LBBBBBBR 
                                ({self.x2}, {self.y2})
        """
        res = res.replace("L", "|") if self.has_left_wall else res.replace("L", " ")
        res = res.replace("T", "_") if self.has_top_wall else res.replace("T", " ")
        res = res.replace("R", "|") if self.has_right_wall else res.replace("R", " ")
        res = res.replace("B", "_") if self.has_bottom_wall else res.replace("B", " ")

        return res
    
    def _center(self):
        return Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
    
    def draw(self):
        bg_color = "#d9d9d9"

        # Draw Top wall
        line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
        self.win.draw_line(line, 'black' if self.has_top_wall else bg_color, 2)
        
        # Draw Right wall
        line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
        self.win.draw_line(line, 'black' if self.has_right_wall else bg_color, 2)
    
        # Draw bottom wall:
        line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
        self.win.draw_line(line, 'black' if self.has_bottom_wall else bg_color, 2)
        
        # Draw Left wall:
        line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
        self.win.draw_line(line, 'black' if self.has_left_wall else bg_color, 2)
    
    def draw_move(self, to_cell, undo=False):
        line = Line(self._center(), to_cell._center())
        self.win.draw_line(line, '#b0b0b0' if undo else 'red')
    
class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed:
            random.seed(seed)

        self.cells = [[None for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.create_cells()
        self.create_entrance_exit()
        self.create_path_recur(0, 0)
        self.reset_visited()
    
    def __repr__(self):
        return str(self.cells)
    
    def create_cells(self):
        for r in range(self.num_rows):     
            for c in range(self.num_cols):
                self.cells[r][c] = Cell()
                self.draw_cell(r, c)
  
    def draw_cell(self, r, c):
        cell = self.cells[r][c]
        cell.win = self.win 
        cell.x1 = self.x1 + self.cell_size_x * c
        cell.y1 = self.y1 + self.cell_size_y * r
        cell.x2 = cell.x1 + self.cell_size_x
        cell.y2 = cell.y1 + self.cell_size_y
        cell.draw()
        self.animate()
    
    def animate(self):
        self.win.redraw()
        sleep(0.025)
    
    def create_entrance_exit(self):
        self.cells[0][0].has_top_wall = False
        self.draw_cell(0, 0)
        self.cells[self.num_rows - 1][self.num_cols - 1].has_bottom_wall = False
        self.draw_cell(self.num_rows - 1, self.num_cols - 1)

    def create_path_recur(self, r, c):
        current = self.cells[r][c]
        current.visited = True

        while True:
            to_visit = []

            if (c > 0) and not (self.cells[r][c - 1].visited):
                to_visit.append((r, c - 1))

            if (r > 0) and not (self.cells[r - 1][c].visited):
                to_visit.append((r - 1, c))

            if (c < self.num_cols - 1) and not (self.cells[r][c + 1].visited):
                to_visit.append((r, c + 1))

            if (r < self.num_rows - 1) and not (self.cells[r + 1][c].visited):
                to_visit.append((r + 1, c))
            
            if len(to_visit) == 0:
                self.draw_cell(r, c)
                return

            # random direction
            next = random.choice(to_visit)

            # remove top wall
            if next[0] == r - 1:
                self.cells[r][c].has_top_wall = False
                self.cells[r - 1][c].has_bottom_wall = False

            # remove bottom wall
            if next[0] == r + 1:
                self.cells[r][c].has_bottom_wall = False
                self.cells[r + 1][c].has_top_wall = False

            # remove left wall
            if next[1] == c - 1:
                self.cells[r][c].has_left_wall = False
                self.cells[r][c - 1].has_right_wall = False

            # remove right wall
            if next[1] == c + 1:
                self.cells[r][c].has_right_wall = False
                self.cells[r][c + 1].has_left_wall = False
                
            self.create_path_recur(next[0], next[1])

    def reset_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False 
    
    def solve(self):
        return self.solve_recur(0, 0)

    def solve_recur(self, r, c):
        
        self.animate()
        goal = (self.num_rows - 1, self.num_cols - 1)
        
        if (r, c) == goal:
            return True

        current = self.cells[r][c]
        current.visited = True

        # Go Left
        if (c > 0) and not (current.has_left_wall) and not (self.cells[r][c - 1].visited):
            current.draw_move(self.cells[r][c - 1])
            
            if self.solve_recur(r, c - 1):
                return True
            else:
                current.draw_move(self.cells[r][c - 1], undo=True)

        # Go Top
        if (r > 0) and not (current.has_top_wall) and not (self.cells[r - 1][c].visited):
            current.draw_move(self.cells[r - 1][c])
            
            if self.solve_recur(r - 1, c):
                return True
            else:
                current.draw_move(self.cells[r - 1][c], undo=True)

        # Go Right
        if (c < self.num_cols - 1) and not (current.has_right_wall) and not (self.cells[r][c + 1].visited):
            current.draw_move(self.cells[r][c + 1])
            
            if self.solve_recur(r, c + 1):
                return True
            else:
                current.draw_move(self.cells[r][c + 1], undo=True)
        # Go Bottom
        if (r < self.num_rows - 1) and not (current.has_bottom_wall) and not (self.cells[r + 1][c].visited):
            current.draw_move(self.cells[r + 1][c])
            
            if self.solve_recur(r + 1, c):
                return True
            else:
                current.draw_move(self.cells[r + 1][c], undo=True)
        
        return False
        



