#version 150
/* 
   Specifies the GLSL version used by this fragment shader.

   GLSL 1.50:
     - requires explicit fragment outputs
     - disallows deprecated gl_FragColor
     - must match the vertex shader version
*/


in vec3 v_normal;
/*
   Declares an input variable from the vertex shader.

   "v_normal":
     - contains the interpolated surface normal
     - varies smoothly across the surface

   Each fragment receives its own normal vector,
   based on its position within the triangle.
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

   This function is executed once per fragment
   produced by rasterization.

   The fragment shader determines the final pixel color.
*/


    vec3 n = normalize(v_normal);
    /*
       Normalizes the interpolated normal.

       Even though normals were normalized in the vertex shader:
         - interpolation can change their length

       Normalizing again ensures:
         - the vector has unit length
         - consistent visual results
    */


    fragColor = vec4(n * 0.5 + 0.5, 1.0);
    /*
       Converts the normal vector into a visible color.

       n is in the range:
         [-1.0, +1.0]

       n * 0.5 + 0.5:
         - remaps the range to [0.0, 1.0]
         - suitable for RGB color output

       Result:
         - X normal → red channel
         - Y normal → green channel
         - Z normal → blue channel

       This produces a colorful visualization
       of surface directions.

       Alpha is set to 1.0 (fully opaque).
    */
}


/*
   End of the fragment shader.

   Combined effect of both shaders:

     - vertices pulse outward along their normals
     - the surface deforms smoothly over time
     - normals are visualized as colors
     - the object appears animated and color-coded
*/
