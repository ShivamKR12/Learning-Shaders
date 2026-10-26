#version 150
/* 
   Specifies the GLSL language version used by this vertex shader.

   "#version 150" corresponds to GLSL 1.50,
   introduced with OpenGL 3.2.

   This version:
     - uses modern "in" qualifiers
     - removes deprecated fixed-function pipeline features
     - is fully compatible with Panda3D’s GLSL system
*/


in vec4 p3d_Vertex;
/*
   Declares a vertex position input attribute.

   "in" means this value is provided per vertex
   from the model’s vertex buffer.

   "p3d_Vertex" is a built-in Panda3D attribute
   containing the vertex position in model-local space.

   Type: vec4
     x, y, z → spatial coordinates
     w       → usually 1.0 for positions
*/


uniform mat4 p3d_ModelViewProjectionMatrix;
/*
   Declares a uniform transformation matrix.

   A "uniform":
     - is constant for all vertices in a draw call
     - is supplied by the application (Panda3D)

   "p3d_ModelViewProjectionMatrix" combines:
     - Model transformation
     - View (camera) transformation
     - Projection (perspective) transformation

   This matrix converts model-space positions
   into clip-space coordinates.
*/


uniform float osg_FrameTime;
/*
   Declares a uniform time value.

   "osg_FrameTime":
     - represents elapsed time
     - increases continuously as the application runs
     - is measured in seconds

   This value is commonly used for animation effects.

   Because it is a uniform:
     - all vertices in the same frame
       receive the same time value
*/


void main() {
/*
   Entry point of the vertex shader.

   This function runs once for every vertex
   processed by the GPU.

   The vertex shader’s job is to:
     - optionally modify vertex data
     - output the final clip-space position
*/


    vec3 center = vec3(0.0);
    /*
       Defines a reference point in space.

       "vec3(0.0)":
         - creates a vector (0.0, 0.0, 0.0)
         - represents the origin of model space

       This point will act as the center
       from which vertices are pushed outward.
    */


    vec3 dir = normalize(p3d_Vertex.xyz - center);
    /*
       Computes a direction vector for displacement.

       p3d_Vertex.xyz:
         - extracts the 3D position of the vertex

       p3d_Vertex.xyz - center:
         - creates a vector pointing from the center
           toward the vertex

       normalize(...):
         - converts the vector to unit length
         - preserves direction while removing magnitude

       Result:
         - "dir" points outward from the center
           for each vertex
    */


    float strength = sin(osg_FrameTime) * 0.5;
    /*
       Computes the displacement strength.

       sin(osg_FrameTime):
         - oscillates smoothly between -1 and +1
         - changes over time

       * 0.5:
         - reduces the amplitude
         - limits how far vertices are displaced

       Result:
         - a time-varying value that expands
           and contracts the geometry
    */


    vec4 pos = p3d_Vertex;
    /*
       Creates a local copy of the vertex position.

       This allows modification of the position
       without altering the original input attribute.
    */


    pos.xyz += dir * strength;
    /*
       Offsets the vertex position.

       dir * strength:
         - scales the outward direction vector
           by the current animation strength

       pos.xyz += ...:
         - moves the vertex along that direction

       Effect:
         - vertices move away from or toward the center
         - creating a pulsing or breathing deformation
    */


    gl_Position = p3d_ModelViewProjectionMatrix * pos;
    /*
       Writes the final transformed position.

       "gl_Position" is a required built-in output.

       The multiplication transforms:
         model space → world space
         world space → camera space
         camera space → clip space

       The GPU uses this value to determine
       where the vertex appears on screen.
    */
}


/*
   After the vertex shader finishes:

     - positions are normalized
     - primitives are assembled
     - triangles are rasterized
     - the fragment shader runs per fragment

   This vertex shader performs a time-based
   radial deformation centered at the origin.
*/
