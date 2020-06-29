# Classes for displaying/turning the cube

import sys, math, pygame, random, time
from operator import itemgetter

MOVES = ["L", "R", "U", "D", "F", "B"]

# Colors of the faces
COLORS = [
    (255, 165, 0),    # orange
    (255, 0, 0),      # red
    (255, 255, 255),  # white
    (255, 255, 0),    # yellow
    (0, 255, 0),      # green
    (0, 0, 255)       # blue
]

# Vertices (8 total) in each cubie face
FACES = [
    (0, 1, 3, 2),
    (4, 5, 7, 6),
    (2, 3, 7, 6),
    (0, 1, 5, 4),
    (0, 2, 6, 4),
    (1, 3, 7, 5)
]

# Cubies definition for turning
CUBIES_AXIS = [
    [4, 2, 1, 0, 3, 6, 7, 8, 5],
    [22, 18, 19, 20, 23, 26, 25, 24, 21],
    [16, 6, 15, 24, 25, 26, 17, 8, 7],
    [10, 2, 11, 20, 19, 18, 9, 0, 1],
    [12, 6, 3, 0, 9, 18, 21, 24, 15],
    [14, 26, 23, 20, 11, 2, 5, 8, 17]
]

# Window width and height
WIN_WIDTH = 900
WIN_HEIGHT = 700

# Projection of the 3D cube onto a 2D display
FOV = 600
VIEWER_DISTANCE = 6

# Speed of cube rotations from fast to slow
ROT_SPEED = 5

class Point3D:
    '''Base 3d point class'''


    def __init__(self, pos):
        '''Initializes x, y, and z of a point in 3d space.'''
        x, y, z = pos
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


    def rotateX(self, angle):
        '''
        Rotates the point about the x axis and returns new point.
        Angle must be in degrees.
        '''
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D((self.x, y, z))


    def rotateY(self, angle):
        '''
        Rotates the point about the y axis and returns new point.
        Angle must be in degrees.
        '''
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D((x, self.y, z))


    def rotateZ(self, angle):
        '''
        Rotates the point about the z axis and returns new point.
        Angle must be in degrees.
        '''
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D((x, y, self.z))


    def project(self, win_width, win_height, fov, viewer_distance):
        '''
        Projects the 3d point onto 2 dimensions and returns the new point
        as a 3d point with the z value unchanged.
        '''
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D((x, y, self.z))


class Cubie3D:
    '''Cubie class'''

    cubie_index = 0

    def __init__(self, pos, width=1):
        '''
        Initializes the rotation and position of the cubie. Creates the 8
        vertices given a center coordinate and a width.

        Args:
            pos {tuple} - 3d position of the cubie
            width {float/int} - width of cubie
        '''
        # Set all positions
        x,y,z = pos
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

        # These are the values of the rotation caused by turning faces
        # of the cube
        self.turX = 0.0
        self.turY = 0.0
        self.turZ = 0.0

        # These are the value of the rotation caused by rotating the whole
        # cube altogether
        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

        self.cubie_index = Cubie3D.cubie_index
        Cubie3D.cubie_index += 1

        # Initialize all the vertices in an array
        self.vertices = []
        for xi in [x-width/2, x+width/2]:
            for yi in [y-width/2, y+width/2]:
                for zi in [z-width/2, z+width/2]:
                    self.vertices.append(Point3D((xi, yi, zi)))

    def clipped(self):
        '''Returns true if no layers are mid-turn'''
        if int(self.turX) % 90 == 0 and int(self.turY) % 90 == 0 and int(self.turZ) % 90 == 0:
            return True
        return False


    def turnX(self, angle):
        '''
        Turns the cubie about the x axis.
        Angle must be in degrees.
        '''
        self.vertices = [v.rotateX(angle) for v in self.vertices]
        self.turX += angle
        self.turX = self.turX % 360


    def turnY(self, angle):
        '''
        Turns the cubie about the y axis.
        Angle must be in degrees.
        '''
        self.vertices = [v.rotateY(angle) for v in self.vertices]
        self.turY += angle
        self.turY = self.turY % 360


    def turnZ(self, angle):
        '''
        Turns the cubie about the z axis.
        Angle must be in degrees.
        '''
        self.vertices = [v.rotateZ(angle) for v in self.vertices]
        self.turZ += angle
        self.turZ = self.turZ % 360


    def rotateX(self, angle):
        '''
        Rotates the cubie about the x axis.
        Angle must be in degrees.
        '''
        self.rotX += angle


    def rotateY(self, angle):
        '''
        Rotates the cubie about the y axis.
        Angle must be in degrees.
        '''
        self.rotY += angle


    def rotateZ(self, angle):
        '''
        Rotates the cubie about the z axis.
        Angle must be in degrees.
        '''
        self.rotZ += angle

    def __repr__(self):
        return "index: {} pos: ({}, {}, {}) tur: ({}, {}, {}) rot: ({}, {}, {})".format(
            self.cubie_index,
            self.x, self.y, self.z,
            self.turX, self.turY, self.turZ,
            self.rotX, self.rotY, self.rotZ
        )

    def get_faces(self, WIN_WIDTH, WIN_HEIGHT):
        '''
        Returns information about the current cubie faces.

        Returns:
            {array} - [[list of vertices as tuples,
                        average z value of all vertices,
                        color of the face]
                       for all 6 faces]
        '''
        t = [v.rotateX(self.rotX).rotateY(self.rotY).rotateZ(self.rotZ).project(WIN_WIDTH, WIN_HEIGHT, FOV, VIEWER_DISTANCE) for v in self.vertices]

        result = []
        for face_idx in range(6):
            f = FACES[face_idx]
            z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
            pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                         (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                         (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                         (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
            result.append([pointlist, z, COLORS[face_idx]])

        return result


class Cube3D:
    '''Rubiks cube class'''

    def __init__(self, WIN_WIDTH=WIN_WIDTH, WIN_HEIGHT=WIN_HEIGHT):
        self.cubies = []
        self.turning = [False] * len(CUBIES_AXIS)
        self.turn_queue = []
        self.ready_frames = 0
        self.ready = False
        self.WIN_WIDTH = WIN_WIDTH
        self.WIN_HEIGHT = WIN_HEIGHT
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.moves_set = []

        for xi in range(-1, 2, 1):
            for yi in range(-1, 2, 1):
                for zi in range(-1, 2, 1):
                    self.cubies.append(Cubie3D((xi, yi, zi)))

    def rotate(self, angles):
        for c in self.cubies:
            c.rotateX(angles[0])
            c.rotateY(angles[1])
            c.rotateZ(angles[2])

    def turn(self, face_idx, callback=False):
        num = face_idx
        cubies_in = CUBIES_AXIS[face_idx][1:]
        turn_case = lambda x: x in CUBIES_AXIS[face_idx]
        cubies_in += cubies_in[0:2]
        arr_ex = [x for i, x in enumerate(self.turning) if i != num]
        if any(b for b in arr_ex) or (not callback) and self.turning[num]:
            self.turn_queue.append(lambda: self.turn(face_idx, callback))
            return False
        self.turning[num] = True;

        result = True
        cubies_resort = []
        rot_speed = 90.0 / float(ROT_SPEED)

        for i, c in enumerate(self.cubies):
            if not callback and i in cubies_in:
                cubies_resort.append(self.cubies[cubies_in[cubies_in.index(i) + 2]])
            else:
                cubies_resort.append(c)
            if turn_case(i):
                if num == 0:
                    c.turnX(-rot_speed)
                elif num == 1:
                    c.turnX(rot_speed)
                elif num == 2:
                    c.turnY(rot_speed)
                elif num == 3:
                    c.turnY(-rot_speed)
                elif num == 4:
                    c.turnZ(-rot_speed)
                elif num == 5:
                    c.turnZ(rot_speed)
                if not c.clipped():
                    result = False
        self.cubies = cubies_resort
        return result

    def show(self, screen):
        # if mid-turn
        for i in range(len(self.turning)):
            if self.turning[i] and self.turn(i, callback=True):
                self.turning[i] = False

        # if finished current turn
        if all(not b for b in self.turning):
            if len(self.turn_queue) > 0:
                self.turn_queue.pop(0)()

        # draw
        total_faces = []
        for cubie in self.cubies:
            total_faces += cubie.get_faces(self.WIN_WIDTH, self.WIN_HEIGHT)
        for tmp in sorted(total_faces, key=itemgetter(1), reverse=True):
            pygame.draw.polygon(screen, tmp[2], tmp[0], 0)
            pygame.draw.polygon(screen, (0, 0, 0), tmp[0], 3)

    def str_moves(self, s):
        sprd = s.split(' ')
        nsprd = []
        for move in sprd:
            if '2' in move:
                nsprd.append(move)
            if '\'' in move:
                nsprd.append(move)
                nsprd.append(move)
            nsprd.append(move)
        for move in nsprd:
            mv = move[0]
            if mv in MOVES:
                self.turn(MOVES.index(mv))
                self.moves_set.append(MOVES.index(mv))
            else:
                raise Exception('Unknown Move Type ' + move)

    def done_turning(self):
        return all(not i for i in self.turning)

    def get_scramble_str(self, length=20):
        result = []
        last = ''
        for rt in range(length):
            f = random.choice(MOVES)
            while f == last:
                # no two same consecutive moves
                f = random.choice(MOVES)
            last = f

            times = random.randint(1, 3)
            if times == 1:
                result.append(f)
            if times == 2:
                result.append(f + '2')
            if times == 3:
                result.append(f + '\'')
        return ' '.join(result)

    def run(self, moves_string=None, scramble_length=20):
        frame_num = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(1000)
            self.screen.fill((0, 0, 0))

            if frame_num == 0:
                self.rotate((-30, -30, 0))
                if moves_string == None:
                    scramble = self._scramble_str(scramble_length)
                    print("Scrambling ... " + scramble)
                    print()
                    self.str_moves(scramble)
                else:
                    self.str_moves(moves_string)

            self.show(self.screen)

            pygame.display.flip()
            frame_num += 1


if __name__ == '__main__':
    Cube3D().run("R U R' U R U' F")
