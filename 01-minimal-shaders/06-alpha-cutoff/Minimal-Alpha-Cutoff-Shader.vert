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


in vec2 p3d_MultiTexCoord0;
/*
   Declares a vertex texture coordinate input attribute.

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
   Declares a uniform transformation matrix.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transformation
     - View (camera) transformation
     - Projection (perspective) transformation

   This converts model-space positions into clip-space coordinates.
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once per vertex
   processed by the GPU.

   Responsibilities of this vertex shader:
     - pass UV coordinates to the fragment shader
     - compute the final clip-space position
*/


    v_uv = p3d_MultiTexCoord0;
    /*
       Passes the texture coordinates to the fragment shader.

       Each fragment receives its own interpolated UVs,
       allowing proper texture sampling.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Computes the final vertex position in clip space.

       "gl_Position" is required by GLSL.
       The MVP matrix transforms model-space coordinates
       to clip space for rasterization.
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
