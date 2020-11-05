import pygame
import time
from astar import AStar

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 820

WHITE = (200, 200, 200)
RED = (200, 0, 0)
CYAN = (0, 200, 200)
YELLOW = (200, 200, 0)
GREEN = (0, 200, 0)
LIME = (161, 235, 0)
LIGHTYELLOW = (180, 180, 120)
BLUE = (0, 0, 200)
BLACK = (50, 50, 50)

#        0 empty, 1 visited, 2 path, 3 wall, 4 goal, 5 start, 6 final_path
colors = [BLACK,    LIGHTYELLOW, YELLOW, WHITE, BLUE, CYAN, LIME]

blockSize = 20  # Set the size of the grid block

grid = []
start: tuple
goal: tuple

top_bar_height = 20


def main(_start=(0, 0), _goal=(30, 30)):
    global grid, start, goal

    pygame.font.init()

    font = pygame.font.SysFont('hacknerdfont', 17)
    top_bar_text = font.render(
        "LMB - draw wall, RMB - erase wall, s - set start, g - set goal, r - run / reset", True, YELLOW)
    success_text = font.render("GOAL REACHED", True, BLACK)
    failure_text = font.render("GOAL NOT REACHED", True, BLACK)

    start = _start
    goal = _goal

    LMB_DOWN = False
    RMB_DOWN = False

    # dont start pathfinding yet, wait for the user to draw
    pathfind = False
    finished = False

    success = False

    path = None

    def reset():
        global grid, start, goal
        grid = []
        for _ in range((WINDOW_HEIGHT//blockSize)-2):
            grid.append([])
            for _ in range((WINDOW_WIDTH//blockSize)-2):
                grid[-1].append(0)
        start = _start
        goal = _goal
        grid[goal[1]][goal[0]] = 4
        grid[start[1]][start[0]] = 5
        path = None

    reset()
    a_star = AStar()

    def draw_top_bar():
        SCREEN.blit(top_bar_text, (0, 0))

    def drawGrid():
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                color = colors[cell]
                pygame.draw.rect(
                    SCREEN, color, (2+x*(blockSize+1), top_bar_height+2+y*(blockSize+1), blockSize, blockSize))

    (width, height) = (WINDOW_WIDTH, WINDOW_HEIGHT)
    SCREEN = pygame.display.set_mode((width, height))
    SCREEN.fill((0, 0, 0))
    pygame.display.flip()
    pygame.display.set_caption('A* showcase')

    running = True

    while running:
        if not finished and pathfind:
            time.sleep(0.03)
        SCREEN.fill((0, 0, 0))

        draw_top_bar()

        # a_star
        if pathfind:
            ret, visited = a_star.step()
            if ret == goal:
                pathfind = False
                finished = True
                success = True
                path = a_star.reconstruct_path(ret)
                for n in path[1:-1]:
                    grid[n[1]][n[0]] = 6
            if ret == None:
                pathfind = False
                finished = True
                success = False
            if ret:
                a, b = ret
                grid[b][a] = max(grid[b][a], 2)
            if visited:
                for v in visited:
                    a, b = v
                    grid[b][a] = max(grid[b][a], 1)

        drawGrid()

        if finished:
            if success:
                pygame.draw.rect(SCREEN, WHITE, (320, 340, 170, 40))
                SCREEN.blit(success_text, (350, 350))
            else:
                pygame.draw.rect(SCREEN, WHITE, (320, 340, 180, 40))
                SCREEN.blit(failure_text, (330, 350))

        pygame.display.flip()
        m_pos_x, m_pos_y = pygame.mouse.get_pos()
        x, y = m_pos_x//(blockSize+1), (m_pos_y-top_bar_height)//(blockSize+1)
        x = min(x, len(grid[0])-1)
        y = min(y, len(grid)-1)

        for event in pygame.event.get():
            if pathfind:
                break
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if finished:
                    finished = False
                    reset()
                if event.button == 1:
                    LMB_DOWN = True
                    RMB_DOWN = False
                elif event.button == 3:
                    RMB_DOWN = True
                    LMB_DOWN = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    LMB_DOWN = False
                elif event.button == 3:
                    RMB_DOWN = False

            if LMB_DOWN:
                if grid[y][x] == 0:
                    grid[y][x] = 3
            elif RMB_DOWN:
                if grid[y][x] == 3:
                    grid[y][x] = 0

            if event.type == pygame.KEYDOWN:
                if event.key == ord("s"):
                    if grid[y][x] == 0:
                        if finished:
                            finished = False
                            reset()
                        grid[start[1]][start[0]] = 0
                        start = (x, y)
                        grid[y][x] = 5
                elif event.key == ord("g"):
                    if grid[y][x] == 0:
                        if finished:
                            finished = False
                            reset()
                        grid[goal[1]][goal[0]] = 0
                        goal = (x, y)
                        grid[y][x] = 4
                elif event.key == ord("r"):
                    if finished:
                        finished = False
                        reset()
                    else:
                        a_star.main(grid, start, goal)
                        pathfind = True


if __name__ == "__main__":
    main()
