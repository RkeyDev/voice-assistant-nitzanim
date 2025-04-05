import pygame
import random
from typing import Tuple, List

# Constants
SCREEN_WIDTH: int = 400
SCREEN_HEIGHT: int = 600
GRAVITY: float = 0.5
JUMP_STRENGTH: int = -10
PIPE_GAP: int = 250
BASE_SPEED: int = 3
SPEED_UP: float = 0.002

# Load images
IMAGE_FOLDER: str = "assets/"
BIRD_IMAGE: str = "bird.png"
BACKGROUND_IMAGE: str = "background.png"
PIPE_IMAGE: str = "pipe.png"

pygame.init()
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock: pygame.time.Clock = pygame.time.Clock()


def load_and_scale_image(filename: str, size: Tuple[int, int]) -> pygame.Surface:
    """Load an image from file and scale it to the given size."""
    image: pygame.Surface = pygame.image.load(IMAGE_FOLDER + filename)
    return pygame.transform.scale(image, size)


class Bird:
    def __init__(self) -> None:
        """Initialize the bird."""
        self.image: pygame.Surface = load_and_scale_image(BIRD_IMAGE, (50, 35))
        self.rect: pygame.Rect = pygame.Rect(50, SCREEN_HEIGHT // 2, self.image.get_width(), self.image.get_height())
        self.velocity: int = 0

    def jump(self) -> None:
        """Make the bird jump."""
        self.velocity = JUMP_STRENGTH

    def update(self) -> None:
        """Update the bird's position."""
        self.velocity += GRAVITY
        self.rect.top += self.velocity

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the bird on the screen."""
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 2)
        screen.blit(self.image, self.rect.topleft)

    def get_rect(self) -> pygame.Rect:
        """Get the bird's rectangle for collision detection."""
        return self.rect


class Pipe:
    speed: int = BASE_SPEED

    def __init__(self, x: int, top_bottom: bool = True) -> None:
        """Initialize a pipe pair.

        top_bottom - true is up false down"""
        self.image: pygame.Surface = load_and_scale_image(PIPE_IMAGE, (60, 400))
        self.top_bottom: bool = top_bottom
        self.scored: bool = False

        if top_bottom:
            self.rect: pygame.Rect = pygame.Rect(x, -random.randint(0, 400), self.image.get_width(),
                                                 self.image.get_height())
        else:
            self.rect: pygame.Rect = pygame.Rect(x, SCREEN_HEIGHT - (random.randint(0, 400)), self.image.get_width(),
                                                 self.image.get_height())

    def update(self) -> None:
        """Move the pipe left."""
        self.rect.left -= Pipe.speed

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the pipes on the screen."""

        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        if self.top_bottom:
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(pygame.transform.flip(self.image, False, True), self.rect.topleft)

    def make_opposite(self):
        if self.top_bottom:
            pipe: Pipe = Pipe(self.rect.left, False)
            if (gap_diff := pipe.rect.top - self.rect.bottom) != PIPE_GAP:
                pipe.rect.top += PIPE_GAP - gap_diff

            return pipe

        pipe = Pipe(self.rect.left)
        if (gap_diff := self.rect.top - pipe.rect.bottom) != PIPE_GAP:
            pipe.rect.top -= PIPE_GAP - gap_diff

        return pipe


def main() -> None:
    """Main game loop."""
    running: bool = True
    bird: Bird = Bird()
    background: pygame.Surface = load_and_scale_image(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pipes: List[Tuple[Pipe, Pipe]] = [(new_pipe := Pipe(int(SCREEN_WIDTH * i * 0.6)), new_pipe.make_opposite()) for i in
                                      range(1, 3)]  # making a list of 2 tuples - every tuple is a pipe pair
    fps: int = 30
    score: int = 0

    while running:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
                bird.jump()

        # Background
        screen.blit(background, (0, 0))

        # Bird update
        bird.update()
        bird.draw(screen)

        # Pipes update
        for pipe1, pipe2 in pipes:
            pipe1.update()
            pipe2.update()
            pipe1.draw(screen)
            pipe2.draw(screen)

            # Collision detection with pipes
            if bird.rect.colliderect(pipes[0][0]) or bird.rect.colliderect(pipes[0][1]):
                running = False

        # Score
        for pipe1, pipe2 in pipes:
            if not pipe1.scored and pipe1.rect.right < bird.rect.left:
                score += 1
                pipe1.scored = True
                pipe2.scored = True  # Mark both pipes as scored since they are a pair
                print("Score:", score)

        # Check if bird in bounds
        if bird.rect.bottom >= SCREEN_HEIGHT or bird.rect.top <= 0:
            running = False

        # pipe bound
        for index, pipe_pair in enumerate(pipes):
            if (pipe_pair[0]).rect.right <= 0:
                pipes.pop(index)
                pipes.append((new_pipe := Pipe(SCREEN_WIDTH), new_pipe.make_opposite()))

        # pipes speed up
        Pipe.speed += SPEED_UP

        # screen update
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
