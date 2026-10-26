#version 150
/* 
   Specifies the GLSL language version used by this vertex shader.

   "#version 150" corresponds to GLSL 1.50,
   introduced with OpenGL 3.2.

   This version:
     - uses modern "in" and "out" qualifiers
     - removes deprecated fixed-function features
     - is compatible with Panda3D’s GLSL system
*/


in vec4 p3d_Vertex;
/*
   Declares a vertex position input attribute.

   "p3d_Vertex":
     - built-in Panda3D attribute
     - contains the vertex position in model-local space

   Type: vec4
     x, y, z → spatial coordinates
     w       → usually 1.0 for positions
*/


in vec3 p3d_Normal;
/*
   Declares a vertex normal input attribute.

   "p3d_Normal":
     - represents the surface normal at each vertex
     - used for lighting calculations

   Type: vec3 (x, y, z)
*/


out vec3 v_normal;
/*
   Declares an output variable to pass the normal to the fragment shader.

   "v_normal":
     - is interpolated across triangles
     - allows per-fragment lighting calculations
*/


uniform mat3 p3d_NormalMatrix;
/*
   Declares a 3×3 uniform normal transformation matrix.

   "p3d_NormalMatrix":
     - transforms normals correctly under non-uniform scaling
     - typically the inverse transpose of the model-view matrix
     - ensures lighting calculations remain accurate
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a 4×4 uniform matrix for transforming vertices.

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transformation
     - View (camera) transformation
     - Projection transformation

   Converts model-space positions into clip-space coordinates.
*/


void main() {
/*
   Entry point of the vertex shader.

   Responsibilities:
     - transform vertex normals
     - compute final clip-space position
*/


    v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
    /*
       Transforms the normal into eye space and normalizes it.

       Normalization ensures a unit-length vector,
       which is required for correct dot-product lighting calculations.
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

     - normals are interpolated across fragments
     - vertices are assembled into triangles
     - triangles are rasterized
     - the fragment shader runs per fragment
*/
