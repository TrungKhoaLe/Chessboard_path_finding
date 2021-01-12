from collections import defaultdict
import numpy as np
import collections
import pprint

""" Rules on the original board
    1. Topology:
        a. The first column is the leftmost,
        b. the first row is the bottom row of the board.
            e.g. the_original_board[0, 3] = 55. We take the first column from the left and the fourth row from the bottom.
    2. Movements:
        a. The value of -1 means the wall, and you cannot go through it,
        b. the value of 0 means freedom, and you can go in any direction,
        c. values that are greater than 0 mean 'jumping off', you can jump when you step on those positions.
            e.g. the_original_board[col, row] = 37 means that you are now teleported to the cell [col = 3, row = 7]
    Requirement(s):
    Find the shortest path from start = (0, 0) to goal (8, 8)
"""
the_original_board = np.array([[37, 20, 0, 6, 20, -1, 0, -1, 0],
                      [0, 25, 0, 3, 15, -1, 0, 0, 0],
                      [0, -1, -1, 0, 0, -1, 0, 0, 17],
                      [-1, -1, 0, -1, 0, 61, 0, -1, 0],
                      [0, 0, 15, -1, 22, 0, 0, 0, 0],
                      [55, 0, 13, -1, -1, -1, 0, -1, 0],
                      [0, 30, 0, -1, -1, 0, 21, -1, 0],
                      [0, 0, -1, -1, -1, 22, 0, 0, 87],
                      [0, -1, -1, 0, -1, 18, 25, -1, 0]])

temp = the_original_board.T
the_remaped_board = np.flip(temp, axis=1)

class Queue:
  def __init__(self):
    self.elements = collections.deque()

  def empty(self):
    return len(self.elements) == 0

  def put(self, x):
    self.elements.append(x)

  def get(self):
    return self.elements.popleft()

class Graph:
  def __init__(self, connections, directed=False):
    self.graph_ = defaultdict(set) # a dictionary of set has been created
    self.directed_ = directed
    self.add_connections(connections)
  def add_connections(self, connections):
    for node1, node2 in connections:
      self.add(node1, node2)
  def add(self, node1, node2):
    self.graph_[node1].add(node2)
    if not self.directed_:
      self.graph_[node2].add(node1)
  def is_connected(self, node1, node2):
    return node1 in self.graph_ and node2 in self.graph_[node1]
  def find_path(self, node1, node2, path=[]):
    path = path + [node1]
    if node1 == node2:
      return path
    if node1 not in self.graph_:
      return None
    for node in self.graph_[node1]:
      if node not in path:
        new_path = self.find_path(node, node2, path)
        if new_path:
          return new_path
    return None

def _find_all_possibilities(the_remaped_board):
  rows = the_remaped_board.shape[0] # y
  cols = the_remaped_board.shape[1] # x
  # find all coordinates where 0's are present
  temp1 = np.where(the_remaped_board == 0)
  coordinates_of_0 = list(zip(temp1[0], temp1[1])) # the height and width order
  # find all coordinates where -1's are present
  temp2 = np.where(the_remaped_board == -1)
  coordinates_of_1 = list(zip(temp2[0], temp2[1])) # the height and width order

  start = (0, 0)
  goal = (8, 8)
  queue = Queue()
  queue.put(start)
  came_from = {start: True}
  revisited = False
  connections = []
  while not queue.empty():
    current = queue.get()
    if current == goal:
      break
    else:
      print(f'[INFO] Visiting {current}')
      for next in _neighbours(the_remaped_board, current, coordinates_of_1, cols, rows):
        if next not in came_from:
          queue.put(next)
          came_from[next] = True
          edge = (current, next)
          connections.append(edge)
        else:
          print(f'[INFO] It\'s heading back to {next}')
  return came_from, connections

def _neighbours(voyager, coordinates, walls, max_y, max_x):

  y, x = coordinates
  if voyager[y, x] == 0:

    #LEFT
    left = (y, x - 1)
    # RIGHT
    right = (y, x + 1)
    # DOWN
    down = (y + 1, x)
    # UP
    up = (y - 1, x)

    directions = [left, down, up, right]
    directions = filter(lambda x: x not in walls, directions)
    directions = filter(lambda x: 0<= x[0] < max_y and 0<= x[1] < max_x, directions)

  elif voyager[y, x] > 0:
    next_y, next_x = int(voyager[y, x]/10), (voyager[y, x] % 10)
    directions = [(next_y, next_x)]
    directions = filter(lambda x: x not in walls, directions)
    directions = filter(lambda x: 0<= x[0] < max_y and 0<= x[1] < max_x, directions)

  return directions # directions follow the Vim directions

def main(voyager, start=(0,0), goal=(8,8)):
  came_from, connections = _find_all_possibilities(the_remaped_board)
  g = Graph(connections, directed=True)
  pretty_print = pprint.PrettyPrinter()
  pretty_print.pprint(g.graph_)
  path = g.find_path(start, goal)
  print(path)
if __name__ == '__main__':
    main(the_remaped_board)
