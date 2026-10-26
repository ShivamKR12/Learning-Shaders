#version 150
/* 
   Specifies the GLSL version used by this fragment shader.

   GLSL 1.50:
     - requires explicit fragment outputs
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


void main() {
/*
   Entry point of the fragment shader.

   This function runs once per fragment
   produced during rasterization.

   The fragment shader determines the final pixel color.
*/


    fragColor = vec4(1.0, 1.0, 1.0, 1.0);
    /*
       Assigns a constant color to every fragment.

       vec4(1.0, 1.0, 1.0, 1.0):
         - full red
         - full green
         - full blue
         - fully opaque

       The object is rendered as solid white.

       No lighting, textures, or shading are applied.
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - vertices rotate around Y over time
     - rotation depends on vertex height
     - the geometry appears to twist or spiral
     - the object is rendered as flat white
*/
