from enum import Enum

class Button(Enum):
    LEFT_CLICK  = 1
    RIGHT_CLICK = 3

# Mouse timings
HOLDING_TIME = 100 # This is the number of milliseconds the mouse has to be held down for the program to detect that an entity has the mouse held over it
DOUBLE_CLICK_TIME = 250 # The interval between two clicks for the click to be counted as a double click

# Default screen dimensions
WIDTH, HEIGHT = 1200, 800

# Textbox dimensions
TEXTBOX_WIDTH  = 250
TEXTBOX_HEIGHT = 50
TEXTBOX_MARGIN = 10

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# FPS Cap
FPS = 60

# Node default radius
RADIUS = 10

# Edge settings
EDGE_WIDTH = 2
EDGE_WEIGHT_OFFSET = 35 # Space between edge and text displaying edge weight
EDGE_CLICK_ZONE = 10 # Space either side of edge will be detected as clicking the edge