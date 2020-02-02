import moderngl
import numpy as np
import pygame

from raymarch.camera import Camera
from raymarch.shaders.shader_load_helper import read_shader_file
from raymarch.util.numpy import normalize

movement_speed = 2  # units per second
"""movement speed in units per second"""
sprint_multiplier = 1.5
"""if sprint key is held, movement speed is multiplied by this value"""


pygame.init()
pygame.display.set_mode((800, 800), pygame.DOUBLEBUF | pygame.OPENGL)
ctx = moderngl.create_context()

program = ctx.program(
    vertex_shader=read_shader_file('vertex_shader.vert'),
    fragment_shader=read_shader_file('fragment_shader.frag')
)
camera_rotation_mat_uniform = program['camera_rotation_mat']
camera_position_uniform = program['camera_position']
time_elapsed_uniform = program['time_elapsed']

vertices = np.dstack([
    [-1, -1, 1, 1],  # x
    [1, -1, 1, -1],  # y
    # [0, 0, 1, 1],  # u
    # [1, 0, 1, 0]  # v
])

vbo = ctx.buffer(vertices.astype('f4').tobytes())
vao = ctx.simple_vertex_array(program, vbo, 'in_vert')

camera = Camera()

focus_toggle_countdown = 0
"""countdown to when we can stop ignoring MOUSEMOTION events."""
focused = False

start_time = pygame.time.get_ticks()
prev_time = start_time
clock = pygame.time.Clock()
while True:
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000
    delta_time = (current_time - prev_time) / 1000
    prev_time = current_time
    time_elapsed_uniform.value = elapsed_time
    clock.tick()
    pygame.display.set_caption(f'{clock.get_fps()} fps')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if focused:
                    pygame.event.set_grab(False)
                    pygame.mouse.set_visible(True)
                    focused = False
                else:
                    pygame.event.set_grab(True)
                    pygame.mouse.set_visible(False)
                    focused = True
                focus_toggle_countdown = 2
        elif event.type == pygame.MOUSEMOTION:
            if focus_toggle_countdown > 0:
                # 2 event loops after we toggle focus, the mouse gets moved to the center of the screen.
                # This causes the camera to abruptly jump whenever we toggle focus, unless we ignore that event.
                focus_toggle_countdown -= 1
                continue
            if focused:
                camera.rotation_y -= event.rel[0] / 100
                camera.rotation_x -= event.rel[1] / 100
    # handle keyboard input
    keys = pygame.key.get_pressed()
    movement = np.array([
        keys[pygame.K_d] - keys[pygame.K_a],
        keys[pygame.K_q] - keys[pygame.K_e],
        keys[pygame.K_w] - keys[pygame.K_s]
    ], dtype=float)
    normalize(movement)
    movement *= delta_time * movement_speed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        movement *= movement_speed
    camera.move_by(movement)
    camera_rotation_mat_uniform.value = tuple(camera.calculate_rotation_matrix().flatten())
    camera_position_uniform.value = tuple(camera.location)
    # render
    vao.render(moderngl.TRIANGLE_STRIP)
    pygame.display.flip()
