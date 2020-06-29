# Rubik's cube solver using Thistlethwaite's algorithm

MOVES = ["L", "R", "U", "D", "F", "B"]

# Cubies definition for setting up Thistlethwaite's algorithm
STATE_CUBIES = [
    [7, 5, 1, 3, 6, 8, 2, 0],
    [25, 21, 19, 23, 26, 24, 18, 20],
    [15, 25, 17, 7, 24, 26, 8, 6],
    [9, 1, 11, 19, 18, 0, 2, 20],
    [15, 3, 9, 21, 24, 6, 0, 18],
    [17, 23, 11, 5, 8, 26, 20, 2]
]

def move_str(m):
    return MOVES[m]

class State:
    def __init__(self, state, orientations, route=None):
        self.state = state
        self.orientations = orientations
        self.route = route or []

    def _id(self, phase):
        # print('.. ', self.state)
        def self_contained(relevants):
            # if all relevant pieces contained amongst themselves
            r = True
            for edge in relevants:
                if not self.state[edge] in relevants:
                    r = False
            return r

        if phase == 0:
            # Orientation of edges
            return tuple(self.orientations[1::2])
        elif phase == 1:
            # Orientation of corners
            result = self.orientations[0::2]

            # E edges in slice
            result += [self_contained([3, 5, 21, 23])]
            return tuple(result)
        elif phase == 2:
            result = [self_contained([9, 11, 15, 17]), # M edges in slice
                      self_contained([1, 7, 19, 25]), # S edges in slice
                      self_contained([8, 24]), # Certain edges in slice diagonal
                      self_contained([6, 26]),
                      self_contained([0, 20]),
                      self_contained([2, 18])]
            corners = [24, 26, 8, 6, 18, 0, 2, 20]
            r = 0
            for i in range(8):
                for j in range(i+1, 8):
                    if corners.index(corners[i]) > corners.index(corners[j]):
                        r += 1
            result += [r%2]
            return tuple(result)
        elif phase == 3:
            # Everything in place
            return tuple(self.state + self.orientations)

    def apply_moves(self, moves_set):
        new_state = self.state[:]
        new_orientations = self.orientations[:]
        for face_idx in moves_set:
            old_state = new_state[:]
            old_orientations = new_orientations[:]
            for i in range(8):
                orientationChange = 0
                if i > 3:
                    if not (1 < face_idx < 4):
                        orientationChange = 2-(i%2)
                elif face_idx > 3:
                    orientationChange = 1
                idx_from = STATE_CUBIES[face_idx][i-3 if (i+1)%4 == 0 else i+1]
                idx_to = STATE_CUBIES[face_idx][i]
                cubie_num = old_state[idx_from]
                orientation = (old_orientations[idx_from] + orientationChange) % (2 + int(i > 3))
                new_state[idx_to] = cubie_num
                new_orientations[idx_to] = orientation
        return State(new_state, new_orientations, self.route + moves_set)

class Solver:
    def __init__(self):
        self.phase_moves = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 16], [1, 4, 6, 7, 8, 9, 10, 11, 13, 16], [1, 4, 7, 10, 13, 16]]

    def apply_moves(self, moves_set):
        current = State(list(range(27)), [0]*27).apply_moves(moves_set)
        self.state = current.state
        self.orientations = current.orientations
        self.o = current

    def get_state(self):
        return {"cubies": self.state, "orientations": self.orientations}

    def _available_moves(self):
        return [([int(i/3)] * (i%3 + 1)) for i in self.phase_moves[self.phase]]

    def solve(self):
        print('Starting solution phases...')
        goal = State(list(range(27)), [0]*27)

        self.o.route = []
        for phase in range(4):
            self.phase = phase
            current_id = self.o._id(phase)
            goal_id = goal._id(phase)

            states = [self.o]
            state_ids = set([current_id])
            if current_id != goal_id:
                phase_ok = False
                while not phase_ok:
                    next_states = []
                    for cur_state in states:
                        for move in self._available_moves():
                            next_state = cur_state.apply_moves(move)
                            next_id = next_state._id(phase)
                            # print(next_id, goal_id)
                            if next_id == goal_id:
                                sol_str = ' '.join([move_str(m) for m in next_state.route]) + ' (%d moves)'% len(next_state.route)
                                print("Phase {} solved with {}".format(phase + 1, sol_str))
                                phase_ok = True
                                self.o = next_state
                                break
                            if next_id not in state_ids:
                                state_ids.add(next_id)
                                next_states.append(next_state)
                        if phase_ok:
                            break
                    states = next_states
            else:
                print("Phase {} solved".format(phase + 1))
        return ' '.join([move_str(m) for m in self.o.route])
