#version 150
/*
   Specifies the GLSL version.

   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2 core profile).

   This version:
     - uses "in" and "out" instead of the old "attribute" and "varying"
     - requires explicit outputs for later pipeline stages
     - is compatible with Panda3D’s modern shader system
*/


in vec4 p3d_Vertex;
/*
   Declares an input attribute to the vertex shader.

   "in" means:
     - this value is provided per-vertex by the application (Panda3D).

   "vec4" means:
     - (x, y, z, w) coordinates in object (model) space.

   "p3d_Vertex":
     - is a built-in Panda3D attribute
     - represents the position of the vertex before any transforms
*/


in vec3 p3d_Normal;
/*
   Declares another per-vertex input attribute.

   "vec3" because normals are 3D direction vectors (x, y, z).

   "p3d_Normal":
     - is provided automatically by Panda3D
     - represents the surface normal in object (model) space
     - used for lighting calculations
*/


out vec3 v_normal;
/*
   Declares an output variable from the vertex shader.

   "out" means:
     - this value will be passed to the next pipeline stage
       (typically the fragment shader).

   "v_normal":
     - is a user-defined name
     - will be interpolated across the triangle
     - each fragment will receive a smoothly interpolated normal
*/


uniform mat3 p3d_NormalMatrix;
/*
   Declares a uniform matrix.

   "uniform" means:
     - this value is constant for all vertices in a draw call
     - it is set by Panda3D, not computed in the shader.

   "mat3":
     - a 3×3 matrix used for transforming direction vectors.

   "p3d_NormalMatrix":
     - is provided automatically by Panda3D
     - typically equals the inverse transpose of the model-view matrix
     - ensures normals remain correct under scaling and rotation
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares another uniform matrix.

   "mat4":
     - a 4×4 matrix used for transforming positions.

   "p3d_ModelViewProjectionMatrix":
     - combines:
         * Model matrix (object → world space)
         * View matrix  (world → camera space)
         * Projection matrix (camera → clip space)
     - provided automatically by Panda3D
*/


void main() {
/*
   Required entry point for the vertex shader.

   This function runs once per vertex.

   The main responsibilities of a vertex shader are:
     - transform vertex positions into clip space
     - compute values (like normals, texture coordinates, etc.)
       that will be passed to the fragment shader
*/


    v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
    /*
       Transforms and normalizes the surface normal.

       Steps:
         1) p3d_NormalMatrix * p3d_Normal
            - transforms the normal from object space
              into view (camera) space.

         2) normalize(...)
            - ensures the vector has unit length (length = 1)
            - required for correct lighting calculations

       The resulting normal is stored in "v_normal" and sent
       to the fragment shader, where it will be interpolated
       per pixel.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Computes the final clip-space position of the vertex.

       "gl_Position":
         - is a built-in GLSL output required by the pipeline
         - determines where the vertex appears on screen.

       The multiplication applies:
         Object Space → World Space → View Space → Clip Space

       Without assigning gl_Position, the vertex would not
       appear on screen.
    */
}
/*
   End of the main() function and end of the vertex shader.
*/
