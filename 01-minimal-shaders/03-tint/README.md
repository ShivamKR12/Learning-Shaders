# Lesson: Tint

Part of the **01-minimal-shaders** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson isolates and demonstrates **Tint**. It illustrates foundational programmable GPU pipeline mechanics in Panda3D using GLSL, applying custom shaders directly onto the `models/teapot` model.

## 📂 File Structure

```
03-tint/
├── Minimal-Tint-Shader.py
├── Minimal-Tint-Shader.vert
├── Minimal-Tint-Shader.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-Tint-Shader.vert`

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

       The GPU uses gl_Position to determine
       where the vertex appears on screen.
    */
}
```

## 🎨 Fragment Shader

File: `Minimal-Tint-Shader.frag`

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
   Declares a uniform color tint.

   "vec3" represents an RGB color:
     x → red
     y → green
     z → blue

   "tint":
     - is supplied by the application
     - remains constant for all fragments in a draw call
     - allows the object color to be changed dynamically

   Values are typically in the range 0.0 to 1.0.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function runs once per fragment.
   Its purpose is to determine the final pixel color.
*/


    fragColor = vec4(tint, 1);
    /*
       Assigns the final fragment color.

       "vec4(tint, 1)":
         - uses the RGB components from "tint"
         - sets alpha to 1.0 (fully opaque)

       This results in a solid, uniformly colored object.

       There is:
         - no lighting
         - no texture sampling
         - no shading calculations

       The entire object is tinted
       using the same uniform color.
    */
}
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-Tint-Shader.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
