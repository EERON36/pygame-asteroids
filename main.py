import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()

    # Music
    pygame.mixer.init()
    pygame.mixer.music.load("OST.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    # Menu
    score = 0
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"

    game_state = MENU

    # Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    def reset_game():
        nonlocal score, player, asteroid_field
        score = 0

        # reset groups
        for group in (updatable, drawable, asteroids, shots):
            group.empty()

        # re-reg
        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable,)
        Shot.containers = (shots, updatable, drawable)

        # re-create objects
        player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_state in (MENU, GAME_OVER):
                        reset_game()
                        game_state = PLAYING

        # Update game state
        dt = clock.tick(60) / 1000
        # player.update(dt)
        if game_state == PLAYING:
            updatable.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                game_state = GAME_OVER
                # sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    score += 10
                    asteroid.split()
                    # asteroid.kill()

        # Start rendering
        screen.fill("black")

        if game_state == MENU:
            title = font.render("ASTEROIDS BY RONSTER", True, (255, 255, 255))
            prompt = small_font.render("Press SPACE to play", True, (255, 255, 255))

            screen.blit(
                title, title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
            )
            screen.blit(
                prompt,
                prompt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20)),
            )

        elif game_state == PLAYING:
            for sprite in drawable:
                sprite.draw(screen)

            score_surf = small_font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_surf, (10, 10))

        elif game_state == GAME_OVER:
            game_over = font.render("GAME OVER", True, (255, 0, 0))
            score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
            prompt = small_font.render(
                "Press SPACE to play again", True, (255, 255, 255)
            )

            screen.blit(
                game_over,
                game_over.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60)),
            )
            screen.blit(
                score_text,
                score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)),
            )
            screen.blit(
                prompt,
                prompt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40)),
            )

        pygame.display.flip()

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
