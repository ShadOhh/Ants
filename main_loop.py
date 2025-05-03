import pygame
from world import World

pygame.init()
default_size = (1000, 1000)
screen = pygame.display.set_mode(default_size)
clock = pygame.time.Clock()
running = True
base_width, base_height = default_size

gameworld = World(screen, default_size[0], default_size[1], 50)

# New: FPS font setup
fps_font = pygame.font.SysFont(None, 24)

def draw_fps(screen, fps):
    fps_color = "green" if fps >= 30 else "red"  
    fps_text = fps_font.render(f"FPS: {int(fps)}", True, fps_color)
    screen.blit(fps_text, (10, 10))

while running:
    current_width, current_height = screen.get_size()
    screen.fill("white")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                gameworld.addAnt(pygame.mouse.get_pos())
            elif event.button == 3:
                gameworld.addFood(pygame.mouse.get_pos())
            elif event.button == 2:
                gameworld.addColony(pygame.mouse.get_pos())

    gameworld.update()    
    
    fps = clock.get_fps()
    draw_fps(screen, fps)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
