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
