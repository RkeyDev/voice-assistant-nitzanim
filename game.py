def start_game() -> None:
    import pygame
    import random
    import json
    from typing import Tuple, List

    # Constants
    SCREEN_WIDTH: int = 400
    SCREEN_HEIGHT: int = 600
    GRAVITY: float = 0.5
    JUMP_STRENGTH: int = -10
    PIPE_GAP: int = 250
    BASE_SPEED: int = 5
    SPEED_UP: float = 0.002
    SCORE_FILE: str = "game_top_scores.json"

    # Load images
    IMAGE_FOLDER: str = "assets/"
    BIRD_IMAGE: str = "bird.png"
    BACKGROUND_IMAGE: str = "background.png"
    PIPE_IMAGE: str = "pipe.png"

    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()
    font: pygame.font.Font = pygame.font.SysFont("Comic Sans MS", 22)

    def load_and_scale_image(filename: str, size: Tuple[int, int]) -> pygame.Surface:
        """Load an image from file and scale it to the given size."""
        image: pygame.Surface = pygame.image.load(IMAGE_FOLDER + filename)
        return pygame.transform.scale(image, size)

    def load_scores() -> List[int]:
        try:
            with open(SCORE_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_score(score: int) -> None:
        scores = load_scores()
        scores.append(score)
        scores = sorted(scores, reverse=True)[:5]  # keep top 5
        with open(SCORE_FILE, "w") as f:
            json.dump(scores, f)

    def show_game_over(score: int) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        scores = load_scores()
        game_over_text = font.render("Game Over!", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 60, 100))

        score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 80, 150))

        for place, score in enumerate(scores):
            entry = font.render(f"{place + 1} place: {score}", True, (255, 255, 255))
            screen.blit(entry, (SCREEN_WIDTH // 2 - 40, 200 + place * 30))

        pygame.display.update()

        # Timer start
        start_ticks = pygame.time.get_ticks()

        # Event loop with a 5-second timeout or until pygame.QUIT is triggered
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Check if 5 seconds have passed
            if pygame.time.get_ticks() - start_ticks >= 10000:
                running = False

            pygame.display.update()

        # Optionally, you can clean up here, such as quitting pygame
        pygame.quit()

    class Bird:
        def __init__(self) -> None:
            """Initialize the bird."""
            self.image: pygame.Surface = load_and_scale_image(BIRD_IMAGE, (50, 35))
            self.rect: pygame.Rect = pygame.Rect(50, SCREEN_HEIGHT // 2, self.image.get_width(),
                                                 self.image.get_height())
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
            # pygame.draw.rect(screen, (0, 0, 255), self.rect, 2) - debug
            screen.blit(self.image, self.rect.topleft)

        def get_rect(self) -> pygame.Rect:
            """Get the bird's rectangle for collision detection."""
            return self.rect

    class Pipe:
        speed: float = BASE_SPEED

        def __init__(self, x: int, top_bottom: bool = True) -> None:
            """Initialize a pipe pair.

            top_bottom - true is up false down
            y_center - Optional vertical center position for gap control
            """
            height = SCREEN_HEIGHT  # ensure pipes are always long enough
            self.image: pygame.Surface = load_and_scale_image(PIPE_IMAGE, (60, height))
            self.top_bottom: bool = top_bottom
            self.scored = False

            rand_height = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP)
            if top_bottom:
                self.rect: pygame.Rect = pygame.Rect(x, rand_height - height, self.image.get_width(), height)
            else:
                self.rect: pygame.Rect = pygame.Rect(x, rand_height + PIPE_GAP, self.image.get_width(), height)

        def update(self) -> None:
            """Move the pipe left."""
            self.rect.left -= Pipe.speed

        def draw(self, screen: pygame.Surface) -> None:
            """Draw the pipes on the screen."""
            # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) - debug
            if self.top_bottom:
                screen.blit(self.image, self.rect.topleft)
            else:
                screen.blit(pygame.transform.flip(self.image, False, True), self.rect.topleft)

        def make_opposite(self):
            # Create a new pipe at the same left position but opposite top/bottom
            pipe = Pipe(self.rect.left, not self.top_bottom)

            if self.top_bottom:
                # Calculate the desired position for the top of the new pipe (bottom of the current pipe + gap)
                desired_top = self.rect.bottom + PIPE_GAP
                if pipe.rect.top < desired_top:
                    pipe.rect.top = desired_top  # Enforce minimum gap if needed

            else:
                # Calculate the desired position for the bottom of the new pipe (top of the current pipe - gap)
                desired_bottom = self.rect.top - PIPE_GAP
                if pipe.rect.bottom > desired_bottom:
                    pipe.rect.bottom = desired_bottom  # Enforce minimum gap if needed

            return pipe

    def main() -> None:
        """Main game loop."""
        running: bool = True
        bird: Bird = Bird()
        background: pygame.Surface = load_and_scale_image(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
        pipes: List[Tuple[Pipe, Pipe]] = [(new_pipe := Pipe(int(SCREEN_WIDTH * i * 0.6)), new_pipe.make_opposite()) for
                                          i in
                                          range(1, 3)]
        fps: int = 30
        score: int = 0

        while running:

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    bird.jump()

            # Background
            screen.blit(background, (0, 0))

            # Bird update
            bird.update()
            bird.draw(screen)

            # Pipes update and Bird collision
            for pipe1, pipe2 in pipes:
                pipe1.update()
                pipe2.update()
                pipe1.draw(screen)
                pipe2.draw(screen)

                # Check bird pipes collisions
                if bird.rect.colliderect(pipe1.rect) or bird.rect.colliderect(pipe2.rect):
                    running = False

            # Score check
            for pipe1, pipe2 in pipes:
                if not pipe1.scored and pipe1.rect.right < bird.rect.left:
                    score += 1
                    pipe1.scored = True
                    pipe2.scored = True

            # Score display
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Check if bird in bounds
            if bird.rect.bottom >= SCREEN_HEIGHT or bird.rect.top <= 0:
                running = False

            # Update pipes
            for index, pipe_pair in enumerate(pipes):
                if pipe_pair[0].rect.right <= 0:
                    pipes.pop(index)
                    pipes.append((new_pipe := Pipe(SCREEN_WIDTH), new_pipe.make_opposite()))

            # increase pipes speed
            Pipe.speed += SPEED_UP

            # Update screen
            pygame.display.update()
            clock.tick(fps)

        save_score(score)
        show_game_over(score)
        pygame.quit()

    main()


if __name__ == '__main__':
    raise RuntimeError("This script is not meant to be run directly.")
