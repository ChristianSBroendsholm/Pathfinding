import pygame as pg
import random

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("A Starry Path")
        self.clock = pg.time.Clock()
        # Disse kan evt. være i Display:
        self.screen = pg.display.set_mode((600, 700)) 
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.running = True

    def setup(self):
        self.algorithm = Algorithm()
        self.display = Display()
        self.player = Player()
        self.grid = Grid(0, 100, 16 ** 2)
        self.grid.make_start_and_goal()

    def run(self):
        while self.running:
            self.draw()
            self.events()

            pg.display.flip()
            self.clock.tick(60)

    def draw(self):
        self.screen.fill(pg.Color("black"))

        for n in self.grid.nodes:
            n.draw()
        
        for s in self.display.stars:
            self.screen.blit(s[0], s[1])
        
        self.display.draw_UI()


    def events(self):
        for event in pg.event.get():
        
            for n in self.grid.nodes:
                n.mouse(event)
            self.player.choose_path(event)

            if event.type == pg.MOUSEBUTTONDOWN:
                if self.display.backspace_rect.collidepoint(event.pos):
                    self.restart()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    closed_exists = False
                    for n in self.grid.nodes:
                        if type(n) == Start:
                            self.algorithm.next_node(n)
                        if type(n) == Closed:
                            closed_exists = True
                    if closed_exists and not self.algorithm.solved:
                        self.algorithm.solve()

                        # For manuel løsning
                        #self.algorithm.next_node(algorithm.best_nb())

                if event.key == pg.K_BACKSPACE:
                    self.restart()

            if event.type == pg.QUIT:
                self.running = False
        
    def restart(self):
        self.algorithm.solved = False
        self.grid.make_grid()
        self.grid.make_start_and_goal()
        self.display.stars = []

        self.player.score = 0 # Disse kan evt. fjernes for at vise totale point
        self.player.total_guesses = 0 

        self.algorithm.iterations = 0
        
    # Overvejelse til refactoring.
    # Kan indeholde et grid, nodes, algoritme og spiller i stedet for at have dem i global scope.
    # Kan stå for state-logik, f.eks. hvor langt algoritmen er (ligesom self.reverse) og kalde metoder på baggrund af det.

class Algorithm:
    def __init__(self):
        self.closed_list = []
        self.reverse = False
        self.solved = False
        self.iterations = 0

    def F_cost(self, node, start, goal):
        f = self.G_cost(node, start) + self.H_cost(node, goal)
        return f

    def G_cost(self, node, start):
       
        dx = abs(int(node.x) - int(start.x)) // int(node.w)
        dy = abs(int(node.y) - int(start.y)) // int(node.h)
        
        if dx > dy:
            return 14 * dy + 10 * (dx - dy)
        return 14 * dx + 10 * (dy - dx)

    def H_cost(self, node, goal):
        dx = abs(int(node.x) - int(goal.x)) // int(node.w)
        dy = abs(int(node.y) - int(goal.y)) // int(node.h)
        
        if dx > dy:
            return 14 * dy + 10 * (dx - dy)
        return 14 * dx + 10 * (dy - dx)
    
    def find_nbs_index(self, node):
        neighbors = []
        node_index = game.grid.nodes.index(node)
        col = node_index % game.grid.size
        row = node_index // game.grid.size

        def not_obstacle(i):
            return type(game.grid.nodes[i]) != Obstacle

        right = node_index + 1
        left = node_index - 1
        down = node_index + game.grid.size
        up = node_index - game.grid.size

        # Højre
        if col < game.grid.size - 1:
            neighbors.append(right)

        # Venstre
        if col > 0:
            neighbors.append(left)

        # Ned
        if row < game.grid.size - 1:
            neighbors.append(down)

        # Op
        if row > 0:
            neighbors.append(up)

        # Diagonaler
        if col < game.grid.size - 1 and row < game.grid.size - 1:
            if not_obstacle(right) or not_obstacle(down):
                neighbors.append(down + 1)

        if col > 0 and row < game.grid.size - 1:
            if not_obstacle(left) or not_obstacle(down):
                neighbors.append(down - 1)

        if col < game.grid.size - 1 and row > 0:
            if not_obstacle(right) or not_obstacle(up):
                neighbors.append(up + 1)

        if col > 0 and row > 0:
            if not_obstacle(left) or not_obstacle(up):
                neighbors.append(up - 1)

        return neighbors

    def next_node(self, node):
        if node and self.reverse == False:
            goal = [n for n in game.grid.nodes if type(n) == Goal][0]
            start = [n for n in game.grid.nodes if type(n) == Start][0]
            nb_i = self.find_nbs_index(node)
            
            if goal and start:
                for i in nb_i:
                    nb = game.grid.nodes[i]

                    if type(nb) == Goal:
                        self.reverse = True
                        self.path(node)
                        
                    if type(nb) == Open: 
                        cost = self.F_cost(nb, start, goal)
                        new_nb = Closed(nb.x, nb.y, nb.w, nb.h, nb.chosen, cost)
                        new_nb.parent = node
                        self.closed_list.append(new_nb)
                        game.grid.nodes[i] = new_nb

    def best_nb(self):
        if self.closed_list and self.reverse == False:
            best = min(self.closed_list, key=lambda c_node: c_node.F_cost)
            self.closed_list.remove(best)
            return best
    
    def path(self, node):
        i = game.grid.nodes.index(node)
        game.grid.nodes[i] = Path(node.x, node.y, node.w, node.h, node.chosen, node.F_cost)
        
        if game.grid.nodes[i].chosen == True:
            game.player.score += 1
            game.grid.nodes[i].color = pg.Color("darkgoldenrod1")
            
        if node.parent:
            if type(node.parent) == Closed:
                self.path(node.parent)
        
    def solve(self):
        while self.reverse == False and self.iterations < game.grid.num_nodes:
            self.next_node(self.best_nb())
            self.iterations += 1

        self.solved = True
        self.closed_list = []
        self.reverse = False

        if self.iterations >= game.grid.num_nodes:
            game.restart()
        

class Display:
    def __init__(self):
        self.stars = []
        self.star = pg.image.load('star_2.png')
        self.UI_star = pg.transform.scale(self.star, (50, 50))
        
        # Stjernen bruges ikke kun i UI, men også på gitteret
        self.backspace = pg.image.load('backspace_3.png')
        self.backspace = pg.transform.scale(self.backspace, (50 * 2.5, 50))
        self.backspace_rect = self.backspace.get_rect(topleft=(game.width - 150, 50))
        
        self.new_round_text = self.text("Ny runde", size=40, color="white")

    def text(self, text, size = None, color = "black"):
        # Size kan ikke sættes til størrelsen som parameter, da game endnu ikke er dannet.
        if size == None:
            size = int(game.grid.n_w / 1.5)
        self.font = pg.font.Font(None, int(size))
        return self.font.render(f"{text}", True, pg.Color(color))
    
    def draw_UI(self):
        
        game.screen.blit(self.UI_star, (20, 25))
        
        self.score_text = self.text(f"{game.player.score}/{game.player.total_guesses}", size=60, color="white")
        game.screen.blit(self.score_text, (80, 35))

        game.screen.blit(self.backspace, self.backspace_rect)
        
        game.screen.blit(self.new_round_text, (450, 20))


class Player:
    def __init__(self):
        self.score = 0
        self.total_guesses = 0

    def choose_path(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for n in game.grid.nodes:
                    if n.rect.collidepoint(event.pos) and type(n) == Open:
                        if n.chosen == False:
                            self.total_guesses += 1
                            game.grid.make_stars(n, 1)
                        n.chosen = True             

        if event.type == pg.MOUSEMOTION:
            for n in game.grid.nodes:
                if event.buttons[0] and n.rect.collidepoint(event.pos) and type(n) == Open:
                    if n.chosen == False:
                        self.total_guesses += 1
                        game.grid.make_stars(n, 1)
                    n.chosen = True  

class Grid:
    def __init__(self, x, y, num_nodes):
        self.x = x
        self.y = y
        self.num_nodes = num_nodes
        self.n_w = (game.width / self.num_nodes ** 0.5) * 0.8
        self.n_h = (game.width / self.num_nodes ** 0.5) * 0.8
        self.spacing = (game.width  / self.num_nodes ** 0.5) * 0.19
        self.size = int(self.num_nodes ** 0.5)
        self.nodes = []

        self.make_grid()

    def text(self, text):
        self.font = pg.font.Font(None, int(self.n_w / 1.5))
        return self.font.render(f"{text}", True, pg.Color("black"))
            
    def make_grid(self):
        self.nodes.clear()
        for i in range(self.num_nodes):
            n_x = self.x + self.spacing + (self.n_w + self.spacing) * (i % int(self.num_nodes ** 0.5))
            n_y = self.y + self.spacing + (self.n_h + self.spacing) * int(i / int(self.num_nodes ** 0.5))

            # Lav obstacle objekter
            if random.random() > 0.45 - abs((len(self.nodes) - self.num_nodes / 2) / self.num_nodes): 
                self.nodes.append(Open(n_x, n_y, self.n_w, self.n_h))
            else:
               self.nodes.append(Obstacle(n_x, n_y, self.n_w, self.n_h))
    
    def make_start_and_goal(self):
        # Start laves tilfældigt inden for de tre sidste linjer af gitteret
        r_i = random.randint(int(self.num_nodes - self.num_nodes ** 0.5 * 3 - 1), self.num_nodes - 1)
        self.nodes[r_i] = Start(self.nodes[r_i].x, self.nodes[r_i].y, self.nodes[r_i].w, self.nodes[r_i].h)
        self.nodes[r_i].text = game.display.text("A")

        # Goal laves tilfældigt inden for de tre første linjer af gitteret
        r_i = random.randint(0, int(self.num_nodes ** 0.5 * 3 - 1))
        self.nodes[r_i] = Goal(self.nodes[r_i].x, self.nodes[r_i].y, self.nodes[r_i].w, self.nodes[r_i].h)
        self.nodes[r_i].text = game.display.text("B")

    # Giver måske bedre mening et andet sted
    def make_stars(self, node, star_amount):
        for _ in range(star_amount):
            scale = int(game.grid.n_w / 1.5)
            r_x = random.randint(int(node.x), int(node.x + node.w / 3))
            r_y = random.randint(int(node.y), int(node.y + node.h / 3))
            node_star = pg.transform.scale(game.display.star, (scale, scale))
            game.display.stars.append((node_star, (r_x, r_y)))
               
class Open:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = pg.Color("white")
        self.rect = pg.Rect(x, y, w, h)
        self.text = ""
        self.parent = None
        self.chosen = False # Om spilleren har gættet på denne node som en del af stien
    
    def draw(self):
        pg.draw.rect(game.screen, self.color, self.rect)

        if self.text:
            game.screen.blit(self.text, (self.x + self.w / 8, self.y + self.h / 8))
    
    # Denne funktion giver bedre mening i Grid, og konverteringen af noder kan være sin egen funktion, da forskellige dele af koden gør det samme.
    def mouse(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and type(self) != Obstacle:
                self.index = game.grid.nodes.index(self)
        
        # Køres hver gang musen bevæges, så man kan tegne mange Obstacle objekter.
        if event.type == pg.MOUSEMOTION:
            # Til debugging
            if event.buttons[1] and self.rect.collidepoint(event.pos) and type(self) != Obstacle:
                game.grid.nodes[game.grid.nodes.index(self)] = Obstacle(self.x, self.y, self.w, self.h)


class Obstacle(Open):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("dimgrey")

class Goal(Open):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("red")

    def draw(self):
        pg.draw.rect(game.screen, self.color, self.rect)
        
        if self.text:
            game.screen.blit(self.text, (self.x + self.w / 3, self.y + self.h / 4))

class Start(Open):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color = pg.Color("green")
        
    def draw(self):
        pg.draw.rect(game.screen, self.color, self.rect)

        if self.text:
            game.screen.blit(self.text, (self.x + self.w / 3, self.y + self.h / 4))

class Closed(Open):
    def __init__(self, x, y, w, h, chosen, F_cost):
        super().__init__(x, y, w, h)
        self.F_cost = F_cost
        self.chosen = chosen

class Path(Closed):
    def __init__(self, x, y, w, h, chosen, F_cost):
        super().__init__(x, y, w, h, chosen, F_cost)
        self.color = pg.Color("darkgoldenrod4")
        self.chosen = chosen


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()