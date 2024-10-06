import pygame
import random
import os
import sys
import time

class FlappyFaceGame:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.WHITE = (255, 255, 255)
        self.GREEN = (52, 231, 119)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Face')
        self.clock = pygame.time.Clock()

        self.player_size = 50
        self.player_x = 50
        self.player_y = self.SCREEN_HEIGHT // 2

        self.obstacle_width = 50
        self.obstacle_gap = 200
        self.initial_obstacle_speed = 5
        self.obstacle_speed = self.initial_obstacle_speed
        self.obstacles = []

        self.score = 0
        self.high_score = self.load_high_score()

        # Load images
        self.intro_background_img = pygame.image.load('background.png').convert()
        self.intro_background_img = pygame.transform.scale(self.intro_background_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.end_screen_background_img = pygame.image.load('background.png').convert()
        self.end_screen_background_img = pygame.transform.scale(self.end_screen_background_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.game_background_img = pygame.image.load('background.png').convert()
        self.game_background_img = pygame.transform.scale(self.game_background_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.player_img = pygame.image.load('player.png').convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (self.player_size, self.player_size))

        self.last_y = self.player_y

        # Timing and rotation state variables
        self.rotation_angle = 1  # Default rotation angle to 1 degree
        self.rotation_target_angle = 1  # Target rotation angle
        self.rotation_direction = None
        self.rotation_pause_start = None
        self.rotation_duration = 0.2  # Duration to smoothly rotate to target angle

    def draw_player(self):
        rotated_player_img = pygame.transform.rotate(self.player_img, self.rotation_angle)
        player_rect = rotated_player_img.get_rect(center=(self.player_x + self.player_size // 2, self.player_y + self.player_size // 2))
        self.screen.blit(rotated_player_img, player_rect.topleft)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            top_rect = pygame.Rect(obstacle['x'], 0, self.obstacle_width, obstacle['top_height'])
            bottom_rect = pygame.Rect(obstacle['x'], self.SCREEN_HEIGHT - obstacle['bottom_height'], self.obstacle_width, obstacle['bottom_height'])
            pygame.draw.rect(self.screen, self.GREEN, top_rect)
            pygame.draw.rect(self.screen, self.GREEN, bottom_rect)

    def update_obstacles(self):
        for obstacle in self.obstacles:
            obstacle['x'] -= self.obstacle_speed

        if len(self.obstacles) == 0 or self.obstacles[-1]['x'] < self.SCREEN_WIDTH - 300:
            self.add_new_obstacle()

        for obstacle in self.obstacles:
            if obstacle['x'] + self.obstacle_width < self.player_x and not obstacle['passed']:
                obstacle['passed'] = True
                self.score += 1
                self.adjust_obstacle_speed()

        self.obstacles = [obs for obs in self.obstacles if obs['x'] + self.obstacle_width > 0]

    def add_new_obstacle(self):
        top_height = random.randint(50, self.SCREEN_HEIGHT - self.obstacle_gap - 50)
        bottom_height = self.SCREEN_HEIGHT - self.obstacle_gap - top_height
        new_obstacle = {
            'x': self.SCREEN_WIDTH,
            'top_height': top_height,
            'bottom_height': bottom_height,
            'passed': False  # To track if the obstacle is passed by the player
        }
        self.obstacles.append(new_obstacle)

    def adjust_obstacle_speed(self):
        if self.score % 5 == 0:
            self.obstacle_speed += 1

    def check_collision(self):
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size)
        for obstacle in self.obstacles:
            top_rect = pygame.Rect(obstacle['x'], 0, self.obstacle_width, obstacle['top_height'])
            bottom_rect = pygame.Rect(obstacle['x'], self.SCREEN_HEIGHT - obstacle['bottom_height'], self.obstacle_width, obstacle['bottom_height'])
            if player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect):
                return True
        return False

    def display_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, self.WHITE)
        self.screen.blit(text, (10, 10))

        high_score_text = font.render(f'High Score: {self.high_score}', True, self.WHITE)
        self.screen.blit(high_score_text, (10, 40))

    def display_message(self, message, sub_message=None):
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, self.WHITE)
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 50))
        self.screen.blit(text, text_rect)

        if sub_message:
            sub_font = pygame.font.Font(None, 36)
            sub_text = sub_font.render(sub_message, True, self.WHITE)
            sub_text_rect = sub_text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + 20))
            self.screen.blit(sub_text, sub_text_rect)

        pygame.display.flip()

    def intro_screen(self):
        self.screen.blit(self.intro_background_img, (0, 0))
        self.display_message("Flappy Face", "Press Any Key to Play")
        self.wait_for_keypress()

    def game_over_screen(self):
        self.screen.blit(self.end_screen_background_img, (0, 0))
        self.display_message("Game Over", f"Score: {self.score} - Press Any Key to Play Again")
        self.save_high_score()
        self.wait_for_keypress()

    def wait_for_keypress(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def run(self, face_tracker):
        self.intro_screen()
        self.reset_game()

        running = True
        while running:
            center_y, _ = face_tracker.get_face_position_and_frame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if center_y is not None:
                self.last_y = self.player_y
                self.player_y = int(center_y * self.SCREEN_HEIGHT // 480)  # Assuming the camera frame height is 480

                # Calculate the angle for rotation based on significant vertical movement
                delta_y = self.player_y - self.last_y
                if delta_y < -5:  # Moving up significantly
                    if self.rotation_direction != 'up':
                        self.rotation_target_angle = 30
                        self.rotation_direction = 'up'
                        self.rotation_pause_start = time.time()
                elif delta_y > 5:  # Moving down significantly
                    if self.rotation_direction != 'down':
                        self.rotation_target_angle = -30
                        self.rotation_direction = 'down'
                        self.rotation_pause_start = time.time()
                else:
                    # Reset rotation after the pause
                    if self.rotation_pause_start and time.time() - self.rotation_pause_start >= 1:
                        self.rotation_target_angle = 1  # Default to 1 degree instead of 0
                        self.rotation_direction = None
                        self.rotation_pause_start = None

            # Smooth rotation
            self.rotation_angle += (self.rotation_target_angle - self.rotation_angle) * 0.1

            self.update_obstacles()

            if self.check_collision():
                self.game_over_screen()
                self.reset_game()
                self.intro_screen()

            self.screen.blit(self.game_background_img, (0, 0))
            self.draw_player()
            self.draw_obstacles()
            self.display_score()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

    def reset_game(self):
        self.player_y = self.SCREEN_HEIGHT // 2
        self.last_y = self.player_y
        self.obstacles = []
        self.add_new_obstacle()
        self.score = 0
        self.obstacle_speed = self.initial_obstacle_speed
        self.rotation_angle = 1  # Default to 1 degree instead of 0
        self.rotation_target_angle = 1  # Default to 1 degree instead of 0
        self.rotation_pause_start = None
        self.rotation_direction = None

    def load_high_score(self):
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('high_score.txt', 'w') as file:
                file.write(str(self.high_score))

if __name__ == "__main__":
    from face_tracking import FaceTracker

    face_tracker = FaceTracker()
    game = FlappyFaceGame()
    game.run(face_tracker)