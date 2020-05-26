#version 330

out vec4 frag_color;

//in vec2 textures;
in vec3 out_normal;
in vec3 frag_pos;

uniform vec3 view_pos;
uniform vec3 light_color;
uniform vec3 obj_color;
uniform bool blinn;

struct LightSource
{
    vec3 light_pos;
    bool light_on;
};

out vec4 color;

//uniform sampler2D tex_sampler;
//uniform sampler2D tex_sampler2;
uniform float tex_alpha;
uniform LightSource light_source[2];


vec3 calcLightSource(LightSource light_source, vec3 my_color, vec3 normal, vec3 frag_pos, vec3 view_pos, bool blinn)
{
    if(light_source.light_on)
    {
        vec3 ambient = 0.2 * my_color;


        vec3 norm = normalize(normal);
        vec3 light_dir = normalize(light_source.light_pos - frag_pos);

        float diff = max(dot(norm, light_dir),0.0);
        vec3 diffuse = diff * my_color;

        vec3 view = normalize(view_pos - frag_pos);

        float spec = 0.0;

        if(blinn)
        {
            vec3 halfwayDir = normalize(light_dir + view);
            spec = pow(max(dot(norm, halfwayDir),0.0),32.0);
        }
        else
        {
            //vec3 reflect_dir = reflect(-light_dir, norm);
            //spec = pow(max(dot(view, reflect_dir),0.0),8.0);
            spec = 0.0;
        }
        
        vec3 specular = vec3(0.3) * spec;

        return (ambient + diffuse + specular);
    }
    else
    {
        return vec3(0.0,0.0,0.0);
    }
}

void main()
{
    //vec3 my_color = texture(tex_sampler, textures).rgb;

    vec3 my_color = vec3(0.3, 0.5, 0.2);
    vec3 result = vec3(0.0,0.0,0.0);
    for(int i = 0; i < 2; i++)
        result += calcLightSource(light_source[i], my_color, out_normal, frag_pos, view_pos, blinn);

    color = vec4(result, 1.0); //* mix(texture(tex_sampler, textures), texture(tex_sampler2, textures), tex_alpha);

}