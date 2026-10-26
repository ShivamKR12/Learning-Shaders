#version 150
/* 
   This sets the GLSL language version for the shader.

   "#version 150" means GLSL 1.50 (OpenGL 3.2 era).
   Using this version:
     - enables modern "in" and "out" syntax
     - disables older deprecated keywords like "attribute" and "varying"
     - ensures compatibility with Panda3D's default GLSL system
*/


in vec4 p3d_Vertex;
/* 
   "in" means this variable is an input attribute to the vertex shader.
   It comes from the model's vertex data.

   Panda3D provides built-in attribute names.
   "p3d_Vertex" contains the position of each vertex in the model's local space.
   Type: vec4 (x, y, z, w).
   w is usually 1.0 for positions.
*/


in vec3 p3d_Normal;
/*
   Another input attribute provided by Panda3D.

   "p3d_Normal" contains the vertex's surface normal:
     - a 3D direction vector
     - used for lighting in more advanced shaders
     - not used in this simple shader, but still auto-sent by Panda3D

   Type: vec3 (x, y, z)
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   A "uniform" is a global variable supplied by the application (Panda3D).
   It does NOT change between vertices during the draw call.

   "mat4" means a 4×4 matrix.

   "p3d_ModelViewProjectionMatrix" is a built-in Panda3D uniform
   that combines three transformations:

     Model      – places the model in the world
     View       – places the world relative to the camera
     Projection – applies perspective

   Combined this transforms positions into clip space.

   Panda3D calculates and updates this automatically every frame.
*/


void main() {
/*
   The entry point of the vertex shader.
   Every vertex processed by the GPU will run this function once.

   The goal of a vertex shader is to output a final position for each vertex.
*/


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       "gl_Position" is a built-in output variable required by GLSL.

       The GPU uses gl_Position to determine where on the screen
       the vertex should appear.

       This line applies the transformation:
          final_position = MVP_matrix × vertex_position

       Breaking down the multiplication:

       p3d_Vertex:
         - The vertex position in model-local coordinates (vec4)

       p3d_ModelViewProjectionMatrix:
         - A mat4 that converts model-space coordinates
           → world-space
           → camera/view-space
           → clip-space
       
       The result is a vec4 representing the clip-space position.

       Without writing to gl_Position, the vertex would not appear onscreen.
    */
}


/*
  After the vertex shader finishes:
    - gl_Position undergoes perspective division (divided by w)
    - The result is converted into normalized device coordinates
    - The GPU rasterizes triangles
    - The fragment shader then runs for each pixel

  This simple shader only handles positions,
  so the model renders as an unlit, uncolored object
  (unless the fragment shader assigns color).
*/
