import random
import copy
import math

class SudokuSolver:
    def __init__(self,board,m,n):
        self.board = board
        self.m = m
        self.n = n
        self.size = m*n
        self.fixed = [[cell != 0 for cell in row] for row in board]
        self.solution = copy.deepcopy(board)

    def initialize(self):
        for box_row in range(0,self.size,self.m):
            for box_col in range(0,self.size,self.n):
                nums = list(range(1,self.size+1))
                for i in range(self.m):
                    for j in range(self.n):
                        r,c = box_row+i,box_col+j
                        if self.fixed[r][c]:
                            if self.solution[r][c] in nums:
                                nums.remove(self.solution[r][c])
                random.shuffle(nums)
                for i in range(self.m):
                    for j in range(self.n):
                        r,c = box_row+i,box_col+j
                        if not self.fixed[r][c]:
                            self.solution[r][c] = nums.pop()

    def cost(self):
        conflicts = 0

        # Row conflicts
        for row in self.solution:
            seen = [0] * (self.size + 1)
            for num in row:
                if num != 0:
                    seen[num] += 1
            conflicts += sum(count - 1 for count in seen if count > 1)

        # Column conflicts
        for col in range(self.size):
            seen = [0] * (self.size + 1)
            for row in range(self.size):
                num = self.solution[row][col]
                if num != 0:
                    seen[num] += 1
            conflicts += sum(count - 1 for count in seen if count > 1)

        # Box conflicts
        for box_row in range(0, self.size, self.m):
            for box_col in range(0, self.size, self.n):
                seen = [0] * (self.size + 1)
                for i in range(self.m):
                    for j in range(self.n):
                        r = box_row + i
                        c = box_col + j
                        num = self.solution[r][c]
                        if num != 0:
                            seen[num] += 1
                conflicts += sum(count - 1 for count in seen if count > 1)

        return conflicts

    
    def get_box_indices(self):
        boxes = []
        for box_row in range(0,self.size,self.m):
            for box_col in range(0,self.size,self.n):
                cells = []
                for i in range(self.m):
                    for j in range(self.n):
                        r, c = box_row+i,box_col+j
                        if not self.fixed[r][c]:
                            cells.append((r,c))
                boxes.append(cells)
        return boxes
    
    def solve(self, max_iter=100000, T=1.0, cooling_rate=0.999):
        for attempt in range(20):  # up to 5 random restarts
            self.initialize()
            current_cost = self.cost()
            boxes = self.get_box_indices()

            for _ in range(max_iter):
                if current_cost == 0:
                    return self.solution

                box = random.choice(boxes)
                if len(box) < 2:
                    continue

                (r1, c1), (r2, c2) = random.sample(box, 2)
                self.solution[r1][c1], self.solution[r2][c2] = self.solution[r2][c2], self.solution[r1][c1]

                new_cost = self.cost()
                delta = new_cost - current_cost

                if delta < 0 or random.random() < math.exp(-delta / T):
                    current_cost = new_cost
                else:
                    self.solution[r1][c1], self.solution[r2][c2] = self.solution[r2][c2], self.solution[r1][c1]

                T *= cooling_rate

            print(f"Restarting... Attempt {attempt+1}/20 failed with cost {current_cost}")
        
        return None  # if all attempts fail
