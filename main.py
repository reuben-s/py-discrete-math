from Engine import Engine
from Node import Node
from Edge import Edge
from Text import Text
from settings import ( Button ) 

engine = Engine()
engine.set_window_title("Python Discrete Math")
engine.cache["pending_node"] = None

def calculate_nodes(text):
    text.text = f"Nodes - {sum(1 for entity in text.engine._entities if isinstance(entity, Node))}"

def calculate_edges(text):
    text.text = f"Edges - {sum(1 for entity in text.engine._entities if isinstance(entity, Edge))}"


def edge_update(edge):
    if not edge.mouse.clicked:
        return 

    # Delete edge if it was right clicked
    match edge.mouse.button:
        case Button.LEFT_CLICK:
            pass
        case Button.RIGHT_CLICK:
            edge.delete()

def node_update(node):
    if node.mouse.holding:
        node.pos = engine.get_mouse_pos()

    if not node.mouse.clicked:
        return

    # If it is a double click then generate new edge
    if node.mouse.double_click and node.engine.cache["pending_node"] is None:
        node.engine.cache["pending_node"] = node
        return

    # Otherwise connect edge or delete node if it is not a double click
    match node.mouse.button:
        case Button.LEFT_CLICK:
            if node.engine.cache["pending_node"] is not None:
                if node.engine.cache["pending_node"] == node:
                    return
                engine.new(Edge(node.engine.cache["pending_node"], node, update=edge_update))
                node.engine.cache["pending_node"] = None
        case Button.RIGHT_CLICK:
            node.delete()

def program(window):
    if window.clicked:
        engine.new(Node(window.mouse_pos, update=node_update)) # Create new node when window is clicked

engine.new(Text("Nodes - ", pos=(5, 5), font_size=25, update=calculate_nodes))
engine.new(Text("Edges - ", pos=(5, 30), font_size=25, update=calculate_edges))

engine.start(program)