# Lesson: Diffuse Ambient Texture

Part of the **03-lambert-lighting** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates Johann Heinrich Lambert's cosine law for **Diffuse Ambient Texture**. It evaluates surface reflectance based on the angle between the normal vector $\mathbf{N}$ and the light direction vector $\mathbf{L}$, rendering a realistic matte shading response on `models/panda-model`.

## 📂 File Structure

```
04-diffuse-ambient-texture/
├── Lambert-Diffuse+Ambient+Texture-Lighting.py
├── Lambert-Diffuse+Ambient+Texture-Lighting.vert
├── Lambert-Diffuse+Ambient+Texture-Lighting.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Lambert-Diffuse+Ambient+Texture-Lighting.vert`

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

   "p3d_Normal" is a built-in Panda3D attribute
   representing the surface normal at each vertex.

   A normal:
     - is a direction vector perpendicular to the surface
     - is commonly used for lighting calculations

   Type: vec3 (x, y, z)
*/


in vec2 p3d_MultiTexCoord0;
/*
   Declares a vertex texture coordinate input attribute.

   "p3d_MultiTexCoord0" is a built-in Panda3D attribute
   containing the first set of UV coordinates.

   Type: vec2 (u, v):
     u → horizontal texture coordinate
     v → vertical texture coordinate
*/


out vec3 v_normal;
/*
   Declares an output variable for the fragment shader.

   "v_normal":
     - carries the transformed vertex normal
     - is interpolated across the surface of triangles
     - used in the fragment shader for lighting calculations
*/


out vec2 v_uv;
/*
   Declares an output variable for the fragment shader.

   "v_uv":
     - carries the vertex UV coordinates
     - interpolated automatically across the surface
     - allows the fragment shader to sample textures accurately
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform transformation matrix.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transformation
     - View (camera) transformation
     - Projection (perspective) transformation

   Converts model-space positions into clip-space coordinates.
*/


uniform mat3 p3d_NormalMatrix;
/*
   Declares a uniform normal transformation matrix.

   "p3d_NormalMatrix":
     - transforms normals correctly under non-uniform scaling
     - is the 3x3 inverse transpose of the model-view matrix
     - ensures lighting calculations remain correct
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once per vertex.
   Responsibilities:
     - transform normals
     - pass UV coordinates
     - compute final clip-space position
*/


    v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
    /*
       Transforms the normal into eye-space and normalizes it.

       normalize(...):
         - ensures unit length for accurate lighting calculations
    */


    v_uv = p3d_MultiTexCoord0;
    /*
       Passes texture coordinates to the fragment shader.

       Each fragment receives interpolated UVs for accurate sampling.
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

     - normals are interpolated per fragment
     - UVs are interpolated per fragment
     - triangles are rasterized
     - the fragment shader runs per pixel
*/
```

## 🎨 Fragment Shader

File: `Lambert-Diffuse+Ambient+Texture-Lighting.frag`

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
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Lambert-Diffuse+Ambient+Texture-Lighting.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
