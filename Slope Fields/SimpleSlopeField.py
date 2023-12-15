import pygame

pygame.init()

w, h = 800, 600
step = 10

screen = pygame.display.set_mode((w, h))

pygame.display.set_caption("Slope Field")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((0, 0, 0))

    #Make new color and modify it with hsva
    tempColor = pygame.Color(255, 255, 255)

    for i in range(int(step / 2), w, step):
        for j in range(int(step / 2), h, step):
            tempVector = pygame.math.Vector2(pygame.mouse.get_pos()[0] - i, pygame.mouse.get_pos()[1] - j)
            if tempVector.length() > 0:
                tempColor.hsva = (tempVector.angle_to(pygame.Vector2(-1, 0)), 100, 100 - (100 * tempVector.length_squared()/(w**2 + h**2)), 100)
                tempVector = tempVector.normalize() * step/2
            pygame.draw.aaline(screen, tempColor, (i, j), (i + tempVector.x, j + tempVector.y), 1)

    pygame.display.update()