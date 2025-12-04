import pygame
import math, random
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
            particle_max_life[i] = life
            particle_decay[i] = decay
            particle_gravity[i] = gravity
            particle_active[i] = True
            return
    print("Not enough particles available in pool.")

def launch_rocket(rocket_name: str, pos_x: int):
    if rocket_name not in ROCKET_PRESETS:
        preset_name = "ClassicRandom"
    
    preset = ROCKET_PRESETS[rocket_name]

    rockets.append({
        "x": pos_x,
        "y": canvas_height,
        "vy": 0,
        "vx": 0,
        "theme": {
            "body": preset["theme"]["body"],
            "exhaust": preset["theme"]["exhaust"],
            "pattern": preset["theme"]["pattern"]
        },
        "fuel": preset["fuel"],
        "thrust_strength": preset["thrust_strength"],
        "burning": True,
        "fuse": preset["fuse"],
        "exploded": False
    })

def explode(rocket):
    cx, cy = rocket["x"], rocket["y"]
    pattern = rocket["theme"]["pattern"]
    for layer in pattern:
        num_particles = layer["particle_count"] + random.randint(-layer["count_randomness"], layer["count_randomness"])

        pattern_red = layer["colour"][0]
        pattern_green = layer["colour"][1]
        pattern_blue = layer["colour"][2]

        if pattern_red == "random": pattern_red = random.randrange(255)
        if pattern_green == "random": pattern_green = random.randrange(255)
        if pattern_blue == "random": pattern_blue = random.randrange(255)

        for _ in range(num_particles):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(layer["explosive_force_min"], layer["explosive_force_max"])
            activate_particle(
                cx,
                cy,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                (pattern_red, pattern_green, pattern_blue),
                layer["life"],
                layer["decay"] + random.uniform(-layer["decay_randomness"], layer["decay_randomness"]),
                7
            )

def physics_update(delta):
    for r in rockets[:]:
        r["y"] += r["vy"] * delta
        r["x"] += r["vx"] * delta
        r["vy"] += 60 * delta
        if r["fuel"] > 0: r["burning"] = True
        else: r["burning"] = False
        if r["burning"]:
            r["vy"] -= r["thrust_strength"] * delta
            r["fuel"] -= 1 * delta
            activate_particle(
                r["x"],
                r["y"],
                r["vx"] + random.uniform(-6, 6),
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
            particle_vx[i] *= 1 - 0.75 * delta
            particle_vy[i] *= 1 - 0.75 * delta
            particle_x[i] += particle_vx[i] * delta
            particle_y[i] += particle_vy[i] * delta
            particle_life[i] += -particle_decay[i] * delta

            if particle_life[i] <= 0 or particle_y[i] > canvas_height:
                particle_active[i] = False


def draw_update(canvas_screen, screen, current_fps, delta):
    canvas_screen.fill((5,5,20))

    for r in rockets:
        canvas_screen.set_at((round(r["x"]), round(r["y"])), r["theme"]["body"])
    
    for i in range(len(particle_active)):
        if particle_active[i]:
            #fade_factor = particle_life[i] / particle_max_life[i]
            #colour = tuple(int(c * fade_factor) for c in particle_colour[i])
            brightness = particle_life[i] / particle_max_life[i]
            colour = tuple(min(255, int(c * brightness * 2.2)) for c in particle_colour[i])
            canvas_screen.set_at((round(particle_x[i]), round(particle_y[i])),colour)
    
    scaled = pygame.transform.scale(canvas_screen, screen.get_size())
    screen.blit(scaled, (0,0))

    screen_text = pygame.font.Font(None, 24 * window_scale).render(f"FPS: {current_fps}", True, (255,255,255))
    screen.blit(screen_text, (10 * window_scale, 10 * window_scale))
    screen_text = pygame.font.Font(None, 24 * window_scale).render(f"Delta: {delta}", True, (255,255,255))
    screen.blit(screen_text, (10 * window_scale, 30 * window_scale))
    screen_text = pygame.font.Font(None, 24 * window_scale).render(f"Current Rocket: {active_rocket}", True, (255,255,255))
    screen.blit(screen_text, (10 * window_scale, 50 * window_scale))

    pygame.display.flip()

def cycle_available_rockets(dir:int = 1):
    global active_rocket_index, active_rocket
    new_index = (active_rocket_index + dir) % len(available_rockets)
    active_rocket = available_rockets[new_index]
    active_rocket_index = new_index

particle_max = 10_000
particle_x = [0 for _ in range(particle_max)]
particle_y = [0 for _ in range(particle_max)]
particle_vx = [0 for _ in range(particle_max)]
particle_vy = [0 for _ in range(particle_max)]
particle_colour = [(0,0,0) for _ in range(particle_max)]
particle_life = [0 for _ in range(particle_max)]
particle_max_life = [0 for _ in range(particle_max)]
particle_decay = [0 for _ in range(particle_max)]
particle_gravity = [0.07 for _ in range(particle_max)]
particle_active = [False for _ in range(particle_max)]

canvas_width, canvas_height = 854, 480
window_scale = 2
rockets = []
last_launch_time = 0
global_wind = 10

available_rockets = list(ROCKET_PRESETS.keys())
active_rocket = available_rockets[0]
active_rocket_index = 0

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
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    launch_pos = mouse_x / window_scale
                    launch_rocket(active_rocket, launch_pos)
                if event.button == 4:
                    cycle_available_rockets(1)
                if event.button == 5:
                    cycle_available_rockets(-1)
        
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