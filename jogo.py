import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Monstro")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Carregamento de imagens (substitua pelos caminhos das imagens)
player_img = pygame.Surface((40, 40))
player_img.fill((0, 0, 255))

monster_img = pygame.Surface((60, 60))
monster_img.fill((255, 0, 0))

power_img = pygame.Surface((10, 10))
power_img.fill((255, 255, 0))

platform_img = pygame.Surface((100, 10))
platform_img.fill((0, 255, 0))

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 50
        self.speed_x = 0
        self.speed_y = 0
        self.on_ground = False
        self.balls = 0

    def update(self):
        self.speed_y += 0.3  # Gravidade
        keys = pygame.key.get_pressed()
        self.speed_x = 0
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.speed_y = -12

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0
            self.on_ground = True

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = monster_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - 60
        self.speed_x = 1
        self.health = 10
        self.shoot_timer = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH or self.rect.left < WIDTH // 2:
            self.speed_x *= -1
        self.shoot_timer += 1
        if self.shoot_timer > 100:
            power = Power(self.rect.centerx, self.rect.centery, -5)
            monster_powers.add(power)
            all_sprites.add(power)
            self.shoot_timer = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platform_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x):
        super().__init__()
        self.image = power_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

# Grupos
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
balls = pygame.sprite.Group()
monster_powers = pygame.sprite.Group()
player_powers = pygame.sprite.Group()

player = Player()
monster = Monster()
platform = Platform(WIDTH//2 - 50, HEIGHT//2)

all_sprites.add(player, monster)
platforms.add(platform)
all_sprites.add(platform)

# Loop principal
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and player.balls > 0:
                power = Power(player.rect.centerx, player.rect.centery, 7)
                player_powers.add(power)
                all_sprites.add(power)
                player.balls -= 1

    # Spawn aleatório de bolas
    if random.randint(1, 100) == 1:
        ball = Ball(random.randint(0, WIDTH-15), random.randint(0, HEIGHT//2))
        balls.add(ball)
        all_sprites.add(ball)

    # Atualização
    all_sprites.update()

    # Verificação de colisão com plataforma
    if pygame.sprite.spritecollide(player, platforms, False):
        if player.speed_y > 0:
            player.rect.bottom = platform.rect.top
            player.speed_y = 0
            player.on_ground = True

    # Coleta de bolas
    hits = pygame.sprite.spritecollide(player, balls, True)
    for hit in hits:
        player.balls += 1

    # Player atinge monstro
    hits = pygame.sprite.spritecollide(monster, player_powers, True)
    for hit in hits:
        monster.health -= 1
        if monster.health <= 0:
            print("Você venceu!")
            running = False

    # Monstro atinge player
    hits = pygame.sprite.spritecollide(player, monster_powers, True)
    if hits:
        print("Você perdeu!")
        running = False

    # Player colide com monstro
    if pygame.sprite.collide_rect(player, monster):
        print("Você perdeu!")
        running = False

    # Renderização
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.draw.rect(screen, RED, (10, 10, monster.health * 20, 20))
    pygame.display.flip()

pygame.quit()
sys.exit()
