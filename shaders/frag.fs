#version 330

out vec4 frag_color;

//in vec2 textures;
in vec3 out_normal;
in vec3 frag_pos;

uniform vec3 view_pos;
uniform vec3 light_color;
uniform vec3 obj_color;
uniform bool blinn;
uniform bool open_shadows;

struct LightSource
{
    vec3 light_pos;
    bool light_on;
};

out vec4 color;

//uniform sampler2D tex_sampler;
//uniform sampler2D tex_sampler2;
uniform float far_plane;
uniform float tex_alpha;
uniform LightSource light_source[2];

float ShadowCalculation(vec3 fragPos, vec3 my_color, LightSource light_source)
{
    if(open_shadows)
    {
        vec3 fragToLight = fragPos - light_source.light_pos;

        float closestDepth = my_color.r;

        closestDepth *= far_plane;

        float currentDepth = length(fragToLight);
        float bias = 20;
        float shadow = currentDepth - bias > closestDepth ? 1.0 : 0.0;
        
        return shadow;
    }
    else
    {
        return 0.0;
    }
    
}




vec3 calcLightSource(LightSource light_source, vec3 my_color, vec3 normal, vec3 frag_pos, vec3 view_pos, bool blinn)
{
    if(light_source.light_on)
    {
        vec3 ambient = 0.3 * my_color;

        vec3 lightColor = vec3(0.3);

        vec3 norm = normalize(normal);
        vec3 light_dir = normalize(light_source.light_pos - frag_pos);

        float diff = max(dot(norm, light_dir),0.0);
        vec3 diffuse = diff * lightColor;

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
        
        float shadow = ShadowCalculation(frag_pos, my_color, light_source);
        
        vec3 specular = lightColor * spec;

        //return (ambient + diffuse + specular);
        return (ambient + (1.0 - shadow) * (diffuse + specular)) * my_color;
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