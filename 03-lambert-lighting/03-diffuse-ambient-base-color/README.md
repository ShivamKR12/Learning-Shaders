# Lesson: Diffuse Ambient Base Color

Part of the **03-lambert-lighting** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates Johann Heinrich Lambert's cosine law for **Diffuse Ambient Base Color**. It evaluates surface reflectance based on the angle between the normal vector $\mathbf{N}$ and the light direction vector $\mathbf{L}$, rendering a realistic matte shading response on `models/teapot`.

## 📂 File Structure

```
03-diffuse-ambient-base-color/
├── Lambert-Diffuse+Ambient+BaseColor-Lighting.py
├── Lambert-Diffuse+Ambient+BaseColor-Lighting.vert
├── Lambert-Diffuse+Ambient+BaseColor-Lighting.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Lambert-Diffuse+Ambient+BaseColor-Lighting.vert`

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


uniform mat3 p3d_NormalMatrix;
/*
   Declares a uniform 3×3 normal transformation matrix.

   "p3d_NormalMatrix":
     - transforms normals correctly under non-uniform scaling
     - is the inverse transpose of the model-view matrix
     - ensures accurate lighting results
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

File: `Lambert-Diffuse+Ambient+BaseColor-Lighting.frag`

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
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Lambert-Diffuse+Ambient+BaseColor-Lighting.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
