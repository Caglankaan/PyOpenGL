#version 330 core

in vec2 textures;
out vec4 outColor;

uniform vec3 color;
uniform sampler2D tex_sampler;

void main() {
    //outColor = texture(tex_sampler, textures);
    outColor = vec4(color, 1.0);
}