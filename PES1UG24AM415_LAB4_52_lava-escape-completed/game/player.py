import pygame

SPEED = 4
GRAVITY = 0.55
MAX_FALL_SPEED = 12
NORMAL_JUMP = -13
SPRING_JUMP = -19


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vel_y = 0.0
        self.on_ground = False
        self.color = (60, 160, 220)

    def update(self, keys, platforms, width):
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = SPEED

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = NORMAL_JUMP
            self.on_ground = False

        previous_bottom = self.rect.bottom
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        self.rect.x = max(0, min(width - self.rect.width, self.rect.x + dx))
        self.rect.y += int(self.vel_y)
        self.on_ground = False

        # One-way platform collision: only land while descending, and only if
        # the player's feet crossed the platform's top during this frame.
        if self.vel_y > 0:
            for platform in platforms:
                p = platform.rect
                horizontal_overlap = self.rect.right > p.left and self.rect.left < p.right
                crossed_top = previous_bottom <= p.top and self.rect.bottom >= p.top
                if horizontal_overlap and crossed_top:
                    self.rect.bottom = p.top
                    if platform.kind == "spring":
                        self.vel_y = SPRING_JUMP
                    else:
                        self.vel_y = 0
                        self.on_ground = True
                        platform.landed_on()
                    break

    def draw(self, screen, cam_y):
        dr = self.rect.move(0, -int(cam_y))
        pygame.draw.rect(screen, self.color, dr, border_radius=6)
        pygame.draw.circle(screen, (255, 220, 180), (dr.centerx, dr.top + 8), 7)
