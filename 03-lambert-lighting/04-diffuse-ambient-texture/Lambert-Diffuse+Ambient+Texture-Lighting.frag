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
     - used for lighting calculations
*/


in vec2 v_uv;
/*
   Declares the interpolated UV coordinates from the vertex shader.

   "v_uv":
     - allows sampling the texture correctly for this fragment
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "fragColor":
     - represents the final RGBA color
     - is written to the framebuffer
*/


uniform sampler2D tex;
/*
   Declares a 2D texture sampler.

   "tex":
     - allows lookup of color values using UV coordinates
     - Panda3D binds the actual texture object at draw time
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
     - compute simple directional lighting
     - sample the texture
     - apply lighting to the texture color
*/


    vec3 N = normalize(v_normal);
    /*
       Normalizes the interpolated normal.

       Interpolation can slightly distort vector length,
       so normalization ensures correct lighting.
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
       Computes the Lambertian (diffuse) term.

       dot(N, L):
         - measures alignment of surface normal and light direction
         - ranges from -1.0 to 1.0

       max(..., 0.0):
         - ensures no negative light
         - surfaces facing away from the light are dark
    */


    float ambient = 0.2;
    /*
       Defines a constant ambient light component.

       Ensures the object is never completely dark,
       even when not directly lit by the directional light.
    */


    float light = clamp(diffuse + ambient, 0.0, 1.0);
    /*
       Combines diffuse and ambient light.

       clamp(..., 0.0, 1.0):
         - ensures the final light intensity remains in [0, 1]
    */


    vec4 texColor = texture(tex, v_uv);
    /*
       Samples the texture using the interpolated UV coordinates.

       Returns a vec4:
         RGB → texture color
         A   → texture alpha
    */


    fragColor = vec4(texColor.rgb * light, texColor.a);
    /*
       Applies lighting to the texture color.

       texColor.rgb * light:
         - modulates the texture color based on lighting
         - creates shading consistent with the light direction

       texColor.a:
         - preserves the original alpha from the texture
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - vertex normals are transformed and interpolated
     - UVs are interpolated for texture sampling
     - directional diffuse lighting plus ambient is applied
     - the texture color is modulated by the lighting
     - produces a textured object with basic shading
*/
