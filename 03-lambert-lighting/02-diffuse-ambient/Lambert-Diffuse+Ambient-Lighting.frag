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
     - is normalized per fragment
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

   Responsibilities:
     - compute simple directional lighting
     - output a grayscale color based on lighting
*/


    vec3 N = normalize(v_normal);
    /*
       Normalizes the interpolated normal.

       Interpolation can slightly alter vector length,
       so normalization ensures accurate lighting calculation.
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
       Computes Lambertian diffuse lighting.

       dot(N, L):
         - measures alignment of surface normal and light direction
         - ranges from -1.0 to +1.0

       max(..., 0.0):
         - ensures no negative light
         - surfaces facing away from light are dark
    */


    float ambient = 0.1;
    /*
       Defines a low ambient light component.

       Ensures surfaces are never completely dark
       even when facing away from the directional light.
    */


    float light = ambient + diffuse;
    /*
       Combines diffuse and ambient light to compute total illumination.
    */


    light = clamp(light, 0.0, 1.0);
    /*
       Clamps the light intensity to [0,1] range
       to avoid over-brightening.
    */


    fragColor = vec4(light, light, light, 1.0);
    /*
       Sets the fragment color as grayscale based on total light.

       R = G = B = light
       A = 1.0 (fully opaque)

       This produces a shaded grayscale object
       lit by a directional light with ambient contribution.
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - vertex normals are transformed and interpolated
     - fragment lighting is calculated using diffuse + ambient
     - object appears shaded in grayscale
     - surfaces facing the light are brighter, others darker
*/
