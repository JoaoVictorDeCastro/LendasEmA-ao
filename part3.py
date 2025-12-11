import pygame
import random
import sys
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 500
FPS = 60

# Cores - Esquema de floresta noturna
FOREST_NIGHT = (10, 15, 25)
DARK_FOREST = (20, 25, 20)
FOREST_GREEN = (25, 40, 25)
DARK_BROWN = (45, 30, 20)
BROWN = (65, 45, 30)
LIGHT_BROWN = (85, 65, 45)
DARK_RED = (100, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FLAME_YELLOW = (255, 220, 80)
FLAME_ORANGE = (255, 140, 60)
FLAME_RED = (220, 70, 40)
DARK_FLAME = (180, 50, 30)
MOON_LIGHT = (220, 230, 240)
GHOST_WHITE = (240, 240, 255)
GHOST_BLUE = (200, 200, 255)
VICTORY_GOLD = (255, 215, 0)
VICTORY_SILVER = (192, 192, 192)

# Cores adicionais para a cutscene
TEXT_COLOR = (255, 255, 200)
TEXT_OUTLINE = (40, 20, 0)
FIRE_ORANGE = (255, 100, 0)
FIRE_YELLOW = (255, 200, 0)
FIRE_RED = (255, 40, 0)
SMOKE_GRAY = (100, 100, 100, 150)
SMOKE_LIGHT = (150, 150, 150, 100)

# Classe para partículas de fogo (para a cutscene)
class FireParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 15)
        self.color = random.choice([FIRE_RED, FIRE_ORANGE, FIRE_YELLOW])
        self.speed_y = random.uniform(-1.5, -3.0)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.lifetime = random.randint(30, 80)
        self.age = 0
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.age += 1
        # Reduzir tamanho com o tempo
        self.size = max(0, self.size * 0.97)
        # Mudar cor conforme envelhece
        if self.age > self.lifetime * 0.7:
            self.color = (min(255, self.color[0] + 20), 
                         max(100, self.color[1] - 30), 
                         max(0, self.color[2] - 20))
        
    def draw(self, surface):
        if self.age < self.lifetime:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
            
    def is_dead(self):
        return self.age >= self.lifetime

# Classe para partículas de fumaça (para a cutscene)
class SmokeParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(10, 25)
        self.color = random.choice([SMOKE_GRAY, SMOKE_LIGHT])
        self.speed_y = random.uniform(-1.0, -2.0)
        self.speed_x = random.uniform(-0.8, 0.8)
        self.lifetime = random.randint(50, 120)
        self.age = 0
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.age += 1
        # Aumentar tamanho com o tempo
        self.size = min(60, self.size * 1.02)
        # Tornar mais transparente com o tempo
        alpha = max(0, self.color[3] * 0.97)
        self.color = (self.color[0], self.color[1], self.color[2], int(alpha))
        
    def draw(self, surface):
        if self.age < self.lifetime:
            # Criar uma superfície temporária para desenhar com alpha
            smoke_surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(smoke_surf, self.color, (self.size, self.size), int(self.size))
            surface.blit(smoke_surf, (int(self.x - self.size), int(self.y - self.size)))
            
    def is_dead(self):
        return self.age >= self.lifetime

# Classe para as árvores da cutscene
class CutsceneTree:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.on_fire = False
        self.fire_particles = []
        self.smoke_particles = []
        self.fire_start_time = random.randint(0, 300)  # Tempo aleatório para começar a queimar
        
    def draw(self, surface, frame_count):
        # Desenhar tronco
        trunk_width = self.size // 4
        trunk_height = self.size
        pygame.draw.rect(surface, DARK_BROWN, 
                         (self.x - trunk_width//2, self.y - trunk_height//2, 
                          trunk_width, trunk_height))
        
        # Desenhar copa da árvore
        crown_radius = self.size // 2
        pygame.draw.circle(surface, FOREST_GREEN, 
                          (self.x, self.y - trunk_height//2), crown_radius)
        
        # Iniciar fogo após um certo tempo
        if frame_count > self.fire_start_time and not self.on_fire:
            self.on_fire = True
            
        # Se a árvore está em chamas
        if self.on_fire:
            # Gerar novas partículas de fogo
            if random.random() < 0.3:
                for _ in range(random.randint(1, 3)):
                    px = self.x + random.randint(-crown_radius//2, crown_radius//2)
                    py = self.y - trunk_height//2 + random.randint(-crown_radius, crown_radius//2)
                    self.fire_particles.append(FireParticle(px, py))
                    
            # Gerar fumaça ocasionalmente
            if random.random() < 0.1:
                for _ in range(random.randint(1, 2)):
                    px = self.x + random.randint(-crown_radius//2, crown_radius//2)
                    py = self.y - trunk_height//2 + random.randint(-crown_radius//2, crown_radius//2)
                    self.smoke_particles.append(SmokeParticle(px, py))
            
            # Atualizar e desenhar partículas de fogo
            for particle in self.fire_particles[:]:
                particle.update()
                particle.draw(surface)
                if particle.is_dead():
                    self.fire_particles.remove(particle)
                    
            # Atualizar e desenhar partículas de fumaça
            for particle in self.smoke_particles[:]:
                particle.update()
                particle.draw(surface)
                if particle.is_dead():
                    self.smoke_particles.remove(particle)

# Classe da Mula Sem Cabeça
class FlamingHorse:
    def __init__(self):
        # Tamanho menor
        self.body_width = 40
        self.body_height = 30
        self.leg_height = 40
        self.neck_height = 25
        self.x = 100
        self.y = GROUND_HEIGHT - self.body_height - self.leg_height - 20
        self.jump_velocity = 0
        self.is_jumping = False
        self.gravity = 1.3
        self.jump_strength = -20
        self.body_color = BROWN
        self.mane_color = DARK_BROWN  
        self.leg_frame = 0
        self.leg_speed = 0.3
        self.flame_timer = 0
        self.flame_intensity = 1.0
        
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = self.jump_strength
    
    def update(self):
        # Aplicar gravidade
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity
            
            # Verificar se atingiu o chão
            ground_level = GROUND_HEIGHT - self.body_height - self.leg_height - 20
            if self.y >= ground_level:
                self.y = ground_level
                self.is_jumping = False
                self.jump_velocity = 0
        
        # Animar as pernas
        if not self.is_jumping:
            self.leg_frame += self.leg_speed
            if self.leg_frame > 4:
                self.leg_frame = 0
        
        # Atualizar timer das chamas
        self.flame_timer += 0.15
        self.flame_intensity = 0.8 + 0.2 * math.sin(self.flame_timer * 0.5)
    
    def draw(self, screen):
        # Posição do corpo
        body_y = self.y + self.leg_height
        
        #CORPO DO CAVALO
        # Corpo principal
        body_length = 45
        body_height = 25
        body_rect = pygame.Rect(self.x, body_y, body_length, body_height)
        pygame.draw.ellipse(screen, self.body_color, body_rect)
        
        #PERNAS
        leg_width = 8
        leg_offset = int(self.leg_frame) * 3
        
        # Pernas da frente
        front_leg_y = body_y + body_height - leg_offset
        front_leg_height = self.leg_height + leg_offset
        
        # Perna dianteira esquerda
        pygame.draw.rect(screen, self.body_color, 
                        (self.x + 8, front_leg_y, leg_width, front_leg_height))
        
        # Perna dianteira direita
        pygame.draw.rect(screen, (self.body_color[0]-10, self.body_color[1]-10, self.body_color[2]-10), 
                        (self.x + 15, body_y + body_height - (leg_offset//2), 
                         leg_width, self.leg_height - (leg_offset//2)))
        
        # Pernas traseiras
        back_leg_x = self.x + body_length - 20
        
        # Perna traseira esquerda
        pygame.draw.rect(screen, self.body_color, 
                        (back_leg_x, body_y + body_height - (leg_offset//2), 
                         leg_width, self.leg_height - (leg_offset//2)))
        
        # Perna traseira direita
        pygame.draw.rect(screen, (self.body_color[0]-10, self.body_color[1]-10, self.body_color[2]-10), 
                        (back_leg_x + 7, front_leg_y, leg_width, front_leg_height))
        
        # Cascos
        hoof_colors = [(self.body_color[0]-30, self.body_color[1]-30, self.body_color[2]-30), BLACK]
        
        # Cascos das pernas da frente
        for i, hoof_x in enumerate([self.x + 8, self.x + 15]):
            hoof_y = body_y + body_height + self.leg_height - 5
            pygame.draw.rect(screen, hoof_colors[i], (hoof_x, hoof_y, leg_width, 5))
        
        # Cascos das pernas de trás
        for i, hoof_x in enumerate([back_leg_x, back_leg_x + 7]):
            hoof_y = body_y + body_height + self.leg_height - 5
            pygame.draw.rect(screen, hoof_colors[1-i], (hoof_x, hoof_y, leg_width, 5))
        
        #PESCOÇO E CABEÇA
        # Pescoço curvado
        neck_start_x = self.x + body_length - 15
        neck_start_y = body_y + 5
        
        # Linha superior do pescoço
        neck_top_points = [
            (neck_start_x, neck_start_y),
            (neck_start_x + 10, neck_start_y - 5),
            (neck_start_x + 25, neck_start_y - 10)
        ]
        
        # Linha inferior do pescoço
        neck_bottom_points = [
            (neck_start_x, neck_start_y + 10),
            (neck_start_x + 10, neck_start_y + 5),
            (neck_start_x + 25, neck_start_y)
        ]
        
        # Desenhar pescoço
        neck_points = neck_top_points + neck_bottom_points[::-1]
        pygame.draw.polygon(screen, self.body_color, neck_points)
        
        # Base do pescoço
        flame_base_x = neck_start_x + 25  # Fim do pescoço
        flame_base_y = neck_start_y - 5   # Ponto médio
        
        # Área queimada na base do pescoço
        pygame.draw.circle(screen, DARK_FLAME, (flame_base_x, flame_base_y), 8)
        
        #VÁRIAS CHAMAS DE FOGO
        num_flames = 7  
        max_flame_height = 35 * self.flame_intensity
        
        for flame_index in range(num_flames):
            # Posição base da chama
            angle_offset = (flame_index / num_flames) * math.pi * 0.8 - math.pi * 0.4
            flame_distance = 5 + flame_index % 3 
            
            flame_center_x = flame_base_x + math.cos(angle_offset) * flame_distance
            flame_center_y = flame_base_y + math.sin(angle_offset) * flame_distance
            
            # Cada chama tem características diferentes
            flame_height = max_flame_height * (0.6 + 0.4 * (flame_index / num_flames))
            flame_width = 12 + flame_index * 1.5
            
            # Animar cada chama independentemente
            flame_wave = math.sin(self.flame_timer + flame_index * 0.7) * 3
            
            # CORPO PRINCIPAL DA CHAMA 
            flame_points = []
            num_segments = 8
            
            for i in range(num_segments + 1):
                # Progressão da base ao topo
                progress = i / num_segments
                
                # Largura diminui do fundo para a ponta
                segment_width = flame_width * (1 - progress * 0.7)
                
                # Altura com curva suave
                segment_height = flame_height * progress
                
                # Adicionar ondulação
                wave_offset = math.sin(progress * math.pi * 2 + self.flame_timer) * 2
                
                # Ponto esquerdo
                left_x = flame_center_x - segment_width/2 + wave_offset
                left_y = flame_center_y - segment_height + flame_wave * (1 - progress)
                flame_points.append((left_x, left_y))
            
            # Pontos do lado direito 
            for i in range(num_segments, -1, -1):
                progress = i / num_segments
                segment_width = flame_width * (1 - progress * 0.7)
                segment_height = flame_height * progress
                wave_offset = math.sin(progress * math.pi * 2 + self.flame_timer) * 2
                
                # Ponto direito
                right_x = flame_center_x + segment_width/2 + wave_offset
                right_y = flame_center_y - segment_height + flame_wave * (1 - progress)
                flame_points.append((right_x, right_y))
            
            # Cor da chama baseada na altura
            if flame_index % 3 == 0:
                # Chama principal 
                flame_color = FLAME_YELLOW
                mid_color = FLAME_ORANGE
                base_color = FLAME_RED
            elif flame_index % 3 == 1:
                # Chama média
                flame_color = FLAME_ORANGE
                mid_color = FLAME_RED
                base_color = DARK_FLAME
            else:
                # Chama mais escura
                flame_color = FLAME_RED
                mid_color = DARK_FLAME
                base_color = (150, 40, 20)
            
            # Desenhar chama com gradiente
            if len(flame_points) > 2:
                # Base da chama
                base_points = flame_points[:len(flame_points)//3] + flame_points[-len(flame_points)//3:][::-1]
                pygame.draw.polygon(screen, base_color, base_points)
                
                # Meio da chama
                mid_start = len(flame_points)//6
                mid_end = -len(flame_points)//6
                mid_points = flame_points[mid_start:len(flame_points)//2] + flame_points[len(flame_points)//2:mid_end][::-1]
                pygame.draw.polygon(screen, mid_color, mid_points)
                
                # Ponta da chama
                top_start = len(flame_points)//3
                top_end = -len(flame_points)//3
                top_points = flame_points[top_start:len(flame_points)//2] + flame_points[len(flame_points)//2:top_end][::-1]
                pygame.draw.polygon(screen, flame_color, top_points)
        
        #CRINA
        # Crina no pescoço
        mane_points_along_neck = [
            (neck_start_x + 3, neck_start_y - 2),
            (neck_start_x + 8, neck_start_y - 4),
            (neck_start_x + 13, neck_start_y - 6),
            (neck_start_x + 18, neck_start_y - 7),
            (neck_start_x + 23, neck_start_y - 8)
        ]
        
        for i, (mane_x, mane_y) in enumerate(mane_points_along_neck):
            mane_length = 8 + i * 2
            mane_angle = -0.3 
            
            mane_end_x = mane_x + math.cos(mane_angle) * mane_length
            mane_end_y = mane_y + math.sin(mane_angle) * mane_length
            
            # Desenhar fio da crina
            pygame.draw.line(screen, self.mane_color, 
                           (mane_x, mane_y), (mane_end_x, mane_end_y), 3)
            
            # Detalhes nos fios da crina
            for j in range(3):
                detail_offset = j * 0.3
                detail_start_x = mane_x + math.cos(mane_angle) * mane_length * (0.3 + detail_offset)
                detail_start_y = mane_y + math.sin(mane_angle) * mane_length * (0.3 + detail_offset)
                
                detail_angle = mane_angle + random.uniform(-0.2, 0.2)
                detail_length = mane_length * 0.4
                
                detail_end_x = detail_start_x + math.cos(detail_angle) * detail_length
                detail_end_y = detail_start_y + math.sin(detail_angle) * detail_length
                
                pygame.draw.line(screen, self.mane_color,
                               (detail_start_x, detail_start_y),
                               (detail_end_x, detail_end_y), 1)
        
        #RABO
        tail_base_x = self.x - 5 
        tail_base_y = body_y + body_height // 2
        
        # Rabo como vários fios
        for i in range(8):
            tail_angle = math.pi + random.uniform(-0.4, 0.4) 
            tail_length = 15 + i * 3
            
            tail_end_x = tail_base_x + math.cos(tail_angle) * tail_length
            tail_end_y = tail_base_y + math.sin(tail_angle) * tail_length
            
            # Fio principal do rabo
            pygame.draw.line(screen, self.mane_color,
                           (tail_base_x, tail_base_y),
                           (tail_end_x, tail_end_y), 2)
            
            # Detalhes no fio
            for j in range(2):
                detail_progress = random.uniform(0.3, 0.7)
                detail_x = tail_base_x + math.cos(tail_angle) * tail_length * detail_progress
                detail_y = tail_base_y + math.sin(tail_angle) * tail_length * detail_progress
                
                detail_angle = tail_angle + random.uniform(-0.3, 0.3)
                detail_length = tail_length * 0.3
                
                detail_end_x = detail_x + math.cos(detail_angle) * detail_length
                detail_end_y = detail_y + math.sin(detail_angle) * detail_length
                
                pygame.draw.line(screen, self.mane_color,
                               (detail_x, detail_y),
                               (detail_end_x, detail_end_y), 1)
        
        #FAÍSCAS DAS CHAMAS
        if random.random() < 0.3:
            for _ in range(random.randint(2, 4)):
                # Escolher uma das chamas como origem
                flame_idx = random.randint(0, num_flames - 1)
                angle_offset = (flame_idx / num_flames) * math.pi * 0.8 - math.pi * 0.4
                flame_distance = 5 + flame_idx % 3
                
                origin_x = flame_base_x + math.cos(angle_offset) * flame_distance
                origin_y = flame_base_y + math.sin(angle_offset) * flame_distance
                
                # Direção da faísca
                spark_angle = angle_offset + random.uniform(-0.8, 0.8)
                spark_distance = random.uniform(10, 25)
                
                spark_x = origin_x + math.cos(spark_angle) * spark_distance
                spark_y = origin_y - 15 + math.sin(spark_angle) * spark_distance  
                
                spark_size = random.randint(1, 3)
                spark_color = random.choice([FLAME_YELLOW, FLAME_ORANGE])
                
                # Desenhar faísca com brilho
                pygame.draw.circle(screen, spark_color, (int(spark_x), int(spark_y)), spark_size)
                
                # Brilho ao redor
                glow_size = spark_size + 1
                for i in range(2):
                    glow_alpha = 100 - i * 50
                    glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                    glow_color = (*spark_color[:3], glow_alpha)
                    pygame.draw.circle(glow_surface, glow_color, 
                                     (glow_size, glow_size), glow_size - i)
                    screen.blit(glow_surface, (spark_x - glow_size, spark_y - glow_size))
    
    def get_rect(self):
        # Retângulo de colisão ajustado para o cavalo visto de lado
        body_y = self.y + self.leg_height
        body_length = 45
        body_height = 25
        
        # Ajustar para a forma alongada do cavalo visto de lado
        return pygame.Rect(self.x + 5, body_y + 5, body_length - 10, body_height + self.leg_height - 10)

# Classe dos Obstáculos
class BurningLog:
    def __init__(self, speed):
        self.width = random.randint(25, 35)
        self.height = random.randint(50, 80)
        self.x = SCREEN_WIDTH
        self.y = GROUND_HEIGHT - self.height
        self.speed = speed
        self.color = BROWN
        self.bark_color = LIGHT_BROWN
        self.passed = False
        self.flame_timer = random.random() * 10
        self.flame_intensity = random.uniform(0.7, 1.0)
        
    def update(self):
        self.x -= self.speed
        self.flame_timer += 0.1
        return self.x < -self.width
    
    def draw(self, screen):
        # Desenhar o tronco
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, 6)
        
        # Textura do tronco
        ring_spacing = 12
        for i in range(ring_spacing, self.height, ring_spacing):
            ring_y = self.y + i
            ring_width = self.width - 4
            pygame.draw.arc(screen, self.bark_color, 
                           (self.x + 2, ring_y - 2, ring_width, 4),
                           0, math.pi, 1)
        
        # Detalhes de casca
        for _ in range(8):
            detail_x = self.x + random.randint(2, self.width - 2)
            detail_y = self.y + random.randint(4, self.height - 4)
            detail_length = random.randint(2, 6)
            pygame.draw.line(screen, self.bark_color, 
                           (detail_x, detail_y), 
                           (detail_x, detail_y + detail_length), 1)
        
        # Chama na ponta do tronco
        flame_height = 30 * self.flame_intensity
        flame_width = 25 * self.flame_intensity
        
        # Base da chama
        flame_base = [
            (self.x + self.width//2, self.y - 4),
            (self.x + self.width//2 - flame_width//2, self.y + flame_height//3),
            (self.x + self.width//2 + flame_width//2, self.y + flame_height//3)
        ]
        
        # Corpo da chama
        flame_mid = [
            (self.x + self.width//2, self.y - 8 - flame_height//3),
            (self.x + self.width//2 - flame_width//3, self.y - 4),
            (self.x + self.width//2 + flame_width//3, self.y - 4)
        ]
        
        # Ponta da chama
        flame_top = [
            (self.x + self.width//2, self.y - 12 - flame_height*2//3),
            (self.x + self.width//2 - flame_width//4, self.y - 8 - flame_height//3),
            (self.x + self.width//2 + flame_width//4, self.y - 8 - flame_height//3)
        ]
        
        # Animar a chama
        flame_offset = math.sin(self.flame_timer) * 1.5
        
        offset_base = [(p[0], p[1] + flame_offset) for p in flame_base]
        offset_mid = [(p[0], p[1] + flame_offset) for p in flame_mid]
        offset_top = [(p[0], p[1] + flame_offset) for p in flame_top]
        
        # Desenhar chama
        pygame.draw.polygon(screen, FLAME_RED, offset_base)
        pygame.draw.polygon(screen, FLAME_ORANGE, offset_mid)
        pygame.draw.polygon(screen, FLAME_YELLOW, offset_top)
        
        # Faíscas
        if random.random() < 0.5:
            spark_angle = random.uniform(-0.5, 0.5)
            spark_distance = random.uniform(8, 15)
            spark_x = self.x + self.width//2 + math.cos(spark_angle) * spark_distance
            spark_y = self.y - 8 + math.sin(spark_angle) * spark_distance + flame_offset
            spark_size = random.randint(1, 3)
            spark_color = random.choice([FLAME_YELLOW, FLAME_ORANGE])
            pygame.draw.circle(screen, spark_color, (int(spark_x), int(spark_y)), spark_size)
        
        # Área queimada
        burnt_y = self.y - 2
        for i in range(2):
            burnt_x = self.x + self.width//2 + random.randint(-self.width//4, self.width//4)
            burnt_color = (max(0, self.color[0] - 20), max(0, self.color[1] - 15), max(0, self.color[2] - 15))
            pygame.draw.circle(screen, burnt_color, (burnt_x, burnt_y), self.width // 4)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Classe das Árvores Estáticas
class StaticTree:
    def __init__(self, x, layer):
        self.x = x
        self.layer = layer
        
        if layer == 1:
            self.width = random.randint(80, 120)
            self.height = random.randint(200, 250)
            self.trunk_width = random.randint(15, 25)
        elif layer == 2:
            self.width = random.randint(50, 80)
            self.height = random.randint(150, 180)
            self.trunk_width = random.randint(10, 18)
        else:
            self.width = random.randint(30, 50)
            self.height = random.randint(80, 120)
            self.trunk_width = random.randint(8, 12)
        
        trunk_r = random.randint(40, 60)
        trunk_g = random.randint(25, 35)
        trunk_b = random.randint(15, 25)
        self.trunk_color = (trunk_r, trunk_g, trunk_b)
        
        # Cores da folhagem
        foliage_r = random.randint(20, 35)
        foliage_g = random.randint(30, 45)
        foliage_b = random.randint(20, 30)
        self.foliage_color = (foliage_r, foliage_g, foliage_b)
        
        # Posição Y
        self.y_base = GROUND_HEIGHT + (3 - self.layer) * 15
        
        # Altura do tronco
        self.trunk_height = self.height * 0.7
    
    def draw(self, screen):
        # Tronco
        trunk_rect = pygame.Rect(
            self.x - self.trunk_width // 2,
            self.y_base - self.trunk_height,
            self.trunk_width,
            self.trunk_height
        )
        pygame.draw.rect(screen, self.trunk_color, trunk_rect)
        
        # Textura simples do tronc
        for i in range(0, int(self.trunk_height), 10):
            line_y = self.y_base - self.trunk_height + i
            line_length = self.trunk_width - 4
            line_x = self.x - line_length // 2
            bark_color = (
                max(0, self.trunk_color[0] + random.randint(-10, 5)),
                max(0, self.trunk_color[1] + random.randint(-10, 5)),
                max(0, self.trunk_color[2] + random.randint(-10, 5))
            )
            pygame.draw.line(screen, bark_color, (line_x, line_y), (line_x + line_length, line_y), 2)
        
        # Folhagem
        foliage_radius = self.width // 2
        foliage_y = self.y_base - self.trunk_height - 15
        pygame.draw.circle(screen, self.foliage_color, (self.x, foliage_y), foliage_radius)
        
        # Detalhes na folhagem
        for _ in range(5):
            detail_x = self.x + random.randint(-foliage_radius, foliage_radius)
            detail_y = foliage_y + random.randint(-foliage_radius, foliage_radius)
            detail_radius = random.randint(3, 8)
            detail_color = (
                max(0, self.foliage_color[0] + random.randint(-10, 10)),
                max(0, self.foliage_color[1] + random.randint(-10, 10)),
                max(0, self.foliage_color[2] + random.randint(-10, 10))
            )
            pygame.draw.circle(screen, detail_color, (detail_x, detail_y), detail_radius)

# Sistema de Cutscene
class CutsceneSystem:
    def __init__(self):
        self.showing_cutscene = True
        self.cutscene_timer = 0
        self.text_alpha = 0
        self.text_visible = False
        self.text_speed = 2  # Velocidade de aparecimento do texto
        
        # Criar árvores para a cutscene
        self.cutscene_trees = []
        for _ in range(15):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(SCREEN_HEIGHT//2, SCREEN_HEIGHT - 50)
            size = random.randint(40, 80)
            self.cutscene_trees.append(CutsceneTree(x, y, size))
        
        # Partículas de fogo no chão
        self.ground_fire_particles = []
        self.ground_smoke_particles = []
        
        # Fontes para o texto
        self.title_font = pygame.font.SysFont('arial', 48, bold=True)
        self.subtitle_font = pygame.font.SysFont('arial', 36)
    
    def draw_text_with_outline(self, text, font, color, outline_color, x, y, surface):
        # Desenhar contorno (8 posições ao redor)
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    text_surface = font.render(text, True, outline_color)
                    surface.blit(text_surface, (x + dx, y + dy))
        
        # Desenhar texto principal
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (x, y))
    
    def update(self):
        if not self.showing_cutscene:
            return
        
        self.cutscene_timer += 1
        
        # Gerar partículas de fogo no chão
        if self.cutscene_timer > 100:
            if random.random() < 0.2:
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(SCREEN_HEIGHT - 50, SCREEN_HEIGHT - 10)
                self.ground_fire_particles.append(FireParticle(x, y))
                
            if random.random() < 0.1:
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(SCREEN_HEIGHT - 50, SCREEN_HEIGHT - 20)
                self.ground_smoke_particles.append(SmokeParticle(x, y))
        
        # Atualizar e remover partículas de fogo no chão
        for particle in self.ground_fire_particles[:]:
            particle.update()
            if particle.is_dead():
                self.ground_fire_particles.remove(particle)
                
        # Atualizar e remover partículas de fumaça no chão
        for particle in self.ground_smoke_particles[:]:
            particle.update()
            if particle.is_dead():
                self.ground_smoke_particles.remove(particle)
        
        # Ativar texto após alguns segundos
        if self.cutscene_timer > 120:
            self.text_visible = True
        
        # Controlar transparência do texto
        if self.text_visible and self.text_alpha < 255:
            self.text_alpha = min(255, self.text_alpha + self.text_speed)
    
    def draw(self, screen):
        if not self.showing_cutscene:
            return
        
        # Preencher fundo
        screen.fill(FOREST_NIGHT)
        
        # Desenhar algumas estrelas no céu
        for i in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT//3)
            brightness = random.randint(100, 255)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)
        
        # Desenhar lua
        moon_pos = (SCREEN_WIDTH - 100, 80)
        pygame.draw.circle(screen, MOON_LIGHT, moon_pos, 40)
        pygame.draw.circle(screen, (200, 210, 220), (moon_pos[0] - 10, moon_pos[1] - 10), 10)
        
        # Desenhar partículas de fogo no chão
        for particle in self.ground_fire_particles:
            particle.draw(screen)
                
        # Desenhar partículas de fumaça no chão
        for particle in self.ground_smoke_particles:
            particle.draw(screen)
        
        # Desenhar árvores
        for tree in self.cutscene_trees:
            tree.draw(screen, self.cutscene_timer)
        
        # Desenhar texto com efeito de fade-in
        if self.text_alpha > 0:
            # Criar superfície para o texto com alpha
            text_surface = pygame.Surface((SCREEN_WIDTH, 200), pygame.SRCALPHA)
            
            # Desenhar título
            title_text = "A floresta está em chamas"
            subtitle_text = "Ajude a mula sem cabeça a escapar"
            
            # Calcular posições centrais
            title_width, title_height = self.title_font.size(title_text)
            subtitle_width, subtitle_height = self.subtitle_font.size(subtitle_text)
            
            # Desenhar texto com contorno na superfície temporária
            self.draw_text_with_outline(title_text, self.title_font, 
                                      TEXT_COLOR + (self.text_alpha,), 
                                      TEXT_OUTLINE + (min(200, self.text_alpha),),
                                      (SCREEN_WIDTH - title_width) // 2, 20, text_surface)
            
            self.draw_text_with_outline(subtitle_text, self.subtitle_font, 
                                      TEXT_COLOR + (self.text_alpha,), 
                                      TEXT_OUTLINE + (min(200, self.text_alpha),),
                                      (SCREEN_WIDTH - subtitle_width) // 2, 90, text_surface)
            
            # Instruções
            if self.text_alpha > 200:
                instruction_font = pygame.font.SysFont('arial', 24)
                instruction_text = instruction_font.render("Pressione ESPAÇO para começar", 
                                                         True, TEXT_COLOR)
                text_surface.blit(instruction_text, 
                                 (SCREEN_WIDTH//2 - instruction_text.get_width()//2, 160))
            
            # Desenhar a superfície de texto na tela principal
            screen.blit(text_surface, (0, 0))
        
        # Finalizar cutscene após 10 segundos ou por comando do jogador
        if self.cutscene_timer > 600:  # 60 FPS * 10 segundos
            self.showing_cutscene = False
    
    def skip_cutscene(self):
        self.showing_cutscene = False

# Classe do Jogo
class FlamingHorseGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("A Mula Sem Cabeça na Floresta em Chamas")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 36, bold=True)
        self.small_font = pygame.font.SysFont('arial', 24)
        self.victory_font = pygame.font.SysFont('arial', 56, bold=True)
        
        # Sistema de cutscene
        self.cutscene = CutsceneSystem()
        
        # Criar fundo estático
        self.background = self.create_static_background()
        
        # Criar árvores estáticas
        self.trees = []
        
        # Árvores de fundo (camada 3)
        for i in range(15):
            x = random.randint(-50, SCREEN_WIDTH + 50)
            self.trees.append(StaticTree(x, 3))
        
        # Árvores do meio (camada 2)
        for i in range(10):
            x = random.randint(-30, SCREEN_WIDTH + 30)
            self.trees.append(StaticTree(x, 2))
        
        # Árvores da frente (camada 1)
        for i in range(5):
            x = random.randint(0, SCREEN_WIDTH)
            self.trees.append(StaticTree(x, 1))
        
        self.reset_game()
    
    def create_static_background(self):
        """Cria um fundo completamente estático"""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Céu noturno gradiente
        for y in range(SCREEN_HEIGHT):
            if y < int(SCREEN_HEIGHT * 0.3):
                factor = y / (SCREEN_HEIGHT * 0.3)
                color = (
                    int(FOREST_NIGHT[0] * (1 - factor) + DARK_FOREST[0] * factor),
                    int(FOREST_NIGHT[1] * (1 - factor) + DARK_FOREST[1] * factor),
                    int(FOREST_NIGHT[2] * (1 - factor) + DARK_FOREST[2] * factor)
                )
            else:
                factor = (y - SCREEN_HEIGHT * 0.3) / (SCREEN_HEIGHT * 0.7)
                color = (
                    int(DARK_FOREST[0] * (1 - factor) + FOREST_GREEN[0] * factor),
                    int(DARK_FOREST[1] * (1 - factor) + FOREST_GREEN[1] * factor),
                    int(DARK_FOREST[2] * (1 - factor) + FOREST_GREEN[2] * factor)
                )
            
            pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))
        
        # Lua
        moon_radius = 30
        moon_x = SCREEN_WIDTH - 80
        moon_y = 60
        pygame.draw.circle(background, MOON_LIGHT, (moon_x, moon_y), moon_radius)
        pygame.draw.circle(background, (200, 210, 220), (moon_x - 8, moon_y - 8), moon_radius // 3)
        
        # Estrelas fixas
        random.seed(42)
        star_height_limit = int(SCREEN_HEIGHT * 0.4)
        for i in range(30):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, star_height_limit)
            size = random.randint(1, 2)
            brightness = random.randint(150, 255)
            pygame.draw.circle(background, (brightness, brightness, brightness), (x, y), size)
        
        # Montanhas
        random.seed(123)
        for i in range(4):
            mountain_x = i * 200 + random.randint(-40, 40)
            mountain_width = random.randint(120, 180)
            mountain_height = random.randint(40, 70)
            
            mountain_points = [
                (mountain_x, int(SCREEN_HEIGHT * 0.3)),
                (mountain_x + mountain_width//2, int(SCREEN_HEIGHT * 0.3) - mountain_height),
                (mountain_x + mountain_width, int(SCREEN_HEIGHT * 0.3))
            ]
            
            mountain_color = (FOREST_GREEN[0] - 10, FOREST_GREEN[1] - 10, FOREST_GREEN[2] - 5)
            pygame.draw.polygon(background, mountain_color, mountain_points)
        
        return background
    
    def reset_game(self):
        self.horse = FlamingHorse()
        self.obstacles = []
        self.score = 0
        self.game_speed = 6
        self.game_over = False
        self.victory_achieved = False 
        self.victory_timer = 0  
        self.obstacle_spawn_timer = 0
        self.high_score = self.load_high_score()
    
    def load_high_score(self):
        try:
            with open("highscore_horse.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    
    def save_high_score(self):
        try:
            with open("highscore_horse.txt", "w") as f:
                f.write(str(int(self.high_score)))
        except:
            pass
    
    def spawn_obstacle(self):
        if self.obstacle_spawn_timer <= 0 and not self.victory_achieved:
            self.obstacles.append(BurningLog(self.game_speed))
            
            min_time = max(20, 60 - self.game_speed * 5)
            max_time = max(40, 100 - self.game_speed * 5)
            self.obstacle_spawn_timer = random.randint(min_time, max_time)
        else:
            self.obstacle_spawn_timer -= 1
    
    def check_collision(self):
        horse_rect = self.horse.get_rect()
        
        for obstacle in self.obstacles:
            if horse_rect.colliderect(obstacle.get_rect()):
                return True
        return False
    
    def update(self):
        # Se estamos na cutscene, atualizar apenas a cutscene
        if self.cutscene.showing_cutscene:
            self.cutscene.update()
            return
        
        if not self.game_over and not self.victory_achieved:
            # Atualizar cavalo
            self.horse.update()
            
            # Atualizar obstáculos
            self.obstacles = [obs for obs in self.obstacles if not obs.update()]
            
            # Spawnar novos obstáculos
            self.spawn_obstacle()
            
            # Atualizar pontuação
            for obstacle in self.obstacles:
                if not obstacle.passed and obstacle.x < self.horse.x:
                    obstacle.passed = True
                    self.score += 1
            
            # Verificar se alcançou 40 barreiras
            if self.score >= 40 and not self.victory_achieved:
                self.victory_achieved = True
                self.victory_timer = 0
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
            
            # Aumentar velocidade
            if not self.victory_achieved and self.score > 0 and self.score % 40 == 0:
                self.game_speed = min(16, 6 + self.score // 40)
                
                for obstacle in self.obstacles:
                    obstacle.speed = self.game_speed
            
            # Verificar colisão
            if self.check_collision():
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
        
        # Atualizar timer da vitória para animação
        if self.victory_achieved:
            self.victory_timer += 0.05
    
    def draw_victory_effects(self, screen):
        # Fundo dourado semi-transparente
        victory_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = int(100 + 50 * math.sin(self.victory_timer * 2))
        victory_overlay.fill((255, 215, 0, alpha // 3))
        screen.blit(victory_overlay, (0, 0))
        
        # Faíscas douradas
        for _ in range(20):
            spark_x = random.randint(0, SCREEN_WIDTH)
            spark_y = random.randint(0, SCREEN_HEIGHT)
            spark_size = random.randint(2, 5)
            spark_alpha = random.randint(100, 200)
            
            spark_color = (
                random.randint(200, 255),
                random.randint(180, 220),
                random.randint(0, 50)
            )
            
            spark_surface = pygame.Surface((spark_size * 2, spark_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(spark_surface, (*spark_color, spark_alpha), 
                             (spark_size, spark_size), spark_size)
            screen.blit(spark_surface, (spark_x - spark_size, spark_y - spark_size))
        
        # Texto de vitória
        victory_text = self.victory_font.render("VITÓRIA!", True, VICTORY_GOLD)
        victory_shadow = self.victory_font.render("VITÓRIA!", True, (100, 80, 0))
        
        # Animar o texto
        text_scale = 1.0 + 0.1 * math.sin(self.victory_timer * 3)
        scaled_width = int(victory_text.get_width() * text_scale)
        scaled_height = int(victory_text.get_height() * text_scale)
        
        scaled_text = pygame.transform.scale(victory_text, (scaled_width, scaled_height))
        scaled_shadow = pygame.transform.scale(victory_shadow, (scaled_width, scaled_height))
        
        text_x = SCREEN_WIDTH // 2 - scaled_width // 2
        text_y = SCREEN_HEIGHT // 2 - 100
        
        screen.blit(scaled_shadow, (text_x + 4, text_y + 4))
        screen.blit(scaled_text, (text_x, text_y))
        
        # Mensagem explicativa
        message_text = self.font.render("Você superou 40 barreiras de fogo!", True, WHITE)
        message_shadow = self.font.render("Você superou 40 barreiras de fogo!", True, BLACK)
        
        screen.blit(message_shadow, (SCREEN_WIDTH//2 - message_text.get_width()//2 + 2, text_y + 90))
        screen.blit(message_text, (SCREEN_WIDTH//2 - message_text.get_width()//2, text_y + 88))
        
        # Instruções para continuar
        continue_text = self.font.render("PRESSIONE R PARA JOGAR NOVAMENTE", True, FLAME_YELLOW)
        continue_shadow = self.font.render("PRESSIONE R PARA JOGAR NOVAMENTE", True, FLAME_RED)
        
        screen.blit(continue_shadow, (SCREEN_WIDTH//2 - continue_text.get_width()//2 + 3, text_y + 200))
        screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, text_y + 197))
        
        # Instruções para sair
        exit_text = self.small_font.render("ESC para sair do jogo", True, GHOST_WHITE)
        screen.blit(exit_text, (SCREEN_WIDTH//2 - exit_text.get_width()//2, text_y + 250))
    
    def draw(self):
        # Se estamos na cutscene, desenhar apenas a cutscene
        if self.cutscene.showing_cutscene:
            self.cutscene.draw(self.screen)
            return
        
        # Fundo estático
        self.screen.blit(self.background, (0, 0))
        
        # Desenhar árvores 
        trees_by_layer = {1: [], 2: [], 3: []}
        for tree in self.trees:
            trees_by_layer[tree.layer].append(tree)
        
        for layer in [3, 2, 1]:
            for tree in trees_by_layer[layer]:
                tree.draw(self.screen)
        
        # Chão 
        ground_height = SCREEN_HEIGHT - GROUND_HEIGHT
        ground_surface = pygame.Surface((SCREEN_WIDTH, ground_height))
        ground_surface.fill((30, 40, 25))
        
        # Textura do chão
        random.seed(999)
        for x in range(0, SCREEN_WIDTH, 15):
            for y in range(0, ground_height, 15):
                if random.random() > 0.7:
                    dirt_color = (
                        max(20, 30 + random.randint(-10, 10)),
                        max(25, 40 + random.randint(-10, 10)),
                        max(15, 25 + random.randint(-10, 10))
                    )
                    dirt_size = random.randint(2, 5)
                    dirt_x = x + random.randint(0, 5)
                    dirt_y = y + random.randint(0, 5)
                    pygame.draw.circle(ground_surface, dirt_color, (dirt_x, dirt_y), dirt_size)
        
        self.screen.blit(ground_surface, (0, GROUND_HEIGHT))
        
        # Linha do horizonte
        pygame.draw.line(self.screen, (0, 0, 0, 100), 
                        (0, GROUND_HEIGHT), 
                        (SCREEN_WIDTH, GROUND_HEIGHT), 2)
        
        # Obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Cavalo Flamejante
        self.horse.draw(self.screen)
        
        # Chamas decorativas
        for i in range(2):
            flame_x = SCREEN_WIDTH//2 - 15 + i * 30
            flame_y = 45
            flame_points = [
                (flame_x, flame_y),
                (flame_x - 4, flame_y - 8),
                (flame_x + 4, flame_y - 8)
            ]
            flame_color = [FLAME_ORANGE, FLAME_YELLOW][i]
            pygame.draw.polygon(self.screen, flame_color, flame_points)
        
        # Velocidade
        speed_text = self.small_font.render(f"Vel: {self.game_speed:.1f}", True, WHITE)
        self.screen.blit(speed_text, (10, 10))
        
        # Barra de progresso para vitória (40 barreiras)
        if not self.victory_achieved and not self.game_over:
            progress_width = 200
            progress_height = 15
            progress_x = SCREEN_WIDTH//2 - progress_width//2
            progress_y = 70
            
            # Fundo da barra de progresso
            pygame.draw.rect(self.screen, (40, 20, 10), 
                           (progress_x, progress_y, progress_width, progress_height), 0, 7)
            
            # Preenchimento da barra
            progress = min(self.score / 40, 1.0)
            fill_width = int(progress_width * progress)
            if progress > 0:
                pygame.draw.rect(self.screen, FLAME_YELLOW, 
                               (progress_x, progress_y, fill_width, progress_height), 0, 7)
            
            # Borda da barra
            pygame.draw.rect(self.screen, FLAME_ORANGE, 
                           (progress_x, progress_y, progress_width, progress_height), 2, 7)
        
        # Tela de vitória
        if self.victory_achieved:
            self.draw_victory_effects(self.screen)
        
        # Tela de game over
        elif self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((20, 10, 5, 200))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("O FOGO SE APAGOU", True, FLAME_YELLOW)
            restart_text = self.font.render("PRESSIONE R", True, FLAME_ORANGE)
            final_score_text = self.small_font.render(f"CHAMAS ATRAVESSADAS: {self.score}", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
            self.screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 - 10))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 40))
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        if self.cutscene.showing_cutscene:
                            self.cutscene.skip_cutscene()
                        elif not self.game_over and not self.victory_achieved:
                            self.horse.jump()
                    
                    if event.key == pygame.K_r:
                        if self.game_over or self.victory_achieved:
                            self.reset_game()
                    
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    # Pular cutscene com Enter também
                    if event.key == pygame.K_RETURN and self.cutscene.showing_cutscene:
                        self.cutscene.skip_cutscene()
            
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Iniciar o jogo
if __name__ == "__main__":
    game = FlamingHorseGame()
    game.run()