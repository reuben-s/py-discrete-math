from Engine import Engine
from Node import Node
from Edge import Edge
from Text import Text
from Textbox import Textbox
from settings import ( Button ) 

engine = Engine()
engine.set_window_title("Python Discrete Math")
engine.cache["pending_node"] = None
engine.cache["pending_edge"] = None
engine.cache["textbox"] = None

def calculate_nodes(text):
    num_nodes = sum(1 for entity in text.engine._entities if isinstance(entity, Node))
    text.text = f"Nodes - {num_nodes}"

def calculate_edges(text):
    num_edges = sum(1 for entity in text.engine._entities if isinstance(entity, Edge))
    text.text = f"Edges - {num_edges}"

def textbox_update(textbox):
    if textbox.engine.cache["pending_edge"] is None:
        textbox.engine.cache["textbox"] = None
        textbox.delete()

def textbox_input(textbox, char):
    if textbox.entered:
        textbox.engine.cache["pending_edge"].weight = textbox.text
        textbox.engine.cache["pending_edge"] = None
        textbox.engine.cache["textbox"] = None
        textbox.delete()
        return

    if char.isdigit() and len(textbox.text) <= 15:
        textbox.text += char

def edge_update(edge):
    if not edge.mouse.clicked:
        return 

    match edge.mouse.button:
        # Query user for edge weight if left clicked
        case Button.LEFT_CLICK:
            if edge.engine.cache["pending_edge"] == None:
                edge.engine.cache["pending_edge"] = edge
                textbox = Textbox("Enter edge weight", input=textbox_input, update=textbox_update)
                engine.new(textbox)
                engine.cache["textbox"] = textbox
            elif edge.engine.cache["pending_edge"] != edge:
                edge.engine.cache["pending_edge"] = edge
                engine.cache["textbox"].reset_input()
        # Delete edge if it was right clicked
        case Button.RIGHT_CLICK:
            if edge.engine.cache["pending_edge"] == edge:
                edge.engine.cache["pending_edge"] = None
                print(edge.engine.cache["pending_edge"])

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
            # Remove all edges connected to node
            entities_copy = node.engine._entities[:]
            for entity in filter(lambda entity: type(entity) == Edge, entities_copy):
                if entity.u == node or entity.v == node:
                    node.engine._entities.remove(entity)
            # Reset cache
            node.engine.cache["pending_node"] = None
            node.delete()

def program(window):
    if not window.clicked: 
        return

    match window.button:
        case Button.LEFT_CLICK:
            new_node = Node(window.mouse_pos, update=node_update)
            engine.new(new_node) # Create new node when window is clicked
            window.set_focused(new_node)

        case Button.RIGHT_CLICK:
            pass
            

engine.new(Text("Nodes - ", pos=(5, 5), font_size=25, update=calculate_nodes))
engine.new(Text("Edges - ", pos=(5, 30), font_size=25, update=calculate_edges))

engine.start(program)