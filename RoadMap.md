
---

# 🌱 **0. Prerequisites (Minimal)** [✅ COMPLETED]

These are *tiny* prerequisites and can be learned alongside Step 1.

0.1 — Understand what a shader is (high-level only)

* Shaders are small programs that run on the GPU.
* Vertex shaders: move and transform geometry
* Fragment shaders: color each pixel

0.2 — Know that shaders are written in GLSL ES or GLSL

* Syntax similar to C
* Strict typing and structure

---

# 🟦 **1. Foundation: “GLSL as a Language” (No 3D yet)** [✅ COMPLETED]

Learn GLSL like a programming language *first*.
Very, very small steps.

### 1.1 — Comments

Learn:

```glsl
// comment
/* comment */
```

### 1.2 — Semicolons

Every statement ends with `;`.

### 1.3 — Basic types

* `float`, `int`, `uint`, `bool`

### 1.4 — Vector types

* `vec2`, `vec3`, `vec4`
* Access via `.x`, `.y`, `.z`, `.w`

### 1.5 — Vector constructors

`vec3 v = vec3(1.0, 0.5, 0.2);`

### 1.6 — Swizzling (major GLSL feature)

Learn:

```
v.xyz
v.xxx
v.zx
v.rgba
```

### 1.7 — Arithmetic on vectors

GLSL supports component-wise ops:
`vec3 a = b * c;`

### 1.8 — GLSL functions

Learn how to write:

```glsl
float foo(float x) { return x * 2.0; }
```

### 1.9 — Built-in math functions

Learn:

* `sin`, `cos`, `pow`, `dot`, `cross`
* `normalize`, `length`
* `clamp`, `mix`, `smoothstep`

You will use these constantly.

---

# 🟧 **2. Shader Program Structure (Still no rendering)** [✅ COMPLETED]

Learn the *formal rules* of what a GLSL file MUST contain.

### 2.1 — Required `#version`

For ES 3.00:

```glsl
#version 300 es
```

### 2.2 — Precision qualifiers

Fragment shaders MUST have:
`precision mediump float;`

### 2.3 — `void main()` structure

Every shader MUST end with a `main()`.

### 2.4 — Why vertex and fragment shaders are separate

High-level explanation only.

---

# 🟩 **3. The Minimal Working Shader (First actual shader)** [✅ COMPLETED]

Goal: Display a solid color.

### 3.1 — Minimal vertex shader

```glsl
#version 300 es
precision highp float;

in vec3 position;

void main() {
    gl_Position = vec4(position, 1.0);
}
```

### 3.2 — Minimal fragment shader

```glsl
#version 300 es
precision mediump float;

out vec4 fragColor;

void main() {
    fragColor = vec4(1.0, 0.4, 0.2, 1.0);
}
```

### 3.3 — Understand the pipeline:

* Vertex shader must output **gl_Position**
* Fragment shader must output **fragColor**

---

# 🟧 **4. Vertex Inputs (Attributes)** [✅ COMPLETED]

Now learn where vertex data comes from.

### 4.1 — `in` variables

Example:

```glsl
in vec3 position;
in vec3 normal;
in vec2 uv;
```

### 4.2 — Using attributes to transform a mesh

Learn:

* Model matrix
* View matrix
* Projection matrix

### 4.3 — Basic MVP transform

```glsl
gl_Position = projection * view * model * vec4(position, 1.0);
```

### 4.4 — Learn why the order matters (row-major vs column-major)

---

# 🌕 **5. Uniforms (CPU → GPU Communication)** [✅ COMPLETED]

Uniforms allow your application code to send values to shaders.

### 5.1 — Declaring uniforms

```glsl
uniform float time;
uniform mat4 mvp;
uniform vec3 lightPos;
```

### 5.2 — Updating uniforms from your engine/framework

(e.g., Panda3D, Unity, WebGL)

### 5.3 — Using uniforms in shaders

Example:

```glsl
float brightness = abs(sin(time));
```

---

# 🟦 **6. Passing Values Between Shaders (`in`/`out`)** [✅ COMPLETED]

### 6.1 — Define an output in the vertex shader

```glsl
out vec3 v_normal;
```

### 6.2 — Match it with an input in the fragment shader

```glsl
in vec3 v_normal;
```

### 6.3 — Rule: types MUST match exactly

`vec3` → `vec3`
`vec2` cannot become `vec3`

### 6.4 — Interpolation understanding (smooth vs flat)

---

# 🌈 **7. Color and Lighting Basics** [✅ COMPLETED]

This is the real jump from “I can draw” to “I can shade.”

### 7.1 — Vertex color pass-through

Vertex shader:

```glsl
out vec4 v_color;
v_color = color;
```

Fragment shader:

```glsl
in vec4 v_color;
fragColor = v_color;
```

### 7.2 — Normal pass-through

Learn how normals reach fragment shaders.

### 7.3 — Dot product lighting

**Lambert diffuse:**

```glsl
float NdotL = max(dot(normalize(v_normal), normalize(lightDir)), 0.0);
fragColor = vec4(NdotL);
```

### 7.4 — Add ambient

```glsl
fragColor = vec4(NdotL + 0.1);
```

### 7.5 — Add color

```glsl
fragColor = vec4(baseColor * (NdotL + 0.1), 1.0);
```

---

# 🟫 **8. Texture Sampling** [✅ COMPLETED]

### 8.1 — Declare a sampler

```glsl
uniform sampler2D tex;
```

### 8.2 — Interpolated UVs

```glsl
in vec2 v_uv;
```

### 8.3 — Sample the texture

```glsl
fragColor = texture(tex, v_uv);
```

### 8.4 — Multiply texture with lighting

```glsl
fragColor = texture(tex, v_uv) * lightFactor;
```

---

# 🟨 **9. Intermediate: Writing Useful Effects** [✅ COMPLETED]

### 9.1 — Tinted texture

```glsl
fragColor = texture(tex, v_uv) * tint;
```

### 9.2 — Time-based animation

```glsl
float pulse = abs(sin(time));
```

### 9.3 — UV distortion (waves)

```glsl
vec2 uv2 = v_uv + vec2(sin(uv.y * 10.0 + time) * 0.02);
```

### 9.4 — Alpha cutoff

```glsl
if (texture(tex, v_uv).a < 0.1) discard;
```

---

# 🟪 **10. Intermediate: Vertex Shader Manipulation** [✅ COMPLETED]

### Techniques:

* Waving flags
* Wobbling/scaling
* Exploding meshes
* Morphing shapes

Example: wave vertices

```glsl
position.y += sin(position.x * 3.0 + time) * 0.2;
```

---

# 🟥 **11. Advanced Lighting Models**

### 11.1 — Diffuse (Lambert) [✅ COMPLETED]
* **What:** Basic matte shading based on the angle between the light and the surface normal.
* **How:** `max(dot(N, L), 0.0)`
* **Why:** To give 3D objects a basic sense of volume and directionality.

### 11.2 — Specular Highlights (Phong) [✅ COMPLETED]
* **What:** Shiny, mirror-like reflections on surfaces.
* **How:** Calculate the reflection vector `R = reflect(-L, N)`, then use `pow(max(dot(R, V), 0.0), shininess)`.
* **Why:** Simulates glossy materials like plastic, glass, or polished metal.

### 11.3 — Blinn-Phong
* **What:** An optimization and visual improvement over the standard Phong model.
* **How:** Instead of calculating a reflection vector, find the halfway vector between the light and the view direction: `H = normalize(L + V)`. Then calculate `pow(max(dot(N, H), 0.0), shininess)`.
* **Why:** It is generally faster to compute on older hardware and produces more physically plausible highlights, especially at grazing angles.

### 11.4 — Point and Spot Lights
* **What:** Lights that have a specific position in space, and lose intensity over distance.
* **How:** Calculate the distance from the fragment to the light. Apply an inverse-square attenuation factor (`1.0 / (distance * distance)`). For spotlights, also check the angle between the light-to-fragment vector and the spotlight's forward direction.
* **Why:** Directional lights (like the sun) are infinite. Real scenes need localized lighting like torches, lamps, or streetlights.

### 11.5 — Multiple Lights
* **What:** Supporting more than one light source acting on a surface at once.
* **How:** Pass arrays of light structs (position, color, intensity, type) into the shader via uniforms. Loop through the array, calculate the diffuse and specular for each, and sum them up.
* **Why:** Real scenes are rarely lit by just a single directional light.

---

# 🟧 **12. Surface Details & Realism**

### 12.1 — Normal Mapping
* **What:** Faking high-resolution geometric detail (bumps, scratches, pores) on a flat, low-polygon mesh.
* **How:** Sample a normal map texture. Unpack its `rgb` values to `xyz` directions (`normal = textureColor * 2.0 - 1.0`). Multiply this normal by a Tangent-Bitangent-Normal (TBN) matrix to move it from tangent space into world or view space.
* **Why:** Essential for modern graphics. It allows complex details to react to dynamic lighting without adding millions of polygons to the model.

### 12.2 — Specular / Gloss Mapping
* **What:** Controlling shininess and reflectivity across different parts of a surface.
* **How:** Sample a grayscale texture. Multiply the specular intensity by this texture value, or use it to map between high and low `shininess` exponents.
* **Why:** A surface like a rusty metal plate or a scuffed wooden floor will be shiny in some spots and completely dull in others.

### 12.3 — Rim Lighting / Fresnel
* **What:** Highlighting the extreme edges of a model based on the viewing angle.
* **How:** Use `1.0 - max(dot(N, V), 0.0)` to detect surfaces that are grazing away from the camera.
* **Why:** Often used in stylized/toon rendering to make characters pop from the background. In realistic rendering, it approximates the Fresnel effect (surfaces become more reflective at grazing angles).

---

# 🟨 **13. The Path to PBR (Physically Based Rendering)**

### 13.1 — Understanding Energy Conservation & BRDFs
* **What:** The conceptual foundation of PBR. It states that an object cannot reflect more light than it receives.
* **How:** Replace arbitrary `diffuse + specular` additions with a Bidirectional Reflectance Distribution Function (BRDF) like Cook-Torrance.
* **Why:** Older models (like Phong) require constant tweaking of lights and material values to look good in different environments. PBR materials look correct and consistent under *any* lighting condition.

### 13.2 — The PBR Material Inputs (Metallic-Roughness Workflow)
* **What:** Moving away from traditional "diffuse" and "specular" colors to physical parameters.
* **How:** Adopt the standard PBR textures:
    * **Albedo (Base Color):** The core color, completely devoid of baked-in lighting or shadows.
    * **Roughness:** A grayscale map defining how microscopically bumpy the surface is (replaces the concept of "shininess"). Rough surfaces scatter light; smooth ones reflect it perfectly.
    * **Metallic:** A black-or-white mask defining if the surface is a metal or a dielectric (non-metal). Metals tint their specular reflections with their base color; dielectrics reflect white light.
* **Why:** Standardized parameters based on real-world measured values make asset creation predictable.

### 13.3 — The Cook-Torrance BRDF (Direct Lighting)
* **What:** The specific mathematical equation used to calculate specular reflections in PBR.
* **How:** It uses three interconnected functions:
    * **Normal Distribution Function (NDF - usually Trowbridge-Reitz GGX):** Determines the size and shape of the highlight based on the roughness.
    * **Geometry Function (Schlick-GGX):** Handles micro-shadowing (light being blocked by the microscopic bumps of the surface).
    * **Fresnel Equation (Schlick's approximation):** Calculates the ratio of light that reflects versus light that refracts/absorbs at different viewing angles.
* **Why:** Calculates extremely accurate specular highlights that naturally spread out and dim as the surface roughness increases.

### 13.4 — Image-Based Lighting (IBL) (Ambient Lighting)
* **What:** Using an HDR environment map (HDRI) to light the scene realistically, replacing the flat `ambient = 0.1` constant.
* **How:** 
    * **Diffuse Irradiance:** Precalculate a heavily blurred version of the environment map to act as complex, multi-directional ambient light.
    * **Specular Pre-filter:** Precalculate progressively blurred versions of the environment map to represent reflections at different roughness levels.
    * **BRDF Integration Map:** A 2D lookup texture (LUT) used to approximate the BRDF for indirect light.
* **Why:** True PBR requires the environment itself to act as the light source, ensuring shiny objects reflect the surrounding world accurately and diffuse objects receive bounced light.

---

# 🟩 **14. Required Concepts for PBR Implementation**

### 14.1 — Gamma Correction & Linear Color Space
* **What:** Monitors display colors non-linearly (gamma curves), but math requires linear values.
* **How:** Sample albedo textures and convert them from sRGB to Linear space `pow(color, 2.2)`. Do lighting calculations. At the very end of the fragment shader, convert back to sRGB `pow(color, 1.0/2.2)`.
* **Why:** Without this, lighting math falls apart. Brights blow out, darks crush, and lights fade incorrectly.

### 14.2 — HDR and Tone Mapping
* **What:** PBR lighting often generates color values far above `1.0`, but monitors can only display `0.0` to `1.0`.
* **How:** Render to a floating-point framebuffer. Then run a post-process step (Tone Mapping, e.g., ACES, Reinhard) to gracefully compress those high values down into the `[0, 1]` range.
* **Why:** Prevents ugly, harsh clipping where bright lights hit surfaces.

---

# 🟦 **15. Other Advanced Topics (Optional Branches)**

### Branch A — Post-processing
* Screen-space shaders (rendering a full-screen quad)
* Blur and Bloom
* Depth of Field
* Edge detection

### Branch B — Procedural effects
* Perlin / Simplex Noise
* Fractals
* Procedural pattern generation

### Branch C — Shadow mapping
* Rendering from the light's perspective to a depth texture
* Comparing fragment depths to shadow samplers
* PCF (Percentage-Closer Filtering) for soft shadows

---

# 🟪 **16. Optimization and GPU Architecture Fundamentals**

* Minimize branching
* Prefer vec operations
* Understand precision performance impact
* Reduce texture lookups
* Avoid dependent texture reads when possible

---

* Lambert        → matte
* Phong          → matte + shiny
* Blinn-Phong    → better shiny
* Cook-Torrance  → real physics
* PBR            → system built on Cook-Torrance
* HDR            → lets PBR work
* BRDF           → the equation used
* BSDF           → BRDF + transparency
* BXDF           → general term
