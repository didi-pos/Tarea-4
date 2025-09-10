import pygame
import random
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Recolección Mejorado")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 215, 0)
BLUE = (65, 105, 225)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BACKGROUND = (240, 248, 255)

player_size = 40
player_x = 400
player_y = 300
player_speed = 5

items = []
obstacles = []
item_size = 20
obstacle_size = 25
item_spawn_rate = 30
obstacle_spawn_rate = 60
game_time = 0

score = 0
lives = 3
level = 1
max_level_reached = 1
final_score = 0

font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_player(x, y):
    pygame.draw.circle(screen, GREEN, (x + player_size//2, y + player_size//2), player_size//2)
    pygame.draw.circle(screen, (0, 150, 0), (x + player_size//2, y + player_size//2), player_size//2 - 4, 2)
    pygame.draw.circle(screen, WHITE, (x + player_size//2 - 8, y + player_size//2 - 8), 5)
    pygame.draw.circle(screen, WHITE, (x + player_size//2 + 8, y + player_size//2 - 8), 5)
    pygame.draw.arc(screen, BLACK, (x + player_size//2 - 10, y + player_size//2, 20, 10), 0, 3.14, 2)

def draw_item(x, y, color):
    pygame.draw.rect(screen, color, (x, y, item_size, item_size), border_radius=5)
    pygame.draw.rect(screen, (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255)), 
                    (x + 4, y + 4, item_size - 8, item_size - 8), border_radius=3)

def draw_obstacle(x, y):
    pygame.draw.rect(screen, RED, (x, y, obstacle_size, obstacle_size), border_radius=8)
    pygame.draw.rect(screen, (255, 150, 150), (x + 5, y + 5, obstacle_size - 10, obstacle_size - 10), border_radius=4)
    pygame.draw.line(screen, BLACK, (x + 5, y + 5), (x + obstacle_size - 5, y + obstacle_size - 5), 2)
    pygame.draw.line(screen, BLACK, (x + obstacle_size - 5, y + 5), (x + 5, y + obstacle_size - 5), 2)

def draw_game_info():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, 800, 40))
    pygame.draw.line(screen, BLACK, (0, 40), (800, 40), 2)
    draw_text(f"Puntos: {score}", font, BLUE, 100, 20)
    draw_text(f"Nivel: {level}", font, BLUE, 250, 20)
    draw_text(f"Vidas: {lives}", font, BLUE, 400, 20)
    
    for i in range(4):  # 4 niveles máximo
        color = GREEN if i < level else (200, 200, 200)
        pygame.draw.rect(screen, color, (550 + i * 40, 15, 30, 10), border_radius=3)

def increase_difficulty():
    global player_speed, item_spawn_rate, obstacle_spawn_rate, game_time, level, max_level_reached
    
    game_time += 1
    
    if game_time % 450 == 0 and level < 4:
        level += 1
        max_level_reached = level
        player_speed += 1
        
    if game_time % 300 == 0 and item_spawn_rate > 10:
        item_spawn_rate -= 2
        
    if game_time % 400 == 0 and obstacle_spawn_rate > 30:
        obstacle_spawn_rate -= 3

def show_game_over():
    global final_score
    screen.fill(BACKGROUND)
    draw_text("¡GAME OVER!", big_font, RED, 400, 150)
    draw_text(f"Puntuación final: {final_score}", font, BLUE, 400, 220)
    draw_text(f"Nivel máximo alcanzado: {max_level_reached}", font, BLUE, 400, 260)
    draw_text("Presiona ENTER para jugar de nuevo", font, BLACK, 400, 350)
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
    screen.fill(BACKGROUND)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 40:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < 600 - player_size:
        player_y += player_speed
        
    increase_difficulty()
        
    if random.randint(1, item_spawn_rate) == 1:
        item_color = (random.randint(150, 255), random.randint(150, 255), random.randint(0, 100))
        items.append([random.randint(0, 800 - item_size), random.randint(40, 600 - item_size), item_color])
        
    if random.randint(1, obstacle_spawn_rate) == 1:
        obstacles.append([random.randint(0, 800 - obstacle_size), random.randint(40, 600 - obstacle_size)])
        
    for item in items[:]:
        if (player_x < item[0] + item_size and
            player_x + player_size > item[0] and
            player_y < item[1] + item_size and
            player_y + player_size > item[1]):
            items.remove(item)
            score += 10
            
            # Subir de nivel con puntos (sin mostrar pantalla)
            if score >= level * 100 and level < 4:
                level += 1
                max_level_reached = level
                player_speed += 1
                item_spawn_rate = max(10, item_spawn_rate - 5)
    
    for obstacle in obstacles[:]:
        if (player_x < obstacle[0] + obstacle_size and
            player_x + player_size > obstacle[0] and
            player_y < obstacle[1] + obstacle_size and
            player_y + player_size > obstacle[1]):
            obstacles.remove(obstacle)
            lives -= 1
            
            if lives <= 0:
                final_score = score
                show_game_over()
                player_x = 400
                player_y = 300
                items = []
                obstacles = []
                score = 0
                lives = 3
                level = 1
                player_speed = 5
                item_spawn_rate = 30
                obstacle_spawn_rate = 60
                game_time = 0
                max_level_reached = 1
            
    for item in items:
        draw_item(item[0], item[1], item[2])
        
    for obstacle in obstacles:
        draw_obstacle(obstacle[0], obstacle[1])
        
    draw_player(player_x, player_y)
    draw_game_info()
    
    if score >= 400:
        final_score = score
        show_game_over()
        player_x = 400
        player_y = 300
        items = []
        obstacles = []
        score = 0
        lives = 3
        level = 1
        player_speed = 5
        item_spawn_rate = 30
        obstacle_spawn_rate = 60
        game_time = 0
        max_level_reached = 1
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
