import pygame
import random
import sys
import time
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Saci")

# Cores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Cores
DARK_BROWN = (45, 25, 5)
MEDIUM_BROWN = (65, 35, 10)
LIGHT_BROWN = (85, 45, 15)
DARK_WOOD = (55, 30, 8)

# Cores para galhos
BARK_DARK = (70, 50, 25)
BARK_MEDIUM = (90, 60, 30)
BARK_LIGHT = (110, 80, 40)
FOREST_FLOOR = (40, 25, 10)

# Cores para raios e efeitos de tempestade
LIGHTNING_YELLOW = (255, 255, 200)
LIGHTNING_WHITE = (255, 255, 255)
LIGHTNING_BLUE = (200, 220, 255)
THUNDER_GRAY = (100, 100, 120)
STORM_BLUE = (80, 90, 120)

# Cores do jogador
SACI_RED = (200, 0, 0)
SACI_SKIN = (76, 56, 30)
SACI_WHITE = (240, 240, 240)
SACI_PIPE = (100, 70, 40)

# Configurações do jogador
player_width, player_height = 35, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 100
player_vel_x = 0
player_vel_y = 0
player_speed = 5
jump_strength = 16
gravity = 0.8
is_jumping = False
facing_right = True

# Sistema de pulo duplo
double_jump_available = True
double_jump_cooldown = 5
last_double_jump_time = time.time()
double_jump_ready = True

# Configurações das plataformas
platform_width = 120
platform_height = 15
platforms = []
platform_gap = 160
max_horizontal_gap = 200
min_platform_y = 100
max_platform_y = HEIGHT - 50

# Configurações dos obstáculos
obstacles = []
obstacle_min_size = 15
obstacle_max_size = 25
obstacle_speed_min = 6
obstacle_speed_max = 10
last_obstacle_time = time.time()
obstacle_spawn_delay = 2.0
min_obstacle_delay = 0.6
obstacle_delay_decrease = 0.1

# Sistema de tempestade
rain_drops = []
lightning_flashes = []
last_rain_time = time.time()
last_lightning_time = time.time()
rain_spawn_delay = 0.03
lightning_spawn_delay = 3.0

# Sistema de pontuação
platforms_jumped = 0
last_platform_y = HEIGHT - 50  # Posição da plataforma inicial

# Variável para controle de vitória
VICTORY_PLATFORMS = 30  # Número de plataformas para vencer
victory_achieved = False
victory_alpha = 0  # Alpha para efeito de fade
victory_timer = 0  # Timer para efeitos de vitória

# Fundo estático
forest_background = None

# Criar fundo de floresta com tempestade
def create_storm_forest_background():
    global forest_background
    forest_background = pygame.Surface((WIDTH, HEIGHT))

    # Gradiente céu
    top_color = (30, 45, 60)
    bottom_color = (20, 30, 30)
    for y in range(HEIGHT):
        r = top_color[0] * (1 - y / HEIGHT) + bottom_color[0] * (y / HEIGHT)
        g = top_color[1] * (1 - y / HEIGHT) + bottom_color[1] * (y / HEIGHT)
        b = top_color[2] * (1 - y / HEIGHT) + bottom_color[2] * (y / HEIGHT)
        pygame.draw.line(forest_background, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

    # Árvores
    for _ in range(12):
        x = random.randint(-80, WIDTH - 40)
        height = random.randint(350, 500)
        width = random.randint(40, 60)
        draw_amazon_tree(forest_background, x, height, width)

    # Neblina
    fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(HEIGHT):
        fog_alpha = int(100 * (y / HEIGHT))
        pygame.draw.line(fog, (120, 120, 140, fog_alpha), (0, y), (WIDTH, y))
    forest_background.blit(fog, (0, 0))

def draw_amazon_tree(surface, x, h, w):
    trunk_color = (70, 50, 25)
    pygame.draw.rect(surface, trunk_color, (x, HEIGHT - h, w, h))

    crown_color = (25, 90, 35)
    for _ in range(8):
        cx = x + random.randint(-40, 80)
        cy = HEIGHT - h + random.randint(-100, 80)
        radius = random.randint(50, 90)
        pygame.draw.circle(surface, crown_color, (cx, cy), radius)

def draw_static_background():
    screen.blit(forest_background, (0, 0))

# Inicializar plataformas
def init_platforms():
    global platforms, platforms_jumped, last_platform_y
    platforms.clear()
    platforms_jumped = 0
    last_platform_y = HEIGHT - 50
    
    # Plataforma inicial
    platforms.append({
        'x': WIDTH // 2 - platform_width // 2,
        'y': HEIGHT - 50,
        'width': platform_width,
        'height': platform_height,
        'color': random.choice([BARK_DARK, BARK_MEDIUM, BARK_LIGHT]),
        'branch_type': random.choice(['straight', 'curved', 'forked']),
        'jumped': False  # Nova flag para verificar se já foi pulada
    })
    
    # Gerar plataformas iniciais
    last_platform = platforms[0]
    for i in range(10):
        y_pos = last_platform['y'] - platform_gap
        
        if y_pos < min_platform_y:
            break
            
        min_x = max(0, last_platform['x'] - max_horizontal_gap)
        max_x = min(WIDTH - platform_width, last_platform['x'] + max_horizontal_gap)
        
        if min_x > max_x:
            min_x = 0
            max_x = WIDTH - platform_width
            
        x_pos = random.randint(int(min_x), int(max_x))
        
        new_platform = {
            'x': x_pos,
            'y': y_pos,
            'width': platform_width,
            'height': platform_height,
            'color': random.choice([BARK_DARK, BARK_MEDIUM, BARK_LIGHT]),
            'branch_type': random.choice(['straight', 'curved', 'forked']),
            'jumped': False  # Nova flag para verificar se já foi pulada
        }
        
        platforms.append(new_platform)
        last_platform = new_platform

# Funções para desenhar plataformas
def draw_platforms():
    for platform in platforms:
        if platform['branch_type'] == 'straight':
            draw_straight_branch(platform)
        elif platform['branch_type'] == 'curved':
            draw_curved_branch(platform)
        else:
            draw_forked_branch(platform)

def draw_straight_branch(platform):
    x, y, w, h = platform['x'], platform['y'], platform['width'], platform['height']
    pygame.draw.rect(screen, platform['color'], (x, y, w, h))
    for i in range(h // 3):
        stripe_y = y + i * 3
        stripe_color = darken_color(platform['color'], random.randint(5, 15))
        pygame.draw.line(screen, stripe_color, (x, stripe_y), (x + w, stripe_y), 1)
    for i in range(3):
        knot_x = x + random.randint(10, w - 10)
        knot_y = y + h // 2
        knot_size = random.randint(2, 4)
        knot_color = darken_color(platform['color'], 20)
        pygame.draw.circle(screen, knot_color, (knot_x, knot_y), knot_size)

def draw_curved_branch(platform):
    x, y, w, h = platform['x'], platform['y'], platform['width'], platform['height']
    points = [
        (x, y + h//2),
        (x + w//4, y),
        (x + 3*w//4, y + h),
        (x + w, y + h//2)
    ]
    pygame.draw.lines(screen, platform['color'], False, points, h)
    for i in range(4):
        detail_x = x + random.randint(5, w - 5)
        detail_y = y + random.randint(2, h - 2)
        detail_size = random.randint(1, 2)
        detail_color = darken_color(platform['color'], random.randint(10, 25))
        pygame.draw.circle(screen, detail_color, (detail_x, detail_y), detail_size)

def draw_forked_branch(platform):
    x, y, w, h = platform['x'], platform['y'], platform['width'], platform['height']
    main_width = w // 2
    pygame.draw.rect(screen, platform['color'], (x + main_width//2, y, main_width, h))
    left_branch_points = [
        (x + main_width//2, y + h//3),
        (x, y + h//2),
        (x + w//4, y + 2*h//3)
    ]
    right_branch_points = [
        (x + main_width + main_width//2, y + h//3),
        (x + w, y + h//2),
        (x + 3*w//4, y + 2*h//3)
    ]
    pygame.draw.lines(screen, platform['color'], False, left_branch_points, h//2)
    pygame.draw.lines(screen, platform['color'], False, right_branch_points, h//2)
    for i in range(6):
        line_x = x + random.randint(5, w - 5)
        line_color = darken_color(platform['color'], random.randint(5, 20))
        pygame.draw.line(screen, line_color, (line_x, y), (line_x, y + h), 1)

# Contar plataformas puladas
def check_platform_collision():
    global player_y, player_vel_y, is_jumping, double_jump_available, double_jump_ready, platforms_jumped, last_platform_y, victory_achieved
    
    for platform in platforms:
        if (player_y + player_height >= platform['y'] and 
            player_y + player_height <= platform['y'] + platform['height'] and
            player_x + player_width > platform['x'] and 
            player_x < platform['x'] + platform['width'] and
            player_vel_y > 0):
            
            player_y = platform['y'] - player_height
            player_vel_y = 0
            is_jumping = False
            double_jump_available = True
            
            # Contar plataforma como pulada se for uma plataforma nova mais alta
            if platform['y'] < last_platform_y and not platform['jumped']:
                platforms_jumped += 1
                platform['jumped'] = True
                last_platform_y = platform['y']
                
                # Verificar se alcançou a vitória
                if platforms_jumped >= VICTORY_PLATFORMS and not victory_achieved:
                    victory_achieved = True
            
            return True
    return False

# Gerar plataformas
def generate_platforms():
    global platforms
    
    if platforms:
        highest_platform = min(platforms, key=lambda p: p['y'])
        
        if highest_platform['y'] > platform_gap:
            platforms[:] = [p for p in platforms if p['y'] < HEIGHT + 100]
            
            current_highest = min(platforms, key=lambda p: p['y'])
            last_platform = current_highest
            
            for i in range(random.randint(2, 3)):
                y_pos = last_platform['y'] - platform_gap
                
                min_x = max(0, last_platform['x'] - max_horizontal_gap)
                max_x = min(WIDTH - platform_width, last_platform['x'] + max_horizontal_gap)
                
                if min_x > max_x:
                    min_x = 0
                    max_x = WIDTH - platform_width
                    
                x_pos = random.randint(int(min_x), int(max_x))
                
                new_platform = {
                    'x': x_pos,
                    'y': y_pos,
                    'width': platform_width,
                    'height': platform_height,
                    'color': random.choice([BARK_DARK, BARK_MEDIUM, BARK_LIGHT]),
                    'branch_type': random.choice(['straight', 'curved', 'forked']),
                    'jumped': False
                }
                
                platforms.append(new_platform)
                last_platform = new_platform

# Desenhar tudo
def draw_all():
    draw_static_background()
    draw_rain()
    draw_lightning_flash()
    draw_platforms()
    draw_obstacles()
    draw_player()
    draw_double_jump_hud()

def generate_lightning_path(start_x, start_y, end_x, end_y, branching_factor=0.3, jaggedness=50):
    points = [(start_x, start_y)]
    
    # Direção geral
    dx = end_x - start_x
    dy = end_y - start_y
    distance = math.sqrt(dx*dx + dy*dy)
    
    if distance < 10:
        points.append((end_x, end_y))
        return points
    
    num_segments = max(5, int(distance // 40))
    
    for i in range(1, num_segments):
        t = i / num_segments
        base_x = start_x + dx * t
        base_y = start_y + dy * t
        
        if random.random() < branching_factor:
            offset_x = random.uniform(-jaggedness, jaggedness)
            offset_y = random.uniform(-jaggedness/2, jaggedness/2)
        else:
            offset_x = random.uniform(-jaggedness/2, jaggedness/2)
            offset_y = random.uniform(-jaggedness/4, jaggedness/4)
        
        points.append((base_x + offset_x, base_y + offset_y))
    
    points.append((end_x, end_y))
    return points

def draw_lightning_bolt(obstacle):
    x, y = obstacle['x'], obstacle['y']
    size = obstacle['size']
    
    base_length = size * 1.5
    thickness = max(2, size // 8 + 1)
    
    start_y = max(0, y - random.randint(100, 200))
    end_y = min(HEIGHT, y + base_length)
    
    points = generate_lightning_path(x, start_y, x, end_y, 
                                    branching_factor=0.4, 
                                    jaggedness=size)
    
    if len(points) > 1:
        main_color = LIGHTNING_YELLOW
        
        for i in range(1):
            offset_points = [(px + random.randint(-2, 2), py + random.randint(-2, 2)) for px, py in points]
            pygame.draw.lines(screen, (255, 255, 180, 150), False, offset_points, thickness + 2)
        
        pygame.draw.lines(screen, main_color, False, points, thickness + 1)
        pygame.draw.lines(screen, LIGHTNING_WHITE, False, points, max(1, thickness))
        
        for i in range(len(points) - 1):
            if random.random() < 0.3:
                branch_point = random.randint(i, i+1)
                if branch_point < len(points):
                    branch_x, branch_y = points[branch_point]
                    branch_length = random.randint(size, size * 2)
                    branch_angle = random.uniform(0, 2 * math.pi)
                    
                    branch_end_x = branch_x + math.cos(branch_angle) * branch_length
                    branch_end_y = branch_y + math.sin(branch_angle) * branch_length
                    
                    branch_points = generate_lightning_path(branch_x, branch_y, 
                                                          branch_end_x, branch_end_y,
                                                          branching_factor=0.2, 
                                                          jaggedness=size//2)
                    
                    if len(branch_points) > 1:
                        pygame.draw.lines(screen, (255, 255, 180, 180), False, 
                                         branch_points, max(1, thickness // 2))
                        pygame.draw.lines(screen, LIGHTNING_YELLOW, False, 
                                         branch_points, max(1, thickness // 3))
        
        for i in range(2):
            glow_points = []
            for px, py in points:
                offset_x = px + random.randint(-2, 2)
                offset_y = py + random.randint(-2, 2)
                glow_points.append((offset_x, offset_y))
            
            if len(glow_points) > 1:
                alpha = random.randint(50, 100)
                pygame.draw.lines(screen, (255, 255, 200, alpha), False, 
                                 glow_points, max(1, thickness // 4))
    
    if y > HEIGHT * 0.7:
        impact_radius = size // 4
        impact_color = (255, 255, 200)
        
        for i in range(2):
            radius = impact_radius + i * 2
            alpha = 200 - i * 50
            for j in range(3):
                angle = random.uniform(0, 2 * math.pi)
                start_radius = random.randint(radius - 1, radius + 1)
                end_radius = start_radius + random.randint(2, 4)
                start_x_circ = x + math.cos(angle) * start_radius
                start_y_circ = end_y + math.sin(angle) * start_radius
                end_x_circ = x + math.cos(angle) * end_radius
                end_y_circ = end_y + math.sin(angle) * end_radius
                pygame.draw.line(screen, (*impact_color[:3], alpha), 
                               (start_x_circ, start_y_circ), (end_x_circ, end_y_circ), 1)

def draw_obstacles():
    for obstacle in obstacles:
        draw_lightning_bolt(obstacle)

def generate_obstacles():
    global last_obstacle_time, obstacles
    
    current_time = time.time()
    score = max(0, HEIGHT - 50 - int(player_y))
    
    current_delay = max(min_obstacle_delay, 
                       obstacle_spawn_delay - (score // 100) * obstacle_delay_decrease)
    
    if current_time - last_obstacle_time > current_delay and not victory_achieved:
        size = random.randint(obstacle_min_size, obstacle_max_size)
        x = random.randint(50, WIDTH - 50)
        
        obstacle_type = 'lightning'  
        
        obstacles.append({
            'x': x,
            'y': -size * 2,
            'size': size,
            'speed': random.uniform(obstacle_speed_min, obstacle_speed_max),
            'type': obstacle_type
        })
        
        last_obstacle_time = current_time

def generate_rain():
    global last_rain_time, rain_drops
    
    current_time = time.time()
    if current_time - last_rain_time > rain_spawn_delay:
        for _ in range(5):
            rain_drops.append({
                'x': random.randint(-50, WIDTH + 50),
                'y': random.randint(-100, -10),
                'length': random.randint(8, 15),
                'speed': random.uniform(8, 12),
                'intensity': random.random()
            })
        last_rain_time = current_time

def update_rain():
    global rain_drops
    
    for drop in rain_drops[:]:
        drop['y'] += drop['speed']
        if drop['y'] > HEIGHT + 20:
            rain_drops.remove(drop)

def draw_rain():
    for drop in rain_drops:
        alpha = 150 + int(drop['intensity'] * 105)
        rain_color = (180, 180, 200, alpha)
        thickness = 1 + int(drop['intensity'] * 2)
        pygame.draw.line(screen, rain_color, 
                        (drop['x'], drop['y']), 
                        (drop['x'], drop['y'] + drop['length']), thickness)

def generate_lightning():
    global last_lightning_time, lightning_flashes
    
    current_time = time.time()
    if current_time - last_lightning_time > lightning_spawn_delay and not victory_achieved:
        lightning_flashes.append({
            'duration': 0.2,
            'start_time': current_time,
            'intensity': random.uniform(0.3, 0.8)
        })
        last_lightning_time = current_time + random.uniform(3, 8)

def update_lightning():
    global lightning_flashes
    
    current_time = time.time()
    for flash in lightning_flashes[:]:
        if current_time - flash['start_time'] > flash['duration']:
            lightning_flashes.remove(flash)

def draw_lightning_flash():
    if lightning_flashes:
        flash = lightning_flashes[0]
        current_time = time.time()
        elapsed = current_time - flash['start_time']
        
        if elapsed < flash['duration']:
            alpha = int(flash['intensity'] * 200 * (1 - elapsed / flash['duration']))
            flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, alpha))
            screen.blit(flash_surface, (0, 0))

def darken_color(color, amount):
    r = max(0, color[0] - amount)
    g = max(0, color[1] - amount)
    b = max(0, color[2] - amount)
    return (r, g, b)

def lighten_color(color, amount):
    r = min(255, color[0] + amount)
    g = min(255, color[1] + amount)
    b = min(255, color[2] + amount)
    return (r, g, b)

def update_double_jump():
    global double_jump_ready, last_double_jump_time
    
    current_time = time.time()
    time_since_last_jump = current_time - last_double_jump_time
    
    if not double_jump_ready and time_since_last_jump >= double_jump_cooldown:
        double_jump_ready = True
        last_double_jump_time = current_time

def draw_double_jump_hud():
    font = pygame.font.SysFont(None, 24)
    
    if double_jump_ready:
        text = font.render("PULO DUPLO PRONTO!", True, LIGHTNING_YELLOW)
        screen.blit(text, (WIDTH - 200, 30))
    else:
        current_time = time.time()
        time_remaining = double_jump_cooldown - (current_time - last_double_jump_time)
        if time_remaining < 0:
            time_remaining = 0
        
        text = font.render(f"Pulo Duplo: {time_remaining:.1f}s", True, LIGHTNING_BLUE)
        screen.blit(text, (WIDTH - 200, 30))
        
        progress = 1 - (time_remaining / double_jump_cooldown)
        bar_width = 150
        bar_height = 10
        bar_x = WIDTH - bar_width - 25
        bar_y = 60
        
        pygame.draw.rect(screen, (60, 60, 80), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, LIGHTNING_YELLOW, (bar_x, bar_y, bar_width * progress, bar_height))

def draw_saci():
    body_width = player_width
    body_height = player_height
    body_color = SACI_RED
    
    pygame.draw.rect(screen, body_color, 
                    (player_x, player_y, body_width, body_height - 15), 
                    border_radius=8)
    
    back_detail_color = darken_color(body_color, 30)
    pygame.draw.ellipse(screen, back_detail_color, 
                       (player_x + body_width//4, player_y + 10, 
                        body_width//2, body_height//4))
    
    head_radius = 12
    head_x = player_x + body_width // 2
    head_y = player_y + head_radius
    
    gorro_color = SACI_RED
    gorro_width = 30
    gorro_height = 25
    
    gorro_rect = pygame.Rect(head_x - gorro_width//2, head_y - 15, 
                            gorro_width, gorro_height//2)
    pygame.draw.rect(screen, gorro_color, gorro_rect, border_radius=5)
    
    pygame.draw.circle(screen, gorro_color, 
                      (head_x, head_y - 15), gorro_width//2)
    
    pompom_radius = 6
    pompom_x = head_x
    pompom_y = head_y - 15 - gorro_width//2
    pygame.draw.circle(screen, SACI_WHITE, (pompom_x, pompom_y), pompom_radius)
    
    ear_radius = 5
    left_ear_x = head_x - head_radius + 2
    right_ear_x = head_x + head_radius - 2
    ear_y = head_y - 5
    
    pygame.draw.circle(screen, SACI_SKIN, (left_ear_x, ear_y), ear_radius)
    pygame.draw.circle(screen, SACI_SKIN, (right_ear_x, ear_y), ear_radius)
    
    pygame.draw.circle(screen, SACI_SKIN, (head_x, head_y), head_radius)
    
    hair_color = darken_color(SACI_SKIN, 20)
    pygame.draw.circle(screen, hair_color, (head_x, head_y + 2), head_radius - 2)
    
    pants_color = darken_color(SACI_RED, 40)
    pants_y = player_y + body_height - 25
    pants_height = 20
    
    pygame.draw.rect(screen, pants_color, 
                    (player_x + 5, pants_y, body_width - 10, 10),
                    border_radius=3)
    
    leg_width = 10
    leg_x = player_x + 8
    
    pygame.draw.rect(screen, pants_color, 
                    (leg_x, pants_y + 10, leg_width, pants_height))
    
    foot_height = 6
    foot_width = 14
    
    foot_x = leg_x - 2
    foot_y = pants_y + 10 + pants_height
    
    pygame.draw.ellipse(screen, (40, 20, 10), 
                       (foot_x, foot_y, foot_width, foot_height))
    
    arm_color = SACI_SKIN
    arm_width = 8
    arm_length = 25
    
    left_arm_x = player_x - 3
    left_arm_y = player_y + 20
    pygame.draw.rect(screen, arm_color, 
                    (left_arm_x, left_arm_y, arm_width, arm_length),
                    border_radius=4)
    
    left_hand_x = left_arm_x + arm_width//2
    left_hand_y = left_arm_y + arm_length
    pygame.draw.circle(screen, arm_color, (left_hand_x, left_hand_y), 5)
    
    right_arm_x = player_x + body_width - 5
    right_arm_y = player_y + 20
    pygame.draw.rect(screen, arm_color, 
                    (right_arm_x, right_arm_y, arm_width, arm_length),
                    border_radius=4)
    
    right_hand_x = right_arm_x + arm_width//2
    right_hand_y = right_arm_y + arm_length
    pygame.draw.circle(screen, arm_color, (right_hand_x, right_hand_y), 5)
    
    if not facing_right:
        pipe_start_x = player_x - 10
        pipe_start_y = player_y + 15
        pipe_length = 25
        pipe_end_x = pipe_start_x + pipe_length
        pipe_end_y = pipe_start_y + 10
        
        pygame.draw.line(screen, SACI_PIPE, 
                        (pipe_start_x, pipe_start_y),
                        (pipe_end_x, pipe_end_y), 4)
        
        pygame.draw.circle(screen, (60, 40, 25), 
                          (pipe_end_x, pipe_end_y), 6)
    else:
        pipe_start_x = player_x + body_width + 10
        pipe_start_y = player_y + 15
        pipe_length = -25
        pipe_end_x = pipe_start_x + pipe_length
        pipe_end_y = pipe_start_y + 10
        
        pygame.draw.line(screen, SACI_PIPE, 
                        (pipe_start_x, pipe_start_y),
                        (pipe_end_x, pipe_end_y), 4)
        
        pygame.draw.circle(screen, (60, 40, 25), 
                          (pipe_end_x, pipe_end_y), 6)
    
    belt_color = (30, 15, 5)
    belt_y = player_y + body_height - 30
    pygame.draw.rect(screen, belt_color, 
                    (player_x + 8, belt_y, body_width - 16, 3))
    
    if double_jump_ready:
        for i in range(3):
            smoke_x = pipe_end_x + random.randint(-6, 6)
            smoke_y = pipe_end_y - random.randint(5, 15)
            smoke_size = random.randint(2, 4)
            smoke_alpha = random.randint(80, 150)
            
            smoke_surface = pygame.Surface((smoke_size*2, smoke_size*2), pygame.SRCALPHA)
            pygame.draw.circle(smoke_surface, (200, 200, 200, smoke_alpha), 
                             (smoke_size, smoke_size), smoke_size)
            screen.blit(smoke_surface, (smoke_x - smoke_size, smoke_y - smoke_size))

def draw_player():
    draw_saci()

def check_obstacle_collision():
    global game_over
    
    if victory_achieved:
        return False
    
    for obstacle in obstacles:
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        
        x, y = obstacle['x'], obstacle['y']
        size = obstacle['size']
        base_length = size * 1.5
        start_y = max(0, y - random.randint(100, 200))
        end_y = min(HEIGHT, y + base_length)
        
        points = generate_lightning_path(x, start_y, x, end_y, 
                                        branching_factor=0.4, 
                                        jaggedness=size)
        
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            
            thickness = max(2, size // 8 + 1)
            half_thickness = thickness / 2
            
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = math.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                dx /= length
                dy /= length
                
                perp_dx = -dy * half_thickness
                perp_dy = dx * half_thickness
                
                rect_points = [
                    (p1[0] + perp_dx, p1[1] + perp_dy),
                    (p1[0] - perp_dx, p1[1] - perp_dy),
                    (p2[0] - perp_dx, p2[1] - perp_dy),
                    (p2[0] + perp_dx, p2[1] + perp_dy)
                ]
                
                player_polygon = [
                    (player_x, player_y),
                    (player_x + player_width, player_y),
                    (player_x + player_width, player_y + player_height),
                    (player_x, player_y + player_height)
                ]
                
                if check_polygon_collision(player_polygon, rect_points):
                    game_over = True
                    return True
    
    return False

def check_polygon_collision(poly1, poly2):
    def project_polygon(axis, polygon):
        min_proj = float('inf')
        max_proj = float('-inf')
        for point in polygon:
            proj = point[0] * axis[0] + point[1] * axis[1]
            min_proj = min(min_proj, proj)
            max_proj = max(max_proj, proj)
        return min_proj, max_proj
    
    def get_axes(polygon):
        axes = []
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            edge = (p1[0] - p2[0], p1[1] - p2[1])
            axis = (-edge[1], edge[0])
            length = math.sqrt(axis[0]*axis[0] + axis[1]*axis[1])
            if length > 0:
                axis = (axis[0]/length, axis[1]/length)
                axes.append(axis)
        return axes
    
    axes = get_axes(poly1) + get_axes(poly2)
    
    for axis in axes:
        min1, max1 = project_polygon(axis, poly1)
        min2, max2 = project_polygon(axis, poly2)
        
        if max1 < min2 or max2 < min1:
            return False
    
    return True

def update_obstacles():
    global obstacles
    
    for obstacle in obstacles[:]:
        obstacle['y'] += obstacle['speed']
        if obstacle['y'] > HEIGHT + 200:
            obstacles.remove(obstacle)

# Efeito de vitória
def update_victory():
    global victory_alpha, victory_timer
    
    if victory_achieved:
        # Aumentar gradualmente o alpha para escurecer a tela
        victory_alpha = min(victory_alpha + 3, 200)
        victory_timer += 1

def draw_victory_screen():
    if victory_achieved and victory_alpha > 0:
        # Criar overlay escuro
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, victory_alpha))
        screen.blit(overlay, (0, 0))
        
        # Desenhar texto de vitória
        font_large = pygame.font.SysFont(None, 72)
        font_medium = pygame.font.SysFont(None, 48)
        font_small = pygame.font.SysFont(None, 36)
        
        # Efeito de brilho intermitente
        pulse = abs(math.sin(victory_timer * 0.05)) * 255
        gold_color = (255, 215, 0, int(pulse))
        
        victory_text = font_large.render("VITÓRIA!", True, LIGHTNING_YELLOW)
        message_text = font_medium.render("Tempestade Superada!", True, LIGHTNING_BLUE)
        platforms_text = font_medium.render(f"{VICTORY_PLATFORMS} Plataformas Conquistadas", True, WHITE)
        
        restart_text = font_small.render("Pressione R para jogar novamente", True, WHITE)
        
        # Posicionar textos
        screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - 120))
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(platforms_text, (WIDTH // 2 - platforms_text.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
        
        # Desenhar efeitos especiais de vitória
        if victory_timer % 10 < 5:
            for _ in range(3):
                x = random.randint(100, WIDTH - 100)
                y = random.randint(100, HEIGHT - 100)
                size = random.randint(5, 15)
                pygame.draw.circle(screen, LIGHTNING_YELLOW, (x, y), size)

# Inicializar o jogo
create_storm_forest_background()
init_platforms()
clock = pygame.time.Clock()
game_over = False

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not victory_achieved:
                if not is_jumping:
                    player_vel_y = -jump_strength
                    is_jumping = True
                elif double_jump_available and double_jump_ready:
                    player_vel_y = -jump_strength * 0.8
                    double_jump_available = False
                    double_jump_ready = False
                    last_double_jump_time = time.time()
            
            if event.key == pygame.K_r and (game_over or victory_achieved):
                # Reiniciar o jogo
                player_x = WIDTH // 2 - player_width // 2
                player_y = HEIGHT - 100
                player_vel_x = 0
                player_vel_y = 0
                is_jumping = False
                double_jump_available = True
                double_jump_ready = True
                last_double_jump_time = time.time()
                last_obstacle_time = time.time()
                obstacles.clear()
                rain_drops.clear()
                lightning_flashes.clear()
                game_over = False
                victory_achieved = False
                victory_alpha = 0
                victory_timer = 0
                platforms_jumped = 0
                init_platforms()
    
    if not game_over and not victory_achieved:
        update_double_jump()
        
        generate_obstacles()
        update_obstacles()
        check_obstacle_collision()
        
        generate_rain()
        update_rain()
        generate_lightning()
        update_lightning()
        
        keys = pygame.key.get_pressed()
        player_vel_x = 0
        
        if keys[pygame.K_LEFT]:
            player_vel_x = -player_speed
            facing_right = False
        if keys[pygame.K_RIGHT]:
            player_vel_x = player_speed
            facing_right = True
        
        player_x += player_vel_x
        
        player_vel_y += gravity
        player_y += player_vel_y
        
        if player_x < 0:
            player_x = 0
        if player_x > WIDTH - player_width:
            player_x = WIDTH - player_width
        
        if player_y > HEIGHT:
            game_over = True
        
        check_platform_collision()
        
        if player_vel_y < 0:
            for platform in platforms:
                platform['y'] -= player_vel_y
            generate_platforms()
    
    # Atualizar efeitos de vitória
    update_victory()
    
    # Desenhar tudo
    draw_all()
    
    # Desenhar tela de vitória
    draw_victory_screen()
    
    if game_over and not victory_achieved:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont(None, 72)
        
        game_over_text = font.render("GAME OVER", True, LIGHTNING_YELLOW)
        message_text = font.render(f"Plataformas: {platforms_jumped}", True, WHITE)
        
        restart_text = font.render("Pressione R para reiniciar", True, WHITE)
        
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 80))
    
    pygame.display.flip()
    clock.tick(60)