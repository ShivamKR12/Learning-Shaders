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
