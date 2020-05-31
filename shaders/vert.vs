#version 330
in layout(location = 0) vec3 position;
in layout(location = 1) vec2 texture_cords;
in layout(location = 2) vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec3 frag_pos;
out vec3 out_normal;
out vec2 textures;
out vec4 FragPosLightSpace;

uniform vec3 color;

void main()
{
    gl_Position =  proj * view * model * vec4(position, 1.0f);

    frag_pos = vec3(model * vec4(position, 1.0));
    out_normal = mat3(transpose(inverse(model))) * normal;
    textures = vec2(texture_cords.x, 1-texture_cords.y);
}