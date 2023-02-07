import tkinter as tk
import pygame
import box
import math
from heapq import heappop, heappush

pygame.init()
window_height = 600
window_width = 1100

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dijkstra's Algorithm")

clock = pygame.time.Clock()

# colors
black = (0, 0, 0)
gray = (30, 30, 30)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

box_size = 20
cols = window_width // box_size
rows = window_height // box_size

grid = []
neighbors = []
path = []
start_and_destination = []

# create a multidimensional grid and fill it with the values of each cell
for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(box.Box(i, j))
    grid.append(arr)

# set the neighbors of each cell
for i in range(cols):
    for j in range(rows):
        grid[i][j].set_neighbor(cols, rows)


def start():
    left_button = 1
    right_button = 3
    start_search = False
    continue_search = True
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                if event.buttons[0]:
                    a = x // box_size
                    b = y // box_size
                    box = grid[a][b]
                    if box not in start_and_destination:
                        grid[a][b].wall = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == right_button:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                box_x = mouse_x // box_size
                box_y = mouse_y // box_size
                print(box_x, box_y)
                selected_box = grid[box_x][box_y]
                if len(start_and_destination) < 2:
                    if not selected_box.is_start and len(start_and_destination) == 0 and not selected_box.wall:
                        selected_box.is_start = True
                        start_and_destination.append(selected_box)

                    if not selected_box.is_start and not selected_box.is_destination and len(
                            start_and_destination) == 1 and not selected_box.wall:
                        selected_box.is_destination = True
                        start_and_destination.append(selected_box)

            if event.type == pygame.KEYDOWN and len(start_and_destination) == 2:
                start_search = True

        if start_search:
            start_box = start_and_destination[0]
            destination_box = start_and_destination[1]
            start_box.distance = 0
            heap = [(start_box.distance, start_box)]
            while heap and continue_search:
                current_box = heappop(heap)[1]
                if current_box == destination_box and not current_box.wall:
                    while current_box.parent:
                        path.append(current_box)
                        current_box = current_box.parent

                current_box.visited = True

                for neighbor in current_box.neighbors:
                    x, y = neighbor
                    box = grid[x][y]
                    if box.visited or box.wall:
                        continue
                    new_distance = current_box.distance + 1
                    if new_distance < box.distance and not box.is_destination:
                        box.queued = True
                        box.distance = new_distance
                        box.parent = current_box
                        heappush(heap, (box.distance, box))

        screen.fill(black)
        for x in range(cols):
            for y in range(rows):
                box = grid[x][y]
                box.draw(screen, box_size, gray)

                if box.is_start:
                    box.draw(screen, box_size, green)

                if box.is_destination:
                    box.draw(screen, box_size, red)

                if box in path[1:]:
                    box.draw(screen, box_size, blue)

                if box.wall:
                    box.draw(screen, box_size, (255, 255, 0))

                # if box.queued:
                #     box.draw(screen, box_size, (0, 255, 255))
                #
                # if box.parent:
                #     box.draw(screen, box_size, (255, 0, 255))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    start()
    pygame.quit()
