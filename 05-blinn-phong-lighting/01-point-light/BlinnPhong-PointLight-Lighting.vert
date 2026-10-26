#version 150

in vec4 p3d_Vertex;
in vec3 p3d_Normal;

out vec3 v_fragPos;
out vec3 v_normal;

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat3 p3d_NormalMatrix;

void main() {
    /*
       =========================================================
       VIEW SPACE (CAMERA SPACE) COMPUTATION
       =========================================================
       In earlier shaders, we didn't care exactly *where* the object 
       was because directional lights are infinite. 
       
       For Point Lights, we must calculate the exact distance between 
       the Light and the Fragment.
       
       We do our lighting calculations in "View Space" (also called 
       Eye Space or Camera Space).
       
       In View Space:
         - The Camera is always exactly at coordinate (0, 0, 0).
         - It is much easier to calculate the View Vector.
    */


    v_fragPos = (p3d_ModelViewMatrix * p3d_Vertex).xyz;
    /*
       Transforms the vertex position from Model Space into View Space.
       
       "v_fragPos" will be sent to the fragment shader, which will 
       interpolate it. This means every pixel will know its exact 
       physical 3D coordinate relative to the camera!
    */


    v_normal = normalize(p3d_NormalMatrix * p3d_Normal);
    /*
       Transforms the normal into View Space as well. 
       
       It is a fundamental rule of Shader Math:
       All vectors interacting with each other (Normals, Light Directions, 
       View Directions) MUST be in the exact same coordinate space!
    */


    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    /*
       Standard transformation to Clip Space so the GPU can draw the geometry
       onto the 2D screen.
       
       NOTE: gl_Position is just for rendering the pixel location on the monitor. 
       Lighting requires the 3D 'v_fragPos' we calculated above.
    */
}