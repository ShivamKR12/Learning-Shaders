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
   Declares a uniform base color.

   "vec3" represents an RGB color:
     x → red
     y → green
     z → blue

   "tint":
     - is supplied by the application
     - remains constant for all fragments in a draw call
     - defines the base color of the object

   Color values are typically in the range 0.0 to 1.0.
*/


uniform float osg_FrameTime;
/*
   Declares a uniform time value.

   "osg_FrameTime":
     - represents elapsed time in seconds
     - increases continuously as the application runs
     - is identical for all fragments in the same frame

   This value is commonly used for
   time-based animation effects.
*/


void main() {
/*
   Entry point of the fragment shader.

   This function runs once per fragment
   generated during rasterization.

   The fragment shader determines the final pixel color.
*/


    float pulse = 0.5 + 0.5 * sin(osg_FrameTime * 5.0);
    /*
       Computes a pulsing intensity value.

       sin(osg_FrameTime * 5.0):
         - produces a smooth oscillation between -1 and +1
         - oscillates faster due to the 5.0 multiplier

       0.5 + 0.5 * sin(...):
         - remaps the range from [-1, +1]
           to [0.0, 1.0]

       Result:
         - "pulse" smoothly increases and decreases over time
         - suitable for brightness or intensity modulation
    */


    vec3 tintColor = tint * pulse;
    /*
       Modulates the base tint color.

       tint * pulse:
         - scales the RGB color by the pulse value
         - makes the color brighter and darker over time

       This creates a visual pulsing effect
       without changing the hue of the color.
    */


    fragColor = vec4(tintColor, 1);
    /*
       Assigns the final fragment color.

       "vec4(tintColor, 1)":
         - uses the pulsed RGB color
         - sets alpha to 1.0 (fully opaque)

       The result is a solid-colored object
       whose brightness pulses over time.

       No lighting or texture sampling is performed.
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - geometry is transformed normally
     - color is defined by a uniform tint
     - brightness pulses smoothly over time
     - the object appears as a flat, animated color
*/
