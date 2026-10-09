import math
import random
import pygame

PLATFORM_COLOR = (100, 80, 50)
CRUMBLE_COLOR = (190, 105, 55)
SPRING_COLOR = (50, 205, 115)
LAVA_COLOR = (220, 60, 20)


class Platform:
    """A platform with a type and optional crumbling behavior."""

    def __init__(self, rect, kind="normal"):
        self.rect = pygame.Rect(rect)
        self.kind = kind  # normal, crumble, spring
        self.crumble_timer = None
        self.remove = False

    def landed_on(self):
        if self.kind == "crumble" and self.crumble_timer is None:
            self.crumble_timer = 0

    def update(self):
        if self.crumble_timer is not None:
            self.crumble_timer += 1
            if self.crumble_timer >= 48:  # about 0.8 seconds at 60 FPS
                self.remove = True

    def draw(self, screen, cam_y, frame):
        r = self.rect.move(0, -int(cam_y))
        if self.kind == "crumble":
            color = CRUMBLE_COLOR
            if self.crumble_timer is not None:
                # Shake more noticeably as the platform approaches collapse.
                if self.crumble_timer < 38:
                    r.x += random.choice((-2, -1, 0, 1, 2))
                    r.y += random.choice((-1, 0, 1))
                color = (230, max(45, 130 - self.crumble_timer * 2), 45)
        elif self.kind == "spring":
            color = SPRING_COLOR
        else:
            color = PLATFORM_COLOR
        pygame.draw.rect(screen, color, r, border_radius=4)
        if self.kind == "spring":
            # Small coil marks make spring platforms visually distinct.
            for x in range(r.left + 8, r.right - 5, 14):
                pygame.draw.line(screen, (225, 255, 225), (x, r.top + 3),
                                 (min(x + 5, r.right - 2), r.bottom - 3), 2)


def generate_platforms(width, base_y, count=30):
    platforms = [Platform(pygame.Rect(0, base_y, width, 20), "normal")]
    y = base_y - 110
    for i in range(count):
        w = random.randint(80, 200)
        x = random.randint(0, width - w)
        # Keep a mix of regular, crumbling, and spring platforms.
        roll = random.random()
        if roll < 0.20:
            kind = "crumble"
        elif roll < 0.36:
            kind = "spring"
        else:
            kind = "normal"
        platforms.append(Platform(pygame.Rect(x, y, w, 16), kind))
        y -= random.randint(80, 130)
    return platforms


def draw_lava(screen, lava_y, cam_y, width, height, frame, surge_active=False):
    ly = int(lava_y - cam_y)
    if ly < height:
        pts = [(0, ly)]
        for x in range(0, width + 20, 20):
            wave = math.sin(x * 0.08 + frame * (0.16 if surge_active else 0.1))
            pts.append((x, ly + int(wave * (12 if surge_active else 8))))
        pts.extend([(width, height), (0, height)])
        pygame.draw.polygon(screen, LAVA_COLOR, pts)
        glow = pygame.Surface((width, 30), pygame.SRCALPHA)
        for i in range(15):
            alpha = max(0, 65 - i * 4)
            pygame.draw.line(glow, (255, 100, 0, alpha), (0, i), (width, i), 1)
        screen.blit(glow, (0, ly - 15))
