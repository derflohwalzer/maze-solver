import unittest
from maze import Maze
from graphics import Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(500,500))

        self.assertEqual(
            len(m1.cells),
            num_rows,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_cols,
        )
    
    def test_resetted_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(500,500))

        for r in range(num_rows):
            for c in range(num_cols):
                self.assertEqual(
                    False, m1.cells[r][c].visited
                )


if __name__ == "__main__":
    unittest.main()