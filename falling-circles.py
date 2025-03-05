import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Falling Circles Game")

# Define colors
background_color = (0, 0, 0)  # Black
circle_color = (255, 0, 0)  # Red for falling circles

# Frame rate control
clock = pygame.time.Clock()

# List to store circle positions
circles = []

# Add some initial falling circles
circles.append([100, 50])
circles.append([300, 150])
circles.append([500, 100])

# Player setup
player_width, player_height = 100, 20  # Rectangle dimensions
player_x = (screen_width - player_width) // 2  # Center horizontally
player_y = screen_height - 50  # Near the bottom of the screen
player_speed = 10  # Speed of movement
player_color = (0, 255, 0)  # Green
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)  # Create the rectangle

# Scoring and difficulty variables
player_score = 0
winning_score = 10
fall_speed = 5
spawn_timer = 0
max_circles = 20

# Font for displaying text
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Add a new circle when the spacebar is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_x = random.randint(0, screen_width)  # Random x-position
                new_y = 0  # Start at the top of the screen
                circles.append([new_x, new_y])  # Add the new circle to the list

    # Handle player movement
    keys = pygame.key.get_pressed()  # Check for key presses
    if keys[pygame.K_LEFT] and player_rect.x > 0:  # Move left
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.x < screen_width - player_width:  # Move right
        player_rect.x += player_speed

    # Increment the spawn timer
    spawn_timer += 1

    # Spawn new circles more frequently as the score increases
    spawn_delay = max(30, 120 - player_score * 5)  # Minimum delay of 30 frames
    if spawn_timer >= spawn_delay:
        new_x = random.randint(0, screen_width)
        new_y = 0
        circles.append([new_x, new_y])
        spawn_timer = 0  # Reset the timer

    # Limit the number of circles on the screen
    if len(circles) > max_circles:
        circles.pop(0)  # Remove the oldest circle

    # Gradually increase the falling speed based on score
    fall_speed = 5 + player_score // 2

    # Update the position of each circle to make them fall
    for circle in circles:
        circle[1] += fall_speed

    # Check for collisions between the player and circles
    for circle in circles[:]:  # Iterate over a copy of the list
        circle_rect = pygame.Rect(circle[0] - 15, circle[1] - 15, 30, 30)  # Create a rectangle around the circle
        if player_rect.colliderect(circle_rect):  # Check for collision
            circles.remove(circle)  # Remove the circle
            player_color = (255, 0, 0)  # Change the player color to red
            player_score += 1  # Increase the score by 1

            # Check if the player has won
            if player_score >= winning_score:
                # Display a winning message
                win_text = font.render("You Win!", True, (0, 255, 0))  # Green winning text
                screen.fill(background_color)  # Clear the screen
                screen.blit(win_text, (screen_width // 2 - 100, screen_height // 2 - 20))  # Center the text
                pygame.display.flip()  # Update the screen
                pygame.time.wait(3000)  # Wait 3 seconds
                running = False  # End the game loop

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw each circle
    for circle in circles:
        x, y = circle  # Get the x and y positions
        pygame.draw.circle(screen, circle_color, (x, y), 30)  # Draw the circle

    # Draw the player rectangle
    pygame.draw.rect(screen, player_color, player_rect)

    # Display the player's score
    score_text = font.render(f"Score: {player_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Reset player color to green after each frame
    if player_color == (255, 0, 0):
        player_color = (0, 255, 0)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()