# Lesson: Diffuse

Part of the **03-lambert-lighting** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates Johann Heinrich Lambert's cosine law for **Diffuse**. It evaluates surface reflectance based on the angle between the normal vector $\mathbf{N}$ and the light direction vector $\mathbf{L}$, rendering a realistic matte shading response on `models/teapot`.

## 📂 File Structure

```
01-diffuse/
├── Lambert-Diffuse-Lighting.py
├── Lambert-Diffuse-Lighting.vert
├── Lambert-Diffuse-Lighting.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Lambert-Diffuse-Lighting.vert`

```glsl
#version 150
/*
   Specifies the GLSL version.

   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2 core profile).

   This version:
     - uses "in" and "out" instead of the old "attribute" and "varying"
     - requires explicit outputs for later pipeline stages
     - is compatible with Panda3D’s modern shader system
*/


in vec4 p3d_Vertex;
/*
   Declares an input attribute to the vertex shader.

   "in" means:
     - this value is provided per-vertex by the application (Panda3D).

   "vec4" means:
     - (x, y, z, w) coordinates in object (model) space.

   "p3d_Vertex":
     - is a built-in Panda3D attribute
     - represents the position of the vertex before any transforms
*/


in vec3 p3d_Normal;
/*
   Declares another per-vertex input attribute.

   "vec3" because normals are 3D direction vectors (x, y, z).

   "p3d_Normal":
     - is provided automatically by Panda3D
     - represents the surface normal in object (model) space
     - used for lighting calculations
*/


out vec3 v_normal;
/*
   Declares an output variable from the vertex shader.

   "out" means:
     - this value will be passed to the next pipeline stage
       (typically the fragment shader).

   "v_normal":
     - is a user-defined name
     - will be interpolated across the triangle
     - each fragment will receive a smoothly interpolated normal
*/


uniform mat3 p3d_NormalMatrix;
/*
   Declares a uniform matrix.

   "uniform" means:
     - this value is constant for all vertices in a draw call
     - it is set by Panda3D, not computed in the shader.

   "mat3":
     - a 3×3 matrix used for transforming direction vectors.

   "p3d_NormalMatrix":
     - is provided automatically by Panda3D
     - typically equals the inverse transpose of the model-view matrix
     - ensures normals remain correct under scaling and rotation
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares another uniform matrix.

   "mat4":
     - a 4×4 matrix used for transforming positions.

   "p3d_ModelViewProjectionMatrix":
     - combines:
         * Model matrix (object → world space)
         * View matrix  (world → camera space)
         * Projection matrix (camera → clip space)
     - provided automatically by Panda3D
*/


void main() {
/*
   Required entry point for the vertex shader.

   This function runs once per vertex.

   The main responsibilities of a vertex shader are:
     - transform vertex positions into clip space
     - compute values (like normals, texture coordinates, etc.)
       that will be passed to the fragment shader
*/


    v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
    /*
       Transforms and normalizes the surface normal.

       Steps:
         1) p3d_NormalMatrix * p3d_Normal
            - transforms the normal from object space
              into view (camera) space.

         2) normalize(...)
            - ensures the vector has unit length (length = 1)
            - required for correct lighting calculations

       The resulting normal is stored in "v_normal" and sent
       to the fragment shader, where it will be interpolated
       per pixel.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Computes the final clip-space position of the vertex.

       "gl_Position":
         - is a built-in GLSL output required by the pipeline
         - determines where the vertex appears on screen.

       The multiplication applies:
         Object Space → World Space → View Space → Clip Space

       Without assigning gl_Position, the vertex would not
       appear on screen.
    */
}
/*
   End of the main() function and end of the vertex shader.
*/
```

## 🎨 Fragment Shader

File: `Lambert-Diffuse-Lighting.frag`

```glsl
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
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Lambert-Diffuse-Lighting.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
