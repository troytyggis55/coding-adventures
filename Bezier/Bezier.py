import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set the window size
w = 1200
h = 700
window_size = (w, h)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the window title
pygame.display.set_caption("Bezier")


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 8

    def pos(self):
        return self.x, self.y

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size, 2)


class Line:
    def __init__(self, node1, node2):
        self.Node1 = node1
        self.Node2 = node2

    def lerp(self, t):
        return Node(self.Node1.x + (self.Node2.x - self.Node1.x) * t, self.Node1.y + (self.Node2.y - self.Node1.y) * t)

    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), (self.Node1.x, self.Node1.y), (self.Node2.x, self.Node2.y), 3)


def recursive_lerp(nodelist, t):
    newNodes = []

    if len(nodelist) > 2:
        for i in range(len(nodelist) - 1):
            newNodes.append(Line(nodelist[i], nodelist[i + 1]).lerp(t))
            Line(nodelist[i], nodelist[i + 1]).draw()
            newNodes[i].draw()

        recursive_lerp(newNodes, t)

    elif len(nodelist) == 2:
        bezierNode = Line(nodelist[0], nodelist[1]).lerp(t)
        bezierNode.draw()
        Line(nodelist[0], nodelist[1]).draw()
        if bezierNode.pos() not in bezPoint:
            bezPoint.append(
                (bezierNode.pos(), (colx(bezierNode.pos()), coly(bezierNode.pos()), colxy(bezierNode.pos()))))


def colx(pos):
    return pos[0] / w * 255


def coly(pos):
    return pos[1] / h * 255


def colxy(pos):
    return (1 - abs((pos[0] / w) - (pos[1] / h))) * 255


def draw_text(text, font, color, pos):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)


NodeList = []
LineList = []
bezPoint = []

lerpVal = 0
mouseHold = False
mouseReleased = False
startTime = 0
# Run the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif pygame.mouse.get_pressed()[0]:
            mouseHold = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            startTime = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP and pygame.time.get_ticks() - startTime < 300:
            mouseReleased = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and lerpVal > 0:
        lerpVal -= 0.001
    elif keys[pygame.K_RIGHT] and lerpVal < 1:
        lerpVal += 0.001
    elif keys[pygame.K_DELETE]:
        NodeList = []
        LineList = []
        bezPoint = []
    elif keys[pygame.K_BACKSPACE]:
        bezPoint = []

    # Update game state
    lastListState = len(NodeList)

    # Add a node when the mouse is released
    if mouseReleased:
        # Handle Nodes
        if len(NodeList) == 0:
            NodeList.append(Node(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        else:
            delete = False
            for tempNode in NodeList:
                if (tempNode.x - tempNode.size < pygame.mouse.get_pos()[0] < tempNode.x + tempNode.size
                        and tempNode.y - tempNode.size < pygame.mouse.get_pos()[1] < tempNode.y + tempNode.size):
                    NodeList.remove(tempNode)
                    break
            else:
                NodeList.append(Node(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

        mouseReleased = False

    if mouseHold:
        # Handle Nodes
        for tempNode in NodeList:
            if (tempNode.x - tempNode.size < pygame.mouse.get_pos()[0] < tempNode.x + tempNode.size
                    and tempNode.y - tempNode.size < pygame.mouse.get_pos()[1] < tempNode.y + tempNode.size):
                tempNode.x = pygame.mouse.get_pos()[0]
                tempNode.y = pygame.mouse.get_pos()[1]
                break

        mouseHold = False

    if len(NodeList) != lastListState:
        # Handle Bezier Curve
        bezPoint = []

    # Handle Lines
    LineList = []
    for i in range(len(NodeList) - 1):
        LineList.append(Line(NodeList[i], NodeList[i + 1]))

    # Draw the screen
    screen.fill((0, 0, 0))  # Clear the screen

    for i in range(len(NodeList)):
        NodeList[i].draw()

    for i in range(len(LineList)):
        LineList[i].draw()

    if len(NodeList) > 1:
        recursive_lerp(NodeList, lerpVal)

    for i in range(len(bezPoint)):
        pygame.draw.circle(screen, bezPoint[i][1], bezPoint[i][0], 4)

    draw_text("Click to place node. Click a node to delete or hold the node to move it. L and R arrows to change the lerpval", pygame.font.Font(None, 25), (255, 255, 255), (10, 10))
    draw_text(f"Lerpvalue: {abs(round(lerpVal, 2))}", pygame.font.Font(None, 25), (255, 255, 255), (10, 40))

    pygame.display.flip()  # Update the screen

# Shut down Pygame
pygame.quit()
