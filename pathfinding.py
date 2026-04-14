import pygame as pg
import random


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((600, 700))
pg.display.set_caption("Pathfinding")
width = screen.get_width()
height = screen.get_height()
UI_font = pg.font.Font(None, 30)
    
#spacing = 5
nodes = []

class Grid:
    def __init__(self, x, y, num_nodes):
        self.x = x
        self.y = y
        self.num_nodes = num_nodes
        self.n_w = (width / self.num_nodes ** 0.5) * 0.8
        self.n_h = (width / self.num_nodes ** 0.5) * 0.8
        self.spacing = (width  / self.num_nodes ** 0.5) * 0.19
        #self.spacing = (((width + height) / 2) / self.num_nodes ** 0.5) * 0.2 + (self.n_w / self.num_nodes ** 0.5)
        #self.n_w = width / (self.num_nodes + spacing) ** 0.5 - spacing + spacing / 2 / self.num_nodes ** 0.5
        #self.n_h = height / (self.num_nodes + spacing) ** 0.5 - spacing + spacing / 2 / self.num_nodes ** 0.5
        #self.start_created = False
        #self.goal_created = False

        self.make_grid()

    def text(self, text):
        self.font = pg.font.Font(None, int(self.n_w / 1.5))
        return self.font.render(f"{text}", True, pg.Color("black"))
            
    def make_grid(self):
        nodes.clear()
        for i in range(self.num_nodes):
            n_x = self.x + self.spacing + (self.n_w + self.spacing) * (i % int(self.num_nodes ** 0.5))
            n_y = self.y + self.spacing + (self.n_h + self.spacing) * int(i / int(self.num_nodes ** 0.5))
            #nodes.append(Open(n_x, n_y, self.n_w, self.n_h))

            # Lav obstacle objekter
            if random.random() > 0.3 - abs((len(nodes) - self.num_nodes / 2) / self.num_nodes): 
                nodes.append(Open(n_x, n_y, self.n_w, self.n_h))
            else:
               nodes.append(Obstacle(n_x, n_y, self.n_w, self.n_h))    

            """
            # Lav start objekt
            elif random.random() < 0.3 - abs((len(nodes) - self.num_nodes / 4) / (self.num_nodes * 1)) and self.start_created == False:
                nodes.append(Start(n_x, n_y, self.n_w, self.n_h))
                self.start_created = True
            
            # Lav goal objekt
            elif random.random() < abs((len(nodes) - self.num_nodes * 0.75) / (self.num_nodes * 1)) and self.goal_created == False:
                nodes.append(Goal(n_x, n_y, self.n_w, self.n_h))
                self.goal_created = True
            """
            
            
            """
            # Lav start objekt
            if random.random() > 0.05 - abs((len(nodes) - self.num_nodes / 4) / (self.num_nodes * 1)):
                # Forhindrer flere start objekter
                for i, c in enumerate(nodes):
                        if type(c) == Start:
                            nodes[i] = Open(c.x, c.y, c.w, c.h)
                    nodes[nodes.index(self)] = Start(self.x, self.y, self.w, self.h)
            """

        """    
        if not any(isinstance(node, Start) for node in nodes):
            r_i = random.randint(0, self.num_nodes - 1)
            nodes[r_i] = Start(nodes[r_i].x, nodes[r_i].y, nodes[r_i].w, nodes[r_i].h)
        """
    
    def make_start_and_goal(self):
        # Start laves tilfældigt inden for de tre sidste linjer af gitteret
        r_i = random.randint(int(self.num_nodes - self.num_nodes ** 0.5 * 3 - 1), self.num_nodes - 1)
        nodes[r_i] = Start(nodes[r_i].x, nodes[r_i].y, nodes[r_i].w, nodes[r_i].h)
        nodes[r_i].text = grid.text("A")

        # Goal laves tilfældigt inden for de tre første linjer af gitteret
        r_i = random.randint(0, int(self.num_nodes ** 0.5 * 3 - 1))
        nodes[r_i] = Goal(nodes[r_i].x, nodes[r_i].y, nodes[r_i].w, nodes[r_i].h)
        nodes[r_i].text = grid.text("B")
            
    
        
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
        self.chosen = False # Om spilleren har gættet på denne node som en del af stien
    
    def draw(self):
        pg.draw.rect(screen, self.color, self.rect)

        if self.text:
            screen.blit(self.text, (self.x + self.w / 8, self.y + self.h / 8))
    
    # Denne funktion giver bedre mening i Grid, og konverteringen af noder kan være sin egen funktion, da forskellige dele af koden gør det samme.
    def mouse(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and type(self) != Obstacle:
                self.index = nodes.index(self)

                """
                if event.button == 1:
                    for i, c in enumerate(nodes):
                        if type(c) == Start:
                            nodes[i] = Open(c.x, c.y, c.w, c.h)
                    nodes[nodes.index(self)] = Start(self.x, self.y, self.w, self.h)
                """

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
                grid.make_start_and_goal()
        

    def update(self):
        self.draw()

class Obstacle(Open):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("dimgrey")

class Goal(Open):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        #self.text = grid.text("B")
        self.color = pg.Color("red")

    def draw(self):
        pg.draw.rect(screen, self.color, self.rect)
        
        if self.text:
            screen.blit(self.text, (self.x + self.w / 3, self.y + self.h / 4))

class Start(Open):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        #self.text = grid.text("A")
        self.color = pg.Color("green")
        
    def draw(self):
        pg.draw.rect(screen, self.color, self.rect)

        if self.text:
            screen.blit(self.text, (self.x + self.w / 3, self.y + self.h / 4))

class Closed(Open):
    def __init__(self, x, y, w, h, chosen, F_cost):
        super().__init__(x, y, w, h)
        self.F_cost = F_cost
        #self.text = grid.text(self.F_cost)
        #self.color = pg.Color("orange")
        self.chosen = chosen

class Path(Closed):
    def __init__(self, x, y, w, h, chosen, F_cost):
        super().__init__(x, y, w, h, chosen, F_cost)
        self.color = pg.Color("blue")
        self.text = grid.text(self.F_cost)
        self.chosen = chosen
    

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
        neighbors = []
        node_index = nodes.index(node)
        size = int(grid.num_nodes ** 0.5)
        col = node_index % size
        row = node_index // size
        # højre
        if col < size - 1:
            neighbors.append(node_index + 1)

        # venstre
        if col > 0:
            neighbors.append(node_index - 1)

        # ned
        if row < size - 1:
            neighbors.append(node_index + size)

        # op
        if row > 0:
            neighbors.append(node_index - size)

        # diagonaler
        if col < size - 1 and row < size - 1:
            neighbors.append(node_index + size + 1)

        if col > 0 and row < size - 1:
            neighbors.append(node_index + size - 1)

        if col < size - 1 and row > 0:
            neighbors.append(node_index - size + 1)

        if col > 0 and row > 0:
            neighbors.append(node_index - size - 1)

        return neighbors

    def next_node(self, node):
        if node and self.reverse == False:
            goal = [n for n in nodes if type(n) == Goal][0]
            start = [n for n in nodes if type(n) == Start][0]
            nb_i = self.find_nbs_index(node)

            if goal and start:
                for i in nb_i:
                    nb = nodes[i]

                    """
                    if i == nb_i[4]:
                        pass

                    if i == nb_i[5]:
                        pass

                    if i == nb_i[6]:
                        pass

                    if i == nb_i[7]:
                        pass
                    """

                    
                    if type(nb) == Goal:
                        self.reverse = True
                        #if type(node) == Closed:
                            #node = Path(node.x, node.y, node.w, node.h, node.F_cost)
                        self.path(node)
                        
                        #self.path(node)
                    if type(nb) == Open: 
                        cost = self.F_cost(nb, start, goal)
                        
                        new_nb = Closed(nb.x, nb.y, nb.w, nb.h, nb.chosen, cost)
                        new_nb.parent = node
                        self.closed_list.append(new_nb)
                        
                        nodes[i] = new_nb



    def best_nb(self):
        if self.closed_list and self.reverse == False:
            best = min(self.closed_list, key=lambda c_node: c_node.F_cost)
            self.closed_list.remove(best)
            #nodes[nodes.index(best)] = Closed(best.x, best.y, best.w, best.h, best.F_cost)
            #best.color = pg.Color("yellow")
            best.color = pg.Color("orange") if best.chosen else pg.Color("white")
            #self.closed_list = []
            return best
    
    def path(self, node):
        #print(node.x, node.y)
        i = nodes.index(node)
        #print(nodes[i].chosen)
        nodes[i] = Path(node.x, node.y, node.w, node.h, node.chosen, node.F_cost)
        #print(nodes[i].chosen)
        if nodes[i].chosen == True:
            player.score += 1
            nodes[i].color = pg.Color("yellow")
        

            
        if node.parent:
            if type(node.parent) == Closed:
                #node.parent = Path(node.parent.x, node.parent.y, node.parent.w, node.parent.h, node.parent.F_cost)
                #nodes[nodes.index(node.parent)] = Path(node.parent.x, node.parent.y, node.parent.w, node.parent.h, node.parent.F_cost)
                self.path(node.parent)
            else:
                pass
                #print(player.score)
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

class UserInterface:
    def __init__(self):
        pass
    
    def show_score(self):
        pass


class System:
    # Overvejelse til refactoring.
    # Kan indeholde et grid, nodes, algoritme og spiller i stedet for at have dem i global scope.
    # Kan stå for state-logik, f.eks. hvor langt algoritmen er (ligesom self.reverse) og kalde metoder på baggrund af det.
    pass


class Player:
    def __init__(self):
        self.score = 0
        self.total_guesses = 0

    def choose_path(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for n in nodes:
                    if n.rect.collidepoint(event.pos) and type(n) == Open:
                        if n.chosen == False:
                            self.total_guesses += 1
                        n.chosen = True
                        n.color = pg.Color("orange")

        if event.type == pg.MOUSEMOTION:
            for n in nodes:
                if event.buttons[0] and n.rect.collidepoint(event.pos) and type(n) == Open:
                    if n.chosen == False:
                        self.total_guesses += 1
                    n.chosen = True
                    n.color = pg.Color("orange")
    

grid = Grid(0, 100, 16 ** 2)
algorithm = Algorithm()
player = Player()

grid.make_start_and_goal()
#grid.make_grid() # Kaldes først her, da Goal objektet i metoden bruger en Grid metode.
#grid.F_cost(cells[20], cells[80], cells[200])

running = True
#cell_list[50] = Goal(cell_list[50].x, cell_list[50].y, cell_list[50].w, cell_list[50].h)

while running:
    screen.fill(pg.Color("black"))
    for event in pg.event.get():
        for n in nodes:
            n.mouse(event)
        player.choose_path(event)
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
    
    # UI
    
    UI_text = UI_font.render(f"{player.score}/{player.total_guesses}", True, pg.Color("white"))
    screen.blit(UI_text, (20, 20))

    pg.display.flip()
    clock.tick(60)

