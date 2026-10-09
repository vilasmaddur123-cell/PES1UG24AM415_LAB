import math
import pygame
from game.player import Player
from game.world import generate_platforms, draw_lava

WIDTH, HEIGHT = 500, 640
FPS = 60
BG = (20, 15, 30)
GROUND_Y = HEIGHT + 200


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lava Escape — Repair Lab")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 18, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 42, bold=True)
        self.small_font = pygame.font.SysFont("monospace", 14, bold=True)
        self.reset()

    def reset(self):
        self.platforms = generate_platforms(WIDTH, GROUND_Y)
        self.player = Player(WIDTH // 2 - 16, GROUND_Y - 50)
        self.cam_y = 0
        self.lava_y = GROUND_Y + 60
        self.lava_rise = 0.4
        self.score = 0
        self.game_over = False
        self.won = False
        self.top_y = self.platforms[-1].rect.y
        self.frame = 0
        self.surge_active = False
        self.surge_timer = 0
        self.next_surge = 600  # first surge after 10 seconds at 60 FPS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
        return True

    def update(self):
        if self.game_over or self.won:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys, self.platforms, WIDTH)

        # Update crumbling platforms and remove them after their countdown.
        for platform in self.platforms:
            platform.update()
        self.platforms = [p for p in self.platforms if not p.remove]

        # Smooth upward camera tracking.
        target = self.player.rect.centery - HEIGHT // 2
        if target < self.cam_y:
            self.cam_y = target

        # Rising lava accelerates slowly over time.
        self.lava_rise = min(1.2, self.lava_rise + 0.0003)
        self.surge_timer += 1
        if self.surge_active:
            if self.surge_timer >= 150:  # surge lasts 2.5 seconds
                self.surge_active = False
                self.surge_timer = 0
                self.next_surge = self.frame + 600
        elif self.frame >= self.next_surge:
            self.surge_active = True
            self.surge_timer = 0
        actual_rise = self.lava_rise * (2.8 if self.surge_active else 1.0)
        self.lava_y -= actual_rise

        self.score = max(0, (GROUND_Y - self.player.rect.y) // 10)
        self.frame += 1

        if self.player.rect.bottom >= self.lava_y:
            self.game_over = True
        if self.player.rect.top <= self.top_y - 20:
            self.won = True

    def draw(self):
        self.screen.fill(BG)
        for platform in self.platforms:
            platform.draw(self.screen, self.cam_y, self.frame)
        self.player.draw(self.screen, self.cam_y)
        draw_lava(self.screen, self.lava_y, self.cam_y, WIDTH, HEIGHT,
                  self.frame, self.surge_active)

        height_text = self.font.render(f"Height: {self.score}m", True, (240, 225, 205))
        self.screen.blit(height_text, (8, 8))
        help_text = self.small_font.render("A/D or arrows: move | SPACE/W/UP: jump | R: restart",
                                           True, (205, 195, 215))
        self.screen.blit(help_text, (8, 34))

        # Danger meter is based on current lava rise speed.
        speed = self.lava_rise * (2.8 if self.surge_active else 1.0)
        danger = min(1.0, speed / 1.5)
        meter_x, meter_y, meter_w, meter_h = 8, 58, 190, 16
        pygame.draw.rect(self.screen, (65, 55, 70), (meter_x, meter_y, meter_w, meter_h), border_radius=4)
        pygame.draw.rect(self.screen, (235, 75, 40) if danger > 0.65 else (230, 175, 45),
                         (meter_x, meter_y, int(meter_w * danger), meter_h), border_radius=4)
        label = "DANGER: LAVA SURGE!" if self.surge_active else "Lava danger"
        self.screen.blit(self.small_font.render(label, True, (255, 230, 210)),
                         (meter_x + meter_w + 8, meter_y))

        if self.game_over:
            self._msg("LAVA GOT YOU!", (220, 80, 40))
        elif self.won:
            self._msg("ESCAPED!", (80, 220, 100))
        pygame.display.flip()

    def _msg(self, text, color):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        msg = self.big_font.render(text, True, color)
        sub = self.font.render("Press R to Play Again", True, (220, 220, 220))
        self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 20))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
