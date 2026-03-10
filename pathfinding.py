import pygame as pg
import random


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((600, 600))
pg.display.set_caption("Pathfinding")
width = screen.get_width()
height = screen.get_height()

    
spacing = 5
nodes = []

class Grid:
    def __init__(self, num_cells):
        self.num_cells = num_cells
        self.c_w = width / (self.num_cells + spacing) ** 0.5 - spacing + spacing / 2 / self.num_cells ** 0.5
        self.c_h = height / (self.num_cells + spacing) ** 0.5 - spacing + spacing / 2 / self.num_cells ** 0.5
        self.font = pg.font.Font(None, int(self.c_w / 1.5))

        self.make_grid()
        
    def make_grid(self):
        for i in range(self.num_cells):
            c_x = spacing + (self.c_w + spacing) * (i % int(self.num_cells ** 0.5))
            c_y = spacing + (self.c_h + spacing) * int(i / int(self.num_cells ** 0.5))
            #print(0.1 - abs((len(cells) - self.num_cells / 2) / (self.num_cells * 1)))
            if random.random() > 0.3 - abs((len(nodes) - self.num_cells / 2) / (self.num_cells * 1)): 
                nodes.append(Node(c_x, c_y, self.c_w, self.c_h))
            else:
                nodes.append(Obstacle(c_x, c_y, self.c_w, self.c_h))
    

    # Skal flyttes til Algorithm
    def F_cost(self, cell, start, goal):
        f = int(self.G_cost(cell, start) + self.H_cost(cell, goal))
        #print(f)
        cell.text = self.font.render(f"{f}", True, pg.Color("black"))

    def G_cost(self, cell, start):
        return ((start.x - cell.x) ** 2 + (start.y - cell.y) ** 2) ** 0.5

    def H_cost(self, cell, goal):
        return ((goal.x - cell.x) ** 2 + (goal.y - cell.y) ** 2) ** 0.5
        


class Node:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = pg.Color("white")
        self.rect = pg.Rect(x, y, w, h)
        #self.surf = pg.Surface((w, h))
        self.text = ""
    
    def draw(self):
        pg.draw.rect(screen, self.color, self.rect)

        if self.text:
            screen.blit(self.text, (self.x + self.w / 8, self.y + self.h / 8))
    
    def mouse(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and type(self) != Obstacle:
                self.index = nodes.index(self)
                if event.button == 1:
                    for i, c in enumerate(nodes):
                        if type(c) == Goal:
                            nodes[i] = Node(c.x, c.y, c.w, c.h)
                    nodes[self.index] = Goal(self.x, self.y, self.w, self.h)
                
                if event.button == 3:
                    for i, c in enumerate(nodes):
                        if type(c) == Start:
                            nodes[i] = Node(c.x, c.y, c.w, c.h)
                    nodes[nodes.index(self)] = Start(self.x, self.y, self.w, self.h)      
    
    def update(self):
        self.draw()

class Obstacle(Node):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("dimgrey")

class Goal(Node):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("red")

class Start(Node):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("green")

    def next_cell(self):
        goal_cell = None
        self.index = nodes.index(self)
        self.nb_i = (int(self.index + 1),
                        int(self.index - 1),
                        int(self.index + grid.num_cells ** 0.5),
                        int(self.index - grid.num_cells ** 0.5),
                        int(self.index + grid.num_cells ** 0.5 + 1),
                        int(self.index + grid.num_cells ** 0.5 - 1),
                        int(self.index - grid.num_cells ** 0.5 - 1),
                        int(self.index - grid.num_cells ** 0.5 + 1))

        goal_cell = [n for n in nodes if isinstance(n, Goal)][0]
        #print(goal_cell)
        if goal_cell:
            for n in self.nb_i:
                if nodes[n]:
                    nb = nodes[n]
                    if type(nb) == Node: 
                        #print(c, self, goal_cell)
                        grid.F_cost(nb, self, goal_cell)

                        new_nb = Closed(nb.x, nb.y, nb.w, nb.h)
                        new_nb.text = nb.text
                        nodes[n] = new_nb
        """
        for c in cells:
            if type(c) == Cell:
                if goal_cell: 
                    #print(c, self, goal_cell)
                    grid.F_cost(c, self, goal_cell)
        """

class Closed(Start):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("blue")

grid = Grid(20 ** 2)

class Algorithm:
    pass

class Player:
    pass




#grid.F_cost(cells[20], cells[80], cells[200])

running = True
#cell_list[50] = Goal(cell_list[50].x, cell_list[50].y, cell_list[50].w, cell_list[50].h)

while running:

    for n in nodes:
        n.update()

    for event in pg.event.get():
        #print(event.type)
        for n in nodes:
            n.mouse(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                
                for n in nodes:
                    if type(n) == Goal:
                        print("rgfejuneirfgn")
                    if type(n) == Start:
                        n.next_cell()


        if event.type == pg.QUIT:
            running = False
        

    pg.display.flip()
    clock.tick(60)

