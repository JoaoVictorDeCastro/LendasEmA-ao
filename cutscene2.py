import pygame
import sys
import random
import math

# Inicialização do PyGame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cutscene: A Tempestade na Floresta")

# Cores
DARK_GREEN = (15, 56, 15)
GREEN = (34, 139, 34)
LIGHT_GREEN = (50, 205, 50)
BROWN = (101, 67, 33)
DARK_BROWN = (54, 38, 20)
BLUE_GRAY = (70, 70, 90)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (220, 20, 20)

# Fonte
try:
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)
except:
    font_large = pygame.font.SysFont('arial', 72)
    font_medium = pygame.font.SysFont('arial', 48)
    font_small = pygame.font.SysFont('arial', 36)

class Raindrop:
    def __init__(self):
        self.reset()
        self.x = random.randint(-50, WIDTH)
        
    def reset(self):
        self.x = random.randint(-50, WIDTH)
        self.y = random.randint(-100, -10)
        self.speed = random.randint(20, 40)
        self.length = random.randint(10, 25)
        self.thickness = random.randint(1, 2)
        self.wind_effect = random.uniform(-3, 3)
        
    def update(self, wind_strength):
        self.y += self.speed
        self.x += self.wind_effect + wind_strength * 2
        
        if self.y > HEIGHT or self.x < -50 or self.x > WIDTH + 50:
            self.reset()
            
    def draw(self, surface):
        pygame.draw.line(surface, LIGHT_GRAY, 
                        (self.x, self.y), 
                        (self.x + self.wind_effect * 2, self.y + self.length), 
                        self.thickness)

class Leaf:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = random.randint(-100, WIDTH + 100)
        self.y = random.randint(-100, HEIGHT)
        self.size = random.randint(5, 15)
        self.color = random.choice([GREEN, LIGHT_GREEN, (100, 160, 80)])
        self.speed_x = random.uniform(-5, 5)
        self.speed_y = random.uniform(-3, 1)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.wind_resistance = random.uniform(0.5, 1.5)
        
    def update(self, wind_strength):
        self.x += self.speed_x + wind_strength * self.wind_resistance
        self.y += self.speed_y
        self.rotation += self.rotation_speed
        
        # Movimento de flutuação
        self.speed_y += 0.05
        self.speed_x *= 0.99
        
        if (self.y > HEIGHT + 100 or self.x < -200 or 
            self.x > WIDTH + 200 or self.y < -100):
            self.reset()
            self.y = random.randint(-100, -10)
            
    def draw(self, surface):
        leaf_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(leaf_surf, self.color, 
                           (0, 0, self.size * 2, self.size))
        
        rotated_leaf = pygame.transform.rotate(leaf_surf, self.rotation)
        surface.blit(rotated_leaf, 
                    (self.x - rotated_leaf.get_width() // 2, 
                     self.y - rotated_leaf.get_height() // 2))

class Tree:
    def __init__(self, x, width, height):
        self.x = x
        self.width = width
        self.height = height
        self.lean = 0
        self.max_lean = width // 2
        self.lean_speed = random.uniform(0.5, 1.5)
        self.lean_direction = 1
        
    def update(self, wind_strength, time):
        # Oscilação das árvores com o vento
        oscillation = math.sin(time * self.lean_speed) * wind_strength * 5
        
        # Movimento de inclinação com a tempestade
        self.lean += wind_strength * self.lean_direction * 0.5
        
        if abs(self.lean) > self.max_lean:
            self.lean_direction *= -1
            
        self.lean *= 0.95  # Reduz gradualmente
            
    def draw(self, surface):
        # Tronco
        trunk_rect = pygame.Rect(
            self.x - self.width // 4 + self.lean, 
            HEIGHT - self.height + 50, 
            self.width // 2, 
            self.height - 50
        )
        pygame.draw.rect(surface, DARK_BROWN, trunk_rect)
        
        # Copa da árvore (múltiplos círculos para aparência orgânica)
        for i in range(5):
            circle_x = self.x + random.randint(-20, 20) + self.lean * 0.7
            circle_y = HEIGHT - self.height + 50 + random.randint(-20, 20)
            radius = self.width + random.randint(-10, 10)
            pygame.draw.circle(surface, GREEN, 
                             (int(circle_x), int(circle_y)), 
                             radius)
            
            # Detalhes mais claros
            highlight_radius = radius - 10
            if highlight_radius > 5:
                pygame.draw.circle(surface, LIGHT_GREEN,
                                 (int(circle_x - 10), int(circle_y - 10)),
                                 highlight_radius)

class Saci:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.size = 40
        self.color = (30, 30, 30)  # Cor próxima ao negro do Saci
        self.red_scarf = (200, 0, 0)
        self.visible = False
        self.alpha = 0
        self.surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
    def update(self, time):
        # Piscar suavemente ao aparecer
        if self.visible:
            self.alpha = min(255, self.alpha + 5)
            
    def draw(self, surface):
        if not self.visible or self.alpha <= 0:
            return
            
        self.surf.fill((0, 0, 0, 0))
        
        # Corpo do Saci
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size)
        
        # Chapéu vermelho
        pygame.draw.rect(self.surf, self.red_scarf, 
                        (self.size - 15, self.size - 35, 30, 20))
        
        # Pipe (cachimbo)
        pygame.draw.rect(self.surf, BROWN, 
                        (self.size + 10, self.size - 15, 20, 5))
        
        # Olho
        pygame.draw.circle(self.surf, WHITE, (self.size + 10, self.size), 5)
        pygame.draw.circle(self.surf, BLACK, (self.size + 10, self.size), 2)
        
        # Sorriso
        pygame.draw.arc(self.surf, WHITE, 
                       (self.size - 10, self.size + 5, 20, 10), 
                       0, math.pi, 2)
        
        self.surf.set_alpha(self.alpha)
        surface.blit(self.surf, (self.x - self.size, self.y - self.size))

class StormEffect:
    def __init__(self):
        self.lightning_alpha = 0
        self.lightning_timer = 0
        self.flash_duration = 0
        self.wind_strength = 0
        self.wind_direction = 1
        self.time = 0
        
    def update(self, dt):
        self.time += dt
        
        # Efeito de vento que aumenta e diminui
        self.wind_strength += random.uniform(-0.5, 0.5) * self.wind_direction
        self.wind_strength = max(0, min(15, self.wind_strength))
        
        # Mudança de direção do vento
        if random.random() < 0.01:
            self.wind_direction *= -1
            
        # Relâmpagos aleatórios
        if self.lightning_alpha > 0:
            self.lightning_alpha -= 300 * dt
            
        if random.random() < 0.02 and self.lightning_timer <= 0:
            self.lightning_alpha = random.randint(150, 220)
            self.lightning_timer = random.uniform(1, 3)
            self.flash_duration = random.uniform(0.1, 0.3)
        else:
            self.lightning_timer -= dt
            
    def draw_lightning(self, surface):
        if self.lightning_alpha > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT))
            flash_surf.fill(WHITE)
            flash_surf.set_alpha(self.lightning_alpha)
            surface.blit(flash_surf, (0, 0))
            
            # Desenhar alguns raios
            for _ in range(3):
                start_x = random.randint(0, WIDTH)
                start_y = 0
                for _ in range(5):
                    end_x = start_x + random.randint(-50, 50)
                    end_y = start_y + random.randint(50, 100)
                    pygame.draw.line(surface, YELLOW, 
                                   (start_x, start_y), 
                                   (end_x, end_y), 
                                   random.randint(2, 4))
                    start_x, start_y = end_x, end_y

def draw_text_with_outline(surface, text, font, color, outline_color, pos):
    x, y = pos
    # Desenha contorno
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                text_surface = font.render(text, True, outline_color)
                surface.blit(text_surface, (x + dx, y + dy))
    
    # Desenha texto principal
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def main():
    clock = pygame.time.Clock()
    
    # Criar floresta
    trees = []
    for i in range(8):
        x = (i * 150) - 50
        width = random.randint(60, 100)
        height = random.randint(200, 350)
        trees.append(Tree(x, width, height))
    
    # Criar chuva
    raindrops = [Raindrop() for _ in range(300)]
    
    # Criar folhas voando
    leaves = [Leaf() for _ in range(50)]
    
    # Criar Saci
    saci = Saci()
    
    # Criar efeito de tempestade
    storm = StormEffect()
    
    # Estados da cutscene
    scene_state = "storm"  # storm, text_appear, saci_appear, final_text
    scene_timer = 0
    
    # Textos
    messages = [
        "O Saci também está em apuros,",
        "ajude-o a escalar as árvores",
        "com seus pulos até que",
        "essa ventania e tempestade passe."
    ]
    
    # Loop principal
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        scene_timer += dt
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    # Pular para próxima cena
                    if scene_state == "storm":
                        scene_state = "text_appear"
                        scene_timer = 0
                    elif scene_state == "text_appear":
                        scene_state = "saci_appear"
                        scene_timer = 0
                        saci.visible = True
                    elif scene_state == "saci_appear":
                        scene_state = "final_text"
                        scene_timer = 0
        
        # Transições automáticas
        if scene_state == "storm" and scene_timer > 5:
            scene_state = "text_appear"
            scene_timer = 0
        elif scene_state == "text_appear" and scene_timer > 6:
            scene_state = "saci_appear"
            scene_timer = 0
            saci.visible = True
        elif scene_state == "saci_appear" and scene_timer > 5:
            scene_state = "final_text"
            scene_timer = 0
        
        # Atualizar elementos
        storm.update(dt)
        
        for tree in trees:
            tree.update(storm.wind_strength, storm.time)
            
        for raindrop in raindrops:
            raindrop.update(storm.wind_strength)
            
        for leaf in leaves:
            leaf.update(storm.wind_strength)
            
        saci.update(dt)
        
        # Desenhar cena
        # Fundo escuro e tempestuoso
        if storm.lightning_alpha > 100:
            screen.fill((50, 50, 70))
        else:
            screen.fill((20, 20, 40))
        
        # Desenhar árvores
        for tree in trees:
            tree.draw(screen)
        
        # Desenhar chuva
        for raindrop in raindrops:
            raindrop.draw(screen)
        
        # Desenhar folhas
        for leaf in leaves:
            leaf.draw(screen)
        
        # Efeitos de tempestade
        storm.draw_lightning(screen)
        
        # Desenhar Saci
        saci.draw(screen)
        
        # Exibir textos conforme estado da cena
        if scene_state == "text_appear" or scene_state == "final_text":
            # Fundo semitransparente para texto
            text_bg = pygame.Surface((WIDTH - 100, 200), pygame.SRCALPHA)
            text_bg.fill((0, 0, 0, 180))
            screen.blit(text_bg, (50, HEIGHT // 2 - 100))
            
            # Animar aparecimento do texto
            text_alpha = min(255, scene_timer * 100)
            
            if scene_state == "text_appear":
                for i, message in enumerate(messages):
                    if scene_timer > i * 0.8:  # Aparece uma linha por vez
                        text = font_medium.render(message, True, YELLOW)
                        text.set_alpha(text_alpha)
                        screen.blit(text, 
                                  (WIDTH // 2 - text.get_width() // 2, 
                                   HEIGHT // 2 - 80 + i * 45))
            else:  # final_text
                text1 = font_large.render("AJUDE O SACI!", True, RED)
                text2 = font_medium.render("Pressione ESPAÇO para começar", True, WHITE)
                
                text1.set_alpha(text_alpha)
                text2.set_alpha(text_alpha)
                
                screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 50))
                
                # Piscar texto instrucional
                if math.sin(scene_timer * 5) > 0:
                    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 30))
        
        # Instrução para pular cena
        if scene_state != "final_text":
            skip_text = font_small.render("Pressione ESPAÇO para avançar", True, LIGHT_GRAY)
            screen.blit(skip_text, (WIDTH - skip_text.get_width() - 20, 20))
        
        # Mostrar força do vento (debug)
        # wind_text = font_small.render(f"Vento: {storm.wind_strength:.1f}", True, WHITE)
        # screen.blit(wind_text, (20, 20))
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()