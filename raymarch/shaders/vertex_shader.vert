#version 330

in vec2 in_vert;
//in vec2 in_uv;

out vec2 screenspace;

void main() {
	screenspace = in_vert;
	gl_Position = vec4(in_vert, 0.0, 1.0);
}
