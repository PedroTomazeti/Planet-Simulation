import pygame
import math
pygame.init()

WIDHT,HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Simulação de órbitas")

WHITE = (255, 255, 255)

class Planet:
    def __init__(self, x, y, raio, cor, massa):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.massa = massa

        self.x_vel = 0
        self.y_vel = 0
        



def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WIN.fill(WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    pygame.quit()

main()
