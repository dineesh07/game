import pygame
import random

# ----- CONFIG -----
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 1
JUMP_VELOCITY = -15
PLAYER_SPEED = 5
BG_COLOR = (135, 206, 235)  # sky blue

# ----- INIT -----
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Physics Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# ----- PLAYER CLASS -----
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(100, 500))
        self.velocity = 0
        self.health = 100
        self.score = 0
        self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity = JUMP_VELOCITY
            self.on_ground = False

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.velocity = 0
            self.on_ground = True

# ----- ANIMAL CLASS -----
class Animal(pygame.sprite.Sprite):
    def __init__(self, is_harmful):
        super().__init__()
        self.is_harmful = is_harmful
        img = "animal_bad.png" if is_harmful else "animal_good.png"
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1600), 500))
        self.speed = random.randint(4, 8)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = random.randint(900, 1600)

# ----- HUD -----
def draw_hud(screen, health, score):
    health_text = font.render(f"Health: {health}", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))

# ----- OPTIONAL PHYSICS & MATH -----
def calculate_jump_velocity(force, mass):
    return force / mass

def get_jump_arc(velocity, gravity):
    return (velocity ** 2) / (2 * gravity)

def calculate_score(survival_time, landings):
    return int(survival_time * 0.5 + landings * 10)

# ----- OPTIONAL CHEMISTRY -----
def is_toxic(entity_type):
    return entity_type in ["snake", "scorpion"]

def apply_chemical_effect(player, entity_type):
    if is_toxic(entity_type):
        player.health -= 10
    else:
        player.health += 5

# ----- GAME OBJECTS -----
player = Player()
player_group = pygame.sprite.GroupSingle(player)

animals_group = pygame.sprite.Group()
for _ in range(5):
    animal = Animal(is_harmful=random.choice([True, False]))
    animals_group.add(animal)

# ----- GAME LOOP -----
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump()

    # Update
    player_group.update()
    animals_group.update()

    # Collision Check
    for animal in animals_group:
        if player.rect.colliderect(animal.rect):
            if animal.is_harmful:
                player.health -= 10
                if player.health <= 0:
                    print("Game Over!")
                    running = False
            else:
                player.score += 10
            animal.rect.left = random.randint(900, 1600)

    # Draw
    animals_group.draw(screen)
    player_group.draw(screen)
    draw_hud(screen, player.health, player.score)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
