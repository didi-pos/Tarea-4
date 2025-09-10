import pygame
import random
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Disparos")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (200, 50, 50)
LIGHT_RED = (255, 150, 150)
BLUE = (50, 100, 220)
LIGHT_BLUE = (100, 150, 255)
BLACK = (0, 0, 0)
BACKGROUND = (15, 20, 40)

player_size = 50
player_x = 400
player_y = 500
player_speed = 7

bullets = []
bullet_speed = 7

enemies = []
enemy_size = 40
enemy_speed = 2
enemy_spawn_rate = 45

score = 0
lives = 3
level = 1
max_level_reached = 1

font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_player(x, y):
    points = [(x + player_size//2, y),
              (x, y + player_size),
              (x + player_size, y + player_size)]
    pygame.draw.polygon(screen, BLUE, points)
    pygame.draw.polygon(screen, LIGHT_BLUE, points, 3)
    pygame.draw.rect(screen, LIGHT_BLUE, (x + player_size//2 - 5, y + 20, 10, 15))

def draw_enemy(x, y):
    pygame.draw.circle(screen, RED, (x + enemy_size//2, y + enemy_size//2), enemy_size//2)
    pygame.draw.circle(screen, LIGHT_RED, (x + enemy_size//2, y + enemy_size//2), enemy_size//3)

def draw_bullet(x, y):
    pygame.draw.rect(screen, (255, 215, 0), (x, y, 6, 12), border_radius=3)

def draw_game_info():
    pygame.draw.rect(screen, (30, 30, 30), (0, 0, 800, 40))
    pygame.draw.line(screen, LIGHT_BLUE, (0, 40), (800, 40), 2)
    draw_text(f"Puntos: {score}", font, WHITE, 100, 20)
    draw_text(f"Nivel: {level}", font, WHITE, 250, 20)
    draw_text(f"Vidas: {lives}", font, WHITE, 400, 20)

def increase_difficulty():
    global enemy_speed, enemy_spawn_rate, level, max_level_reached, player_speed
    if score >= 100 and level == 1:
        level = 2
        enemy_speed = 3
        enemy_spawn_rate = 35
        player_speed += 1
    elif score >= 300 and level == 2:
        level = 3
        enemy_speed = 4
        enemy_spawn_rate = 25
        player_speed += 1
    max_level_reached = max(max_level_reached, level)

running = True
while running:
    screen.fill(BACKGROUND)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + player_size//2 - 2, player_y])
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x += player_speed
        
    increase_difficulty()
    
    if random.randint(1, enemy_spawn_rate) == 1:
        enemies.append([random.randint(0, 800 - enemy_size), 0])
        
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > 600:
            enemies.remove(enemy)
            lives -= 1
            if lives <= 0:
                running = False
        else:
            draw_enemy(enemy[0], enemy[1])
            
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            draw_bullet(bullet[0], bullet[1])
            
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (bullet[0] < enemy[0] + enemy_size and
                bullet[0] + 5 > enemy[0] and
                bullet[1] < enemy[1] + enemy_size and
                bullet[1] + 10 > enemy[1]):
                if bullet in bullets: bullets.remove(bullet)
                if enemy in enemies: enemies.remove(enemy)
                score += 10
                    
    draw_player(player_x, player_y)
    draw_game_info()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
