import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Caçada ao Curupira - Cutscene")

# Cores
SKY_BLUE = (135, 206, 235)
GROUND_GREEN = (34, 139, 34)
TREE_GREEN = (0, 100, 0)
BROWN = (101, 67, 33)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Cores para o Curupira e Javali
BOAR_BROWN = (139, 69, 19)
BOAR_DARK_BROWN = (101, 67, 33)
CURUPIRA_SKIN = (244, 164, 96)
CURUPIRA_SKIRT = (0, 128, 0)
CURUPIRA_HAIR = (255, 69, 0)
FIRE_ORANGE = (255, 140, 0)
FIRE_YELLOW = (255, 215, 0)
SPEAR_BROWN = (101, 67, 33)
SPEAR_METAL = (192, 192, 192)

# Cores para o Caçador
HUNTER_HAT = (30, 144, 255)  # Azul
HUNTER_SKIN = (244, 164, 96)
HUNTER_RED = (178, 34, 34)   # Vermelho escuro
HUNTER_PANTS = (0, 0, 0)     # Preto
GUN_BROWN = (139, 69, 19)

# Tamanho da célula para referência
CELL_SIZE = 80

# Configuração de fontes
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Classe para o Curupira montado no Javali
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
        # Cria frames de animação para corrida
        for frame_num in range(6):
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # Posição central relativa para o frame
            center_x = self.width // 2
            center_y = self.height // 2
            
            # Altura do javali baseada no frame (animação de corrida)
            boar_bounce = math.sin(frame_num * 1.0) * 5
            
            # Javali
            boar_length = CELL_SIZE * 0.7
            boar_height = CELL_SIZE * 0.45
            boar_x = center_x - boar_length // 2
            boar_y = center_y + CELL_SIZE // 8 + boar_bounce
            
            # Corpo principal do javali
            pygame.draw.ellipse(frame, BOAR_BROWN, (boar_x, boar_y, boar_length, boar_height))
            
            # Cabeça do javali
            head_radius = CELL_SIZE // 6
            head_x = center_x + boar_length // 2 - head_radius
            head_y = center_y + boar_height // 2 + boar_bounce
            pygame.draw.circle(frame, BOAR_DARK_BROWN, (head_x, head_y), head_radius)
            
            # Focinho do javali
            snout_width = CELL_SIZE // 8
            snout_height = CELL_SIZE // 12
            snout_x = head_x + head_radius - snout_width // 2
            snout_y = head_y
            pygame.draw.ellipse(frame, BOAR_DARK_BROWN, (snout_x, snout_y - snout_height // 2, snout_width, snout_height))
            
            # Olhos do javali
            eye_radius = CELL_SIZE // 25
            pygame.draw.circle(frame, BLACK, (head_x - eye_radius, head_y - eye_radius), eye_radius)
            
            # Orelhas do javali
            ear_radius = CELL_SIZE // 10
            pygame.draw.circle(frame, BOAR_DARK_BROWN, (head_x - ear_radius, head_y - head_radius), ear_radius)
            
            # Pernas do javali (animadas)
            leg_width = CELL_SIZE // 10
            leg_height = CELL_SIZE // 6
            leg_offset = math.sin(frame_num * 1.5) * 8
            
            # Pernas dianteiras
            front_leg_height = leg_height - leg_offset if leg_offset > 0 else leg_height
            back_leg_height = leg_height + leg_offset if leg_offset > 0 else leg_height
            
            leg_positions = [
                (boar_x + boar_length * 0.2, boar_y + boar_height, front_leg_height),  # Frente esquerda
                (boar_x + boar_length * 0.4, boar_y + boar_height, back_leg_height),   # Traseira esquerda
                (boar_x + boar_length * 0.6, boar_y + boar_height, front_leg_height),  # Frente direita
                (boar_x + boar_length * 0.8, boar_y + boar_height, back_leg_height)    # Traseira direita
            ]
            
            for leg_x, leg_y, l_height in leg_positions:
                pygame.draw.rect(frame, BOAR_DARK_BROWN, 
                                (leg_x - leg_width // 2, leg_y - l_height, leg_width, l_height))
            
            # Curupira montado no javali
            curupira_x = center_x
            curupira_y = boar_y - CELL_SIZE // 8 + boar_bounce
            
            # Corpo do Curupira
            body_width = CELL_SIZE // 4
            body_height = CELL_SIZE // 5
            pygame.draw.ellipse(frame, CURUPIRA_SKIN, 
                              (curupira_x - body_width // 2, curupira_y, body_width, body_height))
            
            # Braços do Curupira
            arm_width = CELL_SIZE // 12
            arm_height = CELL_SIZE // 6
            # Braço esquerdo (segurando as rédeas)
            pygame.draw.ellipse(frame, CURUPIRA_SKIN, 
                              (curupira_x - body_width // 2 - arm_width // 2, curupira_y, arm_width, arm_height))
            # Braço direito (segurando a lança)
            pygame.draw.ellipse(frame, CURUPIRA_SKIN, 
                              (curupira_x + body_width // 2 - arm_width // 2, curupira_y, arm_width, arm_height))
            
            # Saia verde do Curupira
            skirt_width = CELL_SIZE // 3
            skirt_height = CELL_SIZE // 8
            skirt_y = curupira_y + body_height - 2
            pygame.draw.ellipse(frame, CURUPIRA_SKIRT, 
                              (curupira_x - skirt_width // 2, skirt_y, skirt_width, skirt_height))
            
            # Cabeça do Curupira
            head_radius = CELL_SIZE // 6
            head_y_pos = curupira_y - head_radius // 2
            pygame.draw.circle(frame, CURUPIRA_SKIN, (curupira_x, head_y_pos), head_radius)
            
            # Cabelo de fogo do Curupira
            self.draw_fire_hair(frame, curupira_x, head_y_pos, head_radius)
            
            # Olhos virados para trás
            eye_radius = head_radius // 4
            eye_y = head_y_pos + head_radius * 0.2
            pygame.draw.circle(frame, WHITE, (curupira_x - eye_radius, eye_y), eye_radius)
            pygame.draw.circle(frame, WHITE, (curupira_x + eye_radius, eye_y), eye_radius)
            pygame.draw.circle(frame, BLACK, (curupira_x - eye_radius, eye_y), eye_radius//2)
            pygame.draw.circle(frame, BLACK, (curupira_x + eye_radius, eye_y), eye_radius//2)
            
            # Lança do Curupira apontando para trás (em direção ao caçador)
            self.draw_spear(frame, curupira_x, curupira_y, frame_num)
            
            self.running_frames.append(frame)
    
    def draw_fire_hair(self, surface, x, y, head_radius):
        fire_height = head_radius * 2.5
        
        # Base do cabelo de fogo
        base_width = head_radius * 1.8
        pygame.draw.ellipse(surface, CURUPIRA_HAIR, 
                          (x - base_width // 2, y - head_radius - fire_height * 0.1, base_width, fire_height * 0.4))
        
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
            pygame.draw.polygon(surface, FIRE_ORANGE, points)
            
            # Chama amarela (interna)
            inner_height = flame_height * 0.7
            inner_points = [
                (flame_x, y - head_radius),
                (flame_x - base_width * 0.08, y - head_radius - inner_height * 0.3),
                (flame_x, y - head_radius - inner_height),
                (flame_x + base_width * 0.08, y - head_radius - inner_height * 0.3)
            ]
            pygame.draw.polygon(surface, FIRE_YELLOW, inner_points)
            
            # Pontas das chamas (efeito de fogo)
            if i % 2 == 0:
                spark_y = y - head_radius - flame_height
                spark_radius = head_radius // 8
                pygame.draw.circle(surface, FIRE_YELLOW, (int(flame_x), int(spark_y)), spark_radius)
    
    def draw_spear(self, surface, x, y, frame_num):
        spear_length = CELL_SIZE * 0.8
        spear_width = CELL_SIZE // 25
        
        # Animação da lança (balançando com a corrida)
        spear_offset = math.sin(frame_num * 0.8) * 3
        
        # Haste da lança (apontando para trás, em direção ao caçador)
        pygame.draw.rect(surface, SPEAR_BROWN, 
                        (x - CELL_SIZE // 2 - spear_length, y - spear_width // 2 + spear_offset, 
                         spear_length, spear_width))
        
        # Ponta metálica da lança
        tip_height = CELL_SIZE // 8
        tip_points = [
            (x - CELL_SIZE // 2, y + spear_offset),  # Ponta da lança (mais perto do caçador)
            (x - CELL_SIZE // 2 + tip_height, y - tip_height // 2 + spear_offset),
            (x - CELL_SIZE // 2 + tip_height, y + tip_height // 2 + spear_offset)
        ]
        pygame.draw.polygon(surface, SPEAR_METAL, tip_points)
        
        # Detalhes na haste
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
        
        # Atualizar imagem com o frame atual
        self.image = self.running_frames[int(self.frame)]

# Classe para o Caçador (nova versão)
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
        self.speed = 4  # Um pouco mais lento que o Curupira
        self.frame = 0
        self.animation_speed = 0.15
        self.running_frames = []
        self.create_running_frames()
    
    def draw_hunter(self, surface, center_x, center_y, leg_offset=0):
        # Chapéu azul
        hat_width = CELL_SIZE // 2
        hat_height = CELL_SIZE // 4
        pygame.draw.rect(surface, HUNTER_HAT, 
                       (center_x - hat_width//2, center_y - self.radius - hat_height//2, 
                        hat_width, hat_height))
        
        # Cabeça
        pygame.draw.circle(surface, HUNTER_SKIN, (center_x, center_y - self.radius//2), self.radius//2)
        
        # Corpo (blusa vermelha)
        body_width = CELL_SIZE // 2
        body_height = CELL_SIZE // 2
        pygame.draw.rect(surface, HUNTER_RED, 
                       (center_x - body_width//2, center_y - self.radius//2, 
                        body_width, body_height))
        
        # Calças
        pants_width = CELL_SIZE // 3
        pants_height = CELL_SIZE // 4
        pygame.draw.rect(surface, HUNTER_PANTS, 
                       (center_x - pants_width//2, center_y + self.radius//2, 
                        pants_width, pants_height))
        
        # Arma (escopeta)
        gun_length = CELL_SIZE // 1.5
        gun_width = CELL_SIZE // 10
        pygame.draw.rect(surface, GUN_BROWN, 
                       (center_x + self.radius//2, center_y - gun_width//2, 
                        gun_length, gun_width))
        pygame.draw.rect(surface, (80, 50, 30), 
                       (center_x + self.radius//2 - gun_length//4, center_y - gun_width//2, 
                        gun_length//4, gun_width))
        
        # Olhos
        eye_radius = self.radius // 8
        pygame.draw.circle(surface, WHITE, (center_x - eye_radius, center_y - self.radius//2), eye_radius)
        pygame.draw.circle(surface, WHITE, (center_x + eye_radius, center_y - self.radius//2), eye_radius)
        pygame.draw.circle(surface, BLACK, (center_x - eye_radius, center_y - self.radius//2), eye_radius//2)
        pygame.draw.circle(surface, BLACK, (center_x + eye_radius, center_y - self.radius//2), eye_radius//2)
        
        # Pernas (animadas)
        leg_width = CELL_SIZE // 10
        leg_height = CELL_SIZE // 3
        
        # Pernas em diferentes posições para animação
        left_leg_height = leg_height - leg_offset if leg_offset > 0 else leg_height
        right_leg_height = leg_height + leg_offset if leg_offset > 0 else leg_height
        
        # Perna esquerda
        pygame.draw.rect(surface, HUNTER_PANTS, 
                       (center_x - pants_width//3 - leg_width//2, 
                        center_y + self.radius//2 + pants_height - 5, 
                        leg_width, left_leg_height))
        
        # Perna direita
        pygame.draw.rect(surface, HUNTER_PANTS, 
                       (center_x + pants_width//3 - leg_width//2, 
                        center_y + self.radius//2 + pants_height - 5, 
                        leg_width, right_leg_height))
        
        # Boca aberta (gritando)
        pygame.draw.arc(surface, (220, 20, 60), 
                       (center_x - eye_radius*2, center_y - self.radius//3, eye_radius*4, eye_radius*3), 
                       0, 3.14, 2)
    
    def create_running_frames(self):
        # Cria frames de animação para corrida
        for i in range(6):
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # Posição central relativa
            center_x = self.width // 2
            center_y = self.height // 2
            
            # Altura baseada no frame (animação de corrida)
            bounce = math.sin(i * 1.0) * 3
            
            # Offset das pernas para animação
            leg_offset = math.sin(i * 1.5) * 8
            
            # Desenhar o caçador
            self.draw_hunter(frame, center_x, center_y + bounce, leg_offset)
            
            # Adicionar sombra sob os pés
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

# Classe para as árvores
class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size*2), pygame.SRCALPHA)
        self.draw_tree(size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw_tree(self, size):
        # Tronco
        trunk_width = size // 4
        trunk_height = size
        pygame.draw.rect(self.image, BROWN, 
                        (size//2 - trunk_width//2, size, trunk_width, trunk_height))
        
        # Copa da árvore
        pygame.draw.circle(self.image, TREE_GREEN, (size//2, size//2), size//2)
        pygame.draw.circle(self.image, (0, 120, 0), (size//2 - size//4, size//2 - size//6), size//3)
        pygame.draw.circle(self.image, (0, 120, 0), (size//2 + size//4, size//2 - size//6), size//3)

# Classe para os arbustos
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

# Função para desenhar o fundo da floresta
def draw_background():
    # Céu
    screen.fill(SKY_BLUE)
    
    # Sol
    pygame.draw.circle(screen, (255, 255, 150), (900, 80), 50)
    
    # Nuvens
    for i in range(3):
        cloud_x = 100 + i * 250
        cloud_y = 100 + (i % 2) * 20
        pygame.draw.ellipse(screen, (240, 240, 240), (cloud_x, cloud_y, 100, 40))
        pygame.draw.ellipse(screen, (240, 240, 240), (cloud_x + 30, cloud_y - 15, 80, 40))
        pygame.draw.ellipse(screen, (240, 240, 240), (cloud_x - 20, cloud_y + 10, 80, 40))
    
    # Montanhas ao fundo
    pygame.draw.polygon(screen, (50, 120, 50), [(0, 300), (200, 100), (400, 300)])
    pygame.draw.polygon(screen, (40, 110, 40), [(300, 300), (500, 150), (700, 300)])
    pygame.draw.polygon(screen, (30, 100, 30), [(600, 300), (900, 180), (1000, 300)])
    
    # Chão
    pygame.draw.rect(screen, GROUND_GREEN, (0, 300, WIDTH, HEIGHT-300))
    
    # Texturas no chão (grama)
    for i in range(0, WIDTH, 20):
        blade_height = 10 + (i % 3) * 5
        pygame.draw.line(screen, (0, 100, 0), (i, 300), (i, 300 + blade_height), 1)
    
    # Detalhes do solo
    for i in range(20):
        stone_x = (i * 47) % WIDTH
        stone_y = 310 + (i * 23) % 20
        stone_size = 5 + (i % 3)
        pygame.draw.circle(screen, (120, 80, 40), (stone_x, stone_y), stone_size)

# Função principal
def main():
    clock = pygame.time.Clock()
    
    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    bushes = pygame.sprite.Group()
    
    # Criar árvores
    tree_positions = [(50, 250), (150, 280), (300, 260), (450, 270), 
                      (600, 250), (750, 280), (200, 320), (350, 310),
                      (500, 320), (650, 310), (800, 280), (900, 300)]
    
    for i, (x, y) in enumerate(tree_positions):
        size = 60 + (i % 3) * 20
        tree = Tree(x, y, size)
        trees.add(tree)
        all_sprites.add(tree)
    
    # Criar arbustos
    bush_positions = [(100, 380), (250, 400), (400, 390), (550, 380),
                      (700, 400), (50, 420), (200, 410), (350, 420),
                      (500, 410), (650, 420), (800, 400), (950, 410)]
    
    for x, y in bush_positions:
        bush = Bush(x, y)
        bushes.add(bush)
        all_sprites.add(bush)
    
    # Criar personagens
    curupira = CurupiraOnBoar(-150, 380)  # Começa fora da tela à esquerda
    hunter = Hunter(-250, 380)            # Começa mais atrás
    
    all_sprites.add(curupira, hunter)
    
    # Textos da cutscene
    title_text = font.render("A FUGA DO CURUPIRA", True, (255, 255, 220))
    subtitle_text = small_font.render("Montado em seu javali, ele foge do caçador", True, (220, 220, 200))
    instruction_text = small_font.render("Cutscene em andamento...", True, (255, 255, 255))
    end_text = font.render("FIM DA CENA", True, (255, 255, 0))
    
    # Variáveis de controle
    running = True
    scene_started = False
    scene_ended = False
    frame_count = 0
    
    # Loop principal
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not scene_started:
                    scene_started = True
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and scene_ended:
                    # Reiniciar a cena
                    curupira.rect.x = -150
                    hunter.rect.x = -250
                    scene_started = False
                    scene_ended = False
                    frame_count = 0
        
        # Desenhar o fundo
        draw_background()
        
        # Desenhar árvores e arbustos
        trees.draw(screen)
        bushes.draw(screen)
        
        if not scene_started:
            # Tela inicial com fundo semi-transparente
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//2))
            start_text = small_font.render("Pressione ESPAÇO para iniciar a cutscene", True, (255, 255, 255))
            screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 50))
            
            # Desenhar pequena prévia dos personagens
            preview_curupira = CurupiraOnBoar(WIDTH//2 - 100, HEIGHT//2 + 100)
            preview_curupira.draw_hunter = lambda *args: None  # Desativar método desnecessário
            preview_hunter = Hunter(WIDTH//2 + 50, HEIGHT//2 + 100)
            
            preview_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
            preview_curupira_image = preview_curupira.running_frames[0]
            preview_hunter_image = preview_hunter.running_frames[0]
            
            screen.blit(preview_curupira_image, (WIDTH//2 - 150, HEIGHT//2 + 80))
            screen.blit(preview_hunter_image, (WIDTH//2 + 30, HEIGHT//2 + 90))
            
        else:
            # Atualizar e desenhar personagens
            if not scene_ended:
                curupira.update()
                hunter.update()
                frame_count += 1
            
            all_sprites.draw(screen)
            
            # Desenhar instrução
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, 20))
            
            # Verificar se a cena terminou (ambos saíram da tela)
            if curupira.rect.x > WIDTH and hunter.rect.x > WIDTH and not scene_ended:
                scene_ended = True
            
            if scene_ended:
                # Mostrar texto de fim de cena com overlay
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                
                screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2))
                restart_text = small_font.render("Pressione R para reiniciar ou ESC para sair", True, (255, 255, 255))
                screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
        
        # Atualizar a tela
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()