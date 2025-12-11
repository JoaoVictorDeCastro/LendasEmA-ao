import pygame
import sys
import math
import random  # Adicionado import do módulo random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Caçada ao Curupira - Cutscene com Diálogo")

# Cores
SKY_BLUE = (135, 206, 235)
GROUND_GREEN = (34, 139, 34)
TREE_GREEN = (0, 100, 0)
BROWN = (101, 67, 33)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 80, 0)
TEXT_BOX_COLOR = (30, 30, 30, 220)  # Com transparência

# Cores para o Curupira
CURUPIRA_SKIN = (244, 164, 96)
CURUPIRA_SKIRT = (0, 128, 0)
CURUPIRA_HAIR = (255, 69, 0)
FIRE_ORANGE = (255, 140, 0)
FIRE_YELLOW = (255, 215, 0)

# Configuração de fontes
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)
font_dialogue = pygame.font.SysFont(None, 32)

# Classe para o rosto do Curupira (cena de diálogo)
class CurupiraFace:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2 - 50
        self.size = 200
        self.eye_blink_timer = 0
        self.eye_blink_interval = 120  # Frames entre piscadas
        self.eye_blink_duration = 5  # Duração da piscada
        self.mouth_timer = 0
        self.mouth_animation_speed = 0.1
        self.fire_animation = 0
        self.fire_speed = 0.2
        
    def draw(self, screen):
        # Desenhar o rosto do Curupira
        self.draw_face(screen)
        self.draw_fire_hair(screen)
        self.draw_eyes(screen)
        self.draw_mouth(screen)
        
        # Atualizar animações
        self.eye_blink_timer += 1
        self.mouth_timer += self.mouth_animation_speed
        self.fire_animation += self.fire_speed
    
    def draw_face(self, screen):
        # Rosto
        face_radius = self.size // 2
        pygame.draw.circle(screen, CURUPIRA_SKIN, (self.x, self.y), face_radius)
        
        # Contorno do rosto
        pygame.draw.circle(screen, (200, 140, 70), (self.x, self.y), face_radius, 3)
        
        # Bochechas (leve blush)
        cheek_radius = face_radius // 4
        left_cheek_x = self.x - face_radius // 2
        right_cheek_x = self.x + face_radius // 2
        cheek_y = self.y + face_radius // 4
        
        pygame.draw.circle(screen, (255, 200, 180), (left_cheek_x, cheek_y), cheek_radius)
        pygame.draw.circle(screen, (255, 200, 180), (right_cheek_x, cheek_y), cheek_radius)
    
    def draw_fire_hair(self, screen):
        # Base do cabelo de fogo
        base_width = self.size * 0.9
        base_height = self.size * 0.4
        base_y = self.y - self.size // 2 - base_height * 0.3
        
        pygame.draw.ellipse(screen, CURUPIRA_HAIR, 
                          (self.x - base_width//2, base_y, base_width, base_height))
        
        # Chamas principais
        flame_count = 9
        max_flame_height = self.size * 0.8
        
        for i in range(flame_count):
            flame_x = self.x - base_width//2 + (base_width / (flame_count - 1)) * i
            flame_height = max_flame_height * (0.5 + 0.5 * math.sin(self.fire_animation + i * 0.5))
            
            # Chama laranja
            points = [
                (flame_x, base_y + base_height * 0.5),
                (flame_x - base_width * 0.08, base_y - flame_height * 0.3),
                (flame_x, base_y - flame_height),
                (flame_x + base_width * 0.08, base_y - flame_height * 0.3)
            ]
            pygame.draw.polygon(screen, FIRE_ORANGE, points)
            
            # Chama amarela (interna)
            inner_height = flame_height * 0.7
            inner_points = [
                (flame_x, base_y + base_height * 0.5),
                (flame_x - base_width * 0.04, base_y - inner_height * 0.2),
                (flame_x, base_y - inner_height),
                (flame_x + base_width * 0.04, base_y - inner_height * 0.2)
            ]
            pygame.draw.polygon(screen, FIRE_YELLOW, inner_points)
            
            # Centelhas
            if i % 3 == 0:
                spark_x = flame_x + (math.sin(self.fire_animation * 2 + i) * 5)
                spark_y = base_y - flame_height - 5
                spark_radius = 3 + math.sin(self.fire_animation + i) * 2
                pygame.draw.circle(screen, FIRE_YELLOW, (int(spark_x), int(spark_y)), int(spark_radius))
    
    def draw_eyes(self, screen):
        eye_radius = self.size // 8
        eye_y = self.y - self.size // 10
        
        # Olho esquerdo
        left_eye_x = self.x - self.size // 4
        # Olho direito
        right_eye_x = self.x + self.size // 4
        
        # Verificar se está piscando
        is_blinking = (self.eye_blink_timer % self.eye_blink_interval) < self.eye_blink_duration
        
        if not is_blinking:
            # Olhos abertos
            # Olho esquerdo
            pygame.draw.circle(screen, WHITE, (left_eye_x, eye_y), eye_radius)
            pygame.draw.circle(screen, BLACK, (left_eye_x, eye_y), eye_radius // 2)
            
            # Olho direito
            pygame.draw.circle(screen, WHITE, (right_eye_x, eye_y), eye_radius)
            pygame.draw.circle(screen, BLACK, (right_eye_x, eye_y), eye_radius // 2)
            
            # Brilho nos olhos
            sparkle_radius = eye_radius // 4
            pygame.draw.circle(screen, WHITE, (left_eye_x - sparkle_radius//2, eye_y - sparkle_radius//2), sparkle_radius)
            pygame.draw.circle(screen, WHITE, (right_eye_x - sparkle_radius//2, eye_y - sparkle_radius//2), sparkle_radius)
        else:
            # Olhos fechados (piscando)
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
        
        # Boca falando (animada)
        mouth_openness = 0.3 + 0.2 * math.sin(self.mouth_timer)
        
        # Forma da boca (arco)
        pygame.draw.arc(screen, (220, 100, 100), 
                       (self.x - mouth_width//2, mouth_y - mouth_height//2, 
                        mouth_width, mouth_height * (1 + mouth_openness)), 
                       3.14, 6.28, 3)
        
        # Língua (aparece ocasionalmente)
        if math.sin(self.mouth_timer * 1.5) > 0.7:
            tongue_width = mouth_width // 3
            tongue_height = mouth_height // 2
            pygame.draw.ellipse(screen, (255, 150, 150), 
                              (self.x - tongue_width//2, mouth_y + mouth_height * 0.2, 
                               tongue_width, tongue_height))

# Classe para a caixa de diálogo
class DialogueBox:
    def __init__(self, text):
        self.text = text
        self.x = WIDTH // 2
        self.y = HEIGHT - 150
        self.width = WIDTH - 100
        self.height = 120
        self.text_lines = self.wrap_text(text)
        self.show_arrow = True
        self.arrow_timer = 0
        
    def wrap_text(self, text):
        """Quebra o texto em várias linhas para caber na caixa"""
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
        # Desenhar caixa de diálogo semi-transparente
        dialogue_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        dialogue_surface.fill(TEXT_BOX_COLOR)
        
        # Borda da caixa
        pygame.draw.rect(dialogue_surface, (255, 255, 255, 150), 
                        (0, 0, self.width, self.height), 3)
        
        # Cantos arredondados
        corner_radius = 10
        pygame.draw.rect(dialogue_surface, (255, 255, 255, 50), 
                        (0, 0, self.width, self.height), 3, corner_radius)
        
        # Desenhar na tela
        screen.blit(dialogue_surface, (self.x - self.width//2, self.y - self.height//2))
        
        # Desenhar texto
        line_height = font_dialogue.get_height() + 5
        start_y = self.y - self.height//2 + 20
        
        for i, line in enumerate(self.text_lines):
            text_surface = font_dialogue.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.x, start_y + i * line_height))
            screen.blit(text_surface, text_rect)
        
        # Desenhar seta de continuação (piscante)
        self.arrow_timer += 1
        if self.arrow_timer % 60 < 30:  # Pisca a cada 0.5 segundos
            arrow_y = self.y + self.height//2 - 20
            arrow_points = [
                (self.x - 10, arrow_y),
                (self.x, arrow_y + 10),
                (self.x + 10, arrow_y)
            ]
            pygame.draw.polygon(screen, WHITE, arrow_points)

# Função para desenhar o fundo da floresta (versão mais escura para destaque)
def draw_darkened_background():
    # Céu escurecido
    darkened_sky = tuple(max(0, c - 40) for c in SKY_BLUE)
    screen.fill(darkened_sky)
    
    # Sol menos brilhante
    pygame.draw.circle(screen, (200, 200, 100), (900, 80), 50)
    
    # Nuvens esmaecidas
    for i in range(3):
        cloud_x = 100 + i * 250
        cloud_y = 100 + (i % 2) * 20
        pygame.draw.ellipse(screen, (200, 200, 200), (cloud_x, cloud_y, 100, 40))
        pygame.draw.ellipse(screen, (200, 200, 200), (cloud_x + 30, cloud_y - 15, 80, 40))
        pygame.draw.ellipse(screen, (200, 200, 200), (cloud_x - 20, cloud_y + 10, 80, 40))
    
    # Montanhas ao fundo (mais escuras)
    pygame.draw.polygon(screen, (30, 90, 30), [(0, 300), (200, 100), (400, 300)])
    pygame.draw.polygon(screen, (20, 80, 20), [(300, 300), (500, 150), (700, 300)])
    pygame.draw.polygon(screen, (10, 70, 10), [(600, 300), (900, 180), (1000, 300)])
    
    # Chão escurecido
    darkened_ground = tuple(max(0, c - 30) for c in GROUND_GREEN)
    pygame.draw.rect(screen, darkened_ground, (0, 300, WIDTH, HEIGHT-300))
    
    # Texturas no chão (grama escura)
    for i in range(0, WIDTH, 20):
        blade_height = 8 + (i % 3) * 4
        pygame.draw.line(screen, (0, 80, 0), (i, 300), (i, 300 + blade_height), 1)
    
    # Árvores escuras no fundo (silhuetas)
    tree_colors = [(20, 60, 20), (25, 65, 25), (30, 70, 30)]
    for i in range(8):
        tree_x = 50 + i * 120
        tree_size = 50 + (i % 3) * 20
        tree_y = 300 - tree_size//2
        
        # Tronco
        trunk_width = tree_size // 4
        trunk_height = tree_size
        pygame.draw.rect(screen, (60, 40, 20), 
                        (tree_x - trunk_width//2, tree_y + tree_size//2, trunk_width, trunk_height))
        
        # Copa da árvore
        pygame.draw.circle(screen, tree_colors[i % 3], (tree_x, tree_y + tree_size//4), tree_size//2)

# Função para a cena de diálogo
def dialogue_scene():
    clock = pygame.time.Clock()
    
    # Criar rosto do Curupira
    curupira_face = CurupiraFace()
    
    # Criar caixa de diálogo
    dialogue_text = "Estou em apuros, me ajude a escapar dos caçadores e encontrar meus amigos."
    dialogue_box = DialogueBox(dialogue_text)
    
    # Texto de instrução
    instruction_text = font_small.render("Pressione ESPAÇO para continuar", True, (255, 255, 200))
    
    # Variáveis de controle
    running = True
    fade_alpha = 0  # Para efeito de fade in
    fade_speed = 3
    
    # Efeito de partículas (fogo) - CORRIGIDO: usando random.random() em vez de math.random()
    particles = []
    for _ in range(30):
        particles.append({
            'x': WIDTH // 2 + (random.random() - 0.5) * 200,  # CORREÇÃO AQUI
            'y': HEIGHT // 2 - 150 + (random.random() - 0.5) * 100,  # CORREÇÃO AQUI
            'size': random.random() * 4 + 1,  # CORREÇÃO AQUI
            'speed': random.random() * 0.5 + 0.2,  # CORREÇÃO AQUI
            'color': FIRE_ORANGE if random.random() > 0.5 else FIRE_YELLOW,  # CORREÇÃO AQUI
            'life': random.random() * 100 + 50  # CORREÇÃO AQUI
        })
    
    # Loop da cena de diálogo
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "continue"  # Sinal para continuar para a próxima cena
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Atualizar partículas
        for p in particles:
            p['y'] -= p['speed']
            p['x'] += (math.sin(p['life'] * 0.1) * 0.5)
            p['life'] -= 1
            
            # Reciclar partículas que saíram da tela
            if p['y'] < 0 or p['life'] <= 0:
                p['y'] = HEIGHT // 2 - 100 + random.random() * 50  # CORREÇÃO AQUI
                p['x'] = WIDTH // 2 + (random.random() - 0.5) * 200  # CORREÇÃO AQUI
                p['life'] = random.random() * 100 + 50  # CORREÇÃO AQUI
        
        # Desenhar fundo
        draw_darkened_background()
        
        # Desenhar partículas de fogo
        for p in particles:
            alpha = min(255, p['life'] * 2)
            particle_surface = pygame.Surface((int(p['size'] * 2), int(p['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*p['color'], int(alpha)), 
                             (int(p['size']), int(p['size'])), int(p['size']))
            screen.blit(particle_surface, (int(p['x'] - p['size']), int(p['y'] - p['size'])))
        
        # Aplicar fade in
        if fade_alpha < 255:
            fade_alpha = min(255, fade_alpha + fade_speed)
        
        # Desenhar rosto do Curupira
        curupira_face.draw(screen)
        
        # Desenhar caixa de diálogo
        dialogue_box.draw(screen)
        
        # Desenhar instrução
        if fade_alpha > 200:  # Mostrar instrução após o fade in
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT - 50))
        
        # Aplicar fade overlay se necessário
        if fade_alpha < 255:
            fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, 255 - fade_alpha))
            screen.blit(fade_surface, (0, 0))
        
        # Atualizar a tela
        pygame.display.flip()
        clock.tick(60)
    
    return "exit"

# Função principal que controla todas as cenas
def main():
    # Primeiro mostrar a cena de diálogo
    result = dialogue_scene()
    
    if result == "continue":
        # Aqui você pode adicionar a cena de perseguição anterior
        # Por enquanto, apenas mostra uma mensagem e sai
        screen.fill((0, 0, 0))
        continue_text = font_large.render("Cena de Perseguição Iniciada!", True, WHITE)
        instruction_text = font_medium.render("Pressione ESC para sair", True, (200, 200, 200))
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            screen.fill((0, 0, 0))
            screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, HEIGHT//2 + 50))
            pygame.display.flip()
            clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()