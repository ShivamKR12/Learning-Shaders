#version 150
/* 
   Specifies the GLSL version used by this fragment shader.

   GLSL 1.50:
     - requires explicit fragment outputs
     - disallows deprecated gl_FragColor
     - must match the vertex shader version
*/


in vec2 v_uv;
/*
   Declares an input variable from the vertex shader.

   "v_uv":
     - contains interpolated texture coordinates
     - varies smoothly across the surface of the triangle

   Each fragment receives its own UV value
   based on its position within the triangle.
*/


out vec4 fragColor;
/*
   Declares the output color of the fragment shader.

   "fragColor" represents:
     - the final RGBA color written to the framebuffer

   Components:
     R → red
     G → green
     B → blue
     A → alpha (opacity)

   The name is user-defined and not engine-specific.
*/


uniform sampler2D tex;
/*
   Declares a 2D texture sampler.

   "sampler2D":
     - represents a 2D texture bound by the application
     - allows sampling color data using UV coordinates

   Panda3D binds the actual texture object
   to this sampler before drawing.
*/


uniform float osg_FrameTime;
/*
   Declares a uniform time value.

   "osg_FrameTime":
     - increases continuously over time
     - is measured in seconds
     - is the same for all fragments in the frame

   This value is commonly used for animation effects.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function is executed once per fragment
   produced by rasterizing the triangles.

   The fragment shader determines the final pixel color.
*/


    float wave = sin(v_uv.y * 10.0 + osg_FrameTime * 3.0) * 0.02;
    /*
       Computes a horizontal wave offset.

       Breakdown of the expression:

       v_uv.y * 10.0:
         - increases the frequency of the wave vertically
         - creates multiple wave cycles across the texture

       osg_FrameTime * 3.0:
         - advances the wave over time
         - controls animation speed

       sin(...):
         - produces a smooth oscillation between -1 and +1

       * 0.02:
         - reduces the amplitude
         - keeps the distortion subtle

       Result:
         - a small time-varying offset value
    */


    vec2 distortedUV = v_uv + vec2(wave, 0.0);
    /*
       Offsets the texture coordinates.

       The wave is applied only to the X (U) axis:
         - horizontal distortion
         - vertical coordinates remain unchanged

       This creates a rippling or heat-wave effect
       across the texture.
    */


    vec4 texColor = texture(tex, distortedUV);
    /*
       Samples the texture using the distorted UVs.

       "texture(...)":
         - looks up the color at the given coordinates
         - performs filtering based on texture settings

       The returned value is a vec4:
         R, G, B → color channels
         A       → alpha channel
    */


    fragColor = vec4(texColor.rgb, texColor.a);
    /*
       Assigns the final fragment color.

       The RGB and alpha values are taken directly
       from the sampled texture.

       This preserves:
         - the original texture colors
         - the original transparency

       The only modification applied is
       the UV distortion.
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - geometry is rendered normally
     - UV coordinates are passed from vertices to fragments
     - the texture is sampled with animated distortion
     - the result appears as a subtle wave effect
*/
