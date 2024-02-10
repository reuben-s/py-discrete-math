from enum import Enum

class Button(Enum):
    LEFT_CLICK  = 1
    RIGHT_CLICK = 3

# Mouse holding time
# This is the number of milliseconds the mouse has to be held down for the program to detect that an entity has the mouse held over it
HOLDING_TIME = 100 # Default : 50ms

# Default screen dimensions
WIDTH, HEIGHT = 800, 600

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# FPS Cap
FPS = 60

# Node default radius
RADIUS = 10