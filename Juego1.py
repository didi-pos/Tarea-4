import pygame
import random
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Evasión Mejorado")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (65, 105, 225)
BLACK = (0, 0, 0)
DARK_BLUE = (25, 25, 112)
LIGHT_BLUE = (173, 216, 230)

player_size = 50
player_x = 400
player_y = 500
player_speed = 5
score = 0
lives = 3

enemies = []
enemy_size = 30
enemy_speed = 3
enemy_spawn_rate = 20
game_time = 0

max_speed_reached = 3.0
final_score = 0

font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size), border_radius=10)
    pygame.draw.rect(screen, LIGHT_BLUE, (x + 5, y + 5, player_size - 10, player_size - 10), border_radius=5)
    pygame.draw.circle(screen, WHITE, (x + 15, y + 15), 5)
    pygame.draw.circle(screen, WHITE, (x + 35, y + 15), 5)
    pygame.draw.arc(screen, WHITE, (x + 10, y + 25, 30, 15), 0, 3.14, 2)

def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_size, enemy_size), border_radius=8)
    pygame.draw.rect(screen, (255, 150, 150), (x + 5, y + 5, enemy_size - 10, enemy_size - 10), border_radius=4)
    pygame.draw.line(screen, BLACK, (x + 5, y + 5), (x + enemy_size - 5, y + enemy_size - 5), 2)
    pygame.draw.line(screen, BLACK, (x + enemy_size - 5, y + 5), (x + 5, y + enemy_size - 5), 2)

def draw_game_info():
    pygame.draw.rect(screen, (240, 240, 240), (0, 0, 800, 50))
    pygame.draw.line(screen, BLACK, (0, 50), (800, 50), 2)
    draw_text(f"Puntos: {score}", font, DARK_BLUE, 100, 25)
    draw_text(f"Vidas: {lives}", font, DARK_BLUE, 250, 25)
    draw_text(f"Velocidad: {enemy_speed:.1f}", font, DARK_BLUE, 450, 25)
    
    for i in range(lives):
        pygame.draw.polygon(screen, RED, [
            (600 + i * 30, 25),
            (610 + i * 30, 15),
            (620 + i * 30, 25),
            (610 + i * 30, 35)
        ])

def increase_difficulty():
    global enemy_speed, enemy_spawn_rate, game_time, max_speed_reached
    game_time += 1
    
    if game_time % 300 == 0:
        enemy_speed += 0.5
        max_speed_reached = enemy_speed
        
    if game_time % 600 == 0 and enemy_spawn_rate > 5:
        enemy_spawn_rate -= 1

def show_game_over():
    global final_score
    screen.fill(WHITE)
    draw_text("GAME OVER", big_font, RED, 400, 150)
    draw_text(f"Puntuación final: {final_score}", font, BLACK, 400, 220)
    draw_text(f"Velocidad máxima alcanzada: {max_speed_reached:.1f}", font, BLACK, 400, 260)
    draw_text("Presiona cualquier tecla para jugar de nuevo", font, BLACK, 400, 350)
    pygame.display.update()
    
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
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
            score += 1
        else:
            draw_enemy(enemy[0], enemy[1])
            
        if (player_x < enemy[0] + enemy_size and
            player_x + player_size > enemy[0] and
            player_y < enemy[1] + enemy_size and
            player_y + player_size > enemy[1]):
            enemies.remove(enemy)
            lives -= 1
            if lives <= 0:
                final_score = score
                show_game_over()
                player_x = 400
                player_y = 500
                enemies = []
                score = 0
                lives = 3
                enemy_speed = 3
                enemy_spawn_rate = 20
                game_time = 0
                max_speed_reached = 3.0
    
    draw_player(player_x, player_y)
    draw_game_info()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
