import pygame
import sys
import random
import math

from Node import Node
from Edge import Edge
from constants import WIDTH, HEIGHT, BLACK, WHITE, DOUBLE_CLICK_TIME
from util import point_to_line_distance, midpoint

# Initialize Pygame
pygame.init()
font = pygame.font.Font(None, 18)

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
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Delete edge if it was right clicked, otherwise if it was clicked, prompt for edge weight
            for x, edge in enumerate(edges):
                if edge.u is None or edge.v is None:
                    continue

                # Calculate the length of the line segment
                line_length = math.hypot(edge.v.pos[0] - edge.u.pos[0], edge.v.pos[1] - edge.u.pos[1])
                
                # Calculate the midpoint of the line segment
                mid_point = midpoint(edge.u.pos, edge.v.pos)
                
                range_width = line_length - 20 # 10px clearance either side of line

                # Calculate the distance from the click position to the line itself
                distance_to_line = point_to_line_distance(mouse_pos, edge.u.pos, edge.v.pos)

                # Check if the click position falls within the range around the midpoint
                # and if the distance to the line is within a reasonable threshold
                if (mid_point[0] - range_width / 2 <= mouse_pos[0] <= mid_point[0] + range_width / 2) and \
                (mid_point[1] - range_width / 2 <= mouse_pos[1] <= mid_point[1] + range_width / 2) and \
                (distance_to_line <= 10):  # Adjust this threshold as needed
                    if event.button == 3: # Delete edge if it was right clicked
                        edges.pop(x)
                    elif event.button == 1: # Prompt for length weight otherwise
                        pass
                else:
                    pass


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
                            if current_node != last_clicked_node:
                                edges[len(edges) - 1].v = nodes[current_node]
                                drawing_edge = False
                            break

                        # If node was double clicked, create a new edge.
                        current_time = pygame.time.get_ticks()
                        if (current_time - last_click_time < DOUBLE_CLICK_TIME) and (last_clicked_node == current_node):
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
        
        # Calculate the midpoint of the edge
        text_pos = ((edge.u.pos[0] + edge.v.pos[0]) // 2, (edge.u.pos[1] + edge.v.pos[1]) // 2)
        text_pos = (text_pos[0], text_pos[1] - 30)  # Move text above edge to display it more clearly
        
        # Render the text
        text_surface = font.render(edge.get_weight(), True, WHITE)
        
        # Get the rectangle of the text surface
        text_rect = text_surface.get_rect()
        text_rect.topleft = text_pos
        
        # Blit the text onto the screen
        screen.blit(text_surface, text_rect)
        
        # Draw the edge line
        pygame.draw.line(screen, (255, 255, 255), edge.u.pos, edge.v.pos, 3)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()