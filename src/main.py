import tkinter as tk
from tkinter import messagebox
import pygame
import box
import math
from heapq import heappop, heappush

pygame.init()
window_height = 630
window_width = 1080

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dijkstra's Algorithm")
clock = pygame.time.Clock()

# colors
black = (0, 0, 0)
gray = (33, 37, 41)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (252, 163, 17)
cyan = (0, 204, 204)
light_cyan = (0, 100, 100)
dark_blue = (36, 73, 89)

box_size = 18
cols = math.ceil(window_width / box_size)
rows = math.ceil(window_height / box_size)

grid = []
neighbors = []
path = []
start_and_destination = []
heap_queue = []

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
                start_box = start_and_destination[0]
                destination_box = start_and_destination[1]
                start_box.distance = 0
                heap_queue = [(start_box.distance, start_box)]
                start_search = True

        if start_search:
            if heap_queue and continue_search:
                current_box = heappop(heap_queue)[1]
                current_box.visited = True
                if current_box == destination_box and not current_box.wall:
                    continue_search = False
                    while current_box.parent:
                        path.append(current_box)
                        current_box = current_box.parent

                for neighbor in current_box.neighbors:

                    x, y = neighbor
                    box = grid[x][y]
                    if box.visited or box.wall:
                        continue
                    new_distance = current_box.distance + 1

                    if new_distance < box.distance:
                        box.queued = True
                        box.distance = new_distance
                        box.parent = current_box
                        heappush(heap_queue, (box.distance, box))

            else:
                if continue_search:
                    tk.Tk().wm_withdraw()
                    messagebox.showinfo("No path", "No path found!")
                    break

        screen.fill(black)
        for x in range(cols):
            for y in range(rows):
                box = grid[x][y]
                box.draw(screen, box_size, gray)

                if box.queued:
                    box.draw(screen, box_size, light_cyan)

                if box.visited:
                    box.draw(screen, box_size, cyan)

                if box in path:
                    box.draw(screen, box_size, blue)

                if box.is_start:
                    box.draw(screen, box_size, green)

                if box.is_destination:
                    box.draw(screen, box_size, red)

                if box.wall:
                    box.draw(screen, box_size, yellow)

        pygame.display.flip()


if __name__ == "__main__":
    start()
    pygame.quit()
