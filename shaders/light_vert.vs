#version 330 core

layout (location = 0) in vec3 pos;
layout (location = 1) in vec2 texture_coords;

uniform mat4 model;
uniform mat4 proj;
uniform mat4 view;
out vec2 textures;

void main() {
    gl_Position = proj * view * model * vec4(pos, 1.0);
    textures = vec2(texture_coords.x, 1-texture_coords.y);
}