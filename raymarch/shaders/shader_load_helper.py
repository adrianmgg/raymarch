import os


shaders_dir = os.path.dirname(os.path.realpath(__file__))


def read_shader_file(shader_file_name):
    shader_file_path = os.path.join(shaders_dir, shader_file_name)
    with open(shader_file_path, 'r') as shader_file:
        return shader_file.read()



