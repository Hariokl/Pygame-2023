from heapq import heappush, heappop


def setup(grid_):
    global grid, graph
    grid = grid_
    graph = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            graph[(x, y)] = graph.get((x, y), []) + get_neigh_nodes(x, y)


def get_neigh_nodes(x, y):
    check_valid_node = lambda x, y: True if 0 <= x < len(grid[0]) and 0 <= y < len(grid) else False
    check_valid_move = lambda x, y, dx, dy: True if abs(dx+dy) == 1 or (grid[y][x+dx] <= 10 and grid[y+dy][x] <= 10) else False
    ds = [-1, 0], [1, 0], [0, 1], [0, -1], [-1, -1], [-1, 1], [1, 1], [1, -1]
    trans_chack = lambda x, y, dx, dy: grid[y+dy][x+dx] if abs(dx+dy) == 1 else grid[y+dy][x+dx] * 1.4
    return [(trans_chack(x, y, dx, dy), (x+dx, y+dy)) for dx, dy in ds if check_valid_node(x + dx, y + dy) and check_valid_move(x, y, dx, dy)]


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_algorithm(start, goal):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}
    i = 0

    while queue:
        i += 1
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            queue = []
            continue

        if cur_node not in graph:
            print(cur_node, graph)
            print((int(cur_node[0]), int(cur_node[1])) in graph, i)

        neigh_nodes = graph[cur_node]
        for neigh in neigh_nodes:
            neigh_cost, neigh_node = neigh
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                visited[neigh_node] = cur_node
                cost_visited[neigh_node] = new_cost

    cur = goal
    way = list()
    while cur is not None:
        way.append(cur)
        cur = visited[cur]
    return way[::-1]

