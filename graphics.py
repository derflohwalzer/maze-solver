from tkinter import Tk, BOTH, Canvas

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})" 

class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
    
    def __repr__(self) -> str:
        return f"{self.start} -> {self.end}"    

    def draw(self, canvas, fill="black", width=1):
        canvas.create_line(
            self.start.x,
            self.start.y,
            self.end.x,
            self.end.y,
            fill=fill,
            width=width
        )

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.__root = Tk()
        self.__root.title("maze")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(self.__root, width=self.width, height=self.height)
        self.__canvas.pack()

        self.is_running = False
    
    def draw_line(self, line: Line, fill="black", width=1):
        line.draw(self.__canvas, fill, width)
               
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.is_running = True

        while self.is_running:
            self.redraw()
    
    def close(self):
        self.is_running = False
