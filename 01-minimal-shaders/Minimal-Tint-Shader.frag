#version 150
/* 
   Specifies the GLSL version used by this fragment shader.

   GLSL 1.50:
     - requires explicit fragment output variables
     - disallows deprecated gl_FragColor
     - must match the vertex shader version
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "fragColor":
     - represents the final RGBA color
     - is written to the framebuffer

   Components:
     R → red
     G → green
     B → blue
     A → alpha (opacity)
*/


uniform vec3 tint;
/*
   Declares a uniform color tint.

   "vec3" represents an RGB color:
     x → red
     y → green
     z → blue

   "tint":
     - is supplied by the application
     - remains constant for all fragments in a draw call
     - allows the object color to be changed dynamically

   Values are typically in the range 0.0 to 1.0.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function runs once per fragment.
   Its purpose is to determine the final pixel color.
*/


    fragColor = vec4(tint, 1);
    /*
       Assigns the final fragment color.

       "vec4(tint, 1)":
         - uses the RGB components from "tint"
         - sets alpha to 1.0 (fully opaque)

       This results in a solid, uniformly colored object.

       There is:
         - no lighting
         - no texture sampling
         - no shading calculations

       The entire object is tinted
       using the same uniform color.
    */
}