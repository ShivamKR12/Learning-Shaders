# Lesson: Normal Pulse

Part of the **02-vertex-deformations** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates real-time GPU vertex displacement for **Normal Pulse**. Surface vertices are procedurally transformed in model space prior to clip-space projection, creating dynamic wave oscillation and mesh deformation without CPU re-computation.

## 📂 File Structure

```
04-normal-pulse/
├── Minimal-NormalPulse-Deformation.py
├── Minimal-NormalPulse-Deformation.vert
├── Minimal-NormalPulse-Deformation.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-NormalPulse-Deformation.vert`

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
   that represents the surface normal at each vertex.

   A normal:
     - is a direction vector
     - is perpendicular to the surface
     - is commonly used for lighting calculations

   Type: vec3 (x, y, z)
*/


out vec3 v_normal;
/*
   Declares an output variable from the vertex shader.

   "v_normal":
     - will be passed to the fragment shader
     - will be interpolated across the surface of triangles

   Each fragment will receive its own smoothly
   interpolated normal vector.
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

   It is supplied and updated automatically by Panda3D.
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

   This function is executed once for every vertex
   processed by the GPU.

   The vertex shader:
     - prepares data for the fragment shader
     - computes the final clip-space position
*/


    v_normal = normalize(p3d_Normal);
    /*
       Normalizes and outputs the vertex normal.

       normalize(...):
         - converts the normal to unit length
         - ensures consistent direction magnitude

       Normalizing is important because:
         - interpolation can change vector length
         - many lighting calculations assume unit normals
    */


    float pulse = sin(osg_FrameTime) * 0.15;
    /*
       Computes a time-based displacement amount.

       sin(osg_FrameTime):
         - oscillates smoothly between -1 and +1

       * 0.15:
         - scales the effect
         - limits how far vertices are displaced

       Result:
         - a small pulsing value used for deformation
    */


    vec4 pos = p3d_Vertex;
    /*
       Creates a local copy of the vertex position.

       This allows the position to be modified
       without altering the original input attribute.
    */


    pos.xyz += v_normal * pulse;
    /*
       Offsets the vertex position along its normal.

       v_normal * pulse:
         - moves the vertex outward or inward
           relative to the surface direction

       Effect:
         - the model appears to "breathe" or pulse
         - deformation follows the surface shape
    */


    gl_Position = p3d_ModelViewProjectionMatrix * pos;
    /*
       Writes the final transformed vertex position.

       "gl_Position" is a required built-in output.

       The multiplication applies:
         model space → world space
         world space → camera space
         camera space → clip space

       This determines where the vertex appears on screen.
    */
}


/*
   After the vertex shader completes:

     - v_normal is interpolated across each triangle
     - vertices are assembled into primitives
     - triangles are rasterized into fragments
     - the fragment shader runs once per fragment

   This vertex shader performs a normal-based
   pulsing deformation effect.
*/
```

## 🎨 Fragment Shader

File: `Minimal-NormalPulse-Deformation.frag`

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
   Declares an input variable from the vertex shader.

   "v_normal":
     - contains the interpolated surface normal
     - varies smoothly across the surface

   Each fragment receives its own normal vector,
   based on its position within the triangle.
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

   This function is executed once per fragment
   produced by rasterization.

   The fragment shader determines the final pixel color.
*/


    vec3 n = normalize(v_normal);
    /*
       Normalizes the interpolated normal.

       Even though normals were normalized in the vertex shader:
         - interpolation can change their length

       Normalizing again ensures:
         - the vector has unit length
         - consistent visual results
    */


    fragColor = vec4(n * 0.5 + 0.5, 1.0);
    /*
       Converts the normal vector into a visible color.

       n is in the range:
         [-1.0, +1.0]

       n * 0.5 + 0.5:
         - remaps the range to [0.0, 1.0]
         - suitable for RGB color output

       Result:
         - X normal → red channel
         - Y normal → green channel
         - Z normal → blue channel

       This produces a colorful visualization
       of surface directions.

       Alpha is set to 1.0 (fully opaque).
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - vertices pulse outward along their normals
     - the surface deforms smoothly over time
     - normals are visualized as colors
     - the object appears animated and color-coded
*/
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-NormalPulse-Deformation.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
