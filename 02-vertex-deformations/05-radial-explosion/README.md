# Lesson: Radial Explosion

Part of the **02-vertex-deformations** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates real-time GPU vertex displacement for **Radial Explosion**. Surface vertices are procedurally transformed in model space prior to clip-space projection, creating dynamic wave oscillation and mesh deformation without CPU re-computation.

## 📂 File Structure

```
05-radial-explosion/
├── Minimal-RadialExplosion-Deformation.py
├── Minimal-RadialExplosion-Deformation.vert
├── Minimal-RadialExplosion-Deformation.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Minimal-RadialExplosion-Deformation.vert`

```glsl
#version 150
/* 
   Specifies the GLSL language version used by this vertex shader.

   "#version 150" corresponds to GLSL 1.50,
   introduced with OpenGL 3.2.

   This version:
     - uses modern "in" qualifiers
     - removes deprecated fixed-function pipeline features
     - is fully compatible with Panda3D’s GLSL system
*/


in vec4 p3d_Vertex;
/*
   Declares a vertex position input attribute.

   "in" means this value is provided per vertex
   from the model’s vertex buffer.

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
     - is supplied by the application (Panda3D)

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
     - represents elapsed time
     - increases continuously as the application runs
     - is measured in seconds

   This value is commonly used for animation effects.

   Because it is a uniform:
     - all vertices in the same frame
       receive the same time value
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once for every vertex
   processed by the GPU.

   The vertex shader’s job is to:
     - optionally modify vertex data
     - output the final clip-space position
*/


    vec3 center = vec3(0.0);
    /*
       Defines a reference point in space.

       "vec3(0.0)":
         - creates a vector (0.0, 0.0, 0.0)
         - represents the origin of model space

       This point will act as the center
       from which vertices are pushed outward.
    */


    vec3 dir = normalize(p3d_Vertex.xyz - center);
    /*
       Computes a direction vector for displacement.

       p3d_Vertex.xyz:
         - extracts the 3D position of the vertex

       p3d_Vertex.xyz - center:
         - creates a vector pointing from the center
           toward the vertex

       normalize(...):
         - converts the vector to unit length
         - preserves direction while removing magnitude

       Result:
         - "dir" points outward from the center
           for each vertex
    */


    float strength = sin(osg_FrameTime) * 0.5;
    /*
       Computes the displacement strength.

       sin(osg_FrameTime):
         - oscillates smoothly between -1 and +1
         - changes over time

       * 0.5:
         - reduces the amplitude
         - limits how far vertices are displaced

       Result:
         - a time-varying value that expands
           and contracts the geometry
    */


    vec4 pos = p3d_Vertex;
    /*
       Creates a local copy of the vertex position.

       This allows modification of the position
       without altering the original input attribute.
    */


    pos.xyz += dir * strength;
    /*
       Offsets the vertex position.

       dir * strength:
         - scales the outward direction vector
           by the current animation strength

       pos.xyz += ...:
         - moves the vertex along that direction

       Effect:
         - vertices move away from or toward the center
         - creating a pulsing or breathing deformation
    */


    gl_Position = p3d_ModelViewProjectionMatrix * pos;
    /*
       Writes the final transformed position.

       "gl_Position" is a required built-in output.

       The multiplication transforms:
         model space → world space
         world space → camera space
         camera space → clip space

       The GPU uses this value to determine
       where the vertex appears on screen.
    */
}


/*
   After the vertex shader finishes:

     - positions are normalized
     - primitives are assembled
     - triangles are rasterized
     - the fragment shader runs per fragment

   This vertex shader performs a time-based
   radial deformation centered at the origin.
*/
```

## 🎨 Fragment Shader

File: `Minimal-RadialExplosion-Deformation.frag`

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

       This produces a solid white appearance.

       No lighting, textures, or shading calculations
       are performed in this shader.
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - geometry pulses outward and inward over time
     - deformation is centered at the model origin
     - the object is rendered as solid white
*/
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Minimal-RadialExplosion-Deformation.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
