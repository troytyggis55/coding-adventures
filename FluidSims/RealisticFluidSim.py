import pygame
import random

visualize_grid = True
visualize_repelling_force = False

# Physics constants
search_radius = 50  # How far a Node can see, should be a multiple of the screen width and height,
max_node_speed = 10  # Node speed limit
repelling_force = 0.015  # How strong Nodes repel each other
gravity = 0.08
friction = 0.985  # "Air resistance", the lower the value, the more friction

# Screen dimensions
w = 1000
h = 600


class Node:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.neighbour_nodes = []
        self.grid_pos = (int(self.pos.x // search_radius), int(self.pos.y // search_radius))

    def update(self):
        # Wall force
        if self.pos.x < search_radius:
            self.velocity.x += search_radius / self.pos.x
        elif self.pos.x > screen_width - search_radius:
            self.velocity.x -= search_radius / (screen_width - self.pos.x)

        if self.pos.y < search_radius:
            self.velocity.y += search_radius / self.pos.y
        elif self.pos.y > screen_height - search_radius:
            self.velocity.y -= search_radius / (screen_height - self.pos.y)

        # Limit speed
        if self.velocity.magnitude() > max_node_speed:
            self.velocity.scale_to_length(max_node_speed)

        # Add all nodes in the surruonding grid cells to the neighbour_nodes list
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= self.grid_pos[0] + i < len(grid) and 0 <= self.grid_pos[1] + j < len(grid[0]):
                    for node in grid[self.grid_pos[0] + i][self.grid_pos[1] + j]:
                        if node != self:
                            self.neighbour_nodes.append(node)

        # Search for nearby nodes and update accordingly
        for node in self.neighbour_nodes:
            distance = node.pos.distance_to(self.pos)
            if search_radius > distance > 0:
                self.velocity += (self.pos - node.pos).normalize() * (search_radius - distance) * repelling_force
        self.neighbour_nodes = []

        # Update position
        self.velocity.y += gravity
        self.velocity *= friction
        self.pos += self.velocity

        # Wall boundaries
        if self.pos.x <= 0:
            self.pos.x = 1
        elif self.pos.x >= screen_width:
            self.pos.x = screen_width - 1

        if self.pos.y <= 0:
            self.pos.y = 1
        elif self.pos.y >= screen_height:
            self.pos.y = screen_height - 1

        # Update grid position
        self.grid_pos = (int(self.pos.x // search_radius), int(self.pos.y // search_radius))

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), 2)
        if visualize_repelling_force:
            for node in self.neighbour_nodes:
                pygame.draw.line(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)),
                                 (int(node.pos.x), int(node.pos.y)))

# Draw grid lines where nodes are chunked together
def draw_grid():
    for i in range(0, screen_width, search_radius):
        pygame.draw.line(screen, (100, 100, 100), (i, 0), (i, screen_height))
    for i in range(0, screen_height, search_radius):
        pygame.draw.line(screen, (100, 100, 100), (0, i), (screen_width, i))


# Brighten each grid cell based on how many nodes are in it
def draw_grid_activity():
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if len(grid[i][j]) > 0:
                brightness = min(255, len(grid[i][j]) * 10)
                pygame.draw.rect(screen, (brightness, brightness, brightness),
                                 (i * search_radius, j * search_radius, search_radius, search_radius))


def draw_text(screen, text, font, color, pos):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)


# Initialize Pygame
pygame.init()

# Set up the display
screen_width = (w % search_radius) + w
screen_height = (h % search_radius) + h

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("'Realistic' Fluid Sim")

# Set up the game loop
clock = pygame.time.Clock()
running = True

# Init grid
nodes = []
for i in range(10):
    nodes.append(Node(random.randint(0, screen_width - 1), random.randint(0, screen_height - 1)))

grid = [[[] for j in range(screen_height // search_radius)] for i in range(screen_width // search_radius)]


# Chuncking
def place_nodes_in_grid(nodes):
    for row in grid:
        for cell in row:
            cell.clear()

    for node in nodes:
        node.grid_pos = node.grid_pos
        grid[node.grid_pos[0]][node.grid_pos[1]].append(node)


# Game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            visualize_grid = not visualize_grid

    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        nodes.append(Node(pos[0], pos[1]))

    if pygame.mouse.get_pressed()[2] and len(nodes) > 0:
        nodes.remove(nodes[0])

    # Draw to the screen
    s = pygame.Surface((screen_width, screen_height))  # the size of your rect

    # Update chunks
    place_nodes_in_grid(nodes)

    if visualize_grid:
        draw_grid_activity()
        draw_grid()

    for node in nodes:
        node.update()
        node.draw(screen)

    # Draw particle counter
    font = pygame.font.Font(None, 30)
    draw_text(screen, f"Particles: {len(nodes)}", font, (255, 255, 255), (10, 10))

    # Draw fps counter
    fps = str(int(clock.get_fps()))
    draw_text(screen, fps, font, (255, 255, 255), (screen_width - 30, 10))

    font = pygame.font.Font(None, 25)
    draw_text(screen, "Left click addd particles, right click deleted. Space toggles grid", font, (255, 255, 255), (5, screen_height - 20))

    # Update the display
    pygame.display.flip()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
