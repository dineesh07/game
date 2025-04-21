import pygame
import random
import math

# ----- CONFIG -----
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRANCH_Y_POSITION = 200  # Fixed Y position for the branch
SWING_RADIUS = 100
SWING_SPEED = 0.05
PLAYER_SIZE = 40
GRAVITY = 0.02  # Even slower gravity for descending
MAX_DESCEND_SPEED = 0.5  # Max descend speed is slower
GOOD_ANIMAL_SIZE = 40
BAD_ANIMAL_SIZE = 40
GROUND_Y_POSITION = SCREEN_HEIGHT - 40  # The ground level for collision

# ----- INIT -----
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Swinging Branches with Control (Test Version)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# ----- PLAYER -----
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = math.pi / 2  # Start straight down (initial position)
        self.swing_speed = SWING_SPEED
        self.descend_speed = 0  # Controls how fast the player can descend
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill((0, 0, 255))  # Blue square (player)
        self.rect = self.image.get_rect()
        self.rect.centerx = 400  # Starting X position
        self.rect.centery = BRANCH_Y_POSITION  # Starting Y position (branch height)

    def update_position(self):
        cx = 400  # X-position of vine/branch anchor (centered horizontally)
        cy = BRANCH_Y_POSITION if self.descend_speed == 0 else self.rect.centery  # Branch position when swinging, player's own Y when descending
        self.rect.centerx = cx + SWING_RADIUS * math.cos(self.angle)
        self.rect.centery = cy + SWING_RADIUS * math.sin(self.angle)

    def update(self):
        # Apply gravity for swinging motion
        if self.descend_speed == 0:  # Swinging only when not descending
            self.angle += self.swing_speed
            if self.angle > 1.5:  # Limit swing right
                self.swing_speed = -self.swing_speed  # Reverse direction
            elif self.angle < 0.5:  # Limit swing left
                self.swing_speed = -self.swing_speed  # Reverse direction

        # If descending, move straight down
        if self.descend_speed > 0:
            self.rect.centery += self.descend_speed
            if self.rect.centery >= GROUND_Y_POSITION:  # Stop descending when hitting the ground
                self.rect.centery = GROUND_Y_POSITION
                self.descend_speed = 0  # Stop moving downward when hitting ground
        self.update_position()

    def descend(self):
        # Start descending when the down arrow is pressed
        if self.rect.centery < GROUND_Y_POSITION:  # Only allow descending if above the ground
            if self.descend_speed < MAX_DESCEND_SPEED:
                self.descend_speed += GRAVITY  # Increase speed slowly as the player descends

    def stop_descending(self):
        # Stop descending when the down arrow is released
        self.descend_speed = 0


# ----- ANIMAL -----
class Animal(pygame.sprite.Sprite):
    def __init__(self, is_harmful):
        super().__init__()
        self.is_harmful = is_harmful
        self.image = pygame.Surface((GOOD_ANIMAL_SIZE, GOOD_ANIMAL_SIZE))
        self.image.fill((255, 0, 0) if is_harmful else (0, 255, 0))  # Red for harmful, green for good
        self.rect = self.image.get_rect(midbottom=(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT))
        self.speed = random.randint(4, 8)

    def update(self):
        # Move the animal horizontally across the screen
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 400)


# ----- HUD -----
def draw_hud(screen, score):
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))


# ----- GAME OBJECTS -----
player = Player()
player_group = pygame.sprite.GroupSingle(player)

animals_group = pygame.sprite.Group()
for _ in range(5):
    animal = Animal(is_harmful=random.choice([True, False]))
    animals_group.add(animal)

score = 0
running = True

# ----- GAME LOOP -----
while running:
    screen.fill((135, 206, 235))  # Sky blue background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.descend()  # Start descending when down arrow is pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.stop_descending()  # Stop descending when down arrow is released

    # Update
    player_group.update()
    animals_group.update()

    # Collision Check with animals
    for animal in animals_group:
        if player.rect.colliderect(animal.rect):
            if animal.is_harmful:
                print("Game Over!")
                running = False
            else:
                score += 10  # Increase score for collecting good animals
            animal.rect.left = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 400)

    # Draw Branch (Fixed)
    pygame.draw.line(screen, (139, 69, 19), (0, BRANCH_Y_POSITION), (SCREEN_WIDTH, BRANCH_Y_POSITION), 4)

    # Draw everything
    animals_group.draw(screen)
    player_group.draw(screen)
    draw_hud(screen, score)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
