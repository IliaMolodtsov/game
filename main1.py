import pygame

pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("proga")
icon = pygame.image.load('images/Ghost-64.webp')
pygame.display.set_icon(icon)

square = pygame.Surface((50, 170))
square.fill('Red')

myfont = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
text_surface = myfont.render('proga fy', True, 'Green')

player = pygame.image.load('images/Ghost-64.webp')

running = True
while running:

    pygame.draw.circle(screen, 'Blue', (25, 15), 5)
    screen.blit(square, (10, 0))
    screen.blit(text_surface, (300, 100))
    screen.blit(player, (500, 200))


    # screen.fill((41, 219, 215))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()



