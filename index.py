import pygame
import random
import sys
import os

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Set window icon before setting display mode
current_dir = os.path.dirname(__file__)
icon_path = os.path.join(current_dir, 'images', 'icon.png')
try:
    icon_img = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_img)
except pygame.error as e:
    print(f"Failed to load icon image: {e}")

# Screen dimensions
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Eagle's Path")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Game variables
bird_width = 60 # bird width
bird_height = 60 # bird height 
gravity = 0.5  # gravity of bird 
jump_strength = -10
pipe_width = 100 # pipe width
pipe_gap = 200 # gap for every pipe 
pipe_velocity = 3 # speed for pipe incomming 
score = 0  # variable for score 
highest_score = 0  # Variable to keep track of the highest score
frame_index = 0  # To track the current animation frame
animation_speed = 5  # Increased speed of the animation (frames per second)
rotation_angle = 0  # Rotation angle of the bird
rotation_speed = 5  # Speed of rotation
background_frame_index = 100  # Initialize background frame index

font = pygame.font.SysFont('timesnewroman', 30) # for font 

# Load background images
background_frames = []
for i in range(0, 450):  # Assuming you have 450 background images
    bg_image_path = os.path.join(current_dir, 'images', 'background', f'bg{i}.png') # for background image 
    try:
        bg_img = pygame.image.load(bg_image_path)
        bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
        background_frames.append(bg_img)
    except pygame.error as e:
        print(f"Failed to load background image {bg_image_path}: {e}")

# Load bird images
bird_frames = []
for i in range(1, 6):
    image_path = os.path.join(current_dir, 'images', f'bird{i}.png') # for bird image naka gif 
    try:
        bird_img = pygame.image.load(image_path)
        bird_img = pygame.transform.scale(bird_img, (bird_width, bird_height))
        bird_frames.append(bird_img)
    except pygame.error as e:
        print(f"Failed to load bird image {image_path}: {e}")

# Load oak wood image for pipes
oak_wood_path = os.path.join(current_dir, 'images', 'oak2.png') # for pipe image which is yung oak 
try:
    oak_wood_img = pygame.image.load(oak_wood_path)
except pygame.error as e:
    print(f"Failed to load oak wood image: {e}")
    oak_wood_img = None  # Handle missing image if necessary

# Pipe list
pipes = []
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

def load_gif_frames(gif_path):
    """Load all frames from PNG files in the specified directory."""
    frames = []
    for filename in sorted(os.listdir(gif_path)):
        if filename.endswith('.png'):
            try:
                frames.append(pygame.image.load(os.path.join(gif_path, filename)))
            except pygame.error as e:
                print(f"Failed to load GIF frame {filename}: {e}")
    return frames
# Draw the pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if oak_wood_img:
            # Scale the oak wood image based on the pipe height
            scaled_oak_img_top = pygame.transform.scale(oak_wood_img, (pipe_width, pipe[1]))
            # Clip the top part of the pipe image to fit within the screen's top area
            screen.blit(scaled_oak_img_top, (pipe[0], -scaled_oak_img_top.get_height() + pipe[1]))

            # Draw the bottom part of the pipe with a scaled image
            bottom_pipe_height = screen_height - pipe[1] - pipe_gap
            scaled_oak_img_bottom = pygame.transform.scale(oak_wood_img, (pipe_width, bottom_pipe_height))
            # Clip the bottom part of the pipe image to fit within the screen's bottom area
            screen.blit(scaled_oak_img_bottom, (pipe[0], pipe[1] + pipe_gap))
        else:
            # Fallback: Draw simple rectangles if the image isn't loaded
            pygame.draw.rect(screen, green, (pipe[0], 0, pipe_width, pipe[1]))
            pygame.draw.rect(screen, green, (pipe[0], pipe[1] + pipe_gap, pipe_width, screen_height - pipe[1] - pipe_gap))

# the collision of bird in the pipe 
def check_collision(bird_rect, pipes):
    for pipe in pipes:
        pipe_rect_top = pygame.Rect(pipe[0], 0, pipe_width, pipe[1])
        pipe_rect_bottom = pygame.Rect(pipe[0], pipe[1] + pipe_gap, pipe_width, screen_height - pipe[1] - pipe_gap)
        if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= screen_height:
        return True
    return False

# for the background
def draw_background():
    global background_frame_index
    background_frame_index = (background_frame_index + 1) % (len(background_frames) * animation_speed)
    current_background_frame = background_frames[background_frame_index // animation_speed]
    screen.blit(current_background_frame, (0, 0))


# to show the start screen
def show_start_screen():
    # Load the image (if it's a static asset, you might want to load it outside the function to avoid reloading every time)
    image_path = os.path.join(current_dir, 'images', 'getready.png')  # Replace with the path to your image
    try:
        original_image = pygame.image.load(image_path)
    except pygame.error as e:
        print(f"Failed to load start screen image: {e}")
        original_image = None

    if original_image:
        # Resize the image (e.g., 200x200 pixels)
        new_width = 400
        new_height = 250
        resized_image = pygame.transform.scale(original_image, (new_width, new_height))
    else:
        resized_image = None

    # Center the bird on the screen
    bird_x = screen_width // 2
    bird_y = screen_height // 2
    frame_index = 0
    animation_speed_local = 2  # Controls the speed of the animation

    while True:
        draw_background()  # Draw the background with animation

        # Draw the image
        if resized_image:
            image_rect = resized_image.get_rect(center=(screen_width // 2, screen_height // 3))  # Adjust position as needed
            screen.blit(resized_image, image_rect)
        
        # Animate the bird's flight
        if frame_index >= len(bird_frames):
            frame_index = 0

        current_frame = bird_frames[frame_index]
        bird_rect = current_frame.get_rect(center=(bird_x, bird_y))
        screen.blit(current_frame, bird_rect.topleft)

        # Update animation frame
        if pygame.time.get_ticks() % animation_speed_local == 0:
            frame_index += 1

        # Render and draw the "Press SPACE to start" text
        prompt_text = font.render("Press SPACE to start", True, black)
        screen.blit(prompt_text, (screen_width // 2 - prompt_text.get_width() // 2, screen_height // 2 + 50))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        pygame.display.update()
        pygame.time.Clock().tick(30)  # Adjust the frame rate if needed


#show the game over 
def show_game_over_screen(score):
    global highest_score

    # Update the highest score
    if score > highest_score:
        highest_score = score

    while True:
        draw_background()  # Draw the background with animation

        # Game Over text remains red
        game_over_text = font.render("Game Over", True, red, None)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))

        # Score and highest score are black
        score_text = font.render(f"Score: {score}", True, black, None)
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 50))

        highest_score_text = font.render(f"Highest Score: {highest_score}", True, black, None)
        screen.blit(highest_score_text, (screen_width // 2 - highest_score_text.get_width() // 2, screen_height // 2))

        # Restart button is white
        restart_text = font.render("Restart", True, black, None)
        restart_button = pygame.Rect(0, 0, restart_text.get_width() + 20, restart_text.get_height() + 10)
        restart_button.center = (screen_width // 2, screen_height // 2 + 100)
        screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 5))

        # Quit button is white
        quit_text = font.render("Quit", True, black, None)
        quit_button = pygame.Rect(0, 0, quit_text.get_width() + 20, quit_text.get_height() + 10)
        quit_button.center = (screen_width // 2, screen_height // 2 + 175)
        screen.blit(quit_text, (quit_button.x + 10, quit_button.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

#dito lalabas yung main game
def main_game():
    global score, pipes, last_pipe, frame_index, rotation_angle, background_frame_index

    bird_x = 50
    bird_y = 300
    bird_velocity = 0
    score = 0
    pipes = []
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    bird_flapping = True  # Flag to control bird's wing animation
    rotation_angle = 0  # Reset rotation angle

    running = True
    collision_occurred = False  # Track if a collision has occurred
    last_score_update_time = pygame.time.get_ticks()  # To track when the last pipe was passed

    pygame.mixer.music.set_volume(0.3)  # Reduce the volume when the game starts

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not collision_occurred:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
                    if flap_sound:
                        flap_sound.play()

        if not collision_occurred:
            # Update bird
            bird_velocity += gravity
            bird_y += bird_velocity
        else:
            # Let the bird fall to the ground after collision
            bird_velocity += gravity
            bird_y += bird_velocity
            rotation_angle += rotation_speed  # Rotate the bird

            # Check if the bird hits the ground
            if bird_y + bird_height >= screen_height:
                bird_y = screen_height - bird_height
                running = False  # Stop the loop to move to the game over screen
                if die_sound:
                    die_sound.play()  # Play the die sound effect

        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

        if not collision_occurred:
            # Update pipes only if no collision has occurred
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe > pipe_frequency:
                pipe_height = random.randint(100, 400)
                pipes.append([screen_width, pipe_height])
                last_pipe = current_time

            pipes = [[pipe[0] - pipe_velocity, pipe[1]] for pipe in pipes if pipe[0] > -pipe_width]

            # Check for collisions
            if check_collision(bird_rect, pipes):
                collision_occurred = True  # Trigger the falling sequence
                bird_flapping = False  # Stop the animation on collision
                rotation_angle = 0  # Reset rotation angle to prevent continuous rotation
                if collision_sound:
                    collision_sound.play()
                if die_sound:
                    die_sound.play()  # Play the die sound effect

            # Check for scoring
            for pipe in pipes:
                if pipe[0] + pipe_width < bird_x and not pipe[0] + pipe_width < bird_x - pipe_velocity:
                    score += 1
                    if pass_pipe_sound:
                        pass_pipe_sound.play()  # Play sound effect when passing a pipe

        # Update background animation
        draw_background()

        # Draw bird with animation
        if bird_flapping:
            frame_index = (frame_index + 1) % (len(bird_frames) * animation_speed)
            current_frame = bird_frames[frame_index // animation_speed]
        else:
            current_frame = bird_frames[0]  # Show the first frame when not flapping

        # Rotate the bird if a collision has occurred
        rotated_bird = pygame.transform.rotate(current_frame, rotation_angle)
        bird_rect = rotated_bird.get_rect(center=(bird_x + bird_width // 2, bird_y + bird_height // 2))
        screen.blit(rotated_bird, bird_rect.topleft)

        draw_pipes(pipes)

        # Display the score in black
        score_text = font.render(f"Score: {score}", True, black, None)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        pygame.time.Clock().tick(60)

    # After the loop ends (bird hits the ground), show the game over screen
    show_game_over_screen(score)

# Load sound effects after defining functions to ensure paths are correctly set
# Load sound effects
flap_sound_path = os.path.join(current_dir, 'sound', 'flap.wav')
collision_sound_path = os.path.join(current_dir, 'sound', 'collision.wav')
pass_pipe_sound_path = os.path.join(current_dir, 'sound', 'pass.wav')  # New sound effect path
die_sound_path = os.path.join(current_dir, 'sound', 'die.wav')  # Add this line for the die sound

pygame.mixer.music.load(os.path.join(current_dir, 'sound', 'background.mp3'))
pygame.mixer.music.set_volume(0.7) 
pygame.mixer.music.play(-1)  # Loop background music

# Attempt to load the flap sound effect
try:
    flap_sound = pygame.mixer.Sound(flap_sound_path)  # Load sound for bird's flap action
except pygame.error as e:
    print(f"Failed to load flap sound: {e}")  # Print error if sound fails to load
    flap_sound = None  # Assign None to handle missing sound gracefully

# Attempt to load the collision sound effect
try:
    collision_sound = pygame.mixer.Sound(collision_sound_path)  # Load sound for collision events
except pygame.error as e:
    print(f"Failed to load collision sound: {e}")  # Print error if sound fails to load
    collision_sound = None  # Assign None to handle missing sound gracefully

# Attempt to load the pass-pipe sound effect
try:
    pass_pipe_sound = pygame.mixer.Sound(pass_pipe_sound_path)  # Load sound for passing a pipe
except pygame.error as e:
    print(f"Failed to load pass pipe sound: {e}")  # Print error if sound fails to load
    pass_pipe_sound = None  # Assign None to handle missing sound gracefully

# Attempt to load the die sound effect
try:
    die_sound = pygame.mixer.Sound(die_sound_path)  # Load sound for game-over event
except pygame.error as e:
    print(f"Failed to load die sound: {e}")  # Print error if sound fails to load
    die_sound = None  # Assign None to handle missing sound gracefully

# Start the game
show_start_screen()
while True:
    main_game()
