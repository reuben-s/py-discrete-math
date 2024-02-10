from Engine import Engine
from Node import Node

from settings import (WHITE, RED)

engine = Engine()
engine.set_window_title("Python Discrete Math")

def node_update(node):
    if (node.clicked):
        node.colour = WHITE if node.colour == RED else RED

def program(window):
    if window.clicked:
        window.new(Node(window, window.mouse_pos, update=node_update)) # Create new node when window is clicked

engine.start(program)