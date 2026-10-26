#version 150
/* 
   Specifies the version of GLSL the compiler must use.
   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2).

   This version:
     - uses modern "in" and "out" syntax
     - disallows old keywords like "gl_FragColor"
     - ensures compatibility with Panda3D’s shader system
*/


out vec4 fragColor;
/*
   Declares an output variable from the fragment shader.

   "out" means:
      - this variable is the final color the GPU will write
        to the current framebuffer (usually the screen).
      - this replaces older "gl_FragColor", which is deprecated
        in GLSL versions 130+.

   "vec4" means a 4-component vector:
      (red, green, blue, alpha)

   The name "fragColor" is chosen by you.
   Panda3D does NOT require a specific name; any valid out variable works.

   Every pixel (fragment) produced by rasterization will run this shader
   and produce its own "fragColor" value.
*/


void main() {
/*
   Standard function required by GLSL.
   The fragment shader entry point.

   This function is run once per *fragment* (pixel-sized sample)
   that results from rasterizing a triangle.

   The main purpose of a fragment shader is to determine the final color
   and sometimes other values (like depth).
*/


    fragColor = vec4(1.0, 0.3, 0.2, 1.0);  // solid orange color
    /*
       Assigns the output color.

       "vec4(1.0, 0.3, 0.2, 1.0)" is an RGBA color:
         R = 1.0 (full red)
         G = 0.3 (30% green)
         B = 0.2 (20% blue)
         A = 1.0 (fully opaque)

       This combination produces a warm orange/red color.

       Because this is the only line inside main(),
       every pixel will be this exact solid color.

       There is no lighting, no texturing, no input values —
       just a constant color.
    */


}
/*
   End of the main() function and end of the shader.
*/
