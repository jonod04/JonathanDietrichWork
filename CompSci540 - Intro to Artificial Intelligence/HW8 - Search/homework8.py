import heapq


def state_check(state):
    """check the format of state, and return corresponding goal state.
       Do NOT edit this function."""
    non_zero_numbers = [n for n in state if n != 0]
    num_tiles = len(non_zero_numbers)
    if num_tiles == 0:
        raise ValueError('At least one number is not zero.')
    elif num_tiles > 9:
        raise ValueError('At most nine numbers in the state.')
    matched_seq = list(range(1, num_tiles + 1))
    if len(state) != 9 or not all(isinstance(n, int) for n in state):
        raise ValueError('State must be a list contain 9 integers.')
    elif not all(0 <= n <= 9 for n in state):
        raise ValueError('The number in state must be within [0,9].')
    elif len(set(non_zero_numbers)) != len(non_zero_numbers):
        raise ValueError('State can not have repeated numbers, except 0.')
    elif sorted(non_zero_numbers) != matched_seq:
        raise ValueError('For puzzles with X tiles, the non-zero numbers must be within [1,X], '
                          'and there will be 9-X grids labeled as 0.')
    goal_state = matched_seq
    for _ in range(9 - num_tiles):
        goal_state.append(0)
    return tuple(goal_state)


def get_manhattan_distance(from_state, to_state):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (The first one is current state, and the second one is goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    for idx, tile in enumerate(from_state):
        if tile != 0:
            goal_idx = to_state.index(tile)
            r1, c1 = divmod(idx, 3)
            r2, c2 = divmod(goal_idx, 3)
            distance += abs(r1 - r2) + abs(c1 - c2)
    return distance


def naive_heuristic(from_state, to_state):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (The first one is current state, and the second one is goal state)

    RETURNS:
        0 (but experimenting with other constants is encouraged)
    """
    return 0


def sum_of_squares_distance(from_state, to_state):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (The first one is current state, and the second one is goal state)

    RETURNS:
        A scalar that is the sum of squared distances for all tiles
    """
    distance = 0
    for idx, tile in enumerate(from_state):
        if tile != 0:
            goal_idx = to_state.index(tile)
            r1, c1 = divmod(idx, 3)
            r2, c2 = divmod(goal_idx, 3)
            distance += (abs(r1 - r2) ** 2) + (abs(c1 - c2) ** 2)
    return distance


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    succ_states = []
    for i, val in enumerate(state):
        if val == 0:
            row, col = divmod(i, 3)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < 3 and 0 <= nc < 3:
                    j = nr * 3 + nc
                    if state[j] == 0:
                        continue
                    new_state = list(state)
                    new_state[i], new_state[j] = new_state[j], new_state[i]
                    succ_states.append(new_state)
    unique = []
    for s in succ_states:
        if s not in unique:
            unique.append(s)
    return sorted(unique)


def print_succ(state, heuristic=get_manhattan_distance):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        Prints the list of all the valid successors in the puzzle. 
    """
    goal_state = state_check(state)
    succ_states = get_succ(state)
    for succ_state in succ_states:
        print(succ_state, "h={}".format(heuristic(succ_state, goal_state)))


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0], heuristic=get_manhattan_distance):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    goal = list(state_check(state))
    flat = [n for n in state if n != 0]
    if len(flat) == 8:
        inversions = sum(1 for i in range(len(flat)) for j in range(i+1, len(flat)) if flat[i] > flat[j])
        if inversions % 2 != 0:
            print(False)
            return
    print(True)

    open_list = []
    g_values = {tuple(state): 0}
    came_from = {}
    h0 = heuristic(state, goal)
    heapq.heappush(open_list, (h0, tuple(state)))
    closed = set()
    max_queue_length = 1

    while open_list:
        max_queue_length = max(max_queue_length, len(open_list))
        f, current = heapq.heappop(open_list)
        if current in closed:
            continue
        if list(current) == goal:
            break
        closed.add(current)
        g_curr = g_values[current]
        for succ in get_succ(list(current)):
            st = tuple(succ)
            if st in closed:
                continue
            tentative_g = g_curr + 1
            if st not in g_values or tentative_g < g_values[st]:
                g_values[st] = tentative_g
                came_from[st] = current
                f2 = tentative_g + heuristic(succ, goal)
                heapq.heappush(open_list, (f2, st))

    path = []
    node = tuple(goal)
    while True:
        g = g_values.get(node, 0)
        h_val = heuristic(list(node), goal)
        path.append((list(node), h_val, g))
        if node not in came_from:
            break
        node = came_from[node]
    path.reverse()

    for st, h_val, moves in path:
        print(st, "h={}".format(h_val), "moves: {}".format(moves))
    print("Max queue length: {}".format(max_queue_length))

if __name__ == "__main__":
    """
    Feel free to write your own test code here to examine the correctness of your functions.
    Note that this part will not be graded.
    """
    solve([2,5,1,4,0,6,7,0,3], heuristic=get_manhattan_distance)
    solve([4,3,0,5,1,6,7,2,0], heuristic=get_manhattan_distance)
    solve([1,2,3,4,5,6,8,7,0], heuristic=get_manhattan_distance)