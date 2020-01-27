import moderngl
import numpy as np
import pygame

from raymarch.camera import Camera
from raymarch.shaders.shader_load_helper import read_shader_file

movement_speed = 1.25  # units per second
sprint_multiplier = 1.5


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

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

start_time = pygame.time.get_ticks()
prev_time = start_time
while True:
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000
    delta_time = (current_time - prev_time) / 1000
    prev_time = current_time
    time_elapsed_uniform.value = elapsed_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            pass
            # if event.key == pygame.K_ESCAPE:
            #     if focused:
            #         pygame.event.set_grab(False)
            #         pygame.mouse.set_visible(True)
            #         focused = False
            #     else:
            #         pygame.event.set_grab(True)
            #         pygame.mouse.set_visible(False)
            #         focused = True
        elif event.type == pygame.MOUSEMOTION:
            camera.rotation_y -= event.rel[0] / 100
            camera.rotation_x -= event.rel[1] / 100
    # handle keyboard input
    keys = pygame.key.get_pressed()
    movement_x = keys[pygame.K_d] - keys[pygame.K_a]
    movement_y = keys[pygame.K_q] - keys[pygame.K_e]
    movement_z = keys[pygame.K_w] - keys[pygame.K_s]
    sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    movement_delta = delta_time * movement_speed * (1 + sprinting * sprint_multiplier)
    camera.x += movement_x * movement_delta
    camera.y += movement_y * movement_delta
    camera.z += movement_z * movement_delta
    # movement = np.multiply((movement_x, movement_y, movement_z), delta_time * movement_speed * (1 + sprinting * sprint_multiplier))
    # camera_pos_uniform.value = tuple(np.add(movement, camera_pos_uniform.value))
    camera_rotation_mat_uniform.value = tuple(camera.calculate_rotation_matrix().flatten())
    camera_position_uniform.value = tuple(camera.location)
    # render
    vao.render(moderngl.TRIANGLE_STRIP)
    pygame.display.flip()
    # pygame.time.delay(1)
