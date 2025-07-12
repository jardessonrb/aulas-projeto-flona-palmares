import pygame
import sys
import random

# Inicializa o pygame
pygame.init()

# Tamanho da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo com Pontuação')

# Cores
branco = (255, 255, 255)
azul = (0, 0, 255)
vermelho = (255, 0, 0)
preto = (0, 0, 0)

# Fonte para o placar
fonte = pygame.font.SysFont('Arial', 30)

# Configuração do jogador
jogador_pos = [largura // 2, altura // 2]
jogador_tamanho = 50
velocidade = 5

# Configuração do ponto aleatório
ponto_tamanho = 10
ponto_pos = [random.randint(0, largura - ponto_tamanho), random.randint(0, altura - ponto_tamanho)]

# Pontuação
placar = 0

# ===================== FUNÇÕES DE MOVIMENTO =====================
def pra_cima():
    jogador_pos[1] -= velocidade
    if jogador_pos[1] < 0:
        jogador_pos[1] = 0

def pra_baixo():
    jogador_pos[1] += velocidade
    if jogador_pos[1] > altura - jogador_tamanho:
        jogador_pos[1] = altura - jogador_tamanho

def pra_esquerda():
    jogador_pos[0] -= velocidade
    if jogador_pos[0] < 0:
        jogador_pos[0] = 0

def pra_direita():
    jogador_pos[0] += velocidade
    if jogador_pos[0] > largura - jogador_tamanho:
        jogador_pos[0] = largura - jogador_tamanho

# ===================== FUNÇÃO PRINCIPAL DE CONTROLE =====================
def jogar(letra):
    pass

# ===================== FUNÇÃO PARA VERIFICAR COLISÃO =====================
def verificar_colisao():
    jogador_rect = pygame.Rect(jogador_pos[0], jogador_pos[1], jogador_tamanho, jogador_tamanho)
    ponto_rect = pygame.Rect(ponto_pos[0], ponto_pos[1], ponto_tamanho, ponto_tamanho)
    return jogador_rect.colliderect(ponto_rect)

# ===================== LOOP PRINCIPAL =====================
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Teclas pressionadas
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_w]:
        jogar('w')
    if teclas[pygame.K_s]:
        jogar('s')
    if teclas[pygame.K_a]:
        jogar('a')
    if teclas[pygame.K_d]:
        jogar('d')

    # Verificar colisão
    if verificar_colisao():
        placar += 1
        ponto_pos = [
            random.randint(0, largura - ponto_tamanho),
            random.randint(0, altura - ponto_tamanho)
        ]

    # Preenche a tela com branco
    tela.fill(branco)

    # Desenha o ponto aleatório (vermelho)
    pygame.draw.circle(tela, vermelho, (ponto_pos[0], ponto_pos[1]), ponto_tamanho)

    # Desenha o jogador (um quadrado azul)
    pygame.draw.rect(tela, azul, (jogador_pos[0], jogador_pos[1], jogador_tamanho, jogador_tamanho))

    # Desenha o placar
    texto_placar = fonte.render(f'Placar: {placar}', True, preto)
    tela.blit(texto_placar, (10, 10))

    # Atualiza a tela
    pygame.display.flip()

    # Controla o FPS (frames por segundo)
    pygame.time.Clock().tick(60)
