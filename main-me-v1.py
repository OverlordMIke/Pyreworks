import pygame
import math, random
from dataclasses import dataclass
from rocket_presets import ROCKET_PRESETS


def activate_particle(x,y,vx,vy,colour,life,decay,gravity:float=0.07):
    for i in range(len(particle_active)):
        if not particle_active[i]:
            particle_x[i] = x
            particle_y[i] = y
            particle_vx[i] = vx
            particle_vy[i] = vy
            particle_colour[i] = colour
            particle_life[i] = life
            particle_decay[i] = decay
            particle_gravity[i] = gravity
            particle_active[i] = True
            return
    print("Not enough particles available in pool.")

def launch_rocket(rocket_name: str, pos_x: int):
    if rocket_name not in ROCKET_PRESETS:
        preset_name = "ClassicRandom"
    
    preset = ROCKET_PRESETS[rocket_name]

    pattern_red = preset["theme"]["pattern"][0]
    pattern_green = preset["theme"]["pattern"][1]
    pattern_blue = preset["theme"]["pattern"][2]

    if pattern_red == "random": pattern_red = random.randrange(255)
    if pattern_green == "random": pattern_green = random.randrange(255)
    if pattern_blue == "random": pattern_blue = random.randrange(255)

    rockets.append({
        "x": pos_x,
        "y": canvas_height,
        "vy": 0,
        "vx": 0,
        "theme": {
            "body": preset["theme"]["body"],
            "exhaust": preset["theme"]["exhaust"],
            "pattern": (
                pattern_red,
                pattern_green,
                pattern_blue
            )
        },
        "fuel": preset["fuel"],
        "thrust_strength": preset["thrust_strength"],
        "burning": True,
        "fuse": preset["fuse"],
        "exploded": False
    })

def explode(rocket):
    cx, cy = rocket["x"], rocket["y"]
    colour = rocket["theme"]["pattern"]
    num_particles = random.randint(80, 140)

    for _ in range(num_particles):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(0.5, 30.0)
        activate_particle(
            cx,
            cy,
            math.cos(angle) * speed,
            math.sin(angle) * speed,
            colour,
            1.0,
            random.uniform(0.5, 1.0),
            7
        )

def physics_update(delta):
    for r in rockets[:]:
        r["y"] += r["vy"] * delta
        r["x"] += r["vx"] * delta
        r["vy"] += 30 * delta
        if r["fuel"] > 0: r["burning"] = True
        else: r["burning"] = False
        if r["burning"]:
            r["vy"] -= r["thrust_strength"] * delta
            r["fuel"] -= 1 * delta
            activate_particle(
                r["x"],
                r["y"],
                r["vx"] + random.uniform(-6, 6),
                #(r["vy"] * 0.9) + 
                random.uniform(-6, 6),
                r["theme"]["exhaust"],
                1.0,
                random.uniform(0.5, 1.0),
                30
            )
        if abs(r["vx"]) < abs(global_wind):
            r["vx"] += global_wind * 0.03 * delta
        if r["fuse"] < 0 and not r["exploded"]:
            explode(r)
            r["exploded"] = True
            rockets.remove(r)
        else:
            r["fuse"] -= 1 * delta
    
    for i in range(len(particle_active)):
        if particle_active[i]:
            particle_vy[i] += particle_gravity[i] * delta
            if abs(particle_vx[i]) < abs(global_wind):
                particle_vx[i] += global_wind * 0.06 * delta
            particle_x[i] += particle_vx[i] * delta
            particle_y[i] += particle_vy[i] * delta
            particle_life[i] += -particle_decay[i] * delta

            if particle_life[i] <= 0 or particle_y[i] > canvas_height:
                particle_active[i] = False


def draw_update(canvas_screen, screen, current_fps, delta):
    global particle_peak
    canvas_screen.fill((5,5,20))

    for r in rockets:
        canvas_screen.set_at((round(r["x"]), round(r["y"])), r["theme"]["body"])
    
    for i in range(len(particle_active)):
        if particle_active[i]:
            brightness = particle_life[i]
            colour = tuple(min(255, int(c * brightness * 2.2)) for c in particle_colour[i])
            canvas_screen.set_at((round(particle_x[i]), round(particle_y[i])),colour)
    
    scaled = pygame.transform.scale(canvas_screen, screen.get_size())
    screen.blit(scaled, (0,0))

    screen_text = pygame.font.Font(None, 24 * window_scale).render(f"FPS: {current_fps}", True, (255,255,255))
    screen.blit(screen_text, (10 * window_scale, 10 * window_scale))
    screen_text = pygame.font.Font(None, 24 * window_scale).render(f"Delta: {delta}", True, (255,255,255))
    screen.blit(screen_text, (10 * window_scale, 30 * window_scale))

    pygame.display.flip()


particle_max = 2000
particle_x = [0 for _ in range(particle_max)]
particle_y = [0 for _ in range(particle_max)]
particle_vx = [0 for _ in range(particle_max)]
particle_vy = [0 for _ in range(particle_max)]
particle_colour = [(0,0,0) for _ in range(particle_max)]
particle_life = [0 for _ in range(particle_max)]
particle_decay = [0 for _ in range(particle_max)]
particle_gravity = [0.07 for _ in range(particle_max)]
particle_active = [False for _ in range(particle_max)]

canvas_width, canvas_height = 800, 600
window_scale = 1
rockets = []
last_launch_time = 0
particle_peak = 0
global_wind = 10

def main():
    global last_launch_time
    pygame.init()

    screen = pygame.display.set_mode((canvas_width*window_scale, canvas_height*window_scale))
    pygame.display.set_caption("Pyrotechnician")

    canvas_screen = pygame.Surface((canvas_width, canvas_height))

    clock = pygame.time.Clock()

    running = True

    delta = 1/60

    while running:
        fps = clock.get_fps()
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                launch_pos = random.uniform(40, canvas_width-40)
                launch_rocket("ClassicRandom", launch_pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    launch_rocket("ClassicRed", canvas_width/4)
                if event.key == pygame.K_w:
                    launch_rocket("ClassicWhite", canvas_width/4*2)
                if event.key == pygame.K_b:
                    launch_rocket("ClassicBlue", canvas_width/4*3)
        
        #if (current_time - last_launch_time) >= 500:
        #    last_launch_time = current_time
        #    launch_pos = random.uniform(40, canvas_width-40)
        #    launch_rocket(f"ClassicRandom", launch_pos)

        physics_update(delta)
        draw_update(canvas_screen, screen, fps, delta)
        delta = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
    pygame.quit()