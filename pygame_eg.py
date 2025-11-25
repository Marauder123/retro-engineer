import serial
import pygame
import space_api
import time

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
pygame.init()

ip = "10.184.1.111"
port = 9876
role = "engineer"
team = "retro"
space_api.connect(role, team, ip, port)

port = "/dev/tty.usbmodem1101"
baud = 115200
ser = serial.Serial(port)
ser.baudrate = baud

connected = True

font = pygame.font.Font(None, 30)

def button(msg, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    text_surf = font.render(msg, True, BLACK)
    text_rect = text_surf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    screen.blit(text_surf, text_rect)

def quit_game():
    pygame.quit()
    exit()

def connect():
    print("This button does nothing.")

def draw_progress_bar(surface, position, size, border_color, fill_color, progress):
    """
    Draws a progress bar on the given surface.

    Args:
        surface (pygame.Surface): The surface to draw on.
        position (tuple): (x, y) coordinates of the top-left corner of the bar.
        size (tuple): (width, height) of the overall bar.
        border_color (tuple): RGB color for the outer rectangle border.
        fill_color (tuple): RGB color for the inner, filled rectangle.
        progress (float): Current progress as a value between 0.0 and 1.0.
    """
    # Draw the outer rectangle (border)
    pygame.draw.rect(surface, border_color, (*position, *size), 1)

    # Calculate inner rectangle dimensions
    inner_padding = 3  # Padding from the border
    inner_x = position[0] + inner_padding
    inner_y = position[1] + inner_padding
    inner_width = (size[0] - (2 * inner_padding)) * progress
    inner_height = size[1] - (2 * inner_padding)

    # Ensure inner_width is an integer to avoid DeprecationWarning in newer Pygame versions
    inner_width = int(inner_width)

    # Draw the inner, filled rectangle
    pygame.draw.rect(surface, fill_color, (inner_x, inner_y, inner_width, inner_height))

if __name__ == '__main__':
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Engineering")

    clock = pygame.time.Clock()
    running = True
    current_progress = 0.0
    max_progress = 1.0
    progress_speed = 0.005

    # Bar parameters
    pilot_pos = (200, 50)
    science_pos = (200, 150)
    weapons_pos = (200, 250)
    available_pos = (200, 350)
    bar_size = (400, 30)
    border_color = (0, 0, 0)  # Black
    fill_color = (0, 128, 0)  # Green

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # White background
        
        button("Connect", 0, 550, 100, 50, RED, GREEN, connect)
        if connected:
            #Pilot
            draw_progress_bar(screen, pilot_pos, bar_size, border_color, fill_color, space_api.ship["pilot_power"]/6)
            text_surf = font.render("PILOT", True, BLACK)
            text_rect = text_surf.get_rect(topleft=(200,30))
            screen.blit(text_surf, text_rect)
            #Science
            draw_progress_bar(screen, science_pos, bar_size, border_color, fill_color, space_api.ship["science_power"]/6)
            text_surf = font.render("SCIENCE", True, BLACK)
            text_rect = text_surf.get_rect(topleft=(200,130))
            screen.blit(text_surf, text_rect)            
            #Weapons
            draw_progress_bar(screen, weapons_pos, bar_size, border_color, fill_color, space_api.ship["weapon_power"]/6)
            text_surf = font.render("WEAPONS", True, BLACK)
            text_rect = text_surf.get_rect(topleft=(200,230))
            screen.blit(text_surf, text_rect)       
            #Available
            draw_progress_bar(screen, available_pos, bar_size, border_color, fill_color, space_api.ship["available_power"]/6)
            text_surf = font.render("AVAILABLE PWR", True, BLACK)
            text_rect = text_surf.get_rect(topleft=(200,330))
            screen.blit(text_surf, text_rect)  
            
        pygame.display.flip()
        clock.tick(60)
        if (ser.inWaiting()>0):
            data = ser.read().decode()
            if "Q" in data:
                space_api.power("up","pilot")
                print("Power up pilot")
            elif "W" in data:
                space_api.power("up","weapons")
                print("Power up weapons")
            elif "E" in data:
                space_api.power("up", "science")
                print("Power up science")
            elif "R" in data:
                space_api.power("down", "pilot")
                print("Power down pilot")
            elif "T" in data:
                space_api.power("down", "weapons")
                print("Power down weapons")
            elif "Y" in data:
                space_api.power("down", "science")
                print("Power down science")

        

    pygame.quit()