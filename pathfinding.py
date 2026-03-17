import pygame as pg
import random


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((600, 600))
pg.display.set_caption("Pathfinding")
width = screen.get_width()
height = screen.get_height()

    
#spacing = 5
nodes = []

class Grid:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.n_w = (width / self.num_nodes ** 0.5) * 0.8
        self.n_h = (height / self.num_nodes ** 0.5) * 0.8
        self.spacing = (((width + height) / 2) / self.num_nodes ** 0.5) * 0.2 + (self.n_w / self.num_nodes ** 0.5)
        self.make_grid()
        #self.n_w = width / (self.num_nodes + spacing) ** 0.5 - spacing + spacing / 2 / self.num_nodes ** 0.5
        #self.n_h = height / (self.num_nodes + spacing) ** 0.5 - spacing + spacing / 2 / self.num_nodes ** 0.5
        
    def text(self, text):
        self.font = pg.font.Font(None, int(self.n_w / 1.5))
        return self.font.render(f"{text}", True, pg.Color("black"))
            
    def make_grid(self):
        nodes.clear()
        for i in range(self.num_nodes):
            n_x = self.spacing + (self.n_w + self.spacing) * (i % int(self.num_nodes ** 0.5))
            n_y = self.spacing + (self.n_h + self.spacing) * int(i / int(self.num_nodes ** 0.5))
            nodes.append(Open(n_x, n_y, self.n_w, self.n_h))
            #if random.random() > 0.3 - abs((len(nodes) - self.num_nodes / 2) / (self.num_nodes * 1)): 
                #nodes.append(Open(n_x, n_y, self.n_w, self.n_h))
            #else:
                #nodes.append(Obstacle(n_x, n_y, self.n_w, self.n_h))
    
        
class Open:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = pg.Color("white")
        self.rect = pg.Rect(x, y, w, h)
        #self.surf = pg.Surface((w, h))
        self.text = ""
        self.parent = None
    
    def draw(self):
        pg.draw.rect(screen, self.color, self.rect)

        if self.text:
            screen.blit(self.text, (self.x + self.w / 8, self.y + self.h / 8))
    
    # Denne funktion giver bedre mening i Grid, og konverteringen af noder kan være sin egen funktion, da forskellige dele af koden gør det samme.
    def mouse(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and type(self) != Obstacle:
                self.index = nodes.index(self)

                if event.button == 1:
                    for i, c in enumerate(nodes):
                        if type(c) == Start:
                            nodes[i] = Open(c.x, c.y, c.w, c.h)
                    nodes[nodes.index(self)] = Start(self.x, self.y, self.w, self.h)

                if event.button == 3:
                    for i, c in enumerate(nodes):
                        if type(c) == Goal:
                            nodes[i] = Open(c.x, c.y, c.w, c.h)
                    nodes[self.index] = Goal(self.x, self.y, self.w, self.h)
        
        # Køres hver gang musen bevæges, så man kan tegne mange Obstacle objekter.
        if event.type == pg.MOUSEMOTION:
            # Til debugging
            if event.buttons[1] and self.rect.collidepoint(event.pos) and type(self) != Obstacle:
                nodes[nodes.index(self)] = Obstacle(self.x, self.y, self.w, self.h)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                grid.make_grid()
        

    
    def update(self):
        self.draw()

class Obstacle(Open):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("dimgrey")

class Goal(Open):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.text = grid.text("B")
        self.color = pg.Color("red")

    def draw(self):
        pg.draw.rect(screen, self.color, self.rect)
        
        if self.text:
            screen.blit(self.text, (self.x + self.w / 3, self.y + self.h / 4))

class Start(Open):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.text = grid.text("A")
        self.color = pg.Color("green")
        
    def draw(self):
        pg.draw.rect(screen, self.color, self.rect)

        if self.text:
            screen.blit(self.text, (self.x + self.w / 3, self.y + self.h / 4))

class Closed(Open):
    def __init__(self, x, y, w, h, F_cost):
        super().__init__(x, y, w, h)
        self.F_cost = F_cost
        self.text = grid.text(self.F_cost)
        self.color = pg.Color("orange")

class Path(Closed):
    def __init__(self, x, y, w, h, F_cost):
        super().__init__(x, y, w, h, F_cost)
        self.color = pg.Color("blue")
    

class Algorithm:
    def __init__(self):
        self.closed_list = []
        self.reverse = False


    def F_cost(self, node, start, goal):
        f = self.G_cost(node, start) + self.H_cost(node, goal)
        #print(grid.text(self.G_cost(node, start)))
        #return self.G_cost(node, start)
        return f

    def G_cost(self, node, start):
       
        dx = abs(int(node.x) - int(start.x)) // int(node.w)
        dy = abs(int(node.y) - int(start.y)) // int(node.h)
        
        if dx > dy:
            return 14 * dy + 10 * (dx - dy)
        return 14 * dx + 10 * (dy - dx)


        #return (((start.x - node.x) ** 2 + (start.y - node.y) ** 2) ** 0.5)
        #return int((((start.x - node.x) ** 2 + (start.y - node.y) ** 2) ** 0.5) * 10 * (grid.num_nodes ** 0.5 / width))

    def H_cost(self, node, goal):
        dx = abs(int(node.x) - int(goal.x)) // int(node.w)
        dy = abs(int(node.y) - int(goal.y)) // int(node.h)
        
        if dx > dy:
            return 14 * dy + 10 * (dx - dy)
        return 14 * dx + 10 * (dy - dx)

        #return ((goal.x - node.x) ** 2 + (goal.y - node.y) ** 2) ** 0.5
    
    def find_nbs_index(self, node):
        node_index = nodes.index(node)
        return (int(node_index + 1), # Højre
                int(node_index - 1), # Venstre
                int(node_index + grid.num_nodes ** 0.5), # Under
                int(node_index - grid.num_nodes ** 0.5), # Over
                int(node_index + grid.num_nodes ** 0.5 + 1), # Diagonale noder
                int(node_index + grid.num_nodes ** 0.5 - 1),
                int(node_index - grid.num_nodes ** 0.5 - 1),
                int(node_index - grid.num_nodes ** 0.5 + 1))

    def next_node(self, node):
        if node and self.reverse == False:
            goal = [n for n in nodes if type(n) == Goal][0]
            start = [n for n in nodes if type(n) == Start][0]
            nb_i = self.find_nbs_index(node)

            if goal and start:
                for i in nb_i:
                    if i >= 0 and i < len(nodes):
                        nb = nodes[i]
                        if type(nb) == Goal:
                            self.reverse = True
                            #if type(node) == Closed:
                                #node = Path(node.x, node.y, node.w, node.h, node.F_cost)
                            self.path(node)
                            
                            #self.path(node)
                        if type(nb) == Open: 
                            cost = self.F_cost(nb, start, goal)
                            
                            new_nb = Closed(nb.x, nb.y, nb.w, nb.h, cost)
                            new_nb.parent = node
                            self.closed_list.append(new_nb)
                            
                            nodes[i] = new_nb



    def best_nb(self):
        if self.closed_list and self.reverse == False:
            best = min(self.closed_list, key=lambda c_node: c_node.F_cost)
            self.closed_list.remove(best)
            #nodes[nodes.index(best)] = Closed(best.x, best.y, best.w, best.h, best.F_cost)
            best.color = pg.Color("yellow")
            #self.closed_list = []
            return best
    
    def path(self, node):
        print(node.x, node.y)
        nodes[nodes.index(node)] = Path(node.x, node.y, node.w, node.h, node.F_cost)
        if node.parent:
            if type(node.parent) == Closed:
                #node.parent = Path(node.parent.x, node.parent.y, node.parent.w, node.parent.h, node.parent.F_cost)
                #nodes[nodes.index(node.parent)] = Path(node.parent.x, node.parent.y, node.parent.w, node.parent.h, node.parent.F_cost)
                self.path(node.parent)
            else:
                pass
                #self.reverse = False

        """
        nb_i = self.find_nbs_index(node)
        if node:
            while self.final == False:
                for i in nb_i:
                    pass

            if type(nb) == Start:
                self.final = True
        """
        
    def solve(self):
        while self.reverse == False:
            algorithm.next_node(algorithm.best_nb())
        self.closed_list = []
        self.reverse = False

class System:
    # Overvejelse til refactoring.
    # Kan indeholde et grid, nodes, algoritme og spiller i stedet for at have dem i global scope.
    # Kan stå for state-logik, f.eks. hvor langt algoritmen er (ligesom self.reverse) og kalde metoder på baggrund af det.
    pass


class Player:
    pass

grid = Grid(20 ** 2)
algorithm = Algorithm()

#grid.F_cost(cells[20], cells[80], cells[200])

running = True
#cell_list[50] = Goal(cell_list[50].x, cell_list[50].y, cell_list[50].w, cell_list[50].h)

while running:

    for event in pg.event.get():
        for n in nodes:
            n.mouse(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                closed_exists = False
                for n in nodes:
                    if type(n) == Start:
                        algorithm.next_node(n)
                    if type(n) == Closed:
                        closed_exists = True
                if closed_exists:
                    algorithm.solve()
                    #algorithm.next_node(algorithm.best_nb())


        if event.type == pg.QUIT:
            running = False
    for n in nodes:
        n.update()

    pg.display.flip()
    clock.tick(60)

