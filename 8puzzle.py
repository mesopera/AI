# ===================== BASIC UTILITIES =====================

def index_of(state, val):
    for i in range(len(state)):
        if state[i] == val:
            return i
    return -1

def copy_list(lst):
    result = []
    for x in lst:
        result.append(x)
    return result

def lists_equal(a, b):
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

def tuple_to_list(t):
    result = []
    for x in t:
        result.append(x)
    return result

def list_to_tuple(lst):
    return tuple(lst)

# ===================== PUZZLE LOGIC =====================

def get_row(i):
    return i // 3

def get_col(i):
    return i % 3

def manhattan_distance(state, goal):
    total = 0
    for num in range(1, 9):
        si = index_of(state, num)
        gi = index_of(goal, num)
        sr, sc = get_row(si), get_col(si)
        gr, gc = get_row(gi), get_col(gi)
        dr = sr - gr
        dc = sc - gc
        if dr < 0: dr = -dr
        if dc < 0: dc = -dc
        total += dr + dc
    return total

def get_neighbors(state):
    neighbors = []
    blank = index_of(state, 0)
    br = get_row(blank)
    bc = get_col(blank)

    # [direction, row_change, col_change]
    moves = [["Up", -1, 0], ["Down", 1, 0], ["Left", 0, -1], ["Right", 0, 1]]

    for move in moves:
        direction = move[0]
        nr = br + move[1]
        nc = bc + move[2]
        if nr >= 0 and nr < 3 and nc >= 0 and nc < 3:
            neighbor_i = nr * 3 + nc
            new_state = copy_list(state)
            new_state[blank] = new_state[neighbor_i]
            new_state[neighbor_i] = 0
            neighbors.append([new_state, direction])
    return neighbors

# ===================== MANUAL MIN-HEAP =====================

def heap_push(heap, item):
    heap.append(item)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i][0] < heap[parent][0]:
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break

def heap_pop(heap):
    if len(heap) == 1:
        return heap.pop()
    root = heap[0]
    heap[0] = heap.pop()
    i = 0
    size = len(heap)
    while True:
        left  = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        if left < size and heap[left][0] < heap[smallest][0]:
            smallest = left
        if right < size and heap[right][0] < heap[smallest][0]:
            smallest = right
        if smallest != i:
            heap[i], heap[smallest] = heap[smallest], heap[i]
            i = smallest
        else:
            break
    return root

# ===================== VISITED SET (Manual Hash Map) =====================

def state_to_key(state):
    key = ""
    for x in state:
        key += str(x) + ","
    return key

def set_contains(visited, state):
    key = state_to_key(state)
    return key in visited

def set_add(visited, state):
    key = state_to_key(state)
    visited[key] = True

# ===================== A* SEARCH =====================

def a_star(start, goal):
    heap = []
    visited = {}
    h = manhattan_distance(start, goal)
    # heap item: [f, g, state, path]
    heap_push(heap, [h, 0, copy_list(start), []])

    while len(heap) > 0:
        item = heap_pop(heap)
        f = item[0]
        g = item[1]
        state = item[2]
        path = item[3]

        if set_contains(visited, state):
            continue
        set_add(visited, state)

        if lists_equal(state, goal):
            return path

        for neighbor_info in get_neighbors(state):
            neighbor = neighbor_info[0]
            direction = neighbor_info[1]
            if not set_contains(visited, neighbor):
                new_g = g + 1
                new_h = manhattan_distance(neighbor, goal)
                new_f = new_g + new_h
                new_path = copy_list(path)
                new_path.append(direction)
                heap_push(heap, [new_f, new_g, neighbor, new_path])

    return None

# ===================== PRINT =====================

def print_state(state):
    for r in range(3):
        row_str = ""
        for c in range(3):
            val = state[r * 3 + c]
            if val == 0:
                row_str += "_  "
            else:
                row_str += str(val) + "  "
        print(row_str)
    print()

def apply_move(state, direction):
    state = copy_list(state)
    blank = index_of(state, 0)
    br = get_row(blank)
    bc = get_col(blank)
    move_map = {"Up": [-1, 0], "Down": [1, 0], "Left": [0, -1], "Right": [0, 1]}
    delta = move_map[direction]
    nr = br + delta[0]
    nc = bc + delta[1]
    ni = nr * 3 + nc
    state[blank] = state[ni]
    state[ni] = 0
    return state

# ===================== MAIN =====================

start = [7, 2, 4,
         5, 0, 6,
         8, 3, 1]

goal  = [1, 2, 3,
         4, 5, 6,
         7, 8, 0]

solution = a_star(start, goal)

if solution:
    moves_str = ""
    for i in range(len(solution)):
        if i != 0:
            moves_str += " -> "
        moves_str += solution[i]
    print("Solved in " + str(len(solution)) + " moves: " + moves_str + "\n")

    state = copy_list(start)
    print_state(state)
    for move in solution:
        state = apply_move(state, move)
        print("Move: " + move)
        print_state(state)
else:
    print("No solution exists.")