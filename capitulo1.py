import pygame
import random
import sys
from collections import deque

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Curupira")

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

# Classe para o jogador (Curupira montado em javali)
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
        
        # Javali
        boar_length = CELL_SIZE * 0.6
        boar_height = CELL_SIZE * 0.4
        boar_x = center_x - boar_length // 2
        boar_y = center_y + CELL_SIZE // 8
        
        # Corpo principal do javali
        pygame.draw.ellipse(screen, BOAR_BROWN, (boar_x, boar_y, boar_length, boar_height))
        
        # Cabeça do javali
        head_radius = CELL_SIZE // 6
        head_x = center_x + boar_length // 2 - head_radius
        head_y = center_y + boar_height // 2
        pygame.draw.circle(screen, BOAR_DARK_BROWN, (head_x, head_y), head_radius)
        
        # Focinho do javali
        snout_width = CELL_SIZE // 8
        snout_height = CELL_SIZE // 12
        snout_x = head_x + head_radius - snout_width // 2
        snout_y = head_y
        pygame.draw.ellipse(screen, BOAR_DARK_BROWN, (snout_x, snout_y - snout_height // 2, snout_width, snout_height))
        
        # Olhos do javali
        eye_radius = CELL_SIZE // 25
        pygame.draw.circle(screen, BLACK, (head_x - eye_radius, head_y - eye_radius), eye_radius)
        
        # Orelhas do javali
        ear_radius = CELL_SIZE // 10
        pygame.draw.circle(screen, BOAR_DARK_BROWN, (head_x - ear_radius, head_y - head_radius), ear_radius)
        
        # Pernas do javali
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
        
        # Curupira montado no javali
        curupira_x = center_x
        curupira_y = boar_y - CELL_SIZE // 8
        
        # Corpo do Curupira
        body_width = CELL_SIZE // 4
        body_height = CELL_SIZE // 5
        pygame.draw.ellipse(screen, CURUPIRA_SKIN, (curupira_x - body_width // 2, curupira_y, body_width, body_height))
        
        # Braços do Curupira
        arm_width = CELL_SIZE // 12
        arm_height = CELL_SIZE // 6
        # Braço esquerdo
        pygame.draw.ellipse(screen, CURUPIRA_SKIN, (curupira_x - body_width // 2 - arm_width // 2, curupira_y, arm_width, arm_height))
        # Braço direito (segurando a lança)
        pygame.draw.ellipse(screen, CURUPIRA_SKIN, (curupira_x + body_width // 2 - arm_width // 2, curupira_y, arm_width, arm_height))
        
        # Saia verde do Curupira
        skirt_width = CELL_SIZE // 3
        skirt_height = CELL_SIZE // 8
        skirt_y = curupira_y + body_height - 2
        pygame.draw.ellipse(screen, CURUPIRA_SKIRT, (curupira_x - skirt_width // 2, skirt_y, skirt_width, skirt_height))
        
        # Cabeça do Curupira
        head_radius = CELL_SIZE // 6
        head_y_pos = curupira_y - head_radius // 2
        pygame.draw.circle(screen, CURUPIRA_SKIN, (curupira_x, head_y_pos), head_radius)
        
        # Cabelo de fogo do Curupira
        self.draw_fire_hair(screen, curupira_x, head_y_pos, head_radius)
        
        # Olhos virados para trás
        eye_radius = head_radius // 4
        eye_y = head_y_pos + head_radius * 0.2
        pygame.draw.circle(screen, WHITE, (curupira_x - eye_radius, eye_y), eye_radius)
        pygame.draw.circle(screen, WHITE, (curupira_x + eye_radius, eye_y), eye_radius)
        pygame.draw.circle(screen, BLACK, (curupira_x - eye_radius, eye_y), eye_radius//2)
        pygame.draw.circle(screen, BLACK, (curupira_x + eye_radius, eye_y), eye_radius//2)
        
        # Lança do Curupira apontando para a direita
        self.draw_spear(screen, curupira_x, curupira_y)
        
        # Desenhar cooldown da pegada
        if self.footprint_cooldown > 0:
            cooldown_percent = self.footprint_cooldown / FOOTPRINT_COOLDOWN
            angle = 360 * cooldown_percent
            pygame.draw.arc(screen, YELLOW, 
                           (center_x - self.radius, center_y - self.radius,
                            self.radius * 2, self.radius * 2),
                           0, -angle, 3)
        
        # Animação de fogo quando ativa a habilidade
        if self.fire_animation > 0:
            self.draw_fire_animation(screen, center_x, center_y)
    
    def draw_fire_hair(self, screen, x, y, head_radius):
        fire_height = head_radius * 2.5
        
        # Base do cabelo de fogo
        base_width = head_radius * 1.8
        pygame.draw.ellipse(screen, CURUPIRA_HAIR, (x - base_width // 2, y - head_radius - fire_height * 0.1, base_width, fire_height * 0.4))
        
        # Chamas principais para cima
        flame_count = 7
        for i in range(flame_count):
            flame_x = x - base_width // 2 + (base_width / (flame_count - 1)) * i
            flame_height = fire_height * (0.6 + 0.4 * (i % 3) / 3)
            
            # Chama laranja
            points = [
                (flame_x, y - head_radius),
                (flame_x - base_width * 0.15, y - head_radius - flame_height * 0.4),
                (flame_x, y - head_radius - flame_height),
                (flame_x + base_width * 0.15, y - head_radius - flame_height * 0.4)
            ]
            pygame.draw.polygon(screen, FIRE_ORANGE, points)
            
            # Chama amarela (interna)
            inner_height = flame_height * 0.7
            inner_points = [
                (flame_x, y - head_radius),
                (flame_x - base_width * 0.08, y - head_radius - inner_height * 0.3),
                (flame_x, y - head_radius - inner_height),
                (flame_x + base_width * 0.08, y - head_radius - inner_height * 0.3)
            ]
            pygame.draw.polygon(screen, FIRE_YELLOW, inner_points)
            
            # Pontas das chamas (efeito de fogo)
            if i % 2 == 0:
                spark_y = y - head_radius - flame_height
                spark_radius = head_radius // 8
                pygame.draw.circle(screen, FIRE_YELLOW, (int(flame_x), int(spark_y)), spark_radius)
    
    def draw_spear(self, screen, x, y):
        spear_length = CELL_SIZE * 1.0
        spear_width = CELL_SIZE // 25
        
        # Animação da lança
        spear_offset = math.sin(self.spear_animation * 0.5) * 2
        
        # Haste da lança (apontando para a direita)
        pygame.draw.rect(screen, SPEAR_BROWN, 
                        (x + CELL_SIZE // 8, y - spear_width // 2 + spear_offset, 
                         spear_length, spear_width))
        
        # Ponta metálica da lança
        tip_height = CELL_SIZE // 8
        tip_points = [
            (x + CELL_SIZE // 8 + spear_length, y + spear_offset),
            (x + CELL_SIZE // 8 + spear_length - tip_height, y - tip_height // 2 + spear_offset),
            (x + CELL_SIZE // 8 + spear_length - tip_height, y + tip_height // 2 + spear_offset)
        ]
        pygame.draw.polygon(screen, SPEAR_METAL, tip_points)
        
        # Detalhes na haste
        for i in range(2):
            decoration_x = x + CELL_SIZE // 8 + spear_length * (0.3 + i * 0.4)
            pygame.draw.rect(screen, SPEAR_METAL, 
                           (decoration_x, y - spear_width + spear_offset, spear_width * 2, spear_width * 3))
    
    def draw_fire_animation(self, screen, center_x, center_y):
        fire_radius = self.radius * 1.5
        
        # Camada externa do fogo
        outer_alpha = min(200, self.fire_animation * 20)
        temp_surface = pygame.Surface((fire_radius * 4, fire_radius * 4), pygame.SRCALPHA)
        
        # Desenhar chamas ao redor do javali
        for i in range(12):
            angle = (i * 30 + self.fire_animation * 10) * 3.14 / 180
            flame_length = fire_radius * (0.8 + 0.4 * (i % 3) / 3)
            flame_x = center_x + math.cos(angle) * flame_length
            flame_y = center_y + math.sin(angle) * flame_length
            
            # Chama laranja
            points = [
                (center_x, center_y),
                (flame_x - flame_length * 0.3, flame_y - flame_length * 0.3),
                (flame_x, flame_y),
                (flame_x + flame_length * 0.3, flame_y - flame_length * 0.3)
            ]
            pygame.draw.polygon(temp_surface, (*FIRE_ORANGE, outer_alpha), points)
            
            # Chama amarela (interna)
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
            
            # Pegadas do javali
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
        
        # Portal externo (laranja)
        pygame.draw.circle(screen, PORTAL_ORANGE, (center_x, center_y), portal_radius)
        
        # Portal interno (amarelo)
        inner_radius = portal_radius * (0.6 + 0.2 * math.sin(self.animation_timer * 0.2))
        pygame.draw.circle(screen, PORTAL_YELLOW, (center_x, center_y), inner_radius)
        
        # Chamas ao redor
        for i in range(8):
            angle = (i * 45 + self.animation_timer * 3) * 3.14 / 180
            flame_length = portal_radius * 0.8
            flame_x = center_x + math.cos(angle) * (portal_radius + flame_length * 0.3)
            flame_y = center_y + math.sin(angle) * (portal_radius + flame_length * 0.3)
            
            # Chama
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
            # CAÇADOR NORMAL (com arma e chapéu)
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
            # CAÇADOR TONTO (sem arma e sem chapéu, azul)
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

# Funções auxiliares
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

# Função principal
def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    
    # Variáveis de nível
    current_level = 1
    max_levels = 3
    base_enemies = 3  # Começa com 2 inimigos no nível 1
    
    # Inicializar primeiro nível
    maze = generate_maze()
    tree_positions = generate_tree_positions(maze)
    stone_positions = generate_stone_positions(maze)
    player = Player(1, 1)
    portal = FirePortal(GRID_WIDTH - 2, GRID_HEIGHT - 2)
    
    # Número de inimigos baseado no nível
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
                    # Reiniciar do nível 1
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
                    transition_timer = 60  # 2 segundos para transição
                else:
                    game_won = True
        
        # Transição de nível
        if level_transition:
            transition_timer -= 1
            if transition_timer <= 0:
                # Avançar para o próximo nível
                current_level += 1
                
                # Gerar novo labirinto
                maze = generate_maze()
                tree_positions = generate_tree_positions(maze)
                stone_positions = generate_stone_positions(maze)
                player = Player(1, 1)
                portal = FirePortal(GRID_WIDTH - 2, GRID_HEIGHT - 2)
                
                # Adicionar mais um caçador
                num_enemies = base_enemies + (current_level - 1)
                enemies = []
                for _ in range(num_enemies):
                    x, y = find_valid_position(maze, 8)
                    enemies.append(Enemy(x, y))
                
                level_transition = False
        
        # Definir cor de fundo baseada no nível
        background_color = LEVEL_BACKGROUNDS[current_level - 1]
        screen.fill(background_color)
        
        draw_maze(screen, maze, tree_positions, stone_positions, current_level)
        
        player.draw_footprints(screen)
        
        # Desenhar portal de fogo
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
        
        # Tela de transição de nível
        if level_transition:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            level_up_text = font.render(f"NÍVEL {current_level} CONCLUÍDO!", True, YELLOW)
            next_level_text = font.render(f"PREPARANDO NÍVEL {current_level + 1}...", True, ORANGE)
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

if __name__ == "__main__":
    import math
    main()