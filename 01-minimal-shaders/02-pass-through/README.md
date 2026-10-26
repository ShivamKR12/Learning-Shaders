# Lesson: Pass Through

Part of the **01-minimal-shaders** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson isolates and demonstrates **Pass Through**. It illustrates foundational programmable GPU pipeline mechanics in Panda3D using GLSL, applying custom shaders directly onto the `models/teapot` model.

## 📂 File Structure

```
02-pass-through/
├── Minimal-PassThrough-Shader.py
├── Minimal-PassThrough-Shader.vert
├── Minimal-PassThrough-Shader.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-PassThrough-Shader.vert`

```glsl
#version 150
/*  
   Specifies the GLSL version used by this shader.
   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2 era).
   This version uses modern syntax:
       • "in" for vertex inputs
       • "out" for varyings
       • no deprecated keywords like "attribute" or "varying"
*/


in vec4 p3d_Vertex;
/*
   "in" declares a per-vertex input attribute.
   Panda3D automatically provides "p3d_Vertex" for models.

   It contains the vertex position in *model space*:
       (x, y, z, w)
   The 'w' component is normally 1.0 for position vectors.
*/


in vec3 p3d_Normal;
/*
   Another per-vertex input attribute supplied by Panda3D.

   "p3d_Normal" is the surface normal at each vertex.
   It is a direction vector:
       (x, y, z)
   Normals are used in lighting calculations ,
   but here we are passing them to the fragment shader.
*/


out vec3 v_normal;
/*
   "out" declares a varying—data that will be sent from the
   vertex shader to the fragment shader.

   The GPU will:
      • output one v_normal for each vertex
      • interpolate it across the triangle’s surface
      • provide the interpolated value to the fragment shader via `in vec3 v_normal`

   This is the core mechanism for communication between
   vertex → fragment shaders.
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   A "uniform" is a constant value shared by all vertices during one draw call.

   Panda3D automatically supplies this matrix. It combines:
       Model      – transforms the model into world space
       View       – positions world relative to the camera
       Projection – applies perspective transformation

   Together this matrix converts model-space positions into clip space,
   which is required for rendering.
*/


void main() {
/*
   The entry point of the vertex shader.
   This function runs once for every vertex in the model.
*/


    v_normal = normalize(p3d_Normal);
    /*
       Normalize the incoming normal vector.

       Even though most normals are already unit length,
       normalizing ensures correctness, especially if the model
       has scaling applied or the normals are not perfect.

       The resulting v_normal will be smoothly interpolated
       across the triangle in the fragment shader.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       gl_Position is a built-in output variable that all vertex shaders
       MUST write to.

       This multiplication performs the full transformation:
            model-space
               → world-space
               → view-space (camera)
               → clip-space (before perspective division)

       After this:
           • GPU does perspective division
           • the vertex is projected onto the screen
           • rasterization begins (creating fragments for the fragment shader)
    */
}
```

## 🎨 Fragment Shader

File: `Minimal-PassThrough-Shader.frag`

```glsl
#version 150
/*
   Specifies the GLSL language version.
   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2).

   This version:
     • uses modern "in" and "out" qualifiers
     • no longer supports deprecated "gl_FragColor"
     • ensures compatibility with Panda3D’s GLSL pipeline
*/


in vec3 v_normal;
/*
   "in" declares a per-fragment input varying.

   This value comes directly from the vertex shader's:
       out vec3 v_normal;

   The GPU automatically:
       • takes the three v_normal values at the triangle’s vertices
       • linearly interpolates them across the triangle
       • provides the interpolated value per fragment (pixel)

   Because of interpolation, this incoming normal is
   *not guaranteed* to be unit length, which is why we re-normalize it.
*/


out vec4 fragColor;
/*
   "out" is the output variable for the final fragment color.

   This replaces the old "gl_FragColor" variable from earlier GLSL versions.

   The fragment shader must write to at least one output for the fragment
   to appear on screen. Panda3D doesn't require a specific name — you choose.
*/


void main() {
/*
   Fragment shaders run once per *fragment* (pixel-sized sample).
   After rasterization, every screen pixel inside the triangle
   triggers a call to this main() function.
*/


    vec3 n = normalize(v_normal);
    /*
       Normalize the interpolated normal.

       Interpolation across the surface produces vectors
       whose length is no longer exactly 1.0.

       For lighting and shading, it is essential that normals
       are unit vectors, so we normalize them here.

       Example:
           v_normal = (0.3, 0.6, 0.9)
           length might be > 1 or < 1
           normalize(v_normal) makes its length exactly 1
    */


    fragColor = vec4(n * 0.5 + 0.5, 1.0);
    /*
       Convert the normal vector into a visible RGB color.

       Normals range from -1 to +1 on each axis.

       But colors must be in 0 to 1 range.

       To map:
           -1 → 0
            0 → 0.5
           +1 → 1

       We use:
           n * 0.5 + 0.5

       This shifts and scales the vector so it's displayable as a color.

       Final color:
           fragColor = (R, G, B, A)
           A = 1.0 (fully opaque)

       The result is a "normal visualization":
           • blue-ish for +Z
           • red-ish for +X
           • green-ish for +Y
           • smooth gradients across the surface
    */
}
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-PassThrough-Shader.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
