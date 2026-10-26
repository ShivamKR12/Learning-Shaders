#version 150
/* 
   Specifies the GLSL version used by this fragment shader.

   GLSL 1.50:
     - requires explicit fragment outputs
     - disallows deprecated gl_FragColor
     - must match the vertex shader version
*/


in vec3 v_normal;
/*
   Declares the interpolated normal from the vertex shader.

   "v_normal":
     - is normalized in the fragment shader
     - used to calculate diffuse lighting
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "fragColor":
     - represents the final RGBA color
     - is written to the framebuffer
*/


uniform vec3 light_direction;

uniform mat4 p3d_ViewMatrix;
/*
   Converts World Space coordinates into View Space.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function runs once per fragment.
   Responsibilities:
     - compute lighting
     - apply shading to a base color
     - output the final fragment color
*/


    vec3 N = normalize(v_normal);
    /*
       Normalizes the interpolated normal.

       Interpolation can slightly change the length,
       so normalization ensures correct diffuse calculation.
    */


    vec3 L = normalize((p3d_ViewMatrix * vec4(light_direction, 0.0)).xyz);
    /*
       Transforms the World Space light direction into View Space.
       
       Since the surface normal (N) is in View Space, the light direction (L)
       must also be in View Space. We multiply by p3d_ViewMatrix.
       (w = 0.0 because it's a directional vector, not a point).
    */


    float diffuse = max(dot(N, L), 0.0);
    /*
       Computes the Lambertian diffuse term.

       dot(N, L):
         - measures alignment between the surface normal and light
         - ranges from -1.0 to 1.0

       max(..., 0.0):
         - ensures no negative light
         - surfaces facing away from the light are dark
    */


    float ambient = 0.7;
    /*
       Defines ambient lighting.

       Ensures surfaces are never completely dark
       even if the light doesn’t hit them directly.
    */


    float light = diffuse + ambient;
    /*
       Combines diffuse and ambient light to compute total illumination.
    */


    light = clamp(light, 0.0, 1.0);
    /*
       Clamps light intensity to the range [0, 1].

       Prevents over-brightening of the base color.
    */


    vec3 baseColor = vec3(1.0, 0.4, 0.2);
    /*
       Defines the base color of the object.

       Here it is a warm orange:
         R = 1.0
         G = 0.4
         B = 0.2
    */


    fragColor = vec4(baseColor * light, 1.0);
    /*
       Computes the final fragment color.

       baseColor * light:
         - modulates the color according to lighting

       Alpha is set to 1.0 (fully opaque)
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - normals are transformed and passed per fragment
     - directional diffuse lighting plus ambient is applied
     - the object appears shaded with a warm orange color
     - surfaces facing the light are brighter, others darker
*/
