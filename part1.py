import pygame
import random
import sys
import math
from collections import deque

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Curupira - A Lenda da Floresta")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARK_GREEN = (0, 80, 0)
FOREST_GREEN = (34, 139, 34)
TRUNK_BROWN = (101, 67, 33)
PATH_BROWN = (160, 120, 80)
FOOTPRINT_COLOR = (120, 85, 50)
STONE_GRAY = (169, 169, 169)
HUNTER_RED = (180, 0, 0)
HUNTER_BLUE = (0, 100, 200)
HUNTER_PANTS = (80, 80, 120)
HUNTER_SKIN = (240, 200, 160)
HUNTER_HAT = (60, 60, 60)
GUN_BROWN = (110, 70, 40)
CURUPIRA_HAIR = (255, 100, 0) 
CURUPIRA_SKIN = (220, 180, 140)
CURUPIRA_SKIRT = (0, 120, 0) 
FIRE_ORANGE = (255, 100, 0)
FIRE_YELLOW = (255, 200, 0)
FIRE_RED = (255, 50, 0)
PORTAL_ORANGE = (255, 150, 0)
PORTAL_YELLOW = (255, 220, 0)
BOAR_BROWN = (80, 50, 20)
BOAR_DARK_BROWN = (50, 30, 10)
SPEAR_BROWN = (120, 80, 40)
SPEAR_METAL = (200, 200, 200)

# Cores para as cutscenes
SKY_BLUE = (135, 206, 235)
GROUND_GREEN = (34, 139, 34)
TREE_GREEN = (0, 100, 0)
TEXT_BOX_COLOR = (30, 30, 30, 220)

# Configurações do jogo
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
PLAYER_SPEED = 5
ENEMY_SPEED = 10
FOOTPRINT_DURATION = 6
FOOTPRINT_COOLDOWN = 30
REVERSAL_DURATION = 45

# Cores de fundo para diferentes níveis 
LEVEL_BACKGROUNDS = [
    (0, 50, 0),     # Nível 1: Verde escuro claro
    (0, 15, 0),     # Nível 2: Verde mais escuro
    (0, 10, 0)      # Nível 3: Verde mais escuro ainda
]

# Configuração de fontes
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)
font_dialogue = pygame.font.SysFont(None, 32)
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# ============================
# CUTSCENE 1: DIÁLOGO DO CURUPIRA
# ============================

class CurupiraFace:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2 - 50
        self.size = 200
        self.eye_blink_timer = 0
        self.eye_blink_interval = 120
        self.eye_blink_duration = 5
        self.mouth_timer = 0
        self.mouth_animation_speed = 0.1
        self.fire_animation = 0
        self.fire_speed = 0.2
        
    def draw(self, screen):
        self.draw_face(screen)
        self.draw_fire_hair(screen)
        self.draw_eyes(screen)
        self.draw_mouth(screen)
        
        self.eye_blink_timer += 1
        self.mouth_timer += self.mouth_animation_speed
        self.fire_animation += self.fire_speed
    
    def draw_face(self, screen):
        face_radius = self.size // 2
        pygame.draw.circle(screen, CURUPIRA_SKIN, (self.x, self.y), face_radius)
        pygame.draw.circle(screen, (200, 140, 70), (self.x, self.y), face_radius, 3)
        
        cheek_radius = face_radius // 4
        left_cheek_x = self.x - face_radius // 2
        right_cheek_x = self.x + face_radius // 2
        cheek_y = self.y + face_radius // 4
        
        pygame.draw.circle(screen, (255, 200, 180), (left_cheek_x, cheek_y), cheek_radius)
        pygame.draw.circle(screen, (255, 200, 180), (right_cheek_x, cheek_y), cheek_radius)
    
    def draw_fire_hair(self, screen):
        base_width = self.size * 0.9
        base_height = self.size * 0.4
        base_y = self.y - self.size // 2 - base_height * 0.3
        
        pygame.draw.ellipse(screen, CURUPIRA_HAIR, 
                          (self.x - base_width//2, base_y, base_width, base_height))
        
        flame_count = 9
        max_flame_height = self.size * 0.8
        
        for i in range(flame_count):
            flame_x = self.x - base_width//2 + (base_width / (flame_count - 1)) * i
            flame_height = max_flame_height * (0.5 + 0.5 * math.sin(self.fire_animation + i * 0.5))
            
            points = [
                (flame_x, base_y + base_height * 0.5),
                (flame_x - base_width * 0.08, base_y - flame_height * 0.3),
                (flame_x, base_y - flame_height),
                (flame_x + base_width * 0.08, base_y - flame_height * 0.3)
            ]
            pygame.draw.polygon(screen, FIRE_ORANGE, points)
            
            inner_height = flame_height * 0.7
            inner_points = [
                (flame_x, base_y + base_height * 0.5),
                (flame_x - base_width * 0.04, base_y - inner_height * 0.2),
                (flame_x, base_y - inner_height),
                (flame_x + base_width * 0.04, base_y - inner_height * 0.2)
            ]
            pygame.draw.polygon(screen, FIRE_YELLOW, inner_points)
            
            if i % 3 == 0:
                spark_x = flame_x + (math.sin(self.fire_animation * 2 + i) * 5)
                spark_y = base_y - flame_height - 5
                spark_radius = 3 + math.sin(self.fire_animation + i) * 2
                pygame.draw.circle(screen, FIRE_YELLOW, (int(spark_x), int(spark_y)), int(spark_radius))
    
    def draw_eyes(self, screen):
        eye_radius = self.size // 8
        eye_y = self.y - self.size // 10
        left_eye_x = self.x - self.size // 4
        right_eye_x = self.x + self.size // 4
        
        is_blinking = (self.eye_blink_timer % self.eye_blink_interval) < self.eye_blink_duration
        
        if not is_blinking:
            pygame.draw.circle(screen, WHITE, (left_eye_x, eye_y), eye_radius)
            pygame.draw.circle(screen, BLACK, (left_eye_x, eye_y), eye_radius // 2)
            pygame.draw.circle(screen, WHITE, (right_eye_x, eye_y), eye_radius)
            pygame.draw.circle(screen, BLACK, (right_eye_x, eye_y), eye_radius // 2)
            
            sparkle_radius = eye_radius // 4
            pygame.draw.circle(screen, WHITE, (left_eye_x - sparkle_radius//2, eye_y - sparkle_radius//2), sparkle_radius)
            pygame.draw.circle(screen, WHITE, (right_eye_x - sparkle_radius//2, eye_y - sparkle_radius//2), sparkle_radius)
        else:
            pygame.draw.arc(screen, (150, 100, 50), 
                          (left_eye_x - eye_radius, eye_y - eye_radius//3, 
                           eye_radius * 2, eye_radius//2), 
                          3.14, 6.28, 3)
            pygame.draw.arc(screen, (150, 100, 50), 
                          (right_eye_x - eye_radius, eye_y - eye_radius//3, 
                           eye_radius * 2, eye_radius//2), 
                          3.14, 6.28, 3)
    
    def draw_mouth(self, screen):
        mouth_width = self.size // 3
        mouth_height = self.size // 8
        mouth_y = self.y + self.size // 4
        
        mouth_openness = 0.3 + 0.2 * math.sin(self.mouth_timer)
        
        pygame.draw.arc(screen, (220, 100, 100), 
                       (self.x - mouth_width//2, mouth_y - mouth_height//2, 
                        mouth_width, mouth_height * (1 + mouth_openness)), 
                       3.14, 6.28, 3)
        
        if math.sin(self.mouth_timer * 1.5) > 0.7:
            tongue_width = mouth_width // 3
            tongue_height = mouth_height // 2
            pygame.draw.ellipse(screen, (255, 150, 150), 
                              (self.x - tongue_width//2, mouth_y + mouth_height * 0.2, 
                               tongue_width, tongue_height))

class DialogueBox:
    def __init__(self, text):
        self.text = text
        self.x = WIDTH // 2
        self.y = HEIGHT - 150
        self.width = WIDTH - 100
        self.height = 120
        self.text_lines = self.wrap_text(text)
        self.arrow_timer = 0
        
    def wrap_text(self, text):
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font_dialogue.size(test_line)[0]
            
            if test_width < self.width - 40:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def draw(self, screen):
        dialogue_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        dialogue_surface.fill(TEXT_BOX_COLOR)
        
        pygame.draw.rect(dialogue_surface, (255, 255, 255, 150), 
                        (0, 0, self.width, self.height), 3)
        
        corner_radius = 10
        pygame.draw.rect(dialogue_surface, (255, 255, 255, 50), 
                        (0, 0, self.width, self.height), 3, corner_radius)
        
        screen.blit(dialogue_surface, (self.x - self.width//2, self.y - self.height//2))
        
        line_height = font_dialogue.get_height() + 5
        start_y = self.y - self.height//2 + 20
        
        for i, line in enumerate(self.text_lines):
            text_surface = font_dialogue.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.x, start_y + i * line_height))
            screen.blit(text_surface, text_rect)
        
        self.arrow_timer += 1
        if self.arrow_timer % 60 < 30:
            arrow_y = self.y + self.height//2 - 20
            arrow_points = [
                (self.x - 10, arrow_y),
                (self.x, arrow_y + 10),
                (self.x + 10, arrow_y)
            ]
            pygame.draw.polygon(screen, WHITE, arrow_points)

def draw_darkened_background():
    darkened_sky = tuple(max(0, c - 40) for c in SKY_BLUE)
    screen.fill(darkened_sky)
    
    pygame.draw.circle(screen, (200, 200, 100), (900, 80), 50)
    
    for i in range(3):
        cloud_x = 100 + i * 250
        cloud_y = 100 + (i % 2) * 20
        pygame.draw.ellipse(screen, (200, 200, 200), (cloud_x, cloud_y, 100, 40))
        pygame.draw.ellipse(screen, (200, 200, 200), (cloud_x + 30, cloud_y - 15, 80, 40))
        pygame.draw.ellipse(screen, (200, 200, 200), (cloud_x - 20, cloud_y + 10, 80, 40))
    
    pygame.draw.polygon(screen, (30, 90, 30), [(0, 300), (200, 100), (400, 300)])
    pygame.draw.polygon(screen, (20, 80, 20), [(300, 300), (500, 150), (700, 300)])
    pygame.draw.polygon(screen, (10, 70, 10), [(600, 300), (900, 180), (1000, 300)])
    
    darkened_ground = tuple(max(0, c - 30) for c in GROUND_GREEN)
    pygame.draw.rect(screen, darkened_ground, (0, 300, WIDTH, HEIGHT-300))
    
    for i in range(0, WIDTH, 20):
        blade_height = 8 + (i % 3) * 4
        pygame.draw.line(screen, (0, 80, 0), (i, 300), (i, 300 + blade_height), 1)
    
    tree_colors = [(20, 60, 20), (25, 65, 25), (30, 70, 30)]
    for i in range(8):
        tree_x = 50 + i * 120
        tree_size = 50 + (i % 3) * 20
        tree_y = 300 - tree_size//2
        
        trunk_width = tree_size // 4
        trunk_height = tree_size
        pygame.draw.rect(screen, (60, 40, 20), 
                        (tree_x - trunk_width//2, tree_y + tree_size//2, trunk_width, trunk_height))
        
        pygame.draw.circle(screen, tree_colors[i % 3], (tree_x, tree_y + tree_size//4), tree_size//2)

def dialogue_scene():
    clock = pygame.time.Clock()
    curupira_face = CurupiraFace()
    dialogue_text = "Estou em apuros, me ajude a escapar dos caçadores e encontrar meus amigos."
    dialogue_box = DialogueBox(dialogue_text)
    instruction_text = font_small.render("Pressione ESPAÇO para continuar", True, (255, 255, 200))
    
    fade_alpha = 0
    fade_speed = 3
    
    particles = []
    for _ in range(30):
        particles.append({
            'x': WIDTH // 2 + (random.random() - 0.5) * 200,
            'y': HEIGHT // 2 - 150 + (random.random() - 0.5) * 100,
            'size': random.random() * 4 + 1,
            'speed': random.random() * 0.5 + 0.2,
            'color': FIRE_ORANGE if random.random() > 0.5 else FIRE_YELLOW,
            'life': random.random() * 100 + 50
        })
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        for p in particles:
            p['y'] -= p['speed']
            p['x'] += (math.sin(p['life'] * 0.1) * 0.5)
            p['life'] -= 1
            
            if p['y'] < 0 or p['life'] <= 0:
                p['y'] = HEIGHT // 2 - 100 + random.random() * 50
                p['x'] = WIDTH // 2 + (random.random() - 0.5) * 200
                p['life'] = random.random() * 100 + 50
        
        draw_darkened_background()
        
        for p in particles:
            alpha = min(255, p['life'] * 2)
            particle_surface = pygame.Surface((int(p['size'] * 2), int(p['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*p['color'], int(alpha)), 
                             (int(p['size']), int(p['size'])), int(p['size']))
            screen.blit(particle_surface, (int(p['x'] - p['size']), int(p['y'] - p['size'])))
        
        if fade_alpha < 255:
            fade_alpha = min(255, fade_alpha + fade_speed)
        
        curupira_face.draw(screen)
        dialogue_box.draw(screen)
        
        if fade_alpha > 200:
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 50))
        
        if fade_alpha < 255:
            fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, 255 - fade_alpha))
            screen.blit(fade_surface, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)

# ============================
# CUTSCENE 2: PERSEGUIÇÃO
# ============================

class CurupiraOnBoar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = CELL_SIZE * 1.5
        self.height = CELL_SIZE * 1.2
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.frame = 0
        self.animation_speed = 0.15
        self.spear_animation = 0
        self.running_frames = []
        self.create_running_frames()
    
    def create_running_frames(self):
        for frame_num in range(6):
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            center_x = self.width // 2
            center_y = self.height // 2
            boar_bounce = math.sin(frame_num * 1.0) * 5
            
            boar_length = CELL_SIZE * 0.7
            boar_height = CELL_SIZE * 0.45
            boar_x = center_x - boar_length // 2
            boar_y = center_y + CELL_SIZE // 8 + boar_bounce
            
            pygame.draw.ellipse(frame, BOAR_BROWN, (boar_x, boar_y, boar_length, boar_height))
            
            head_radius = CELL_SIZE // 6
            head_x = center_x + boar_length // 2 - head_radius
            head_y = center_y + boar_height // 2 + boar_bounce
            pygame.draw.circle(frame, BOAR_DARK_BROWN, (head_x, head_y), head_radius)
            
            snout_width = CELL_SIZE // 8
            snout_height = CELL_SIZE // 12
            snout_x = head_x + head_radius - snout_width // 2
            snout_y = head_y
            pygame.draw.ellipse(frame, BOAR_DARK_BROWN, (snout_x, snout_y - snout_height // 2, snout_width, snout_height))
            
            eye_radius = CELL_SIZE // 25
            pygame.draw.circle(frame, BLACK, (head_x - eye_radius, head_y - eye_radius), eye_radius)
            
            ear_radius = CELL_SIZE // 10
            pygame.draw.circle(frame, BOAR_DARK_BROWN, (head_x - ear_radius, head_y - head_radius), ear_radius)
            
            leg_width = CELL_SIZE // 10
            leg_height = CELL_SIZE // 6
            leg_offset = math.sin(frame_num * 1.5) * 8
            
            front_leg_height = leg_height - leg_offset if leg_offset > 0 else leg_height
            back_leg_height = leg_height + leg_offset if leg_offset > 0 else leg_height
            
            leg_positions = [
                (boar_x + boar_length * 0.2, boar_y + boar_height, front_leg_height),
                (boar_x + boar_length * 0.4, boar_y + boar_height, back_leg_height),
                (boar_x + boar_length * 0.6, boar_y + boar_height, front_leg_height),
                (boar_x + boar_length * 0.8, boar_y + boar_height, back_leg_height)
            ]
            
            for leg_x, leg_y, l_height in leg_positions:
                pygame.draw.rect(frame, BOAR_DARK_BROWN, 
                                (leg_x - leg_width // 2, leg_y - l_height, leg_width, l_height))
            
            curupira_x = center_x
            curupira_y = boar_y - CELL_SIZE // 8 + boar_bounce
            
            body_width = CELL_SIZE // 4
            body_height = CELL_SIZE // 5
            pygame.draw.ellipse(frame, CURUPIRA_SKIN, 
                              (curupira_x - body_width // 2, curupira_y, body_width, body_height))
            
            arm_width = CELL_SIZE // 12
            arm_height = CELL_SIZE // 6
            pygame.draw.ellipse(frame, CURUPIRA_SKIN, 
                              (curupira_x - body_width // 2 - arm_width // 2, curupira_y, arm_width, arm_height))
            pygame.draw.ellipse(frame, CURUPIRA_SKIN, 
                              (curupira_x + body_width // 2 - arm_width // 2, curupira_y, arm_width, arm_height))
            
            skirt_width = CELL_SIZE // 3
            skirt_height = CELL_SIZE // 8
            skirt_y = curupira_y + body_height - 2
            pygame.draw.ellipse(frame, CURUPIRA_SKIRT, 
                              (curupira_x - skirt_width // 2, skirt_y, skirt_width, skirt_height))
            
            head_radius = CELL_SIZE // 6
            head_y_pos = curupira_y - head_radius // 2
            pygame.draw.circle(frame, CURUPIRA_SKIN, (curupira_x, head_y_pos), head_radius)
            
            self.draw_fire_hair(frame, curupira_x, head_y_pos, head_radius)
            
            eye_radius = head_radius // 4
            eye_y = head_y_pos + head_radius * 0.2
            pygame.draw.circle(frame, WHITE, (curupira_x - eye_radius, eye_y), eye_radius)
            pygame.draw.circle(frame, WHITE, (curupira_x + eye_radius, eye_y), eye_radius)
            pygame.draw.circle(frame, BLACK, (curupira_x - eye_radius, eye_y), eye_radius//2)
            pygame.draw.circle(frame, BLACK, (curupira_x + eye_radius, eye_y), eye_radius//2)
            
            self.draw_spear(frame, curupira_x, curupira_y, frame_num)
            
            self.running_frames.append(frame)
    
    def draw_fire_hair(self, surface, x, y, head_radius):
        fire_height = head_radius * 2.5
        base_width = head_radius * 1.8
        pygame.draw.ellipse(surface, CURUPIRA_HAIR, 
                          (x - base_width // 2, y - head_radius - fire_height * 0.1, base_width, fire_height * 0.4))
        
        flame_count = 7
        for i in range(flame_count):
            flame_x = x - base_width // 2 + (base_width / (flame_count - 1)) * i
            flame_height = fire_height * (0.6 + 0.4 * (i % 3) / 3)
            
            points = [
                (flame_x, y - head_radius),
                (flame_x - base_width * 0.15, y - head_radius - flame_height * 0.4),
                (flame_x, y - head_radius - flame_height),
                (flame_x + base_width * 0.15, y - head_radius - flame_height * 0.4)
            ]
            pygame.draw.polygon(surface, FIRE_ORANGE, points)
            
            inner_height = flame_height * 0.7
            inner_points = [
                (flame_x, y - head_radius),
                (flame_x - base_width * 0.08, y - head_radius - inner_height * 0.3),
                (flame_x, y - head_radius - inner_height),
                (flame_x + base_width * 0.08, y - head_radius - inner_height * 0.3)
            ]
            pygame.draw.polygon(surface, FIRE_YELLOW, inner_points)
            
            if i % 2 == 0:
                spark_y = y - head_radius - flame_height
                spark_radius = head_radius // 8
                pygame.draw.circle(surface, FIRE_YELLOW, (int(flame_x), int(spark_y)), spark_radius)
    
    def draw_spear(self, surface, x, y, frame_num):
        spear_length = CELL_SIZE * 0.8
        spear_width = CELL_SIZE // 25
        spear_offset = math.sin(frame_num * 0.8) * 3
        
        pygame.draw.rect(surface, SPEAR_BROWN, 
                        (x - CELL_SIZE // 2 - spear_length, y - spear_width // 2 + spear_offset, 
                         spear_length, spear_width))
        
        tip_height = CELL_SIZE // 8
        tip_points = [
            (x - CELL_SIZE // 2, y + spear_offset),
            (x - CELL_SIZE // 2 + tip_height, y - tip_height // 2 + spear_offset),
            (x - CELL_SIZE // 2 + tip_height, y + tip_height // 2 + spear_offset)
        ]
        pygame.draw.polygon(surface, SPEAR_METAL, tip_points)
        
        for i in range(2):
            decoration_x = x - CELL_SIZE // 2 - spear_length * (0.3 + i * 0.4)
            pygame.draw.rect(surface, SPEAR_METAL, 
                           (decoration_x, y - spear_width + spear_offset, spear_width * 2, spear_width * 3))
    
    def update(self):
        self.rect.x += self.speed
        self.frame += self.animation_speed
        self.spear_animation += 0.1
        
        if self.frame >= len(self.running_frames):
            self.frame = 0
        
        self.image = self.running_frames[int(self.frame)]

class Hunter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = CELL_SIZE // 4
        self.width = CELL_SIZE
        self.height = CELL_SIZE * 1.2
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4
        self.frame = 0
        self.animation_speed = 0.15
        self.running_frames = []
        self.create_running_frames()
    
    def draw_hunter(self, surface, center_x, center_y, leg_offset=0):
        hat_width = CELL_SIZE // 2
        hat_height = CELL_SIZE // 4
        pygame.draw.rect(surface, HUNTER_HAT, 
                       (center_x - hat_width//2, center_y - self.radius - hat_height//2, 
                        hat_width, hat_height))
        
        pygame.draw.circle(surface, HUNTER_SKIN, (center_x, center_y - self.radius//2), self.radius//2)
        
        body_width = CELL_SIZE // 2
        body_height = CELL_SIZE // 2
        pygame.draw.rect(surface, HUNTER_RED, 
                       (center_x - body_width//2, center_y - self.radius//2, 
                        body_width, body_height))
        
        pants_width = CELL_SIZE // 3
        pants_height = CELL_SIZE // 4
        pygame.draw.rect(surface, HUNTER_PANTS, 
                       (center_x - pants_width//2, center_y + self.radius//2, 
                        pants_width, pants_height))
        
        gun_length = CELL_SIZE // 1.5
        gun_width = CELL_SIZE // 10
        pygame.draw.rect(surface, GUN_BROWN, 
                       (center_x + self.radius//2, center_y - gun_width//2, 
                        gun_length, gun_width))
        pygame.draw.rect(surface, (80, 50, 30), 
                       (center_x + self.radius//2 - gun_length//4, center_y - gun_width//2, 
                        gun_length//4, gun_width))
        
        eye_radius = self.radius // 8
        pygame.draw.circle(surface, WHITE, (center_x - eye_radius, center_y - self.radius//2), eye_radius)
        pygame.draw.circle(surface, WHITE, (center_x + eye_radius, center_y - self.radius//2), eye_radius)
        pygame.draw.circle(surface, BLACK, (center_x - eye_radius, center_y - self.radius//2), eye_radius//2)
        pygame.draw.circle(surface, BLACK, (center_x + eye_radius, center_y - self.radius//2), eye_radius//2)
        
        leg_width = CELL_SIZE // 10
        leg_height = CELL_SIZE // 3
        
        left_leg_height = leg_height - leg_offset if leg_offset > 0 else leg_height
        right_leg_height = leg_height + leg_offset if leg_offset > 0 else leg_height
        
        pygame.draw.rect(surface, HUNTER_PANTS, 
                       (center_x - pants_width//3 - leg_width//2, 
                        center_y + self.radius//2 + pants_height - 5, 
                        leg_width, left_leg_height))
        
        pygame.draw.rect(surface, HUNTER_PANTS, 
                       (center_x + pants_width//3 - leg_width//2, 
                        center_y + self.radius//2 + pants_height - 5, 
                        leg_width, right_leg_height))
        
        pygame.draw.arc(surface, (220, 20, 60), 
                       (center_x - eye_radius*2, center_y - self.radius//3, eye_radius*4, eye_radius*3), 
                       0, 3.14, 2)
    
    def create_running_frames(self):
        for i in range(6):
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            center_x = self.width // 2
            center_y = self.height // 2
            bounce = math.sin(i * 1.0) * 3
            leg_offset = math.sin(i * 1.5) * 8
            
            self.draw_hunter(frame, center_x, center_y + bounce, leg_offset)
            
            shadow_y = center_y + self.radius//2 + CELL_SIZE//2 + 5
            shadow_width = CELL_SIZE // 2
            shadow_height = CELL_SIZE // 10
            pygame.draw.ellipse(frame, (0, 0, 0, 100), 
                              (center_x - shadow_width//2, shadow_y, shadow_width, shadow_height))
            
            self.running_frames.append(frame)
    
    def update(self):
        self.rect.x += self.speed
        self.frame += self.animation_speed
        if self.frame >= len(self.running_frames):
            self.frame = 0
        self.image = self.running_frames[int(self.frame)]

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size*2), pygame.SRCALPHA)
        self.draw_tree(size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw_tree(self, size):
        trunk_width = size // 4
        trunk_height = size
        pygame.draw.rect(self.image, BROWN, 
                        (size//2 - trunk_width//2, size, trunk_width, trunk_height))
        
        pygame.draw.circle(self.image, TREE_GREEN, (size//2, size//2), size//2)
        pygame.draw.circle(self.image, (0, 120, 0), (size//2 - size//4, size//2 - size//6), size//3)
        pygame.draw.circle(self.image, (0, 120, 0), (size//2 + size//4, size//2 - size//6), size//3)

class Bush(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
        self.draw_bush()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw_bush(self):
        pygame.draw.circle(self.image, (0, 150, 0), (15, 20), 15)
        pygame.draw.circle(self.image, (0, 150, 0), (30, 15), 15)
        pygame.draw.circle(self.image, (0, 150, 0), (45, 20), 15)
        pygame.draw.circle(self.image, (0, 170, 0), (20, 30), 12)
        pygame.draw.circle(self.image, (0, 170, 0), (40, 30), 12)

def draw_background():
    screen.fill(SKY_BLUE)
    
    pygame.draw.circle(screen, (255, 255, 150), (900, 80), 50)
    
    for i in range(3):
        cloud_x = 100 + i * 250
        cloud_y = 100 + (i % 2) * 20
        pygame.draw.ellipse(screen, (240, 240, 240), (cloud_x, cloud_y, 100, 40))
        pygame.draw.ellipse(screen, (240, 240, 240), (cloud_x + 30, cloud_y - 15, 80, 40))
        pygame.draw.ellipse(screen, (240, 240, 240), (cloud_x - 20, cloud_y + 10, 80, 40))
    
    pygame.draw.polygon(screen, (50, 120, 50), [(0, 300), (200, 100), (400, 300)])
    pygame.draw.polygon(screen, (40, 110, 40), [(300, 300), (500, 150), (700, 300)])
    pygame.draw.polygon(screen, (30, 100, 30), [(600, 300), (900, 180), (1000, 300)])
    
    pygame.draw.rect(screen, GROUND_GREEN, (0, 300, WIDTH, HEIGHT-300))
    
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, (0, 100, 0), (i, 300), (i, HEIGHT), 2)
    
    for i in range(300, HEIGHT, 40):
        pygame.draw.line(screen, (0, 100, 0), (0, i), (WIDTH, i), 2)

def chase_scene():
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    bushes = pygame.sprite.Group()
    
    tree_positions = [(50, 250), (150, 280), (300, 260), (450, 270), 
                      (600, 250), (750, 280), (200, 320), (350, 310),
                      (500, 320), (650, 310), (800, 280), (900, 300)]
    
    for i, (x, y) in enumerate(tree_positions):
        size = 60 + (i % 3) * 20
        tree = Tree(x, y, size)
        trees.add(tree)
        all_sprites.add(tree)
    
    bush_positions = [(100, 380), (250, 400), (400, 390), (550, 380),
                      (700, 400), (50, 420), (200, 410), (350, 420),
                      (500, 410), (650, 420), (800, 400), (950, 410)]
    
    for x, y in bush_positions:
        bush = Bush(x, y)
        bushes.add(bush)
        all_sprites.add(bush)
    
    curupira = CurupiraOnBoar(-150, 380)
    hunter = Hunter(-250, 380)
    
    all_sprites.add(curupira, hunter)
    
    title_text = font.render("A FUGA DO CURUPIRA", True, (255, 255, 220))
    subtitle_text = small_font.render("Montado em seu javali, ele foge do caçador", True, (220, 220, 200))
    instruction_text = small_font.render("Cutscene em andamento...", True, (255, 255, 255))
    end_text = font.render("FIM DA CENA", True, (255, 255, 0))
    
    scene_started = False
    scene_ended = False
    frame_count = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not scene_started:
                    scene_started = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r and scene_ended:
                    return True
        
        draw_background()
        trees.draw(screen)
        bushes.draw(screen)
        
        if not scene_started:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//2))
            start_text = small_font.render("Pressione ESPAÇO para iniciar a cutscene", True, (255, 255, 255))
            screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 50))
        else:
            if not scene_ended:
                curupira.update()
                hunter.update()
                frame_count += 1
            
            all_sprites.draw(screen)
            
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, 20))
            
            if curupira.rect.x > WIDTH and hunter.rect.x > WIDTH and not scene_ended:
                scene_ended = True
            
            if scene_ended:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                
                screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2))
                restart_text = small_font.render("Pressione R para continuar para o jogo", True, (255, 255, 255))
                screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
        
        pygame.display.flip()
        clock.tick(60)

# ============================
# JOGO PRINCIPAL
# ============================

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = CELL_SIZE // 3
        self.footprint_cooldown = 0
        self.move_timer = 0
        self.move_delay = PLAYER_SPEED
        self.footprints = []
        self.fire_animation = 0
        self.spear_animation = 0
        
    def move(self, dx, dy, maze):
        self.move_timer += 1
        if self.move_timer < self.move_delay:
            return False
            
        self.move_timer = 0
        new_x = self.x + dx
        new_y = self.y + dy
        
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and not maze[new_y][new_x]:
            self.footprints.append((self.x, self.y, 0))
            self.x = new_x
            self.y = new_y
            return True
        return False
            
    def draw(self, screen):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        
        boar_length = CELL_SIZE * 0.6
        boar_height = CELL_SIZE * 0.4
        boar_x = center_x - boar_length // 2
        boar_y = center_y + CELL_SIZE // 8
        
        pygame.draw.ellipse(screen, BOAR_BROWN, (boar_x, boar_y, boar_length, boar_height))
        
        head_radius = CELL_SIZE // 6
        head_x = center_x + boar_length // 2 - head_radius
        head_y = center_y + boar_height // 2
        pygame.draw.circle(screen, BOAR_DARK_BROWN, (head_x, head_y), head_radius)
        
        snout_width = CELL_SIZE // 8
        snout_height = CELL_SIZE // 12
        snout_x = head_x + head_radius - snout_width // 2
        snout_y = head_y
        pygame.draw.ellipse(screen, BOAR_DARK_BROWN, (snout_x, snout_y - snout_height // 2, snout_width, snout_height))
        
        eye_radius = CELL_SIZE // 25
        pygame.draw.circle(screen, BLACK, (head_x - eye_radius, head_y - eye_radius), eye_radius)
        
        ear_radius = CELL_SIZE // 10
        pygame.draw.circle(screen, BOAR_DARK_BROWN, (head_x - ear_radius, head_y - head_radius), ear_radius)
        
        leg_width = CELL_SIZE // 10
        leg_height = CELL_SIZE // 6
        leg_positions = [
            (boar_x + boar_length * 0.2, boar_y + boar_height),
            (boar_x + boar_length * 0.4, boar_y + boar_height),
            (boar_x + boar_length * 0.6, boar_y + boar_height),
            (boar_x + boar_length * 0.8, boar_y + boar_height)
        ]
        for leg_x, leg_y in leg_positions:
            pygame.draw.rect(screen, BOAR_DARK_BROWN, (leg_x - leg_width // 2, leg_y - leg_height, leg_width, leg_height))
        
        curupira_x = center_x
        curupira_y = boar_y - CELL_SIZE // 8
        
        body_width = CELL_SIZE // 4
        body_height = CELL_SIZE // 5
        pygame.draw.ellipse(screen, CURUPIRA_SKIN, (curupira_x - body_width // 2, curupira_y, body_width, body_height))
        
        arm_width = CELL_SIZE // 12
        arm_height = CELL_SIZE // 6
        pygame.draw.ellipse(screen, CURUPIRA_SKIN, (curupira_x - body_width // 2 - arm_width // 2, curupira_y, arm_width, arm_height))
        pygame.draw.ellipse(screen, CURUPIRA_SKIN, (curupira_x + body_width // 2 - arm_width // 2, curupira_y, arm_width, arm_height))
        
        skirt_width = CELL_SIZE // 3
        skirt_height = CELL_SIZE // 8
        skirt_y = curupira_y + body_height - 2
        pygame.draw.ellipse(screen, CURUPIRA_SKIRT, (curupira_x - skirt_width // 2, skirt_y, skirt_width, skirt_height))
        
        head_radius = CELL_SIZE // 6
        head_y_pos = curupira_y - head_radius // 2
        pygame.draw.circle(screen, CURUPIRA_SKIN, (curupira_x, head_y_pos), head_radius)
        
        self.draw_fire_hair(screen, curupira_x, head_y_pos, head_radius)
        
        eye_radius = head_radius // 4
        eye_y = head_y_pos + head_radius * 0.2
        pygame.draw.circle(screen, WHITE, (curupira_x - eye_radius, eye_y), eye_radius)
        pygame.draw.circle(screen, WHITE, (curupira_x + eye_radius, eye_y), eye_radius)
        pygame.draw.circle(screen, BLACK, (curupira_x - eye_radius, eye_y), eye_radius//2)
        pygame.draw.circle(screen, BLACK, (curupira_x + eye_radius, eye_y), eye_radius//2)
        
        self.draw_spear(screen, curupira_x, curupira_y)
        
        if self.footprint_cooldown > 0:
            cooldown_percent = self.footprint_cooldown / FOOTPRINT_COOLDOWN
            angle = 360 * cooldown_percent
            pygame.draw.arc(screen, YELLOW, 
                           (center_x - self.radius, center_y - self.radius,
                            self.radius * 2, self.radius * 2),
                           0, -angle, 3)
        
        if self.fire_animation > 0:
            self.draw_fire_animation(screen, center_x, center_y)
    
    def draw_fire_hair(self, screen, x, y, head_radius):
        fire_height = head_radius * 2.5
        base_width = head_radius * 1.8
        pygame.draw.ellipse(screen, CURUPIRA_HAIR, (x - base_width // 2, y - head_radius - fire_height * 0.1, base_width, fire_height * 0.4))
        
        flame_count = 7
        for i in range(flame_count):
            flame_x = x - base_width // 2 + (base_width / (flame_count - 1)) * i
            flame_height = fire_height * (0.6 + 0.4 * (i % 3) / 3)
            
            points = [
                (flame_x, y - head_radius),
                (flame_x - base_width * 0.15, y - head_radius - flame_height * 0.4),
                (flame_x, y - head_radius - flame_height),
                (flame_x + base_width * 0.15, y - head_radius - flame_height * 0.4)
            ]
            pygame.draw.polygon(screen, FIRE_ORANGE, points)
            
            inner_height = flame_height * 0.7
            inner_points = [
                (flame_x, y - head_radius),
                (flame_x - base_width * 0.08, y - head_radius - inner_height * 0.3),
                (flame_x, y - head_radius - inner_height),
                (flame_x + base_width * 0.08, y - head_radius - inner_height * 0.3)
            ]
            pygame.draw.polygon(screen, FIRE_YELLOW, inner_points)
            
            if i % 2 == 0:
                spark_y = y - head_radius - flame_height
                spark_radius = head_radius // 8
                pygame.draw.circle(screen, FIRE_YELLOW, (int(flame_x), int(spark_y)), spark_radius)
    
    def draw_spear(self, screen, x, y):
        spear_length = CELL_SIZE * 1.0
        spear_width = CELL_SIZE // 25
        spear_offset = math.sin(self.spear_animation * 0.5) * 2
        
        pygame.draw.rect(screen, SPEAR_BROWN, 
                        (x + CELL_SIZE // 8, y - spear_width // 2 + spear_offset, 
                         spear_length, spear_width))
        
        tip_height = CELL_SIZE // 8
        tip_points = [
            (x + CELL_SIZE // 8 + spear_length, y + spear_offset),
            (x + CELL_SIZE // 8 + spear_length - tip_height, y - tip_height // 2 + spear_offset),
            (x + CELL_SIZE // 8 + spear_length - tip_height, y + tip_height // 2 + spear_offset)
        ]
        pygame.draw.polygon(screen, SPEAR_METAL, tip_points)
        
        for i in range(2):
            decoration_x = x + CELL_SIZE // 8 + spear_length * (0.3 + i * 0.4)
            pygame.draw.rect(screen, SPEAR_METAL, 
                           (decoration_x, y - spear_width + spear_offset, spear_width * 2, spear_width * 3))
    
    def draw_fire_animation(self, screen, center_x, center_y):
        fire_radius = self.radius * 1.5
        outer_alpha = min(200, self.fire_animation * 20)
        temp_surface = pygame.Surface((fire_radius * 4, fire_radius * 4), pygame.SRCALPHA)
        
        for i in range(12):
            angle = (i * 30 + self.fire_animation * 10) * 3.14 / 180
            flame_length = fire_radius * (0.8 + 0.4 * (i % 3) / 3)
            flame_x = center_x + math.cos(angle) * flame_length
            flame_y = center_y + math.sin(angle) * flame_length
            
            points = [
                (center_x, center_y),
                (flame_x - flame_length * 0.3, flame_y - flame_length * 0.3),
                (flame_x, flame_y),
                (flame_x + flame_length * 0.3, flame_y - flame_length * 0.3)
            ]
            pygame.draw.polygon(temp_surface, (*FIRE_ORANGE, outer_alpha), points)
            
            inner_flame_length = flame_length * 0.6
            inner_flame_x = center_x + math.cos(angle) * inner_flame_length
            inner_flame_y = center_y + math.sin(angle) * inner_flame_length
            
            inner_points = [
                (center_x, center_y),
                (inner_flame_x - inner_flame_length * 0.2, inner_flame_y - inner_flame_length * 0.2),
                (inner_flame_x, inner_flame_y),
                (inner_flame_x + inner_flame_length * 0.2, inner_flame_y - inner_flame_length * 0.2)
            ]
            pygame.draw.polygon(temp_surface, (*FIRE_YELLOW, outer_alpha), inner_points)
        
        screen.blit(temp_surface, (center_x - fire_radius * 2, center_y - fire_radius * 2))
    
    def can_drop_footprint(self):
        return self.footprint_cooldown <= 0
        
    def drop_footprint(self):
        if self.can_drop_footprint():
            self.footprint_cooldown = FOOTPRINT_COOLDOWN
            self.fire_animation = 10
            return True
        return False
    
    def update(self):
        if self.footprint_cooldown > 0:
            self.footprint_cooldown -= 1
        
        if self.fire_animation > 0:
            self.fire_animation -= 1
        
        self.spear_animation += 1
        
        new_footprints = []
        for x, y, progress in self.footprints:
            progress += 1
            if progress <= FOOTPRINT_DURATION:
                new_footprints.append((x, y, progress))
        self.footprints = new_footprints
    
    def draw_footprints(self, screen):
        for x, y, progress in self.footprints:
            if progress < FOOTPRINT_DURATION / 2:
                alpha = int(255 * (progress / (FOOTPRINT_DURATION / 2)))
            else:
                alpha = int(255 * (1 - (progress - FOOTPRINT_DURATION / 2) / (FOOTPRINT_DURATION / 2)))
            
            footprint_color = (*FOOTPRINT_COLOR, alpha)
            
            temp_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            
            footprint_radius = CELL_SIZE // 8
            
            footprints_positions = [
                (CELL_SIZE // 4, 2 * CELL_SIZE // 3),
                (3 * CELL_SIZE // 4, 2 * CELL_SIZE // 3),
                (CELL_SIZE // 3, 3 * CELL_SIZE // 4),
                (2 * CELL_SIZE // 3, 3 * CELL_SIZE // 4)
            ]
            
            for pos_x, pos_y in footprints_positions:
                offset_x = random.randint(-2, 2)
                offset_y = random.randint(-2, 2)
                pygame.draw.circle(temp_surface, footprint_color, 
                                 (pos_x + offset_x, pos_y + offset_y), 
                                 footprint_radius)
            
            screen.blit(temp_surface, (x * CELL_SIZE, y * CELL_SIZE))

class FirePortal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_timer = 0
    
    def draw(self, screen):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        portal_radius = CELL_SIZE // 2 - 2
        
        self.animation_timer += 1
        
        pygame.draw.circle(screen, PORTAL_ORANGE, (center_x, center_y), portal_radius)
        
        inner_radius = portal_radius * (0.6 + 0.2 * math.sin(self.animation_timer * 0.2))
        pygame.draw.circle(screen, PORTAL_YELLOW, (center_x, center_y), inner_radius)
        
        for i in range(8):
            angle = (i * 45 + self.animation_timer * 3) * 3.14 / 180
            flame_length = portal_radius * 0.8
            flame_x = center_x + math.cos(angle) * (portal_radius + flame_length * 0.3)
            flame_y = center_y + math.sin(angle) * (portal_radius + flame_length * 0.3)
            
            points = [
                (center_x + math.cos(angle) * portal_radius, 
                 center_y + math.sin(angle) * portal_radius),
                (flame_x - flame_length * 0.2, flame_y),
                (flame_x, flame_y - flame_length * 0.4),
                (flame_x + flame_length * 0.2, flame_y)
            ]
            pygame.draw.polygon(screen, FIRE_RED, points)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = CELL_SIZE // 3
        self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        self.reversed = False
        self.reversal_timer = 0
        self.move_timer = 0
        self.move_delay = ENEMY_SPEED
        
    def move(self, maze, player_x, player_y, is_reversed):
        self.move_timer += 1
        if self.move_timer < self.move_delay:
            return
            
        self.move_timer = 0
        
        if is_reversed and not self.reversed:
            self.reversed = True
            self.reversal_timer = REVERSAL_DURATION
        
        if self.reversal_timer > 0:
            self.reversal_timer -= 1
        else:
            self.reversed = False
        
        if self.reversed:
            dx = 0
            dy = 0
            if player_x > self.x:
                dx = -1
            elif player_x < self.x:
                dx = 1
            if player_y > self.y:
                dy = -1
            elif player_y < self.y:
                dy = 1
        else:
            dx = 0
            dy = 0
            if player_x > self.x:
                dx = 1
            elif player_x < self.x:
                dx = -1
            if player_y > self.y:
                dy = 1
            elif player_y < self.y:
                dy = -1
        
        if abs(dx) > abs(dy):
            self.direction = (dx, 0)
        elif abs(dy) > abs(dx):
            self.direction = (0, dy)
        else:
            if random.random() < 0.5 and dx != 0:
                self.direction = (dx, 0)
            elif dy != 0:
                self.direction = (0, dy)
        
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and not maze[new_y][new_x]:
            self.x = new_x
            self.y = new_y
        else:
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and not maze[new_y][new_x]:
                    self.direction = (dx, dy)
                    self.x = new_x
                    self.y = new_y
                    break
    
    def draw(self, screen):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        
        if not self.reversed:
            hat_width = CELL_SIZE // 2
            hat_height = CELL_SIZE // 4
            pygame.draw.rect(screen, HUNTER_HAT, 
                           (center_x - hat_width//2, center_y - self.radius - hat_height//2, 
                            hat_width, hat_height))
            
            pygame.draw.circle(screen, HUNTER_SKIN, (center_x, center_y - self.radius//2), self.radius//2)
            
            body_width = CELL_SIZE // 2
            body_height = CELL_SIZE // 2
            pygame.draw.rect(screen, HUNTER_RED, 
                           (center_x - body_width//2, center_y - self.radius//2, 
                            body_width, body_height))
            
            pants_width = CELL_SIZE // 3
            pants_height = CELL_SIZE // 4
            pygame.draw.rect(screen, HUNTER_PANTS, 
                           (center_x - pants_width//2, center_y + self.radius//2, 
                            pants_width, pants_height))
            
            gun_length = CELL_SIZE // 1.5
            gun_width = CELL_SIZE // 10
            pygame.draw.rect(screen, GUN_BROWN, 
                           (center_x + self.radius//2, center_y - gun_width//2, 
                            gun_length, gun_width))
            pygame.draw.rect(screen, (80, 50, 30), 
                           (center_x + self.radius//2 - gun_length//4, center_y - gun_width//2, 
                            gun_length//4, gun_width))
            
            eye_radius = self.radius // 8
            pygame.draw.circle(screen, WHITE, (center_x - eye_radius, center_y - self.radius//2), eye_radius)
            pygame.draw.circle(screen, WHITE, (center_x + eye_radius, center_y - self.radius//2), eye_radius)
            pygame.draw.circle(screen, BLACK, (center_x - eye_radius, center_y - self.radius//2), eye_radius//2)
            pygame.draw.circle(screen, BLACK, (center_x + eye_radius, center_y - self.radius//2), eye_radius//2)
            
        else:
            pygame.draw.circle(screen, HUNTER_SKIN, (center_x, center_y - self.radius//2), self.radius//2)
            
            body_width = CELL_SIZE // 2
            body_height = CELL_SIZE // 2
            pygame.draw.rect(screen, HUNTER_BLUE, 
                           (center_x - body_width//2, center_y - self.radius//2, 
                            body_width, body_height))
            
            pants_width = CELL_SIZE // 3
            pants_height = CELL_SIZE // 4
            pygame.draw.rect(screen, HUNTER_PANTS, 
                           (center_x - pants_width//2, center_y + self.radius//2, 
                            pants_width, pants_height))
            
            eye_radius = self.radius // 8
            eye_offset = eye_radius
            
            pygame.draw.line(screen, BLACK, 
                           (center_x - eye_offset - eye_radius//2, center_y - self.radius//2 - eye_radius//2),
                           (center_x - eye_offset + eye_radius//2, center_y - self.radius//2 + eye_radius//2), 2)
            pygame.draw.line(screen, BLACK, 
                           (center_x - eye_offset - eye_radius//2, center_y - self.radius//2 + eye_radius//2),
                           (center_x - eye_offset + eye_radius//2, center_y - self.radius//2 - eye_radius//2), 2)
            
            pygame.draw.line(screen, BLACK, 
                           (center_x + eye_offset - eye_radius//2, center_y - self.radius//2 - eye_radius//2),
                           (center_x + eye_offset + eye_radius//2, center_y - self.radius//2 + eye_radius//2), 2)
            pygame.draw.line(screen, BLACK, 
                           (center_x + eye_offset - eye_radius//2, center_y - self.radius//2 + eye_radius//2),
                           (center_x + eye_offset + eye_radius//2, center_y - self.radius//2 - eye_radius//2), 2)
            
            if self.reversal_timer > REVERSAL_DURATION // 2:
                star_radius = self.radius // 6
                star_positions = [
                    (center_x - self.radius, center_y - self.radius),
                    (center_x + self.radius, center_y - self.radius),
                    (center_x - self.radius, center_y),
                    (center_x + self.radius, center_y)
                ]
                
                for pos_x, pos_y in star_positions:
                    pygame.draw.circle(screen, YELLOW, (int(pos_x), int(pos_y)), star_radius)

def draw_tree(screen, x, y):
    trunk_width = CELL_SIZE // 4
    trunk_height = CELL_SIZE // 2
    trunk_x = x * CELL_SIZE + (CELL_SIZE - trunk_width) // 2
    trunk_y = y * CELL_SIZE + (CELL_SIZE - trunk_height) // 2
    
    pygame.draw.rect(screen, TRUNK_BROWN, 
                    (trunk_x, trunk_y, trunk_width, trunk_height))
    
    leaf_radius = CELL_SIZE // 3
    leaf_centers = [
        (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 4),
        (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 3),
        (x * CELL_SIZE + 3 * CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 3),
        (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 6)
    ]
    
    for center_x, center_y in leaf_centers:
        pygame.draw.circle(screen, FOREST_GREEN, (center_x, center_y), leaf_radius)

def draw_stones(screen, x, y, stone_positions):
    for stone_x, stone_y in stone_positions:
        if stone_x == x and stone_y == y:
            stone_size = CELL_SIZE // 8
            positions = [
                (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4),
                (x * CELL_SIZE + 3 * CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 3),
                (x * CELL_SIZE + CELL_SIZE // 3, y * CELL_SIZE + 3 * CELL_SIZE // 4),
                (x * CELL_SIZE + 2 * CELL_SIZE // 3, y * CELL_SIZE + CELL_SIZE // 2)
            ]
            
            for pos_x, pos_y in positions:
                pygame.draw.circle(screen, STONE_GRAY, (pos_x, pos_y), stone_size)
                pygame.draw.circle(screen, (100, 100, 100), (pos_x - 1, pos_y - 1), stone_size)

def generate_maze():
    maze = [[True for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    def is_valid(x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT
    
    def get_unvisited_neighbors(x, y):
        neighbors = []
        for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and maze[ny][nx]:
                neighbors.append((nx, ny))
        return neighbors
    
    start_x, start_y = 1, 1
    maze[start_y][start_x] = False
    
    stack = [(start_x, start_y)]
    
    while stack:
        x, y = stack[-1]
        neighbors = get_unvisited_neighbors(x, y)
        
        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[(y + ny) // 2][(x + nx) // 2] = False
            maze[ny][nx] = False
            stack.append((nx, ny))
        else:
            stack.pop()
    
    maze[GRID_HEIGHT-2][GRID_WIDTH-2] = False
    
    for _ in range(GRID_WIDTH * GRID_HEIGHT // 20):
        x, y = random.randint(1, GRID_WIDTH-2), random.randint(1, GRID_HEIGHT-2)
        if maze[y][x]:
            empty_neighbors = 0
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny) and not maze[ny][nx]:
                    empty_neighbors += 1
            if empty_neighbors >= 2:
                maze[y][x] = False
    
    return maze

def generate_stone_positions(maze):
    stone_positions = set()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not maze[y][x] and random.random() < 0.3:
                stone_positions.add((x, y))
    return stone_positions

def draw_maze(screen, maze, tree_positions, stone_positions, level):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x]:
                pygame.draw.rect(screen, DARK_GREEN, 
                                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                
                if (x, y) in tree_positions:
                    draw_tree(screen, x, y)
                
            else:
                pygame.draw.rect(screen, PATH_BROWN, 
                                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                
                draw_stones(screen, x, y, stone_positions)
                
                pygame.draw.rect(screen, (140, 100, 60), 
                                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def generate_tree_positions(maze):
    tree_positions = set()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] and random.random() < 0.7:
                tree_positions.add((x, y))
    return tree_positions

def find_valid_position(maze, min_distance=5):
    while True:
        x = random.randint(1, GRID_WIDTH - 2)
        y = random.randint(1, GRID_HEIGHT - 2)
        if not maze[y][x]:
            distance = abs(x - 1) + abs(y - 1)
            if distance >= min_distance:
                return x, y

def show_instructions():
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    
    title = font_large.render("INSTRUÇÕES DO JOGO", True, YELLOW)
    instruction1 = font.render("Use as setas do teclado para mover o Curupira", True, WHITE)
    instruction2 = font.render("Pressione ESPAÇO para deixar pegadas mágicas", True, WHITE)
    instruction3 = font.render("As pegadas confundem os caçadores temporariamente", True, WHITE)
    instruction4 = font.render("Encontre o portal de fogo para passar de nível", True, WHITE)
    instruction5 = font.render("Evite ser pego pelos caçadores!", True, WHITE)
    continue_text = font.render("Pressione ESPAÇO para começar", True, GREEN)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        
        screen.fill((0, 0, 0))
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        screen.blit(instruction1, (WIDTH//2 - instruction1.get_width()//2, 150))
        screen.blit(instruction2, (WIDTH//2 - instruction2.get_width()//2, 200))
        screen.blit(instruction3, (WIDTH//2 - instruction3.get_width()//2, 250))
        screen.blit(instruction4, (WIDTH//2 - instruction4.get_width()//2, 300))
        screen.blit(instruction5, (WIDTH//2 - instruction5.get_width()//2, 350))
        screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, 450))
        
        pygame.display.flip()
        clock.tick(60)

def game_loop():
    clock = pygame.time.Clock()
    
    current_level = 1
    max_levels = 3
    base_enemies = 3
    
    maze = generate_maze()
    tree_positions = generate_tree_positions(maze)
    stone_positions = generate_stone_positions(maze)
    player = Player(1, 1)
    portal = FirePortal(GRID_WIDTH - 2, GRID_HEIGHT - 2)
    
    num_enemies = base_enemies + (current_level - 1)  
    enemies = []
    for _ in range(num_enemies):
        x, y = find_valid_position(maze, 8)
        enemies.append(Enemy(x, y))
    
    exit_x, exit_y = GRID_WIDTH - 2, GRID_HEIGHT - 2
    
    game_over = False
    game_won = False
    global_reversal = False
    reversal_timer = 0
    level_transition = False
    transition_timer = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over and not game_won and not level_transition:
                    if player.drop_footprint():
                        global_reversal = True
                        reversal_timer = REVERSAL_DURATION
                
                if (game_over or game_won) and event.key == pygame.K_r:
                    current_level = 1
                    maze = generate_maze()
                    tree_positions = generate_tree_positions(maze)
                    stone_positions = generate_stone_positions(maze)
                    player = Player(1, 1)
                    
                    num_enemies = base_enemies + (current_level - 1)
                    enemies = []
                    for _ in range(num_enemies):
                        x, y = find_valid_position(maze, 8)
                        enemies.append(Enemy(x, y))
                    
                    game_over = False
                    game_won = False
                    global_reversal = False
                    reversal_timer = 0
                    level_transition = False
        
        if not game_over and not game_won and not level_transition:
            keys = pygame.key.get_pressed()
            moved = False
            if keys[pygame.K_LEFT]:
                moved = player.move(-1, 0, maze)
            elif keys[pygame.K_RIGHT]:
                moved = player.move(1, 0, maze)
            elif keys[pygame.K_UP]:
                moved = player.move(0, -1, maze)
            elif keys[pygame.K_DOWN]:
                moved = player.move(0, 1, maze)
            
            player.update()
            
            if reversal_timer > 0:
                reversal_timer -= 1
            else:
                global_reversal = False
            
            for enemy in enemies:
                enemy.move(maze, player.x, player.y, global_reversal)
                
                if enemy.x == player.x and enemy.y == player.y:
                    if not enemy.reversed:
                        game_over = True
            
            if player.x == exit_x and player.y == exit_y:
                if current_level < max_levels:
                    level_transition = True
                    transition_timer = 60
                else:
                    game_won = True
        
        if level_transition:
            transition_timer -= 1
            if transition_timer <= 0:
                current_level += 1
                
                maze = generate_maze()
                tree_positions = generate_tree_positions(maze)
                stone_positions = generate_stone_positions(maze)
                player = Player(1, 1)
                portal = FirePortal(GRID_WIDTH - 2, GRID_HEIGHT - 2)
                
                num_enemies = base_enemies + (current_level - 1)
                enemies = []
                for _ in range(num_enemies):
                    x, y = find_valid_position(maze, 8)
                    enemies.append(Enemy(x, y))
                
                level_transition = False
        
        background_color = LEVEL_BACKGROUNDS[current_level - 1]
        screen.fill(background_color)
        
        draw_maze(screen, maze, tree_positions, stone_positions, current_level)
        
        player.draw_footprints(screen)
        
        portal.draw(screen)
        
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        
        if global_reversal:
            reversal_text = font.render("MAGIA DO CURUPIRA ATIVA!", True, ORANGE)
            screen.blit(reversal_text, (WIDTH // 2 - reversal_text.get_width() // 2, 10))
            
            time_left = reversal_timer // 30 + 1
            timer_text = font.render(f"Tempo: {time_left}s", True, ORANGE)
            screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 50))
        
        level_text = font.render(f"Nível: {current_level}", True, WHITE)
        screen.blit(level_text, (10, 10))
        
        enemies_text = font.render(f"Caçadores: {len(enemies)}", True, WHITE)
        screen.blit(enemies_text, (10, 50))
        
        if level_transition:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            level_up_text = font.render(f"NÍVEL {current_level-1} CONCLUÍDO!", True, YELLOW)
            next_level_text = font.render(f"PREPARANDO NÍVEL {current_level}...", True, ORANGE)
            info_text = small_font.render(f"Novos caçadores aparecerão e a floresta ficará mais escura!", True, WHITE)
            
            screen.blit(level_up_text, (WIDTH // 2 - level_up_text.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(next_level_text, (WIDTH // 2 - next_level_text.get_width() // 2, HEIGHT // 2 - 10))
            screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 2 + 40))
        
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            game_over_text = font.render("GAME OVER", True, RED)
            level_text = font.render(f"Você chegou ao nível {current_level}", True, WHITE)
            restart_text = font.render("Pressione R para reiniciar", True, WHITE)
            
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 10))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
        
        if game_won:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            win_text = font.render("VOCÊ VENCEU TODOS OS NÍVEIS!", True, GREEN)
            congrats_text = font.render("Parabéns, você dominou a floresta!", True, YELLOW)
            restart_text = font.render("Pressione R para jogar novamente", True, WHITE)
            
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - 10))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
        
        pygame.display.flip()
        clock.tick(30)

def main():
    # Tela de abertura
    screen.fill((0, 0, 0))
    title = font_large.render("CURUPIRA - A LENDA DA FLORESTA", True, ORANGE)
    subtitle = font.render("Um jogo de aventura e magia do folclore brasileiro", True, YELLOW)
    start_text = font.render("Pressione ESPAÇO para começar", True, GREEN)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    break
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        else:
            screen.fill((0, 0, 0))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
            screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 - 20))
            screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 50))
            pygame.display.flip()
            clock.tick(60)
            continue
        break
    
    # Mostrar cutscene de diálogo
    dialogue_scene()
    
    # Mostrar cutscene de perseguição
    chase_scene()
    
    # Mostrar instruções do jogo
    show_instructions()
    
    # Iniciar o jogo principal
    game_loop()

if __name__ == "__main__":
    main()