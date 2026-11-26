import math
import pygame
import torch
import torch.nn as nn

# 1. Neural Network (5 rays -> 16 hidden neurons -> 3 actions)
class AgentBrain(nn.Module):
    def __init__(self, num_rays=5, num_actions=3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(num_rays, 16),
            nn.ReLU(),
            nn.Linear(16, num_actions)
        )

    def forward(self, x):
        return self.net(x)

# 2. Ray Casting Function (returns normalized distances AND hit points for drawing)
def cast_rays(pos, angle, walls, num_rays=5, fov=90, max_dist=180):
    distances = []
    hit_points = []
    start_angle = angle - fov / 2
    step = fov / (num_rays - 1) if num_rays > 1 else 0

    for i in range(num_rays):
        ray_angle = math.radians(start_angle + i * step)
        end_x = pos[0] + math.cos(ray_angle) * max_dist
        end_y = pos[1] + math.sin(ray_angle) * max_dist

        closest_dist = max_dist
        closest_point = (end_x, end_y)

        for wall in walls:
            # clipline returns ((x1, y1), (x2, y2)) if the line intersects the rect
            clipped = wall.clipline(pos, (end_x, end_y))
            if clipped:
                hit_x, hit_y = clipped[0]
                dist = math.hypot(hit_x - pos[0], hit_y - pos[1])
                if dist < closest_dist:
                    closest_dist = dist
                    closest_point = (hit_x, hit_y)

        distances.append(closest_dist / max_dist)
        hit_points.append(closest_point)

    return distances, hit_points

# 3. Pygame Window & Simulation Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Ray-Casting Neural Network")
clock = pygame.time.Clock()

# Arena border walls + inner obstacles
walls = [
    pygame.Rect(0, 0, WIDTH, 20),
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
    pygame.Rect(0, 0, 20, HEIGHT),
    pygame.Rect(WIDTH - 20, 0, 20, HEIGHT),
    pygame.Rect(250, 150, 80, 300),
    pygame.Rect(500, 100, 80, 250),
    pygame.Rect(450, 420, 200, 60),
]

brain = AgentBrain(num_rays=5, num_actions=3)
agent_pos = [120.0, 300.0]
agent_angle = 0.0
speed = 3.0

# 4. Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Cast rays and get sensor readings
    ray_distances, ray_hits = cast_rays(agent_pos, agent_angle, walls)

    # Pass sensor readings into the Neural Network
    state_tensor = torch.tensor(ray_distances, dtype=torch.float32)
    with torch.no_grad():
        action = torch.argmax(brain(state_tensor)).item()

    # Apply network output (0 = Turn Left, 1 = Go Straight, 2 = Turn Right)
    if action == 0:
        agent_angle -= 4.0
    elif action == 2:
        agent_angle += 4.0

    # Move agent forward
    rad = math.radians(agent_angle)
    agent_pos[0] += math.cos(rad) * speed
    agent_pos[1] += math.sin(rad) * speed

    # Reset position if the agent hits a wall
    agent_rect = pygame.Rect(agent_pos[0] - 10, agent_pos[1] - 10, 20, 20)
    if any(agent_rect.colliderect(w) for w in walls):
        agent_pos = [120.0, 300.0]
        agent_angle = 0.0

    # --- DRAWING ---
    screen.fill((25, 28, 36))  # Dark background

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, (90, 100, 120), wall)

    # Draw rays and red collision dots
    for hit in ray_hits:
        pygame.draw.line(screen, (0, 255, 140), agent_pos, hit, 2)
        pygame.draw.circle(screen, (255, 70, 70), (int(hit[0]), int(hit[1])), 4)

    # Draw agent circle and heading indicator
    pygame.draw.circle(screen, (60, 180, 255), (int(agent_pos[0]), int(agent_pos[1])), 12)
    nose_x = agent_pos[0] + math.cos(rad) * 18
    nose_y = agent_pos[1] + math.sin(rad) * 18
    pygame.draw.line(screen, (255, 255, 255), agent_pos, (nose_x, nose_y), 3)

    pygame.display.flip()
    clock.tick(60)  # Cap at 60 FPS

pygame.quit()
