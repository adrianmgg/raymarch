import os
import re

_shaders_dir = os.path.dirname(os.path.realpath(__file__))

# from opengl language specification:
# "Each number sign (#) can be preceded in its line only by spaces or horizontal tabs.
# It may also be followed by spaces and horizontal tabs, preceding the directive.
# Each directive is terminated by a new-line."
_include_pragma_regex = re.compile(r'^[ \t]*#[ \t]*pragma[ \t]+include[ \t]+"(?P<include_path>.*?)"', flags=re.MULTILINE)


# TODO insert #line directives before/after includes? (specifically "#line line source-string-number")

def read_shader_file(shader_file_name):
    shader_file_path = os.path.join(_shaders_dir, shader_file_name)
    shader_text = ''
    with open(shader_file_path, 'r') as shader_file:
        for line in shader_file.readlines():
            include_match = _include_pragma_regex.match(line)
            if include_match:
                include_path = include_match.group('include_path')
                shader_text += '\n'
                shader_text += read_shader_file(include_path)
                shader_text += '\n'
            else:
                shader_text += line
    return shader_text
