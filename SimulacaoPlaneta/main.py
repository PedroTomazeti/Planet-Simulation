from sre_constants import BRANCH
from turtle import distance
import pygame
import math
pygame.init()

WIDHT, HEIGHT = 900, 900 # Proporção da janela
WIN = pygame.display.set_mode((WIDHT, HEIGHT)) # Definição da variável que receberá a Janela
pygame.display.set_caption("Simulação de órbitas")

PRETO = (0, 0, 0) # Background branco
BRANCO = (255, 255, 255)
# Criação das cores para o sol e planetas
AMARELO = (255, 255, 0)
AZUL = (0, 191, 255)
VERMELHO = (220, 20, 60)
CINZA = (105, 105, 105)
LARANJA = (255, 140, 0)

# Fonte para ser utilizado em algo escrito na aplicação
FONTE = pygame.font.SysFont("helvetica", 16)

class Planeta:
    AU = 149.6e6 * 1000 # Distância da terra para o sol
    G = 6.67428e-11
    SCALE = 250 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # 1 dia

    def __init__(self ,x ,y , raio, cor, massa):
        # Distâncias dos planetas em relação ao sol
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.massa = massa

        self.orbit = [] # Valores das distâncias registradas
        self.sun = False # Não vai desenhar a órbita do sol (obviamente)
        self.distance_to_sun = 0

        self.x_vel = 0 # Velocidade do eixo x
        self.y_vel = 0 # Velocidade do eixo y
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDHT / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Pegará os pontos registrados das órbitas dos planetas
        # E desenhará uma linha representando-a, com suas escalas corretas
        # Fazendo a sua constante atualização para ter também impressão de movimento
        # Só começará a desenhar depois que registrar mais de 2 posições de órbita
        if len(self.orbit) > 2:
            updated_pontos = []
            for pontos in self.orbit:
                x,y = pontos
                x = x * self.SCALE + WIDHT / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_pontos.append((x, y))
        
            pygame.draw.lines(win, self.cor, False, updated_pontos, 2)
        # Desenha o planeta
        pygame.draw.circle(win, self.cor, (x, y), self.raio)
        # Escreve a distância entre o planeta e o sol
        if not self.sun:
            distancia_texto = FONTE.render(f"{round(self.distance_to_sun/1000)}km", 1, BRANCO)
            win.blit(distancia_texto, (x - distancia_texto.get_width()/2, y - distancia_texto.get_height()/2))

    def attraction(self, other):
        # Cálculo da distancia entre um planeta e outro
        other_x, other_y = other.x, other.y
        distancia_x = other_x - self.x
        distancia_y = other_y - self.y
        # Para evitar valores negativos
        distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)
        # Caso o "other" seja o sol
        if other.sun:
            self.distance_to_sun =  distancia
        # Necessário quebrar essa força em duas para X e Y
        forca = self.G * self.massa * other.massa / distancia**2
        # Dará o ângulo associado ao cálculo
        theta = math.atan2(distancia_y, distancia_x)
        # A força está associada ao lado do triângulo retângulo que ele está cos = adjacente, sen = oposto
        forca_x = math.cos(theta) * forca
        forca_y = math.sin(theta) * forca
        return forca_x, forca_y

    def update_position(self, planetas):
        # Todas as forças começam em 0
        total_fx = total_fy = 0
        # Análise da lista de planetas
        for planeta in planetas:
            # Caso seja planetas iguais não irá fazer o cálculo
            if self == planeta:
                continue
            # Atualização dos valores da atração entre planetas
            fx, fy = self.attraction(planeta)
            total_fx += fx
            total_fy += fy
        # Cálculo da velocidade do planeta no eixo X e Y(F = m * a, a = m / F)
        self.x_vel += total_fx / self.massa * self.TIMESTEP
        self.y_vel += total_fy / self.massa * self.TIMESTEP
        # Atualização da posição
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        

def main():
    run = True
    clock = pygame.time.Clock()

    sol = Planeta(0, 0, 30, AMARELO, 1.98892 * 10 **30)
    sol.sun = True
    
    # Criação dos planetas
    # (Distância para o sol(eixo x), posição eixo Y, raio, cor, massa)
    # Será colocada uma velocidade no eixo Y para se ter o movimento ao redor do sol
    # Unidade é metros por segundo (m/s)
    terra = Planeta(-1 * Planeta.AU, 0, 16, AZUL, 5.9742 * 10**24)
    terra.y_vel = 29.783 * 1000

    marte = Planeta(-1.524 * Planeta.AU, 0, 12, VERMELHO, 6.39 * 10**23)
    marte.y_vel = 24.077 * 1000

    mercurio = Planeta(-0.387 * Planeta.AU, 0, 8, CINZA, 3.285 * 10**23)
    mercurio.y_vel = 47.4 * 1000

    venus = Planeta(-0.723 * Planeta.AU, 0, 16, LARANJA, 4.8685 * 10**24)
    venus.y_vel = 35.02 * 1000

    planetas = [sol, terra, marte, mercurio, venus]

    while run:
        clock.tick(60) # Atualização de FPS
        WIN.fill(PRETO)
        # Analisa todas as ações feitas por exemplo: apertar alguma tecla
        for event in pygame.event.get(): 
            # Caso seja no botão de fechar a janela, fechará a aplicação
            if event.type == pygame.QUIT: 
                run = False
        # Passa o parâmetro da lista dos planetas para as funções
        for planeta in planetas:
            planeta.update_position(planetas)
            planeta.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()
