# Lesson: Diffuse Ambient

Part of the **03-lambert-lighting** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates Johann Heinrich Lambert's cosine law for **Diffuse Ambient**. It evaluates surface reflectance based on the angle between the normal vector $\mathbf{N}$ and the light direction vector $\mathbf{L}$, rendering a realistic matte shading response on `models/teapot`.

## 📂 File Structure

```
02-diffuse-ambient/
├── Lambert-Diffuse+Ambient-Lighting.py
├── Lambert-Diffuse+Ambient-Lighting.vert
├── Lambert-Diffuse+Ambient-Lighting.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Lambert-Diffuse+Ambient-Lighting.vert`

```glsl
#version 150
/* 
   Specifies the GLSL language version used by this vertex shader.

   "#version 150" corresponds to GLSL 1.50,
   introduced with OpenGL 3.2.

   This version:
     - uses modern "in" and "out" qualifiers
     - removes deprecated fixed-function features
     - is compatible with Panda3D’s GLSL system
*/


in vec4 p3d_Vertex;
/*
   Declares a vertex position input attribute.

   "p3d_Vertex":
     - built-in Panda3D attribute
     - contains the vertex position in model-local space

   Type: vec4
     x, y, z → spatial coordinates
     w       → usually 1.0 for positions
*/


in vec3 p3d_Normal;
/*
   Declares a vertex normal input attribute.

   "p3d_Normal":
     - represents the surface normal at each vertex
     - used for lighting calculations

   Type: vec3 (x, y, z)
*/


out vec3 v_normal;
/*
   Declares an output variable to pass the normal to the fragment shader.

   "v_normal":
     - is interpolated across triangles
     - allows per-fragment lighting calculations
*/


uniform mat3 p3d_NormalMatrix;
/*
   Declares a 3×3 uniform normal transformation matrix.

   "p3d_NormalMatrix":
     - transforms normals correctly under non-uniform scaling
     - typically the inverse transpose of the model-view matrix
     - ensures lighting calculations remain accurate
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a 4×4 uniform matrix for transforming vertices.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transformation
     - View (camera) transformation
     - Projection transformation

   Converts model-space positions into clip-space coordinates.
*/


void main() {
/*
   Entry point of the vertex shader.

   Responsibilities:
     - transform vertex normals
     - compute final clip-space position
*/


    v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
    /*
       Transforms the normal into eye space and normalizes it.

       Normalization ensures a unit-length vector,
       which is required for correct dot-product lighting calculations.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Computes the final vertex position in clip space.

       "gl_Position" is required by GLSL.
       The MVP matrix transforms model-space coordinates to clip space.
    */
}


/*
   After the vertex shader completes:

     - normals are interpolated across fragments
     - vertices are assembled into triangles
     - triangles are rasterized
     - the fragment shader runs per fragment
*/
```

## 🎨 Fragment Shader

File: `Lambert-Diffuse+Ambient-Lighting.frag`

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
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Lambert-Diffuse+Ambient-Lighting.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
