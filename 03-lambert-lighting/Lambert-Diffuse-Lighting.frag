#version 150
/*
   Specifies the GLSL version.

   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2 core).

   This version:
     - uses modern "in" and "out" qualifiers
     - does not allow deprecated variables like gl_FragColor
     - works cleanly with Panda3D’s shader pipeline
*/


in vec3 v_normal;
/*
   Declares an input variable to the fragment shader.

   "in" means:
     - this value comes from the previous pipeline stage
       (the vertex shader).

   "v_normal":
     - must exactly match the name and type of an "out"
       variable in the vertex shader
     - is automatically interpolated across the triangle
     - each fragment receives a smoothly interpolated normal

   The normal is typically already in view space
   (depending on how the vertex shader transformed it).
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "out" means:
     - this variable will be written to the framebuffer
       (usually the screen).

   "vec4":
     - represents RGBA color (red, green, blue, alpha).

   "fragColor":
     - is a user-defined name
     - replaces the deprecated "gl_FragColor"
*/


uniform vec3 light_direction;

uniform mat4 p3d_ViewMatrix;
/*
   Converts World Space coordinates into View Space.
*/


void main() {
/*
   Required entry point for the fragment shader.

   This function runs once per fragment (pixel-sized sample).

   The purpose of a fragment shader is to compute the final
   color (and possibly depth or other outputs) of each pixel.
*/


    vec3 N = normalize(v_normal);
    /*
       Normalizes the surface normal.

       Why this is necessary:
         - normals passed from the vertex shader are interpolated
           across the triangle
         - interpolation can change their length

       normalize(...) ensures:
         - the normal has unit length (length = 1)
         - lighting calculations using dot products are correct

       "N" now represents the final per-fragment surface normal.
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
       Computes the diffuse lighting term (Lambertian shading).

       dot(N, L):
         - computes the cosine of the angle between
           the surface normal (N) and light direction (L)
         - values range from -1.0 to 1.0

       max(..., 0.0):
         - clamps negative values to zero
         - prevents light from affecting back-facing surfaces

       "diffuse":
         - represents how strongly the surface is lit
         - 0.0 = fully dark
         - 1.0 = fully lit
    */


    fragColor = vec4(diffuse, diffuse, diffuse, 1.0);
    /*
       Writes the final fragment color.

       The diffuse value is used for:
         - red channel
         - green channel
         - blue channel

       This produces:
         - grayscale shading
         - brighter where the surface faces the light
         - darker where it faces away

       Alpha is set to 1.0:
         - fully opaque
    */
}
/*
   End of the main() function and end of the fragment shader.
*/
