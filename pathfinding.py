import pygame as pg
import random
import time

def benchmark(game, runs=100, repeats=20, mode="obstacles"):

    results = []

    for i in range(runs):

        if mode == "nodes":
            num_nodes = (i + 3) ** 2
            obstacle = 0
        elif mode == "obstacles":
            num_nodes = 50 ** 2
            obstacle = i / runs

        times = []

        for _ in range(repeats):
            start = time.perf_counter()

            game.algorithm = Algorithm()
            game.grid = Grid(0, 100, num_nodes, obstacle)
            game.grid.make_start_and_goal()

            game.algorithm.solve()

            end = time.perf_counter()
            times.append(end - start)

        avg_time = sum(times) / len(times)
        results.append((num_nodes, avg_time, obstacle))

    def fmt(x):
        """Formatterer decimaltal til indsættelse i Excel"""
        return str(x).replace(".", ",")

    print("noder;tid;forhindringschance")

    for n, t, o in results:
        print(f"{n};{fmt(t)};{fmt(o)}")


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("A Starry Path")
        self.clock = pg.time.Clock()
        self.running = True

    def setup(self):
        self.algorithm = Algorithm()
        self.display = Display(600, 700)
        self.player = Player()
        self.grid = Grid(0, 100, 16 ** 2, 0.45)
        self.grid.make_start_and_goal()

    def run(self):
        while self.running:
            self.draw()
            self.events()

            pg.display.flip()
            self.clock.tick(60)

    def draw(self):
        self.display.screen.fill(pg.Color("black"))

        for n in self.grid.nodes:
            n.draw()
        
        for s in self.display.stars:
            self.display.screen.blit(s[0], s[1])
        
        self.display.draw_UI()


    def events(self):
        for event in pg.event.get():
        
            for n in self.grid.nodes:
                n.mouse(event)
            self.player.choose_path(event)

            if event.type == pg.MOUSEBUTTONDOWN:

                if self.display.difficulty_easy.collidepoint(event.pos):
                    self.set_difficulty(0.1)

                elif self.display.difficulty_mid.collidepoint(event.pos):
                    self.set_difficulty(0.3)

                elif self.display.difficulty_hard.collidepoint(event.pos):
                    self.set_difficulty(0.5)

                if self.display.backspace_rect.collidepoint(event.pos):
                    self.restart()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not self.algorithm.solved:
                        self.algorithm.solve()

                if event.key == pg.K_BACKSPACE:
                    self.restart()

            if event.type == pg.QUIT:
                self.running = False
    
    def set_difficulty(self, dif):
        self.display.difficulty = dif
        self.grid.obstacle_chance = dif
        self.restart()

    def restart(self):
        self.algorithm = Algorithm()
        self.grid = Grid(0, 100, self.grid.num_nodes, self.grid.obstacle_chance)
        self.grid.make_start_and_goal()
        self.display.stars = []

        self.player.score = 0
        self.player.total_guesses = 0

        self.algorithm.iterations = 0

class Algorithm:
    def __init__(self):
        self.open_set = []
        self.closed_set = []
        self.solved = False
        self.iterations = 0
        self.start = None
        self.goal = None

    def reset(self):
        self.open_set = []
        self.closed_set = []
        self.solved = False
        self.iterations = 0
        self.start = None
        self.goal = None

        for n in game.grid.nodes:
            n.parent = None
            n.g_cost = None
            n.h_cost = None
            n.f_cost = None

            if n.state == "closed":
                n.state = "open" if n.state != "obstacle" else "obstacle"
            if n.state == "path":
                n.state = "open" if n.state != "obstacle" else "obstacle"

    def find_special(self, state_name):
        for n in game.grid.nodes:
            if n.state == state_name:
                return n

    def node_pos(self, node):
        i = game.grid.nodes.index(node)
        return i % game.grid.size, i // game.grid.size

    def H_cost(self, node, goal):
        x1, y1 = self.node_pos(node)
        x2, y2 = self.node_pos(goal)
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return 14 * min(dx, dy) + 10 * abs(dx - dy)

    def movement_cost(self, a, b):
        ax, ay = self.node_pos(a)
        bx, by = self.node_pos(b)
        if ax != bx and ay != by:
            return 14
        return 10

    def find_nbs_index(self, node):
        neighbors = []
        node_index = game.grid.nodes.index(node)
        size = game.grid.size
        col = node_index % size
        row = node_index // size

        def is_not_obstacle(i):
            return 0 <= i < len(game.grid.nodes) and game.grid.nodes[i].state != "obstacle"

        right = node_index + 1
        left = node_index - 1
        down = node_index + size
        up = node_index - size

        if col < size - 1 and is_not_obstacle(right):
            neighbors.append(right)

        if col > 0 and is_not_obstacle(left):
            neighbors.append(left)

        if row < size - 1 and is_not_obstacle(down):
            neighbors.append(down)

        if row > 0 and is_not_obstacle(up):
            neighbors.append(up)

        if col < size - 1 and row < size - 1:
            diag = down + 1
            if is_not_obstacle(diag) and (is_not_obstacle(right) or is_not_obstacle(down)):
                neighbors.append(diag)

        if col > 0 and row < size - 1:
            diag = down - 1
            if is_not_obstacle(diag) and (is_not_obstacle(left) or is_not_obstacle(down)):
                neighbors.append(diag)

        if col < size - 1 and row > 0:
            diag = up + 1
            if is_not_obstacle(diag) and (is_not_obstacle(right) or is_not_obstacle(up)):
                neighbors.append(diag)

        if col > 0 and row > 0:
            diag = up - 1
            if is_not_obstacle(diag) and (is_not_obstacle(left) or is_not_obstacle(up)):
                neighbors.append(diag)

        if not neighbors:
            # Hvis der er ingen naboer, kan spillet ikke komme videre, og spillet genstartes ikke under solve(). 
            game.restart()

        return neighbors

    def begin_search(self):
        self.reset()

        self.start = self.find_special("start")
        self.goal = self.find_special("goal")

        if self.start is None or self.goal is None:
            self.solved = True
            return

        self.start.g_cost = 0
        self.start.h_cost = self.H_cost(self.start, self.goal)
        self.start.f_cost = self.start.g_cost + self.start.h_cost
        self.open_set = [self.start]

    def reconstruct_path(self, node):
        current = node
        while current is not None:
            if current.state not in ("start", "goal"):
                current.state = "path"
                if current.chosen:
                    game.player.score += 1
            current = current.parent

    def step(self):
        if not self.open_set:
            self.solved = True
            return

        current = min(self.open_set, key=lambda n: (n.f_cost, n.h_cost))
        self.open_set.remove(current)
        self.closed_set.append(current)

        if current.state not in ("start", "goal"):
            current.state = "closed"

        if current is self.goal:
            self.reconstruct_path(current)
            self.solved = True
            return

        for idx in self.find_nbs_index(current):
            neighbor = game.grid.nodes[idx]

            if neighbor in self.closed_set:
                continue

            tentative_g = current.g_cost + self.movement_cost(current, neighbor)

            if neighbor.g_cost is None or tentative_g < neighbor.g_cost:
                neighbor.parent = current
                neighbor.g_cost = tentative_g
                neighbor.h_cost = self.H_cost(neighbor, self.goal)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost

                if neighbor not in self.open_set:
                    self.open_set.append(neighbor)

    def solve(self):
        if self.solved:
            return

        self.begin_search()

        while not self.solved and self.open_set and self.iterations < game.grid.num_nodes:
            self.step()
            self.iterations += 1

        if not self.solved:
            game.restart()
        

class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((self.width, self.height)) 

        self.stars = []
        self.star = pg.image.load('star_2.png')
        self.UI_star = pg.transform.scale(self.star, (50, 50))

        self.difficulty_easy = pg.Rect(160, 40, 80, 30)
        self.difficulty_mid = pg.Rect(255, 40, 80, 30)
        self.difficulty_hard = pg.Rect(350, 40, 80, 30)

        self.difficulty = 0.3
        
        self.backspace = pg.image.load('backspace_3.png')
        self.backspace = pg.transform.scale(self.backspace, (50 * 2.5, 50))
        self.backspace_rect = self.backspace.get_rect(topleft=(self.width - 150, 40))
        
        self.new_round_text = self.text("Ny runde", size=40, color="white")

    def text(self, text, size = None, color = "black"):
        # Size kan ikke sættes til størrelsen som parameter, da game endnu ikke er dannet.
        # Derfor sættes den i selve funktionen til en default værdi.
        if size == None:
            size = int(game.grid.n_w / 1.5)
        self.font = pg.font.Font(None, int(size))
        return self.font.render(f"{text}", True, pg.Color(color))
    
    def draw_UI(self):
        
        self.screen.blit(self.UI_star, (20, 25))
        
        self.score_text = self.text(f"{game.player.score}/{game.player.total_guesses}", size=60, color="white")
        self.screen.blit(self.score_text, (80, 35))

        pg.draw.rect(self.screen, (80, 200, 80), self.difficulty_easy)
        pg.draw.rect(self.screen, (200, 200, 80), self.difficulty_mid)
        pg.draw.rect(self.screen, (200, 80, 80), self.difficulty_hard)

        easy_text = self.text("0.1", size=20, color="black")
        mid_text = self.text("0.3", size=20, color="black")
        hard_text = self.text("0.5", size=20, color="black")

        self.screen.blit(easy_text, easy_text.get_rect(center=self.difficulty_easy.center))
        self.screen.blit(mid_text, mid_text.get_rect(center=self.difficulty_mid.center))
        self.screen.blit(hard_text, hard_text.get_rect(center=self.difficulty_hard.center))

        self.screen.blit(self.backspace, self.backspace_rect)
        
        self.screen.blit(self.new_round_text, (450, 10))


class Player:
    def __init__(self):
        self.score = 0
        self.total_guesses = 0

    def choose_path(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for n in game.grid.nodes:
                if n.rect.collidepoint(event.pos) and n.state == "open":
                    if not n.chosen:
                        self.total_guesses += 1
                        game.grid.make_stars(n, 1)
                    n.chosen = True

        if event.type == pg.MOUSEMOTION and event.buttons[0]:
            for n in game.grid.nodes:
                if n.rect.collidepoint(event.pos) and n.state == "open":
                    if not n.chosen:
                        self.total_guesses += 1
                        game.grid.make_stars(n, 1)
                    n.chosen = True

class Grid:
    def __init__(self, x, y, num_nodes, obstacle_chance):
        self.x = x
        self.y = y
        self.num_nodes = num_nodes
        self.n_w = (game.display.width / self.num_nodes ** 0.5) * 0.8
        self.n_h = (game.display.width / self.num_nodes ** 0.5) * 0.8
        self.spacing = (game.display.width / self.num_nodes ** 0.5) * 0.19
        self.size = int(self.num_nodes ** 0.5)
        self.nodes = []
        self.obstacle_chance = obstacle_chance

        self.make_grid(self.obstacle_chance)

    def make_grid(self, o_c):
        self.nodes.clear()

        for i in range(self.num_nodes):
            n_x = self.x + self.spacing + (self.n_w + self.spacing) * (i % self.size)
            n_y = self.y + self.spacing + (self.n_h + self.spacing) * (i // self.size)

            node = Node(n_x, n_y, self.n_w, self.n_h)

            if random.random() <= o_c - abs((len(self.nodes) - self.num_nodes / 2) / self.num_nodes):
                node.state = "obstacle"

            self.nodes.append(node)

    def make_start_and_goal(self):
        start_i = random.randint(int(self.num_nodes - self.num_nodes ** 0.5 * 3 - 1), self.num_nodes - 1)
        self.nodes[start_i].state = "start"
        self.nodes[start_i].text = game.display.text("A", 30)

        goal_i = random.randint(0, int(self.num_nodes ** 0.5 * 3 - 1))
        self.nodes[goal_i].state = "goal"
        self.nodes[goal_i].text = game.display.text("B", 30)

    def make_stars(self, node, star_amount):
        for _ in range(star_amount):
            scale = int(self.n_w / 1.5)
            r_x = random.randint(int(node.x), int(node.x + node.w / 3))
            r_y = random.randint(int(node.y), int(node.y + node.h / 3))
            node_star = pg.transform.scale(game.display.star, (scale, scale))
            game.display.stars.append((node_star, (r_x, r_y)))
               
class Node:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.Rect(x, y, w, h)

        self.state = "open" # open, obstacle, start, goal, closed, path
        self.chosen = False

        self.text = ""
        self.parent = None

        self.g_cost = None
        self.h_cost = 0
        self.f_cost = None

    def draw(self):
        if self.state == "obstacle":
            self.color = pg.Color("dimgrey")
        elif self.state == "start":
            self.color = pg.Color("green")
        elif self.state == "goal":
            self.color = pg.Color("red")
        elif self.state == "path":
            self.color = pg.Color("darkgoldenrod1") if self.chosen else pg.Color("darkgoldenrod3")
        else:
            self.color = pg.Color("white")
        
        pg.draw.rect(game.display.screen, self.color, self.rect)

        if self.text:
            text_rect = self.text.get_rect(center=self.rect.center)
            game.display.screen.blit(self.text, text_rect)

    # Til debugging
    def mouse(self, event):
        return # Fjern for debugging
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if event.button == 2 and self.state not in ("start", "goal"):
                self.state = "obstacle"

            if event.button == 3:
                for n in game.grid.nodes:
                    if n.state == "goal":
                        n.state = "open" if n.state != "obstacle" else "obstacle"
                        n.text = ""
                        break

                if self.state != "start":
                    self.state = "goal"
    

if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run() # Udkommentér denne for benchmark
    #benchmark(game)