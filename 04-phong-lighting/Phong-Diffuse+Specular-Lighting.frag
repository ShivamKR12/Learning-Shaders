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
     - used to calculate lighting equations
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "fragColor":
     - represents the final RGBA color
     - is written to the framebuffer
*/


uniform vec3 light_direction;
/*
   Declares a uniform for the directional light.

   "light_direction":
     - passed from the Python application
     - represents the direction the light is pointing
*/


uniform mat4 p3d_ViewMatrix;
/*
   Converts World Space coordinates into View Space.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function runs once per fragment.
   Responsibilities:
     - compute diffuse and specular lighting
     - combine lighting components
     - output the final fragment color
*/


    vec3 N = normalize(v_normal);
    /*
       Normalizes the interpolated surface normal.

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


    vec3 V = vec3(0.0, 0.0, 1.0);
    /*
       Defines the View (Camera) vector.

       "vec3(0.0, 0.0, 1.0)":
         - points directly out of the screen toward the camera
         - assumes a simplified "infinite viewer" or directional camera
         - avoids passing true camera coordinates for simplicity

       "V" represents the direction from the fragment being shaded
       to the viewer's eye, essential for calculating specular reflections.
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


    vec3 R = reflect(-L, N);
    /*
       Computes the reflection vector.

       reflect(-L, N):
         - calculates the direction that light bounces off the surface
         - "-L" reverses the light vector so it points FROM the light TO the surface
         - "N" is the surface normal

       "R" represents the perfect mirror reflection direction.
       It is the core vector used to calculate specular highlights.
    */


    float shininess = 32.0;
    /*
       Defines the material's shininess exponent.

       "shininess":
         - controls the concentration and sharpness of the specular highlight
         - higher values (e.g., 64.0, 128.0) produce smaller, sharper highlights
         - lower values (e.g., 8.0, 16.0) produce larger, softer highlights
    */


    float specular = pow(max(dot(R, V), 0.0), shininess);
    /*
       Computes the Specular (Phong) highlight term.

       dot(R, V):
         - measures the alignment between the reflected light (R)
           and the view direction (V)
         - max(..., 0.0) ensures we don't get negative specular light
           if the reflection points away from the camera

       pow(..., shininess):
         - raises the dot product to the power of the shininess exponent
         - sharply focuses the light to create a bright, localized spot
         - simulates a glossy or shiny surface finish
    */


    float light =  diffuse  + specular;
    /*
       Combines the lighting components into a single intensity value.

       Total illumination is the sum of:
         - diffuse (matte shading based on light angle)
         - specular (shiny mirror-like reflection)

       Without ambient light, parts in shadow will be completely black.
    */


    fragColor = vec4(light, light, light, 1.0);
    /*
       Sets the final pixel color.

       vec4(light, light, light, 1.0):
         - The light intensity is mapped equally to R, G, and B
         - This creates a grayscale material (white object)
         - Alpha is set to 1.0 for a fully opaque object
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - vertex normals are transformed and interpolated
     - fragment lighting is calculated using diffuse and specular
     - object appears with sharp specular highlights and shading
*/