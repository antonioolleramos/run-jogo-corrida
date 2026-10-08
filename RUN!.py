import pygame
import esper
import random
from pathlib import Path

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
GAME_TITLE = "RUN!"
ASSETS_DIR = Path(__file__).resolve().parent
MUSIC_FILE = "Snoop Dogg  The Doors - Riders On The Storm (Fredwreck Remix) (NFS Underground 2 OST).mp3"

def asset_path(filename):
    """Resolve imagens, fontes e música em relação ao arquivo do jogo."""
    return str(ASSETS_DIR / filename)

def start_original_music():
    """Reproduz a trilha original se o usuário tiver o MP3 localmente."""
    music = ASSETS_DIR / MUSIC_FILE
    if not music.is_file():
        print("[RUN!] Música original opcional não encontrada; jogo iniciado sem trilha.")
        return
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(str(music))
        pygame.mixer.music.play(-1)
    except pygame.error as error:
        print(f"[RUN!] Não foi possível reproduzir a música: {error}")
BACKGROUND_IMAGE_FILE = "pistas3.png"
BACKGROUND_IMAGE_FILE2 = "pistas2.png"
BACKGROUND_IMAGE_FILE3 = "pistas1.png"
PLAYER_IMAGE_FILE = "moto1.png"
ENEMY_IMAGE_FILE_1 = "carro 1.png"
ENEMY_IMAGE_FILE_2 = "carro 2.png"
ENEMY_IMAGE_FILE_3 = "carro 3.png"
ENEMY_SPEED = 200
ENEMY_SIZE = (100,180)
ENEMY_SPAWN_RATE = 1.5
PLAYER_SPEED = 500 
PLAYER_SIZE = (60,140)

def run_game():
    pygame.init() 
    start_original_music() 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
    pygame.display.set_caption(GAME_TITLE) 
    clock = pygame.time.Clock() 

    font = pygame.font.Font(asset_path("FONTE GAME.ttf"), 30) 
    font_game_over = pygame.font.Font(asset_path("FONTE GAME.ttf"), 70) 
    font_titulo = pygame.font.Font(asset_path("FONTE GAME.ttf"), 90) 
    font_pequena = pygame.font.Font(asset_path("FONTE GAME.ttf"), 15) 
    font_pequena2 = pygame.font.Font(asset_path("FONTE GAME.ttf"), 10) 

    player_image = pygame.image.load(asset_path(PLAYER_IMAGE_FILE)).convert_alpha() 
    player_image = pygame.transform.scale(player_image, PLAYER_SIZE) 
    
    enemy_img_1 = pygame.image.load(asset_path(ENEMY_IMAGE_FILE_1)).convert_alpha()
    enemy_img_1 = pygame.transform.scale(enemy_img_1, ENEMY_SIZE)
    
    enemy_img_2 = pygame.image.load(asset_path(ENEMY_IMAGE_FILE_2)).convert_alpha()
    enemy_img_2 = pygame.transform.scale(enemy_img_2, ENEMY_SIZE)
    
    enemy_img_3 = pygame.image.load(asset_path(ENEMY_IMAGE_FILE_3)).convert_alpha()
    enemy_img_3 = pygame.transform.scale(enemy_img_3, ENEMY_SIZE)
    enemy_images_list = [enemy_img_1, enemy_img_2, enemy_img_3] 

    background= pygame.image.load(asset_path(BACKGROUND_IMAGE_FILE)) 
    background2= pygame.image.load(asset_path(BACKGROUND_IMAGE_FILE2))
    background3= pygame.image.load(asset_path(BACKGROUND_IMAGE_FILE3))

    class GameState: 
        def __init__(self, is_running: bool = True, current_scene: str = "MENU"): 

            self.is_running = is_running 
            self.score: int = 0 
            self.score_timer: float = 0.0 
            self.enemy_spawn_timer: float = 0.0 
            
            self.current_scene: str = current_scene 
            self.final_score: int = 0 
            
    esper.create_entity(GameState()) 
    game_state = esper.get_component(GameState)[0][1] 
    
    class Position:
        def __init__(self, x=0.0, y=0.0): 
            self.x = x
            self.y = y

    class Velocity:
        def __init__(self, dx=0.0, dy=0.0): 
            self.dx = dx
            self.dy = dy

    class Renderable:
        def __init__(self, image, size): 
            self.image = image
            self.size = size 
            self.rect = image.get_rect() 
    
            self.mask = pygame.mask.from_surface(image) 

    class PlayerControlled:
        pass 

    class Enemy:
        pass 

    class ScoreSystem(esper.Processor):
        def process(self, dt): 
            game_state = esper.get_component(GameState)[0][1]
            
            if game_state.current_scene != "GAME": 
                return 

            game_state.score_timer += dt 
            if game_state.score_timer >= 0.1: 
                game_state.score += 1 
                
                game_state.score_timer -= 0.1 

    class EnemySpawnerSystem(esper.Processor):
        def __init__(self, image, size, speed, spawn_rate):
            self.image = image
            self.size = size
            self.speed = speed
            self.spawn_rate = spawn_rate

        def process(self, dt):
            game_state = esper.get_component(GameState)[0][1]
            
            if game_state.current_scene != "GAME":
                return 

            game_state.enemy_spawn_timer += dt 

            current_spawn_rate = max(0.4, self.spawn_rate - (game_state.score * 0.005))

            if game_state.enemy_spawn_timer >= current_spawn_rate:
                game_state.enemy_spawn_timer= 0 

                spawn_x = random.randint(0, SCREEN_WIDTH - self.size[0]) 
                spawn_y = -self.size[1] 

                imagem_sorteada = random.choice(self.image) 

                nova_velocidade = self.speed + (game_state.score*1.4) 

                esper.create_entity(
                    Position(x=spawn_x, y=spawn_y),
                    Velocity(dx=0, dy= nova_velocidade), 
                    Renderable(image=imagem_sorteada, size=self.size),
                    Enemy() 
                )

    class CleanupSystem(esper.Processor):
        def process(self,dt):
            for ent, (pos, enemy) in esper.get_components(Position, Enemy):
                if pos.y > SCREEN_HEIGHT:
                    esper.delete_entity(ent) 


    class CollisionSystem(esper.Processor): 
        def process(self, dt):
            game_state = esper.get_component(GameState)[0][1]
            
            if game_state.current_scene != "GAME":
                return

            player_renderable = None 
            for ent, (rend, player) in esper.get_components(Renderable, PlayerControlled): 
                player_renderable = rend 
                break 

            if not player_renderable: 
                return

            for ent, (enemy_renderable, enemy) in esper.get_components(Renderable, Enemy):
                
                
                if player_renderable.rect.colliderect(enemy_renderable.rect):
                    
                    
                    offset_x = enemy_renderable.rect.x - player_renderable.rect.x
                    offset_y = enemy_renderable.rect.y - player_renderable.rect.y 
                    
                    
                    if player_renderable.mask.overlap(enemy_renderable.mask, (offset_x, offset_y)): 
                        game_state.final_score = game_state.score 
                        game_state.current_scene = "GAME_OVER" 
                        break 

    class InputSystem(esper.Processor): 
        def process(self, dt):
            game_state = esper.get_component(GameState)[0][1]
            if game_state.current_scene != "GAME":
                return

            keys = pygame.key.get_pressed() 
            
            for ent, (player_tag, vel) in esper.get_components(PlayerControlled, Velocity):
                vel.dx = 0
                vel.dy = 0
                if keys[pygame.K_w]:
                    vel.dy = -PLAYER_SPEED
                if keys[pygame.K_s]:
                    vel.dy = PLAYER_SPEED
                if keys[pygame.K_a]:
                    vel.dx = -PLAYER_SPEED
                if keys[pygame.K_d]:
                    vel.dx = PLAYER_SPEED
            
    class MovementSystem(esper.Processor):
        def process(self, dt): 
            game_state = esper.get_component(GameState)[0][1]
            if game_state.current_scene != "GAME":
                return 

            for ent, (pos, vel) in esper.get_components(Position, Velocity):
                pos.x += vel.dx * dt
                pos.y += vel.dy * dt 

                if esper.has_component(ent, PlayerControlled):
                    pos.x = max(13, min(pos.x, SCREEN_WIDTH - 12 - PLAYER_SIZE[0]))
                    pos.y = max(0, min(pos.y, SCREEN_HEIGHT - PLAYER_SIZE[1]))

                renderable = esper.try_component(ent, Renderable)
                if renderable:
                    renderable.rect.x = int(pos.x)
                    renderable.rect.y = int(pos.y) 

    
    class RenderSystem(esper.Processor):
        def __init__(self, screen, font, background, background2, background3):
            self.screen = screen 
            self.font = font
            self.backgrounds = [background, background2, background3]

        def process(self, dt):
            game_state = esper.get_component(GameState)[0][1] 
            
            if game_state.current_scene != "GAME":
                return 

            self.screen.blit(self.backgrounds[game_state.score % 3], (0, 0)) 
            
            
            for ent, (pos, rend) in esper.get_components(Position, Renderable):
                self.screen.blit(rend.image, rend.rect)
            
            score_text = self.font.render(f"|SCORE| {game_state.score}", True, (255, 0, 0)) 
            self.screen.blit(score_text, (20, 15)) 
            pygame.display.flip() 
    
    esper.add_processor(ScoreSystem()) 
    esper.add_processor(EnemySpawnerSystem(
        image= enemy_images_list,
        size= ENEMY_SIZE,
        speed= ENEMY_SPEED,
        spawn_rate= ENEMY_SPAWN_RATE 
    ))
    esper.add_processor(InputSystem()) 
    esper.add_processor(MovementSystem()) 
    
    esper.add_processor(CollisionSystem()) 
    
    esper.add_processor(CleanupSystem()) 
    esper.add_processor(RenderSystem(screen, font, background, background2, background3)) 

    
    start_x = SCREEN_WIDTH / 2 - PLAYER_SIZE[0] / 2
    start_y = SCREEN_HEIGHT - PLAYER_SIZE[1] - 50 

    esper.create_entity(
        Position(x=start_x, y=start_y),
        Velocity(dx=0, dy=0),
        Renderable(image=player_image, size=PLAYER_SIZE),
        PlayerControlled()
    )
    
    class MENU: 
        in_menu = True
        while in_menu:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    in_menu = False
                    game_state.is_running = False 
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_RETURN: 
                        in_menu = False 
                        game_state.current_scene = "GAME" 
                    if event.key == pygame.K_ESCAPE: 
                        in_menu = False
                        game_state.is_running = False 
            screen.fill((0, 0, 0))

            titulo_surf = font_titulo.render("RUN!", True, (255, 255, 0))
            titulo_rect = titulo_surf.get_rect(center= (18 + SCREEN_WIDTH / 2, SCREEN_HEIGHT /3)) 
            screen.blit(titulo_surf, titulo_rect)

            instrucao_surf = font_pequena.render("aperte ENTER para jogar", True, (255, 0, 255))
            instrucao_rect = instrucao_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 +10))
            screen.blit(instrucao_surf, instrucao_rect)

            sair_surf = font_pequena2.render(" ESC para sair", True, (255, 0, 0))
            screen.blit(sair_surf, (10, SCREEN_HEIGHT - 40))

            pygame.display.flip() 
            clock.tick(60) 
            
    
    while game_state.is_running: 
        dt = clock.tick(60) / 1000.0 
        
        if game_state.current_scene == "GAME":
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    game_state.is_running = False
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        game_state.is_running = False 
            
            esper.process(dt) 
        
        elif game_state.current_scene == "GAME_OVER":
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state.is_running = False
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE: 
                        game_state.is_running = False 
                    if event.key == pygame.K_r: 
                        esper.clear_database() 
                        
                        esper.create_entity(GameState(is_running=True, current_scene="GAME"))
                        game_state = esper.get_component(GameState)[0][1]
                        
                        esper.create_entity(
                            Position(x=start_x, y=start_y),
                            Velocity(dx=0, dy=0),
                            Renderable(image=player_image, size=PLAYER_SIZE),
                            PlayerControlled()
                        )
            
            screen.fill((0, 0, 0)) 
            
            go_surf = font_game_over.render("GAME OVER", True, (255, 0, 0)) 
            go_rect = go_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
            screen.blit(go_surf, go_rect)
            
            final_score_text = f"SCORE FINAL: {game_state.final_score}"
            fs_surf = font.render(final_score_text, True, (255, 255, 255)) 
            fs_rect = fs_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(fs_surf, fs_rect)
            
            inst_surf = font_pequena.render("R para reiniciar | ESC para sair", True, (255, 255, 255))
            inst_rect = inst_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))
            screen.blit(inst_surf, inst_rect)
            
            pygame.display.flip() 

    esper.clear_database() 
    pygame.quit()

if __name__ == "__main__":
    run_game()