# Lesson: Diffuse Ambient Specular

Part of the **04-phong-lighting** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson implements Bui Tuong Phong's specular reflection model for **Diffuse Ambient Specular**. It computes view-dependent specular highlights using the reflection vector $\mathbf{R} = \text{reflect}(-\mathbf{L}, \mathbf{N})$, combined with ambient and diffuse lighting.

## 📂 File Structure

```
02-diffuse-ambient-specular/
├── Phong-Diffuse+Ambient+Specular-Lighting.py
├── Phong-Diffuse+Ambient+Specular-Lighting.vert
├── Phong-Diffuse+Ambient+Specular-Lighting.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Phong-Diffuse+Ambient+Specular-Lighting.vert`

```glsl
#version 150
/* 
   Specifies the GLSL language version used by this vertex shader.

   "#version 150" corresponds to GLSL 1.50,
   introduced with OpenGL 3.2.

   This version:
     - uses modern "in" and "out" qualifiers
     - removes deprecated fixed-function pipeline features
     - is compatible with Panda3D’s GLSL system
*/


in vec4 p3d_Vertex;
/*
   Declares a vertex position input attribute.

   "p3d_Vertex" is a built-in Panda3D attribute
   containing the vertex position in model-local space.

   Type: vec4
     x, y, z → spatial coordinates
     w       → usually 1.0 for positions
*/

in vec3 p3d_Normal;
/*
   Declares a vertex normal input attribute.

   "p3d_Normal":
     - represents the surface normal at the vertex
     - is used for lighting calculations

   Type: vec3 (x, y, z)
*/


out vec3 v_normal;
/*
   Declares an output variable to pass the normal to the fragment shader.

   "v_normal":
     - is interpolated across each triangle
     - allows per-fragment lighting calculations
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform 4×4 matrix for transforming vertices.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transform
     - View (camera) transform
     - Projection transform

   Converts model-space positions into clip-space coordinates.
*/

uniform mat3 p3d_NormalMatrix;
/*
   Declares a uniform 3×3 normal transformation matrix.

   "p3d_NormalMatrix":
     - transforms normals correctly under non-uniform scaling
     - is the inverse transpose of the model-view matrix
     - ensures accurate lighting results
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once per vertex.

   Responsibilities:
     - transform normals
     - compute final clip-space position
*/


    v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
    /*
       Transforms the vertex normal into eye space
       and normalizes it for consistent lighting calculations.

       Normalization ensures a unit-length vector,
       which is required for dot product lighting calculations.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Computes the final clip-space position.

       "gl_Position" is required by GLSL.
       The MVP matrix transforms model-space coordinates
       to clip space for rasterization.
    */
}


/*
   After the vertex shader completes:

     - normals are interpolated per fragment
     - vertices are assembled into triangles
     - rasterization produces fragments
     - the fragment shader runs per fragment
*/
```

## 🎨 Fragment Shader

File: `Phong-Diffuse+Ambient+Specular-Lighting.frag`

```glsl
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
     - compute ambient, diffuse, and specular lighting
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


    float ambient = 0.1;
    /*
       Defines a constant ambient light component.

       Ensures the object is never completely dark,
       even when not directly lit by the directional light.
       Simulates scattered or indirect lighting.
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


    float light =  diffuse + ambient + specular;
    /*
       Combines all lighting components into a single intensity value.

       Total illumination is the sum of:
         - diffuse (matte shading based on light angle)
         - ambient (base brightness in shadows)
         - specular (shiny mirror-like reflection)
    */


    light = clamp(light, 0.0, 1.0);
    /*
       Clamps the final light intensity.

       clamp(light, 0.0, 1.0):
         - ensures the total light value does not drop below 0.0
         - ensures the total light value does not exceed 1.0
         - prevents over-brightening when diffuse and specular stack
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
     - fragment lighting is calculated using diffuse, ambient, and specular
     - object appears with sharp specular highlights and shading
*/
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Phong-Diffuse+Ambient+Specular-Lighting.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
