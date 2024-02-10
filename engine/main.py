from Engine import Engine
from Node import Node
from Edge import Edge
from settings import (
    WHITE, 
    RED, 
    Button
    )

engine = Engine()
engine.set_window_title("Python Discrete Math")
engine.cache["pending_node"] = None

def node_update(node):
    if node.holding:
        node.pos = engine.get_mouse_pos()

    if not node.clicked:
        return

    if node.double_click and node.engine.cache["pending_node"] is None:
        node.engine.cache["pending_node"] = node
        return

    match node.button:
        case Button.LEFT_CLICK:
            if node.engine.cache["pending_node"] is not None:
                engine.new(Edge(node.engine.cache["pending_node"], node))
                node.engine.cache["pending_node"] = None
        case Button.RIGHT_CLICK:
            node.delete()
            print(node._delete)

def program(window):
    if window.clicked:
        engine.new(Node(window.mouse_pos, update=node_update)) # Create new node when window is clicked

engine.start(program)