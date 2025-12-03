import pygame
import random
import math
from dataclasses import dataclass

pygame.init()

# Internal "pixel" resolution (your simulation runs here)
VIRTUAL_W, VIRTUAL_H = 320, 240

# Scale factor for display (4x = 1280x960, perfect crisp pixels)
SCALE = 2

screen = pygame.display.set_mode((VIRTUAL_W * SCALE, VIRTUAL_H * SCALE))
pygame.display.set_caption("Pixel Fireworks Simulator")

# This is our simulation surface (pixel-perfect)
virtual_screen = pygame.Surface((VIRTUAL_W, VIRTUAL_H))

clock = pygame.time.Clock()
running = True

################################################

@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    color: tuple       # (r, g, b)
    life: float        # decreases over time
    decay: float       # how fast life decreases
    gravity: float = 0.07
    trail: list = None # optional trail particles

particles = []
rockets = []  # rockets going up before exploding

####################################################

def launch_rocket():
    rockets.append({
        "x": random.randint(40, VIRTUAL_W-40),
        "y": VIRTUAL_H,
        "vy": random.uniform(-3.5, -4.8),
        "color": (random.randint(100,255), random.randint(100,255), random.randint(100,255)),
        "exploded": False
    })

def explode(rocket):
    cx, cy = rocket["x"], rocket["y"]
    color = rocket["color"]
    num_particles = random.randint(80, 140)

    for _ in range(num_particles):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(0.5, 3.0)
        particles.append(Particle(
            x=cx,
            y=cy,
            vx=math.cos(angle) * speed,
            vy=math.sin(angle) * speed,
            color=color,
            life=1.0,
            decay=random.uniform(0.008, 0.018)
        ))

##############################################################################

frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            launch_rocket()  # click to launch

    # Auto-launch every ~1.5–3 seconds
    if frame % (30 + random.randint(0,90)) == 0:
        launch_rocket()
    frame += 1

    # Update rockets
    for r in rockets[:]:
        r["y"] += r["vy"]
        r["vy"] += 0.07  # gravity pulls up-rocket down when vy > 0
        if r["vy"] > 0 and not r["exploded"]:  # peaked
            explode(r)
            r["exploded"] = True
            rockets.remove(r)

    # Update particles
    for p in particles[:]:
        p.vy += p.gravity
        p.x += p.vx
        p.y += p.vy
        p.life -= p.decay

        if p.life <= 0 or p.y > VIRTUAL_H:
            particles.remove(p)

    # Draw everything on virtual_screen (pixel level)
    virtual_screen.fill((5, 5, 15))  # dark night sky

    # Draw rockets (small bright line or dot)
    for r in rockets:
        pygame.draw.circle(virtual_screen, r["color"], (int(r["x"]), int(r["y"])), 3)

    # Draw particles (single pixels or small circles for glow)
    # Draw particles
    for p in particles[:]:
        p.vy += p.gravity
        p.x += p.vx
        p.y += p.vy
        p.life -= p.decay

        if p.life <= 0 or p.y > VIRTUAL_H:
            particles.remove(p)
            continue

        # ← THIS IS THE FIXED LINE
        brightness = p.life
        color = tuple(min(255, int(c * brightness * 2.2)) for c in p.color)
        #                                         ^^^^^^^^ dot, not ["color"]

        radius = max(1, int(brightness * 3))
        pygame.draw.circle(virtual_screen, color, (int(p.x), int(p.y)), radius)

    # Optional: draw trails
    # (you can append (x,y) positions and draw fading lines)

    # Scale up and blit to real screen (nearest-neighbor = crisp pixels!)
    scaled = pygame.transform.scale(virtual_screen, screen.get_size())
    screen.blit(scaled, (0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()