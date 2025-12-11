import pygame
import random
import sys
import math

# Inicializar pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floresta em Chamas - Cutscene")

# Cores
BACKGROUND = (10, 20, 10)
TREE_BROWN = (60, 40, 20)
TREE_GREEN = (20, 80, 30)
FIRE_ORANGE = (255, 100, 0)
FIRE_YELLOW = (255, 200, 0)
FIRE_RED = (255, 40, 0)
SMOKE_GRAY = (100, 100, 100, 150)
SMOKE_LIGHT = (150, 150, 150, 100)
TEXT_COLOR = (255, 255, 200)
TEXT_OUTLINE = (40, 20, 0)

# Fonte para o texto
title_font = pygame.font.SysFont('arial', 48, bold=True)
subtitle_font = pygame.font.SysFont('arial', 36)

# Classe para partículas de fogo
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

# Classe para partículas de fumaça
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

# Classe para as árvores
class Tree:
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
        pygame.draw.rect(surface, TREE_BROWN, 
                         (self.x - trunk_width//2, self.y - trunk_height//2, 
                          trunk_width, trunk_height))
        
        # Desenhar copa da árvore
        crown_radius = self.size // 2
        pygame.draw.circle(surface, TREE_GREEN, 
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

# Função para criar texto com contorno
def draw_text_with_outline(text, font, color, outline_color, x, y, surface):
    # Desenhar contorno (8 posições ao redor)
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                text_surface = font.render(text, True, outline_color)
                surface.blit(text_surface, (x + dx, y + dy))
    
    # Desenhar texto principal
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Função principal
def main():
    clock = pygame.time.Clock()
    frame_count = 0
    
    # Criar árvores
    trees = []
    for _ in range(15):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(HEIGHT//2, HEIGHT - 50)
        size = random.randint(40, 80)
        trees.append(Tree(x, y, size))
    
    # Variáveis para controle do texto
    text_alpha = 0
    text_visible = False
    text_speed = 2  # Velocidade de aparecimento do texto
    
    # Partículas de fogo no chão
    ground_fire_particles = []
    ground_smoke_particles = []
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Reiniciar a cena
                    frame_count = 0
                    text_alpha = 0
                    text_visible = False
                    trees = []
                    for _ in range(15):
                        x = random.randint(50, WIDTH - 50)
                        y = random.randint(HEIGHT//2, HEIGHT - 50)
                        size = random.randint(40, 80)
                        trees.append(Tree(x, y, size))
        
        # Preencher fundo
        screen.fill(BACKGROUND)
        
        # Desenhar algumas estrelas no céu
        for i in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT//3)
            brightness = random.randint(100, 255)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)
        
        # Desenhar lua
        moon_pos = (WIDTH - 100, 80)
        pygame.draw.circle(screen, (200, 200, 180), moon_pos, 40)
        pygame.draw.circle(screen, (180, 180, 160), (moon_pos[0] - 10, moon_pos[1] - 10), 10)
        
        # Gerar partículas de fogo no chão
        if frame_count > 100:
            if random.random() < 0.2:
                x = random.randint(0, WIDTH)
                y = random.randint(HEIGHT - 50, HEIGHT - 10)
                ground_fire_particles.append(FireParticle(x, y))
                
            if random.random() < 0.1:
                x = random.randint(0, WIDTH)
                y = random.randint(HEIGHT - 50, HEIGHT - 20)
                ground_smoke_particles.append(SmokeParticle(x, y))
        
        # Atualizar e desenhar partículas de fogo no chão
        for particle in ground_fire_particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.is_dead():
                ground_fire_particles.remove(particle)
                
        # Atualizar e desenhar partículas de fumaça no chão
        for particle in ground_smoke_particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.is_dead():
                ground_smoke_particles.remove(particle)
        
        # Desenhar árvores
        for tree in trees:
            tree.draw(screen, frame_count)
        
        # Ativar texto após alguns segundos
        if frame_count > 120:
            text_visible = True
        
        # Controlar transparência do texto
        if text_visible and text_alpha < 255:
            text_alpha = min(255, text_alpha + text_speed)
        
        # Desenhar texto com efeito de fade-in
        if text_alpha > 0:
            # Criar superfície para o texto com alpha
            text_surface = pygame.Surface((WIDTH, 200), pygame.SRCALPHA)
            
            # Desenhar título
            title_text = "A floresta está em chamas"
            subtitle_text = "Ajude a mula sem cabeça a escapar"
            
            # Calcular posições centrais
            title_width, title_height = title_font.size(title_text)
            subtitle_width, subtitle_height = subtitle_font.size(subtitle_text)
            
            # Desenhar texto com contorno na superfície temporária
            draw_text_with_outline(title_text, title_font, 
                                  TEXT_COLOR + (text_alpha,), 
                                  TEXT_OUTLINE + (min(200, text_alpha),),
                                  (WIDTH - title_width) // 2, 20, text_surface)
            
            draw_text_with_outline(subtitle_text, subtitle_font, 
                                  TEXT_COLOR + (text_alpha,), 
                                  TEXT_OUTLINE + (min(200, text_alpha),),
                                  (WIDTH - subtitle_width) // 2, 90, text_surface)
            
            # Desenhar a superfície de texto na tela principal
            screen.blit(text_surface, (0, 0))
        
        # Instruções para o usuário
        if frame_count > 300:
            instruction_font = pygame.font.SysFont('arial', 20)
            instruction_text = instruction_font.render("Pressione ESPAÇO para reiniciar ou ESC para sair", 
                                                      True, (200, 200, 200))
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 40))
        
        # Atualizar tela
        pygame.display.flip()
        
        # Controlar FPS
        clock.tick(60)
        frame_count += 1
        
        # Reiniciar automaticamente após 10 segundos
        if frame_count > 600:  # 60 FPS * 10 segundos
            frame_count = 0
            text_alpha = 0
            text_visible = False
            trees = []
            for _ in range(15):
                x = random.randint(50, WIDTH - 50)
                y = random.randint(HEIGHT//2, HEIGHT - 50)
                size = random.randint(40, 80)
                trees.append(Tree(x, y, size))
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()