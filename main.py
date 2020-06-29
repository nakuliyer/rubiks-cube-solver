# Nakul Iyer 2020
#
# Python translation and 3D visualization of Stefan Pochmann's C++ implementation
# http://www.stefan-pochmann.info/spocc/other_stuff/tools/
# inspired by Mark Dufour's Python translation at
# https://github.com/shedskin/shedskin/blob/master/examples/rubik2.py
#
# 3D visualization with pygame

import sys, math, pygame, random, time
from cube import Cube3D
from solver import Solver

# Window width and height
WIN_WIDTH = 900
WIN_HEIGHT = 700

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.cube = Cube3D()

    def run(self, scramble=None, scramble_length=20):
        frame_num = 0
        stage = 0 # 0 for scrambling, 1 for solving, 2 for turning solution
        verbose = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(1000)
            self.screen.fill((0, 0, 0))

            if frame_num == 0:
                self.cube.rotate((-30, -30, 0))
                scramble = self.cube.get_scramble_str(scramble_length) if scramble == None else scramble
                print("Scrambling ... " + scramble)
                print()
                self.cube.str_moves(scramble)

            if stage == 0:
                if self.cube.done_turning():
                    stage = 1
            if stage == 1:
                moves_set = self.cube.moves_set
                solver = Solver()
                solver.apply_moves(moves_set)
                state = solver.get_state()

                if verbose == 0:
                    print("Scramble returned: ")
                    print(state)
                    print()
                    print("Solving...")
                    verbose = 1
                    solution = solver.solve()
                    stage = 2
            if stage == 2:
                if verbose == 1:
                    print("Showing solution...")
                    self.cube.str_moves(solution)
                    verbose += 1
                if self.cube.done_turning():
                    time.sleep(5)
                    sys.exit()

            self.cube.show(self.screen)

            pygame.display.flip()
            frame_num += 1

if __name__ == '__main__':
    Main().run(scramble_length=4)
