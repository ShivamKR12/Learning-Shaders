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
