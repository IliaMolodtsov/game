import pygame

pygame.init()
screen = pygame.display.set_mode((1099, 669))
pygame.display.set_caption("proga")
icon = pygame.image.load('images/Ghost-64.webp')
pygame.display.set_icon(icon)


bg = pygame.image.load('images/bg5.png')

bg_x = 0

running = True
while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1099, 0))

    bg_x -= 1
    if bg_x == -1099:
        bg_x = 0

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()



