from Engine import Engine
from Node import Node

from settings import (WHITE, RED, Button)

engine = Engine()
engine.set_window_title("Python Discrete Math")

def node_update(node):
    if node.holding:
        node.pos = engine.get_mouse_pos()

    if not node.clicked:
        return
    
    match node.button:
        case Button.LEFT_CLICK:
            node.colour = WHITE if node.colour == RED else RED
        case Button.RIGHT_CLICK:
            node.delete()
            print(node._delete)

def program(window):
    if window.clicked:
        window.new(Node(window, window.mouse_pos, update=node_update)) # Create new node when window is clicked

engine.start(program)