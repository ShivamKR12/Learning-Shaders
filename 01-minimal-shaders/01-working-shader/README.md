# Lesson: Working Shader

Part of the **01-minimal-shaders** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson isolates and demonstrates **Working Shader**. It illustrates foundational programmable GPU pipeline mechanics in Panda3D using GLSL, applying custom shaders directly onto the `models/teapot` model.

## 📂 File Structure

```
01-working-shader/
├── Minimal-Working-Shader.py
├── Minimal-Working-Shader.vert
├── Minimal-Working-Shader.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-Working-Shader.vert`

```glsl
#version 150
/* 
   This sets the GLSL language version for the shader.

   "#version 150" means GLSL 1.50 (OpenGL 3.2 era).
   Using this version:
     - enables modern "in" and "out" syntax
     - disables older deprecated keywords like "attribute" and "varying"
     - ensures compatibility with Panda3D's default GLSL system
*/


in vec4 p3d_Vertex;
/* 
   "in" means this variable is an input attribute to the vertex shader.
   It comes from the model's vertex data.

   Panda3D provides built-in attribute names.
   "p3d_Vertex" contains the position of each vertex in the model's local space.
   Type: vec4 (x, y, z, w).
   w is usually 1.0 for positions.
*/


in vec3 p3d_Normal;
/*
   Another input attribute provided by Panda3D.

   "p3d_Normal" contains the vertex's surface normal:
     - a 3D direction vector
     - used for lighting in more advanced shaders
     - not used in this simple shader, but still auto-sent by Panda3D

   Type: vec3 (x, y, z)
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   A "uniform" is a global variable supplied by the application (Panda3D).
   It does NOT change between vertices during the draw call.

   "mat4" means a 4×4 matrix.

   "p3d_ModelViewProjectionMatrix" is a built-in Panda3D uniform
   that combines three transformations:

     Model      – places the model in the world
     View       – places the world relative to the camera
     Projection – applies perspective

   Combined this transforms positions into clip space.

   Panda3D calculates and updates this automatically every frame.
*/


void main() {
/*
   The entry point of the vertex shader.
   Every vertex processed by the GPU will run this function once.

   The goal of a vertex shader is to output a final position for each vertex.
*/


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       "gl_Position" is a built-in output variable required by GLSL.

       The GPU uses gl_Position to determine where on the screen
       the vertex should appear.

       This line applies the transformation:
          final_position = MVP_matrix × vertex_position

       Breaking down the multiplication:

       p3d_Vertex:
         - The vertex position in model-local coordinates (vec4)

       p3d_ModelViewProjectionMatrix:
         - A mat4 that converts model-space coordinates
           → world-space
           → camera/view-space
           → clip-space
       
       The result is a vec4 representing the clip-space position.

       Without writing to gl_Position, the vertex would not appear onscreen.
    */
}


/*
  After the vertex shader finishes:
    - gl_Position undergoes perspective division (divided by w)
    - The result is converted into normalized device coordinates
    - The GPU rasterizes triangles
    - The fragment shader then runs for each pixel

  This simple shader only handles positions,
  so the model renders as an unlit, uncolored object
  (unless the fragment shader assigns color).
*/
```

## 🎨 Fragment Shader

File: `Minimal-Working-Shader.frag`

```glsl
#version 150
/* 
   Specifies the version of GLSL the compiler must use.
   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2).

   This version:
     - uses modern "in" and "out" syntax
     - disallows old keywords like "gl_FragColor"
     - ensures compatibility with Panda3D’s shader system
*/


out vec4 fragColor;
/*
   Declares an output variable from the fragment shader.

   "out" means:
      - this variable is the final color the GPU will write
        to the current framebuffer (usually the screen).
      - this replaces older "gl_FragColor", which is deprecated
        in GLSL versions 130+.

   "vec4" means a 4-component vector:
      (red, green, blue, alpha)

   The name "fragColor" is chosen by you.
   Panda3D does NOT require a specific name; any valid out variable works.

   Every pixel (fragment) produced by rasterization will run this shader
   and produce its own "fragColor" value.
*/


void main() {
/*
   Standard function required by GLSL.
   The fragment shader entry point.

   This function is run once per *fragment* (pixel-sized sample)
   that results from rasterizing a triangle.

   The main purpose of a fragment shader is to determine the final color
   and sometimes other values (like depth).
*/


    fragColor = vec4(1.0, 0.3, 0.2, 1.0);  // solid orange color
    /*
       Assigns the output color.

       "vec4(1.0, 0.3, 0.2, 1.0)" is an RGBA color:
         R = 1.0 (full red)
         G = 0.3 (30% green)
         B = 0.2 (20% blue)
         A = 1.0 (fully opaque)

       This combination produces a warm orange/red color.

       Because this is the only line inside main(),
       every pixel will be this exact solid color.

       There is no lighting, no texturing, no input values —
       just a constant color.
    */


}
/*
   End of the main() function and end of the shader.
*/
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-Working-Shader.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
