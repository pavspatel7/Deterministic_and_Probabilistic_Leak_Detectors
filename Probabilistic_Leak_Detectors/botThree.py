import random
from helperMethod import *

class bot3():
    def __init__(self, getGrid, botpos, leakpos_1, alpha):

        self.grid = getGrid
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        # temp grid
        self.MOVES = 0
        self.SENSOR = 0
        self.bot_3_grid = [row.copy() for row in self.grid]
        self.task_for_bot3(self.bot_3_grid, botpos, alpha)

    def task_for_bot3(self, grid, botpos, alpha):
        debug = False
        # probability matrix
        cell_probability_dict = {}
        opent = 0
        leak_in_i = 0

        if debug:
            for x in grid:
                print(''.join(x))
            print()

        # In dictionary storing the cell as (x,y) as key and probabilities as value:
        # 1) open and leak cell to by default probability is 1 / total open cells
        # 2) block and bot cell to by default probability is 0
        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] == "⬜️" or grid[x][y] == "🟥":
                    opent += 1
                    cell_probability_dict[(x, y)] = 1
                if grid[x][y] == "⬛️" or grid[x][y] == "😀":
                    cell_probability_dict[(x, y)] = 0
        for items in cell_probability_dict.keys():
            if cell_probability_dict[items] == 1:
                cell_probability_dict[items] = 1 / opent

        while botpos != self.leakpos_1:

            # precalculate distances from botpos to all other locations
            distances = all_distances_bfs(2, grid, 1, botpos)
            if debug: print(distances)

            # P(leak in j | leak not in i)
            cell_probability_dict = leak_in_j_given_no_leak_in_i(cell_probability_dict, botpos, leak_in_i)

            # P(beep in i | leak in leak location)
            curr_beep_prob = beep_in_i_given_leak_in_j(alpha, grid, botpos, self.leakpos_1, distances)
            # generate a random number to compare
            rand = random.uniform(0, 1)
            self.SENSOR += 1
            if curr_beep_prob >= rand:
                if debug: print("beep")
                cell_probability_dict = prob_leak_given_beep(alpha, grid, cell_probability_dict, botpos, distances)
            else:
                if debug: print("no beep")
                cell_probability_dict = prob_leak_given_no_beep(alpha, grid, cell_probability_dict, botpos, distances)

            # plan a path towards high probability with short path from botpos in grid
            max_value = max(cell_probability_dict.values())
            max_keys = [k for k, v in cell_probability_dict.items() if v == max_value]
            min_path_len = float('inf')
            for key in max_keys:
                path_len = distances.get(key, float('inf'))
                if min_path_len > path_len:
                    min_path_len = path_len
            max_keys_w_min_len = [k for k in max_keys if distances.get(k, float('inf')) == min_path_len]
            end_a, end_b = max_keys_w_min_len[random.randint(0, len(max_keys_w_min_len) - 1)]
            path = find_shortest_path_bot3(2, grid, 1, botpos, (end_a, end_b))

            while len(path) != 0:
                botpos = path.pop(0)

                if debug:
                    i, j = botpos
                    grid[i][j] = "😀"
                    for x in grid:
                        print(''.join(x))
                    print()

                if botpos == self.leakpos_1:
                    if debug: print("leak found")
                    break
                else:
                    leak_in_i = cell_probability_dict[botpos]
                    # P(leak in j | leak not in i)
                    cell_probability_dict = leak_in_j_given_no_leak_in_i(cell_probability_dict, botpos, leak_in_i)
                self.MOVES += 1

            temp_distance_dict.clear()
