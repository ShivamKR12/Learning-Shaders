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
     - compute ambient, diffuse, and BLINN-PHONG specular lighting
     - combine lighting components
     - output the final fragment color
*/


    vec3 N = normalize(v_normal);
    /*
       Normalizes the interpolated surface normal.

       Interpolation across the triangle can alter vector length.
       normalize(...) ensures unit length (length = 1) for accurate
       lighting calculations.
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
    */


    float diffuse = max(dot(N, L), 0.0);
    /*
       Computes the diffuse lighting term (Lambertian shading).

       dot(N, L):
         - computes the cosine of the angle between surface normal and light
       max(..., 0.0):
         - prevents light from affecting back-facing surfaces
    */


    float ambient = 0.1;
    /*
       Defines a constant ambient light component.
       Ensures the object is never completely dark in shadows.
    */


    /*
       =========================================================
       BLINN-PHONG SPECULAR CALCULATION
       =========================================================
       Instead of calculating the reflection vector (R) like in
       standard Phong, Blinn-Phong calculates the "Halfway Vector" (H).
    */
    vec3 H = normalize(L + V);
    /*
       The Halfway Vector:
       - is the vector exactly halfway between the Light (L) and View (V)
       - avoids the expensive reflect() function
       - creates a specular highlight that is physically more accurate, 
         especially at steep grazing angles where standard Phong fails.
    */


    float shininess = 32.0;
    /*
       Defines the material's shininess exponent.

       IMPORTANT: Because the angle between N and H is smaller than the
       angle between R and V, Blinn-Phong highlights appear much larger.
       To match the visual size of a standard Phong highlight, you typically 
       multiply the shininess by 2 to 4.
    */
    
    
    float specular = pow(max(dot(N, H), 0.0), shininess * 4.0);
    /*
       Computes the Specular highlight term.

       dot(N, H):
         - measures the alignment between the surface normal (N)
           and the halfway vector (H)
         - if the normal aligns perfectly with the halfway vector,
           the camera is looking perfectly into the reflection.

       pow(..., shininess * 4.0):
         - sharply focuses the light to create a bright, localized spot.
    */


    float light = diffuse + ambient + specular;
    /*
       Combines all lighting components into a single intensity value.

       Total illumination is the sum of:
         - diffuse (matte shading)
         - ambient (base brightness)
         - specular (shiny reflection)
    */


    light = clamp(light, 0.0, 1.0);
    /*
       Clamps the final light intensity.

       clamp(light, 0.0, 1.0):
         - ensures the total light value does not drop below 0.0
         - ensures the total light value does not exceed 1.0
    */


    fragColor = vec4(light, light, light, 1.0);
    /*
       Sets the final pixel color as a grayscale material (white object).
    */
}


/*
   End of the fragment shader.

   Combined effect:
     - The model has smooth diffuse lighting and ambient shadow
     - The specular highlights use the Blinn-Phong halfway vector,
       yielding more accurate grazing reflections and saving computation.
*/