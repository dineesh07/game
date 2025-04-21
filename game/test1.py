import pygame
import random
import math

# ----- CONFIG -----
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRANCH_Y_POSITION = 200
SWING_RADIUS = 100
SWING_SPEED = 0.05
PLAYER_SIZE = 40
GRAVITY = 0.02
MAX_DESCEND_SPEED = 0.5
GOOD_ANIMAL_SIZE = 40
BAD_ANIMAL_SIZE = 40
GROUND_Y_POSITION = SCREEN_HEIGHT - 40

# ----- INIT -----
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Swinging Branches with Math")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
small_font = pygame.font.SysFont("arial", 20)

# ----- PLAYER -----
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = math.pi / 2
        self.swing_speed = SWING_SPEED
        self.descend_speed = 0
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.centery = BRANCH_Y_POSITION

    def update_position(self):
        cx = 400
        cy = BRANCH_Y_POSITION if self.descend_speed == 0 else self.rect.centery
        self.rect.centerx = cx + SWING_RADIUS * math.cos(self.angle)
        self.rect.centery = cy + SWING_RADIUS * math.sin(self.angle)

    def update(self):
        if self.descend_speed == 0:
            self.angle += self.swing_speed
            if self.angle > 1.5 or self.angle < 0.5:
                self.swing_speed = -self.swing_speed
        if self.descend_speed > 0:
            self.rect.centery += self.descend_speed
            if self.rect.centery >= GROUND_Y_POSITION:
                self.rect.centery = GROUND_Y_POSITION
                self.descend_speed = 0
        self.update_position()

    def descend(self):
        if self.rect.centery < GROUND_Y_POSITION:
            if self.descend_speed < MAX_DESCEND_SPEED:
                self.descend_speed += GRAVITY

    def stop_descending(self):
        self.descend_speed = 0

# ----- ANIMAL -----
class Animal(pygame.sprite.Sprite):
    def __init__(self, answer, is_correct):
        super().__init__()
        self.answer = answer
        self.is_correct = is_correct
        self.image = pygame.Surface((GOOD_ANIMAL_SIZE, GOOD_ANIMAL_SIZE))
        self.image.fill((0, 255, 0) if is_correct else (255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 400), SCREEN_HEIGHT))
        self.speed = random.randint(4, 8)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 400)

    def draw_with_text(self, surface):
        surface.blit(self.image, self.rect)
        text = small_font.render(str(self.answer), True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

# ----- HUD -----
def draw_hud(screen, score, lives, question):
    text = font.render(f"Score: {score}   Lives: {lives}   Question: {question}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

# ----- GAME SETUP -----
def generate_math_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    correct = num1 + num2
    question_text = f"{num1} + {num2} = ?"
    answers = [correct]

    while len(answers) < 3:
        wrong = correct + random.choice([-3, -2, -1, 1, 2, 3])
        if wrong not in answers and wrong > 0:
            answers.append(wrong)

    random.shuffle(answers)
    animals = []
    for ans in answers:
        animals.append(Animal(ans, ans == correct))

    return question_text, animals

# ----- GAME OBJECTS -----
player = Player()
player_group = pygame.sprite.GroupSingle(player)
animals_group = pygame.sprite.Group()

question, animal_list = generate_math_question()
for animal in animal_list:
    animals_group.add(animal)

score = 0
lives = 3
running = True

# ----- GAME LOOP -----
while running:
    screen.fill((135, 206, 235))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.descend()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.stop_descending()

    # Update
    player_group.update()
    animals_group.update()

    # Collision check
    for animal in animals_group:
        if player.rect.colliderect(animal.rect):
            if animal.is_correct:
                score += 10
                question, animal_list = generate_math_question()
                animals_group.empty()
                for new_animal in animal_list:
                    animals_group.add(new_animal)
            else:
                lives -= 1
                if lives <= 0:
                    print("Game Over!")
                    running = False
                else:
                    print(f"Wrong! Lives left: {lives}")
                    # Refresh animals only on wrong answer too
                    question, animal_list = generate_math_question()
                    animals_group.empty()
                    for new_animal in animal_list:
                        animals_group.add(new_animal)
            break

    # Draw
    pygame.draw.line(screen, (139, 69, 19), (0, BRANCH_Y_POSITION), (SCREEN_WIDTH, BRANCH_Y_POSITION), 4)
    for animal in animals_group:
        animal.draw_with_text(screen)

    player_group.draw(screen)
    draw_hud(screen, score, lives, question)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
