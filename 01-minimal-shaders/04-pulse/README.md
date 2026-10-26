# Lesson: Pulse

Part of the **01-minimal-shaders** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson isolates and demonstrates **Pulse**. It illustrates foundational programmable GPU pipeline mechanics in Panda3D using GLSL, applying custom shaders directly onto the `models/teapot` model.

## 📂 File Structure

```
04-pulse/
├── Minimal-Pulse-Shader.py
├── Minimal-Pulse-Shader.vert
├── Minimal-Pulse-Shader.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-Pulse-Shader.vert`

```glsl
#version 150
/* 
   Specifies the GLSL language version used by this vertex shader.

   "#version 150" corresponds to GLSL 1.50,
   introduced with OpenGL 3.2.

   This version:
     - uses modern "in" qualifiers
     - removes deprecated fixed-function pipeline features
     - is compatible with Panda3D’s GLSL system
*/


in vec4 p3d_Vertex;
/*
   Declares a vertex position input attribute.

   "in" indicates that this variable is supplied
   per vertex from the model’s vertex buffer.

   "p3d_Vertex" is a built-in Panda3D attribute
   containing the vertex position in model-local space.

   Type: vec4
     x, y, z → spatial coordinates
     w       → usually 1.0 for positions
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform transformation matrix.

   A "uniform":
     - is constant for all vertices in a draw call
     - is provided by the application (Panda3D)

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transformation
     - View (camera) transformation
     - Projection (perspective) transformation

   This matrix converts model-space positions
   into clip-space coordinates.
*/


void main() {
/*
   Entry point of the vertex shader.

   This function is executed once per vertex
   processed by the GPU.

   The vertex shader’s primary responsibility
   is to compute the final position of each vertex.
*/


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Writes the final transformed vertex position.

       "gl_Position" is a required built-in output variable.

       The multiplication applies:
         model space → world space
         world space → camera space
         camera space → clip space

       The GPU uses gl_Position to:
         - perform perspective division
         - determine where the vertex appears on screen

       Without assigning gl_Position,
       the geometry would not be rendered.
    */
}


/*
   After the vertex shader completes:

     - positions are normalized
     - primitives are assembled
     - triangles are rasterized into fragments
     - the fragment shader runs once per fragment

   This vertex shader performs only
   geometric transformation with no animation.
*/
```

## 🎨 Fragment Shader

File: `Minimal-Pulse-Shader.frag`

```glsl
#version 150
/* 
   Specifies the GLSL version used by this fragment shader.

   GLSL 1.50:
     - requires explicit fragment output variables
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


uniform vec3 tint;
/*
   Declares a uniform base color.

   "vec3" represents an RGB color:
     x → red
     y → green
     z → blue

   "tint":
     - is supplied by the application
     - remains constant for all fragments in a draw call
     - defines the base color of the object

   Color values are typically in the range 0.0 to 1.0.
*/


uniform float osg_FrameTime;
/*
   Declares a uniform time value.

   "osg_FrameTime":
     - represents elapsed time in seconds
     - increases continuously as the application runs
     - is identical for all fragments in the same frame

   This value is commonly used for
   time-based animation effects.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function runs once per fragment
   generated during rasterization.

   The fragment shader determines the final pixel color.
*/


    float pulse = 0.5 + 0.5 * sin(osg_FrameTime * 5.0);
    /*
       Computes a pulsing intensity value.

       sin(osg_FrameTime * 5.0):
         - produces a smooth oscillation between -1 and +1
         - oscillates faster due to the 5.0 multiplier

       0.5 + 0.5 * sin(...):
         - remaps the range from [-1, +1]
           to [0.0, 1.0]

       Result:
         - "pulse" smoothly increases and decreases over time
         - suitable for brightness or intensity modulation
    */


    vec3 tintColor = tint * pulse;
    /*
       Modulates the base tint color.

       tint * pulse:
         - scales the RGB color by the pulse value
         - makes the color brighter and darker over time

       This creates a visual pulsing effect
       without changing the hue of the color.
    */


    fragColor = vec4(tintColor, 1);
    /*
       Assigns the final fragment color.

       "vec4(tintColor, 1)":
         - uses the pulsed RGB color
         - sets alpha to 1.0 (fully opaque)

       The result is a solid-colored object
       whose brightness pulses over time.

       No lighting or texture sampling is performed.
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - geometry is transformed normally
     - color is defined by a uniform tint
     - brightness pulses smoothly over time
     - the object appears as a flat, animated color
*/
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-Pulse-Shader.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
