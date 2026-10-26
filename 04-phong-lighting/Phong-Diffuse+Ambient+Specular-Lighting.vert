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

   "p3d_Normal":
     - represents the surface normal at the vertex
     - is used for lighting calculations

   Type: vec3 (x, y, z)
*/


out vec3 v_normal;
/*
   Declares an output variable to pass the normal to the fragment shader.

   "v_normal":
     - is interpolated across each triangle
     - allows per-fragment lighting calculations
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform 4×4 matrix for transforming vertices.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transform
     - View (camera) transform
     - Projection transform

   Converts model-space positions into clip-space coordinates.
*/

uniform mat3 p3d_NormalMatrix;
/*
   Declares a uniform 3×3 normal transformation matrix.

   "p3d_NormalMatrix":
     - transforms normals correctly under non-uniform scaling
     - is the inverse transpose of the model-view matrix
     - ensures accurate lighting results
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once per vertex.

   Responsibilities:
     - transform normals
     - compute final clip-space position
*/


    v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
    /*
       Transforms the vertex normal into eye space
       and normalizes it for consistent lighting calculations.

       Normalization ensures a unit-length vector,
       which is required for dot product lighting calculations.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Computes the final clip-space position.

       "gl_Position" is required by GLSL.
       The MVP matrix transforms model-space coordinates
       to clip space for rasterization.
    */
}


/*
   After the vertex shader completes:

     - normals are interpolated per fragment
     - vertices are assembled into triangles
     - rasterization produces fragments
     - the fragment shader runs per fragment
*/