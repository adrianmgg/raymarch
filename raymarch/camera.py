import math
import numpy as np


class Camera:
    # TODO move this class to a more relevant subpackage of raymarch
    def __init__(self, fov: float = 80):
        self.fov = fov
        self.rotation = np.array([0, 0, 0], dtype=float)
        self.location = np.array([0, 0, 0], dtype=float)

    def calculate_rotation_matrix(self):
        sx, sy, sz = np.sin(self.rotation)
        cx, cy, cz = np.cos(self.rotation)
        return np.array([
            (cy * cz, -cy * sz, sy),
            (cx * sz + sx * sy * cz, cx * cz - sx * sy * sz, -sx * cy),
            (sx * sz - cx * sy * cz, sx * cz - cx * sy * sz, cx * cy)
        ])

    def move_by(self, movement_vector):
        self.location += np.dot(movement_vector, self.calculate_rotation_matrix())

    # region location getters/setters
    @property
    def x(self):
        return self.location[0]

    @x.setter
    def x(self, x):
        self.location[0] = x

    @property
    def y(self):
        return self.location[1]

    @y.setter
    def y(self, y):
        self.location[1] = y

    @property
    def z(self):
        return self.location[2]

    @z.setter
    def z(self, z):
        self.location[2] = z

    # endregion

    # region rotation getters/setters
    @property
    def rotation_x(self):
        return self.rotation[0]

    @rotation_x.setter
    def rotation_x(self, n):
        self.rotation[0] = np.clip(n, a_min=-math.pi / 2, a_max=math.pi / 2)

    @property
    def rotation_y(self):
        return self.rotation[1]

    @rotation_y.setter
    def rotation_y(self, n):
        self.rotation[1] = math.fmod(n, math.tau)

    @property
    def rotation_z(self):
        return self.rotation[2]

    @rotation_z.setter
    def rotation_z(self, n):
        self.rotation[2] = math.fmod(n, math.tau)
    # endregion
