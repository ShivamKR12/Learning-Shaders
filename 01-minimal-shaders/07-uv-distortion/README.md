# Lesson: Uv Distortion

Part of the **01-minimal-shaders** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson isolates and demonstrates **Uv Distortion**. It illustrates foundational programmable GPU pipeline mechanics in Panda3D using GLSL, applying custom shaders directly onto the `models/panda-model` model.

## 📂 File Structure

```
07-uv-distortion/
├── Minimal-UVDistortion-Shader.py
├── Minimal-UVDistortion-Shader.vert
├── Minimal-UVDistortion-Shader.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-UVDistortion-Shader.vert`

```glsl
#version 150
/* 
   Specifies the GLSL version used by this vertex shader.

   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2).

   This version:
     - uses modern "in" and "out" qualifiers
     - removes legacy fixed-function features
     - is fully compatible with Panda3D’s GLSL pipeline
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


in vec2 p3d_MultiTexCoord0;
/*
   Declares a texture coordinate input attribute.

   "p3d_MultiTexCoord0" is a built-in Panda3D attribute
   that contains the first set of texture coordinates (UVs).

   Type: vec2
     u → horizontal texture coordinate
     v → vertical texture coordinate

   These coordinates typically range from 0.0 to 1.0
   across the surface of the model.
*/


out vec2 v_uv;
/*
   Declares an output variable from the vertex shader.

   "out" means:
     - this value will be interpolated across the triangle
     - and passed to the fragment shader

   "v_uv" will carry texture coordinates from:
     vertex shader → rasterizer → fragment shader

   Interpolation is automatic and handled by the GPU.
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform transformation matrix.

   A "uniform":
     - is constant for all vertices in the draw call
     - is supplied by the application (Panda3D)

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

   This function runs once for each vertex.

   The vertex shader is responsible for:
     - passing data to the fragment shader
     - computing the final clip-space position
*/


    v_uv = p3d_MultiTexCoord0;
    /*
       Passes texture coordinates to the fragment shader.

       The value assigned here:
         - is not a single value per triangle
         - but will be smoothly interpolated per pixel

       This allows each fragment to sample the texture
       at the correct UV coordinate.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Writes the final transformed vertex position.

       "gl_Position" is a required built-in output.

       The multiplication applies:
         model space → world space
         world space → camera space
         camera space → clip space

       The GPU uses gl_Position to:
         - perform perspective division
         - determine where the vertex appears on screen
    */
}


/*
   After the vertex shader completes:

     - v_uv is interpolated across each triangle
     - vertices are assembled into primitives
     - triangles are rasterized into fragments
     - the fragment shader runs once per fragment

   This vertex shader:
     - passes UVs forward
     - performs no animation
     - performs no lighting
*/
```

## 🎨 Fragment Shader

File: `Minimal-UVDistortion-Shader.frag`

```glsl
#version 150
/* 
   Specifies the GLSL version used by this fragment shader.

   GLSL 1.50:
     - requires explicit fragment outputs
     - disallows deprecated gl_FragColor
     - must match the vertex shader version
*/


in vec2 v_uv;
/*
   Declares an input variable from the vertex shader.

   "v_uv":
     - contains interpolated texture coordinates
     - varies smoothly across the surface of the triangle

   Each fragment receives its own UV value
   based on its position within the triangle.
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "fragColor" represents:
     - the final RGBA color written to the framebuffer

   Components:
     R → red
     G → green
     B → blue
     A → alpha (opacity)

   The name is user-defined and not engine-specific.
*/


uniform sampler2D tex;
/*
   Declares a 2D texture sampler.

   "sampler2D":
     - represents a 2D texture bound by the application
     - allows sampling color data using UV coordinates

   Panda3D binds the actual texture object
   to this sampler before drawing.
*/


uniform float osg_FrameTime;
/*
   Declares a uniform time value.

   "osg_FrameTime":
     - increases continuously over time
     - is measured in seconds
     - is the same for all fragments in the frame

   This value is commonly used for animation effects.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function is executed once per fragment
   produced by rasterizing the triangles.

   The fragment shader determines the final pixel color.
*/


    float wave = sin(v_uv.y * 10.0 + osg_FrameTime * 3.0) * 0.02;
    /*
       Computes a horizontal wave offset.

       Breakdown of the expression:

       v_uv.y * 10.0:
         - increases the frequency of the wave vertically
         - creates multiple wave cycles across the texture

       osg_FrameTime * 3.0:
         - advances the wave over time
         - controls animation speed

       sin(...):
         - produces a smooth oscillation between -1 and +1

       * 0.02:
         - reduces the amplitude
         - keeps the distortion subtle

       Result:
         - a small time-varying offset value
    */


    vec2 distortedUV = v_uv + vec2(wave, 0.0);
    /*
       Offsets the texture coordinates.

       The wave is applied only to the X (U) axis:
         - horizontal distortion
         - vertical coordinates remain unchanged

       This creates a rippling or heat-wave effect
       across the texture.
    */


    vec4 texColor = texture(tex, distortedUV);
    /*
       Samples the texture using the distorted UVs.

       "texture(...)":
         - looks up the color at the given coordinates
         - performs filtering based on texture settings

       The returned value is a vec4:
         R, G, B → color channels
         A       → alpha channel
    */


    fragColor = vec4(texColor.rgb, texColor.a);
    /*
       Assigns the final fragment color.

       The RGB and alpha values are taken directly
       from the sampled texture.

       This preserves:
         - the original texture colors
         - the original transparency

       The only modification applied is
       the UV distortion.
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - geometry is rendered normally
     - UV coordinates are passed from vertices to fragments
     - the texture is sampled with animated distortion
     - the result appears as a subtle wave effect
*/
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-UVDistortion-Shader.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
