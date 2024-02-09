import math

# Function to calculate the distance between a point and a line segment
def point_to_line_distance(point, line_start, line_end):
    x1, y1 = line_start
    x2, y2 = line_end
    x0, y0 = point
    
    dx = x2 - x1
    dy = y2 - y1
    
    if dx == dy == 0:  # Line is a point
        return math.hypot(x1 - x0, y1 - y0)

    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)
    
    if t < 0:
        px, py = x1, y1
    elif t > 1:
        px, py = x2, y2
    else:
        px, py = x1 + t * dx, y1 + t * dy

    return math.hypot(x0 - px, y0 - py)

# Function to calculate the midpoint of a line segment
def midpoint(line_start, line_end):
    return ((line_start[0] + line_end[0]) // 2, (line_start[1] + line_end[1]) // 2)