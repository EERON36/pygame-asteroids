import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        # must override
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        # must override
        self.position = self.position + (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        # angle for new spawns
        ran_angle = random.uniform(20, 50)
        first_velocity = self.velocity.rotate(ran_angle)
        second_velocity = self.velocity.rotate(-ran_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # create new asteroids
        asteroid_one = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_two = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid_one.velocity = first_velocity * 1.2
        asteroid_two.velocity = second_velocity * 1.2
