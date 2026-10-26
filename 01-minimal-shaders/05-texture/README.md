# Lesson: Texture

Part of the **01-minimal-shaders** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson isolates and demonstrates **Texture**. It illustrates foundational programmable GPU pipeline mechanics in Panda3D using GLSL, applying custom shaders directly onto the `models/panda-model` model.

## 📂 File Structure

```
05-texture/
├── Minimal-Texture-Shader.py
├── Minimal-Texture-Shader.vert
├── Minimal-Texture-Shader.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-Texture-Shader.vert`

```glsl
#version 150
/* 
   Specifies the GLSL language version used by this vertex shader.

   "#version 150" corresponds to GLSL 1.50,
   introduced with OpenGL 3.2.

   This version:
     - uses modern "in" qualifiers for vertex inputs
     - requires explicit outputs
     - removes deprecated fixed-function features
     - is compatible with Panda3D’s GLSL pipeline
*/


in vec4 p3d_Vertex;
/*
   Declares a vertex position input attribute.

   "in" means this variable is provided per vertex
   from the model’s vertex buffer.

   "p3d_Vertex" is a built-in Panda3D attribute
   that contains the position of each vertex
   in model-local (object) space.

   Type: vec4
     x, y, z → spatial coordinates
     w       → usually 1.0 for positions
*/


in vec2 p3d_MultiTexCoord0;
/*
   Declares a texture coordinate input attribute.

   "p3d_MultiTexCoord0" is a built-in Panda3D attribute
   containing the first set of UV coordinates for the vertex.

   Type: vec2 (u, v):
     u → horizontal texture coordinate
     v → vertical texture coordinate
*/


out vec2 v_uv;
/*
   Declares an output variable to pass data to the fragment shader.

   "v_uv":
     - carries the texture coordinates from vertex shader → fragment shader
     - is automatically interpolated across each triangle
     - allows the fragment shader to sample the texture accurately
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform 4×4 matrix for transforming vertices.

   A "uniform":
     - is constant for all vertices in a draw call
     - is supplied by the application (Panda3D)

   "mat4" indicates a 4×4 matrix.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transform
     - View (camera) transform
     - Projection (perspective) transform

   This matrix converts model-space positions
   into clip-space coordinates.
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once for each vertex
   processed by the GPU.

   Responsibilities:
     - pass UV coordinates to the fragment shader
     - compute final clip-space position
*/


    v_uv = p3d_MultiTexCoord0;
    /*
       Passes the texture coordinates to the fragment shader.

       Each fragment receives its own interpolated UVs,
       allowing proper texture sampling.
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

       Without writing to gl_Position,
       the vertex will not be rendered.
    */
}


/*
   After the vertex shader completes:

     - v_uv is interpolated across triangles
     - vertices are assembled into primitives
     - triangles are rasterized
     - the fragment shader runs per fragment

   This vertex shader only passes UVs and transforms positions.
*/
```

## 🎨 Fragment Shader

File: `Minimal-Texture-Shader.frag`

```glsl
#version 150
/* 
   Specifies the GLSL version used by this fragment shader.

   GLSL 1.50:
     - requires explicit fragment output variables
     - disallows legacy gl_FragColor
     - must match the vertex shader version
*/


in vec2 v_uv;
/*
   Declares an input variable from the vertex shader.

   "v_uv":
     - contains interpolated texture coordinates for this fragment
     - allows sampling the correct color from the texture
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "out" indicates:
     - this variable contains the final color
       written to the framebuffer

   "vec4" components:
     R → red
     G → green
     B → blue
     A → alpha (opacity)

   The variable name "fragColor" is user-defined.
*/


uniform sampler2D tex;
/*
   Declares a 2D texture sampler.

   "sampler2D":
     - represents a texture bound by the application
     - allows lookup of color values using UV coordinates

   "tex":
     - is supplied by the application
     - allows sampling the texture's color
       using UV coordinates.
   
   Panda3D binds the actual texture object before drawing.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function executes once per fragment
   generated by rasterizing the geometry.

   Responsibilities:
     - sample the texture
     - output the final color
*/


    vec4 texColor = texture(tex, v_uv);
    /*
       Samples the texture using the interpolated UV coordinates.

       Returns a vec4:
         RGB → texture color
         A   → texture alpha
    */


    fragColor = texColor;
    /*
       Assigns the final color to the fragment.

       This preserves the original texture colors and transparency
       exactly as they appear in the image file.
       No lighting or shading is applied.
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - geometry passes UV coordinates to the fragment shader
     - the fragment shader samples the texture
     - the object is rendered with the unlit texture color
*/
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-Texture-Shader.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
