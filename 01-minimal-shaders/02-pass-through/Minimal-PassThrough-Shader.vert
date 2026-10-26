#version 150
/*  
   Specifies the GLSL version used by this shader.
   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2 era).
   This version uses modern syntax:
       • "in" for vertex inputs
       • "out" for varyings
       • no deprecated keywords like "attribute" or "varying"
*/


in vec4 p3d_Vertex;
/*
   "in" declares a per-vertex input attribute.
   Panda3D automatically provides "p3d_Vertex" for models.

   It contains the vertex position in *model space*:
       (x, y, z, w)
   The 'w' component is normally 1.0 for position vectors.
*/


in vec3 p3d_Normal;
/*
   Another per-vertex input attribute supplied by Panda3D.

   "p3d_Normal" is the surface normal at each vertex.
   It is a direction vector:
       (x, y, z)
   Normals are used in lighting calculations ,
   but here we are passing them to the fragment shader.
*/


out vec3 v_normal;
/*
   "out" declares a varying—data that will be sent from the
   vertex shader to the fragment shader.

   The GPU will:
      • output one v_normal for each vertex
      • interpolate it across the triangle’s surface
      • provide the interpolated value to the fragment shader via `in vec3 v_normal`

   This is the core mechanism for communication between
   vertex → fragment shaders.
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   A "uniform" is a constant value shared by all vertices during one draw call.

   Panda3D automatically supplies this matrix. It combines:
       Model      – transforms the model into world space
       View       – positions world relative to the camera
       Projection – applies perspective transformation

   Together this matrix converts model-space positions into clip space,
   which is required for rendering.
*/


void main() {
/*
   The entry point of the vertex shader.
   This function runs once for every vertex in the model.
*/


    v_normal = normalize(p3d_Normal);
    /*
       Normalize the incoming normal vector.

       Even though most normals are already unit length,
       normalizing ensures correctness, especially if the model
       has scaling applied or the normals are not perfect.

       The resulting v_normal will be smoothly interpolated
       across the triangle in the fragment shader.
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       gl_Position is a built-in output variable that all vertex shaders
       MUST write to.

       This multiplication performs the full transformation:
            model-space
               → world-space
               → view-space (camera)
               → clip-space (before perspective division)

       After this:
           • GPU does perspective division
           • the vertex is projected onto the screen
           • rasterization begins (creating fragments for the fragment shader)
    */
}
