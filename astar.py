import math
import heapq

test_world = [
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '.', '.', '.', '.', '.', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
]

cardinal_moves = [(0,-1), (1,0), (0,1), (-1,0)]

costs = { '.': 1, '*': 3, '#': 5, '~': 7}

def add_coord(moves, vert):
  y = vert[0] + moves[0]
  x = vert[1] + moves[1]
  return((y,x))

assert add_coord(cardinal_moves[0], (0,0)) == (0,-1)


def get_cost_neighbor(costs,world,next):
  next_y = next[0]
  next_x = next[1]  
  char = world[next_y][next_x]
  if char in costs:
    cost = costs[char]
  else:
      cost = 9999
  return cost

next_boi = (5,5)
world_boi = [[],[],[],[],[],['.','.','.','.','.','x']]
cost_boi = get_cost_neighbor(costs, world_boi, next_boi)
assert cost_boi == 9999

def heuristic(world, start, end):
  start_row = start[1]
  end_row = end[1]
  start_col = start[0]
  end_col = end[0]
  if start_row == end_row:
    return end_col - start_col
  if start_col == end_col:  
    return end_row - start_row
  return(round(math.sqrt(((end_col - start_col)**2) + (end_row - start_row)**2)))

def get_current_neighbors(world, moves, current, neighbors):
    for vert in moves:
        coord = add_coord(vert, current)
        if coord[0] < 0 or coord[1] < 0 or coord[0] > len(world) - 1 or coord[1] > len(world[0]) - 1:
            continue
        neighbors.append(coord)

def reconstruct_path(came_from, current, final_node):
    total_path = []
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.insert(0,final_node)
    return total_path

def construct_movement(return_path):
    flip_tup = []
    movement = []
    for i in range(len(return_path)):
        flip_tup.append((return_path[i][1], return_path[i][0]))
    for i in range(len(return_path) - 1):
        movement.append((flip_tup[i][0] - flip_tup[i + 1][0], flip_tup[i][1] - flip_tup[i + 1][1]))
    movement.reverse()
    return movement

def a_star_search( world, start, goal, costs, moves, heuristic):
    open_set = {start : 0}
    came_from = {}
    g_score = {}
    f_score = {}
    for i in range(len(world)):
        for j in range(len(world[0])):
            g_score[(i,j)] = 9999
            f_score[(i,j)] = 9999
    g_score[start] = 0
    neighbors = []
    f_score[start] = heuristic(world, start, goal)
    return_path = []

    while len(open_set) > 0:
        current = min(open_set, key=open_set.get)
        if current == goal:
            return_path = reconstruct_path(came_from, current, goal)
            #spit out movement path from node path
            return construct_movement(return_path)
        del open_set[current]
        get_current_neighbors(world, moves, current, neighbors)
        for n in neighbors:
            tentative_g_score = g_score[current] + get_cost_neighbor(costs, world, n)
            if tentative_g_score < g_score[n]:
                came_from[n] = current
                g_score[n] = tentative_g_score
                f_score[n] = g_score[n] + heuristic(world, n, goal)
                if n not in open_set:
                    open_set[n] = 0
    print("path not found")

s = a_star_search(test_world, (0,0), (6,6), costs, cardinal_moves, heuristic)
assert s == [(0,1), (0,1), (0,1), (1,0), (1,0), (1,0), (1,0), (1,0), (1,0), (0,1), (0,1), (0,1)]
