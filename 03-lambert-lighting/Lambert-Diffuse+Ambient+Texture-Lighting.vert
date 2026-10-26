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


in vec3 p3d_Normal;
/*
   Declares a vertex normal input attribute.

   "p3d_Normal" is a built-in Panda3D attribute
   representing the surface normal at each vertex.

   A normal:
     - is a direction vector perpendicular to the surface
     - is commonly used for lighting calculations

   Type: vec3 (x, y, z)
*/


in vec2 p3d_MultiTexCoord0;
/*
   Declares a vertex texture coordinate input attribute.

   "p3d_MultiTexCoord0" is a built-in Panda3D attribute
   containing the first set of UV coordinates.

   Type: vec2 (u, v):
     u → horizontal texture coordinate
     v → vertical texture coordinate
*/


out vec3 v_normal;
/*
   Declares an output variable for the fragment shader.

   "v_normal":
     - carries the transformed vertex normal
     - is interpolated across the surface of triangles
     - used in the fragment shader for lighting calculations
*/


out vec2 v_uv;
/*
   Declares an output variable for the fragment shader.

   "v_uv":
     - carries the vertex UV coordinates
     - interpolated automatically across the surface
     - allows the fragment shader to sample textures accurately
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform transformation matrix.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transformation
     - View (camera) transformation
     - Projection (perspective) transformation

   Converts model-space positions into clip-space coordinates.
*/


uniform mat3 p3d_NormalMatrix;
/*
   Declares a uniform normal transformation matrix.

   "p3d_NormalMatrix":
     - transforms normals correctly under non-uniform scaling
     - is the 3x3 inverse transpose of the model-view matrix
     - ensures lighting calculations remain correct
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once per vertex.
   Responsibilities:
     - transform normals
     - pass UV coordinates
     - compute final clip-space position
*/


    v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
    /*
       Transforms the normal into eye-space and normalizes it.

       normalize(...):
         - ensures unit length for accurate lighting calculations
    */


    v_uv = p3d_MultiTexCoord0;
    /*
       Passes texture coordinates to the fragment shader.

       Each fragment receives interpolated UVs for accurate sampling.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Computes the final vertex position in clip space.

       "gl_Position" is required by GLSL.
       The MVP matrix transforms model-space coordinates to clip space.
    */
}


/*
   After the vertex shader completes:

     - normals are interpolated per fragment
     - UVs are interpolated per fragment
     - triangles are rasterized
     - the fragment shader runs per pixel
*/
