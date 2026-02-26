import pygame as pg

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((600, 600))
width = screen.get_width()
height = screen.get_height()
spacing = 5
cell_list = []

class Grid:
    def __init__(self, num_cells):
        self.num_cells = num_cells
        self.c_w = width / (self.num_cells + spacing) ** 0.5 - spacing + spacing / 2 / self.num_cells ** 0.5
        self.c_h = height / (self.num_cells + spacing) ** 0.5 - spacing + spacing / 2 / self.num_cells ** 0.5

        self.make_grid()
        
        
            
    def make_grid(self):
        for i in range(self.num_cells):
            c_x = spacing + (self.c_w + spacing) * (i % self.num_cells ** 0.5)
            c_y = spacing + (self.c_h + spacing) * int(i / self.num_cells ** 0.5)
            cell_list.append(Cell(c_x, c_y, self.c_w, self.c_h))

class Cell:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = pg.Color("grey")
        self.rect = pg.Rect(x, y, w, h)
        #self.surf = pg.Surface((w, h))
    
    def show(self):
        pg.draw.rect(screen, self.color, self.rect)
    
    def mouse(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.index = cell_list.index(self)
                if event.button == 1:
                    for i, c in enumerate(cell_list):
                        if type(c) == Goal:
                            cell_list[i] = Cell(c.x, c.y, c.w, c.h)
                    cell_list[self.index] = Goal(self.x, self.y, self.w, self.h)
                
                if event.button == 3:
                    for i, c in enumerate(cell_list):
                        if type(c) == Start:
                            cell_list[i] = Cell(c.x, c.y, c.w, c.h)
                    cell_list[cell_list.index(self)] = Start(self.x, self.y, self.w, self.h)      
    
    def update(self):
        self.show()

class Obstacle(Cell):
    pass

class Goal(Cell):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("green")

class Start(Cell):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("red")

grid = Grid(13 ** 2)


running = True
#cell_list[50] = Goal(cell_list[50].x, cell_list[50].y, cell_list[50].w, cell_list[50].h)

while running:

    for c in cell_list:
        c.update()

    for event in pg.event.get():
        for c in cell_list:
            c.mouse(event)
        if event.type == pg.QUIT:
            running = False

    pg.display.flip()
    clock.tick(60)

