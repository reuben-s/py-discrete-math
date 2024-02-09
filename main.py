import pygame
import sys
import random

from Node import Node
from Edge import Edge
from constants import WIDTH, HEIGHT, BLACK, DOUBLE_CLICK_TIME

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Discrete Math")

# List of node & edge objects
nodes = []
edges = []

# Information
last_click_time = 0
current_node = -1
last_clicked_node = -1
drawing_edge = False

# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        print(len(edges))

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Delete edge if it was right clicked, otherwise if it was clicked, prompt for edge weight
            for x, edge in enumerate(edges):
                if edge.u is None or edge.v is None:
                    continue
                # Calculate distance from mouse position to the line
                distance = abs((edge.u.pos[1] - edge.v.pos[1]) * mouse_pos[0] -
                        (edge.u.pos[0] - edge.v.pos[0]) * mouse_pos[1] +
                        edge.u.pos[0] * edge.v.pos[1] - edge.u.pos[1] * edge.v.pos[0]) / \
                    ((edge.u.pos[1] - edge.v.pos[1])**2 + (edge.u.pos[0] - edge.v.pos[0])**2)**0.5

                # Check if distance is within a threshold (5px). If it is, delete edge.
                if distance <= 5:
                    print("Edge clicked")
                    #edges.pop(x)

            # Check if the mouse click is within any node
            for x, node in enumerate(nodes):
                if node.is_clicked(mouse_pos):
                    if event.button == 3:
                        edges_copy = edges[:]
                        for edge in edges_copy:
                            if edge.u == node or edge.v == node:
                                edges.remove(edge)
                        nodes.pop(x)
                    else:
                        current_node = x

                        if drawing_edge:
                            edges[len(edges) - 1].v = nodes[current_node]
                            drawing_edge = False
                            break

                        # If node was double clicked, create a new edge.
                        current_time = pygame.time.get_ticks()
                        if (current_time - last_click_time < DOUBLE_CLICK_TIME) and (last_clicked_node == current_node):  
                            print(f"Double click = TRUE")
                            edges.append(Edge(node))
                            drawing_edge = True
                        else: # If it was not a double click, the user wanted to drag the node
                            nodes[x].set_dragging(True)

                        last_click_time = current_time
                        last_clicked_node = current_node
                    break
            else:
                if event.button != 1: # Break out of loop if left click was not used.
                    break
                # If no node is being clicked then create a new node.
                nodes.append(Node(mouse_pos))
                current_node = len(nodes) - 1

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button != 1:
                break
            # On mouse button release, stop dragging all nodes
            current_node = -1
            nodes[current_node].set_dragging(False)

    # Update node positions if dragging
    if current_node != -1:
        nodes[current_node].set_position(pygame.mouse.get_pos())

    # Draw the nodes
    for node in nodes:
        node.draw(screen)

    for edge in edges:
        if edge.u is None or edge.v is None:
            continue
        pygame.draw.line(screen, (255, 255, 255), edge.u.pos, edge.v.pos, 3)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()