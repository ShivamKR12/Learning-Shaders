#version 150
/*
   Specifies the GLSL language version.
   "#version 150" corresponds to GLSL 1.50 (OpenGL 3.2).

   This version:
     • uses modern "in" and "out" qualifiers
     • no longer supports deprecated "gl_FragColor"
     • ensures compatibility with Panda3D’s GLSL pipeline
*/


in vec3 v_normal;
/*
   "in" declares a per-fragment input varying.

   This value comes directly from the vertex shader's:
       out vec3 v_normal;

   The GPU automatically:
       • takes the three v_normal values at the triangle’s vertices
       • linearly interpolates them across the triangle
       • provides the interpolated value per fragment (pixel)

   Because of interpolation, this incoming normal is
   *not guaranteed* to be unit length, which is why we re-normalize it.
*/


out vec4 fragColor;
/*
   "out" is the output variable for the final fragment color.

   This replaces the old "gl_FragColor" variable from earlier GLSL versions.

   The fragment shader must write to at least one output for the fragment
   to appear on screen. Panda3D doesn't require a specific name — you choose.
*/


void main() {
/*
   Fragment shaders run once per *fragment* (pixel-sized sample).
   After rasterization, every screen pixel inside the triangle
   triggers a call to this main() function.
*/


    vec3 n = normalize(v_normal);
    /*
       Normalize the interpolated normal.

       Interpolation across the surface produces vectors
       whose length is no longer exactly 1.0.

       For lighting and shading, it is essential that normals
       are unit vectors, so we normalize them here.

       Example:
           v_normal = (0.3, 0.6, 0.9)
           length might be > 1 or < 1
           normalize(v_normal) makes its length exactly 1
    */


    fragColor = vec4(n * 0.5 + 0.5, 1.0);
    /*
       Convert the normal vector into a visible RGB color.

       Normals range from -1 to +1 on each axis.

       But colors must be in 0 to 1 range.

       To map:
           -1 → 0
            0 → 0.5
           +1 → 1

       We use:
           n * 0.5 + 0.5

       This shifts and scales the vector so it's displayable as a color.

       Final color:
           fragColor = (R, G, B, A)
           A = 1.0 (fully opaque)

       The result is a "normal visualization":
           • blue-ish for +Z
           • red-ish for +X
           • green-ish for +Y
           • smooth gradients across the surface
    */
}
