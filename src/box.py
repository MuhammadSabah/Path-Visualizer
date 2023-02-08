import pygame


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.is_start = False
        self.is_destination = False
        self.distance = float('inf')
        self.parent = None
        self.visited = False
        self.wall = False
        self.queued = False

    def draw(self, screen, box_size, color):
        rect = pygame.Rect(self.x * box_size, self.y * box_size, box_size - 1, box_size - 1)
        pygame.draw.rect(screen, color, rect, border_radius=2)

    def set_neighbor(self, cols, rows):
        # Check the cell above the current cell
        if self.y > 0:
            self.neighbors.append((self.x, self.y - 1))
        # Check the cell below the current cell
        if self.y < rows - 1:
            self.neighbors.append((self.x, self.y + 1))
        # Check the cell to the left of the current cell
        if self.x > 0:
            self.neighbors.append((self.x - 1, self.y))
        # Check the cell to the right of the current cell
        if self.x < cols - 1:
            self.neighbors.append((self.x + 1, self.y))

    def __lt__(self, other):
        return self.distance < other.distance
