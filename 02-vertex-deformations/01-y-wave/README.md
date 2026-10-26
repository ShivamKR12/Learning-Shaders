# Lesson: Y Wave

Part of the **02-vertex-deformations** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates real-time GPU vertex displacement for **Y Wave**. Surface vertices are procedurally transformed in model space prior to clip-space projection, creating dynamic wave oscillation and mesh deformation without CPU re-computation.

## 📂 File Structure

```
01-y-wave/
├── Minimal-YWave-Deformation.py
├── Minimal-YWave-Deformation.vert
├── Minimal-YWave-Deformation.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-YWave-Deformation.vert`

```glsl
#version 150
/* 
   Specifies the GLSL language version used by this shader.

   "#version 150" corresponds to GLSL 1.50,
   which matches the OpenGL 3.2 core profile era.

   This version:
     - uses modern "in" and "out" qualifiers
     - removes deprecated fixed-function pipeline features
     - is fully compatible with Panda3D’s default GLSL setup
*/


in vec4 p3d_Vertex;
/*
   Declares a vertex input attribute.

   "in" means this variable is provided per-vertex
   from the model’s vertex buffer.

   "p3d_Vertex" is a built-in Panda3D attribute that contains:
     - the position of each vertex
     - in model-local (object) space

   Type: vec4
     x, y, z → spatial coordinates
     w       → usually 1.0 for positions
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform matrix supplied by Panda3D.

   A "uniform":
     - is constant for all vertices in a draw call
     - is updated by the application, not the shader

   "mat4" is a 4×4 matrix.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model matrix      (object → world)
     - View matrix       (world → camera)
     - Projection matrix (camera → clip space)

   Panda3D automatically computes and updates this matrix every frame.
*/


uniform float osg_FrameTime;
/*
   Declares a uniform float representing time.

   "osg_FrameTime":
     - is a time value provided by the engine
     - increases continuously as the application runs
     - is commonly used for animation effects

   Units:
     - measured in seconds
     - high precision floating-point value

   Because this is a uniform:
     - every vertex processed in this frame sees the same time value
*/


void main() {
/*
   The entry point of the vertex shader.

   This function is executed once for every vertex
   sent to the GPU.

   The main responsibility of a vertex shader is to:
     - compute the final clip-space position
     - assign it to gl_Position
*/


    vec4 pos = p3d_Vertex;
    /*
       Creates a local copy of the vertex position.

       This allows us to:
         - modify the vertex position
         - without changing the original input attribute

       "pos" initially contains the model-space coordinates
       of the vertex.
    */


    pos.y = sin(pos.x + 4.0 * osg_FrameTime);
    /*
       Modifies the vertex’s vertical (Y) position.

       Explanation of the expression:

       pos.x:
         - the horizontal position of the vertex

       osg_FrameTime:
         - current time value (in seconds)

       4.0 * osg_FrameTime:
         - scales time to increase animation speed

       pos.x + time:
         - creates a phase offset so different X positions
           animate at different times

       sin(...):
         - produces a smooth oscillation between -1 and +1

       Result:
         - vertices move up and down over time
         - creating a wave-like animation along the X axis
    */


    gl_Position = p3d_ModelViewProjectionMatrix * pos;
    /*
       Writes the final transformed position.

       "gl_Position" is a required built-in output variable.

       The multiplication applies:
         model space → world space
         world space → camera space
         camera space → clip space

       The GPU uses gl_Position to:
         - perform perspective division
         - determine where the vertex appears on screen

       If gl_Position is not written,
       the vertex will not be rendered.
    */
}


/*
   After the vertex shader completes:

     - gl_Position is divided by its w component
     - coordinates are converted to normalized device space
     - triangles are assembled and rasterized
     - the fragment shader runs for each generated pixel

   This vertex shader adds time-based animation,
   but does not handle color, lighting, or texturing.
*/
```

## 🎨 Fragment Shader

File: `Minimal-YWave-Deformation.frag`

```glsl
#version 150
/* 
   Specifies the GLSL version for the fragment shader.

   GLSL 1.50:
     - requires explicit output variables
     - does not allow legacy "gl_FragColor"
     - matches the vertex shader version for compatibility
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "out" means:
     - this value is written to the framebuffer
     - it represents the final color of a pixel

   "vec4" components:
     R → red
     G → green
     B → blue
     A → alpha (opacity)

   The variable name "fragColor" is user-defined.
   Panda3D accepts any valid output variable name.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function is executed once per fragment
   generated by rasterization.

   The fragment shader determines:
     - the final pixel color
     - and optionally depth or other outputs
*/


    fragColor = vec4(1.0, 1.0, 1.0, 1.0);
    /*
       Assigns a constant color to every fragment.

       vec4(1.0, 1.0, 1.0, 1.0) represents:
         - full red
         - full green
         - full blue
         - full opacity

       This produces pure white.

       Because the color is constant:
         - no lighting calculations are performed
         - no textures are sampled
         - every pixel has the same color
    */
}


/*
   End of the fragment shader.

   Combined with the vertex shader:
     - vertices animate in a wave pattern
     - the object is rendered as solid white
     - no shading or lighting effects are applied
*/
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-YWave-Deformation.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
