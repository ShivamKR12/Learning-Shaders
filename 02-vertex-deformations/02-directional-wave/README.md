# Lesson: Directional Wave

Part of the **02-vertex-deformations** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates real-time GPU vertex displacement for **Directional Wave**. Surface vertices are procedurally transformed in model space prior to clip-space projection, creating dynamic wave oscillation and mesh deformation without CPU re-computation.

## 📂 File Structure

```
02-directional-wave/
├── Minimal-DirectionalWave-Deformation.py
├── Minimal-DirectionalWave-Deformation.vert
├── Minimal-DirectionalWave-Deformation.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-DirectionalWave-Deformation.vert`

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

   "p3d_Vertex" is a built-in Panda3D attribute
   containing the vertex position in model-local space.

   Type: vec4
     x, y, z → spatial coordinates
     w       → usually 1.0 for positions
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform transformation matrix.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transformation
     - View (camera) transformation
     - Projection (perspective) transformation

   This matrix converts model-space positions
   into clip-space coordinates.
*/


uniform float osg_FrameTime;
/*
   Declares a uniform time value.

   "osg_FrameTime":
     - represents elapsed time in seconds
     - increases continuously as the application runs
     - is the same for all vertices in a frame

   This value is commonly used to drive animations.
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once for each vertex
   processed by the GPU.

   The vertex shader’s responsibilities:
     - optionally modify vertex positions
     - compute the final clip-space position
*/


    vec4 pos = p3d_Vertex;
    /*
       Creates a local copy of the vertex position.

       This allows modifying the position without
       altering the original input attribute.
    */


    float wave = sin(pos.x * 5.0 + pos.z * 5.0 + osg_FrameTime * 3.0);
    /*
       Computes a wave-based displacement.

       Breakdown of the expression:

       pos.x * 5.0 + pos.z * 5.0:
         - increases the frequency of the wave along
           the X and Z axes
         - ensures multiple wave peaks across the surface

       osg_FrameTime * 3.0:
         - animates the wave over time
         - the 3.0 multiplier increases speed

       sin(...):
         - produces a smooth oscillation between -1 and +1

       Result:
         - a time-varying wave value for this vertex
    */


    pos.y += wave * 0.15;
    /*
       Applies vertical displacement based on the wave.

       wave * 0.15:
         - scales the amplitude to 15% of a unit
         - ensures a subtle deformation

       pos.y += ...:
         - moves the vertex up and down
         - creates a wavy surface animation
    */


    gl_Position = p3d_ModelViewProjectionMatrix * pos;
    /*
       Writes the final transformed vertex position.

       "gl_Position" is a required built-in output.

       Multiplying by the MVP matrix transforms:
         model space → world space
         world space → camera space
         camera space → clip space

       The GPU uses this value to determine
       where the vertex appears on screen.
    */
}


/*
   After the vertex shader finishes:

     - the wavy vertices are transformed into clip space
     - primitives are assembled
     - triangles are rasterized
     - the fragment shader runs for each pixel

   This vertex shader produces a simple animated wave effect
   on the surface geometry.
*/
```

## 🎨 Fragment Shader

File: `Minimal-DirectionalWave-Deformation.frag`

```glsl
#version 150
/* 
   Specifies the GLSL version used by this fragment shader.

   GLSL 1.50:
     - requires explicit fragment outputs
     - disallows deprecated gl_FragColor
     - must match the vertex shader version
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "fragColor":
     - represents the final RGBA color
     - is written to the framebuffer

   Components:
     R → red
     G → green
     B → blue
     A → alpha (opacity)
*/


void main() {
/*
   Entry point of the fragment shader.

   This function runs once per fragment
   generated during rasterization.

   The fragment shader determines the final pixel color.
*/


    fragColor = vec4(1.0, 1.0, 1.0, 1.0);
    /*
       Assigns a constant color to every fragment.

       vec4(1.0, 1.0, 1.0, 1.0):
         - full red
         - full green
         - full blue
         - fully opaque

       The object is rendered as solid white.

       No lighting, textures, or shading calculations are performed.
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - geometry is deformed with a wavy animation
       along X and Z coordinates
     - vertical displacement is subtle and continuous
     - the object is rendered as solid white
*/
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-DirectionalWave-Deformation.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
