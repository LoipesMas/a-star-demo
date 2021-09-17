from queue import PriorityQueue
from collections import defaultdict


class AStar:
    def __init__(self, grid: list, start: tuple, goal: tuple):
        self.grid = grid
        self.goal = goal
        self.openSet : PriorityQueue = PriorityQueue()
        self.qSize = 1
        self.count = 0
        self.openSet.put((d(start, self.goal), self.count, start))
        self.visited : dict = defaultdict(lambda: False)

        self.gScore : dict = defaultdict(lambda: float("inf"))
        self.gScore[start] = 0

        self.fScore : dict = defaultdict(lambda: float("inf"))
        self.fScore[start] = d(start, self.goal)

        self.cameFrom : dict = defaultdict(lambda: ())

    def step(self):
        if self.qSize == 0:
            return (None, None)

        visited = []
        current = self.openSet.get()[2]

        if current == self.goal:
            self.qSize = 0
            return (current, visited)

        self.qSize -= 1
        c_x, c_y = current

        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            n_x, n_y = c_x + x, c_y + y
            neighbor = (n_x, n_y)
            if (
                n_x < 0
                or n_x >= len(self.grid[0])
                or n_y < 0
                or n_y >= len(self.grid)
            ):
                continue

            if self.grid[n_y][n_x] in [2, 3]:
                continue

            visited.append(neighbor)
            tentative_gScore = self.gScore[current] + d(current, neighbor)
            if tentative_gScore < self.gScore[neighbor]:
                self.cameFrom[neighbor] = current
                self.gScore[neighbor] = tentative_gScore
                self.fScore[neighbor] = self.gScore[neighbor] + d(
                    neighbor, self.goal
                )
                if not self.visited[neighbor]:
                    self.count += 1
                    self.openSet.put((self.fScore[neighbor], self.count, neighbor))
                    self.qSize += 1

        return (current, visited)


    def reconstruct_path(self, current: tuple):
        total_path = [current]
        while current in self.cameFrom.keys():
            current = self.cameFrom[current]
            total_path.append(current)
        return total_path


def d(curr: tuple, target: tuple):
    x = abs(curr[0] - target[0])
    y = abs(curr[1] - target[1])
    return x + y  # math.sqrt(x**2+y**2)


if __name__ == "__main__":
    pass
