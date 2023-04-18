import sys
import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width=0, height=0):
        super().__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.scaled_image = None
        self.target_health = 100
        self.health_bar_length = 200
        self.health_ratio = self.target_health / self.health_bar_length
        self.health_timer = 0
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height
        self.vel = 5

    def boundries(self):
        if player.rect.x > self.vel:
            player.rect.x -= self.vel

        if player.rect.x < 1280 - self.vel - self.rect.width:
            player.rect.x += self.vel

        if player.rect.y > self.vel:
            player.rect.y -= self.vel

        if player.rect.y < 720 - self.vel - self.rect.height:
            player.rect.y += self.vel

    def health_bar(self):
        self.HealthBar = pygame.draw.rect(
            screen, (255, 0, 0), (10, 10, self.target_health / self.health_ratio, 25)
        )
        pygame.draw.rect(
            screen, (255, 255, 255), (10, 10, self.health_bar_length, 25), 4
        )

    def update(self):
        self.health_bar()
        self.boundries()

    def shape(self, scale_factor):
        if self.scaled_image is None:
            self.scaled_image = pygame.transform.scale(
                self.image,
                (
                    int(self.image.get_width() * scale_factor),
                    int(self.image.get_height() * scale_factor),
                ),
            )
        self.rect = self.scaled_image.get_rect(topleft=(self.rect.x, self.rect.y))
        return self.scaled_image.get_rect()

    def get_damage(self, amount):
        current_time = pygame.time.get_ticks()

        if current_time > self.health_timer:
            self.target_health -= amount
            self.health_timer = current_time + 100

        if self.target_health <= 0:
            print("You Died!")
            pygame.quit()
            sys.exit(0)


pygame.mixer.init()
pygame.mixer.music.load("Assets/done/Music.mp3")
pygame.mixer.music.play(-1)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True
clock = pygame.time.Clock()
dt = 2
player = "Assets/done/characteran1.png"
#   'Assets/done/characteran3.png']
obsticle = "Assets/done/Spike.png"

player = Sprite(player, 0, 0, 110, 150)
obsticle = Sprite(obsticle, 1205, 400)
obsticle.shape(5.0)
player.health_bar()
sprite_group = pygame.sprite.Group()
sprite_group.add(player, obsticle)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit(0)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.rect.y -= 3 * dt
    if keys[pygame.K_s]:
        player.rect.y += 3 * dt
    if keys[pygame.K_a]:
        player.rect.x -= 3 * dt
    if keys[pygame.K_d]:
        player.rect.x += 3 * dt

    screen.fill("Green")
    screen.blit(player.image, player.rect)
    screen.blit(obsticle.scaled_image, obsticle.rect)
    player.update()

    for obj1 in sprite_group:
        for obj2 in sprite_group:
            if obj1 != obj2 and obj1.rect.colliderect(obj2.rect):
                player.get_damage(10)
                pygame.draw.rect(screen, (255, 0, 0), player.rect)
                pygame.draw.rect(screen, (255, 0, 0), obsticle.rect)

    clock.tick(60) / 1000
    pygame.display.update()
    pygame.display.flip()
