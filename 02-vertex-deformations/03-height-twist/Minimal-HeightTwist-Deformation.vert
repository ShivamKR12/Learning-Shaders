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

   This value is commonly used for time-based animations.
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once for every vertex
   processed by the GPU.

   The vertex shader’s main responsibilities:
     - compute the final clip-space position
     - optionally apply animations or deformations
*/


    vec4 position = p3d_Vertex;
    /*
       Creates a local copy of the vertex position.

       This allows modification without altering
       the original input attribute.
    */


    float angle = position.y * 2.0 + osg_FrameTime;
    /*
       Computes a rotation angle based on:
         - vertex height (position.y)
         - current time (osg_FrameTime)

       Multiplying position.y by 2.0:
         - increases rotation variation along the Y axis

       Adding osg_FrameTime:
         - animates the rotation over time
    */


    float s = sin(angle);
    /*
       Computes the sine of the rotation angle.

       This will be used in the 2×2 rotation matrix.
    */


    float c = cos(angle);
    /*
       Computes the cosine of the rotation angle.

       Along with sine, this completes the rotation matrix.
    */


    mat2 rotation = mat2(c, -s, s, c);
    /*
       Creates a 2×2 rotation matrix for the XZ plane.

       Standard 2D rotation matrix:
         | cosθ  -sinθ |
         | sinθ   cosθ |

       This will rotate points around the Y axis
       when applied to X and Z components.
    */


    position.xz = rotation * position.xz;
    /*
       Applies rotation to the vertex’s XZ position.

       position.xz:
         - selects the horizontal (X) and depth (Z) components

       Multiplying by the rotation matrix:
         - rotates the vertex around the Y axis
         - rotation amount depends on vertex height and time
         - creates a twisting animation along Y
    */


    gl_Position = p3d_ModelViewProjectionMatrix * position;
    /*
       Writes the final transformed position.

       "gl_Position" is a required built-in output.

       Multiplication applies:
         model space → world space
         world space → camera space
         camera space → clip space

       The GPU uses this to determine where the vertex
       appears on screen.
    */
}


/*
   After the vertex shader finishes:

     - rotated vertices are transformed into clip space
     - primitives are assembled and rasterized
     - the fragment shader runs for each generated pixel

   This shader produces a Y-axis twisting animation
   where vertices rotate around Y based on height
   and time.
*/
