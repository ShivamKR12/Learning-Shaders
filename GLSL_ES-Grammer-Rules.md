# OpenGL ES Shading Language (GLSL ES): The Complete Grammar, Syntax & Specification Reference

A comprehensive, authoritative specification and language reference manual for the **OpenGL ES Shading Language (GLSL ES)**. This document serves as both a standalone guide for mobile and web graphics (OpenGL ES 2.0 through 3.2, WebGL 1.0, and WebGL 2.0) and an in-depth companion to [`GLSL-Grammer-Rules.md`](file:///D:/Learning-Shaders/GLSL-Grammer-Rules.md), detailing the architectural paradigms, precision rules, compiler constraints, and syntactic differences between Desktop GLSL and GLSL ES.

---

## 📑 Table of Contents

1. [Architectural Overview & The Mobile Paradigm](#1-architectural-overview--the-mobile-paradigm)
   - [Desktop IMR vs. Mobile TBDR Architectures](#11-desktop-imr-vs-mobile-tbdr-architectures)
   - [Why GLSL ES Diverges from Desktop GLSL](#12-why-glsl-es-diverges-from-desktop-glsl)
2. [GLSL ES Version Evolution & Compatibility Matrix](#2-glsl-es-version-evolution--compatibility-matrix)
   - [Version Matrix (GLSL ES 1.00 through 3.20 & WebGL)](#21-version-matrix)
   - [Desktop GLSL vs. GLSL ES Version Equivalence](#22-desktop-glsl-vs-glsl-es-version-equivalence)
3. [Source Code Structure & Preprocessor Directives](#3-source-code-structure--preprocessor-directives)
   - [Version Declaration Syntax Rules](#31-version-declaration-syntax-rules)
   - [Built-in Macros & Feature Detection](#32-built-in-macros--feature-detection)
   - [The Extension System (`#extension`)](#33-the-extension-system)
4. [The Precision System: The Core Pillar of GLSL ES](#4-the-precision-system-the-core-pillar-of-glsl-es)
   - [Precision Qualifiers (`highp`, `mediump`, `lowp`)](#41-precision-qualifiers)
   - [Floating-Point Hardware Encodings & Ranges](#42-floating-point-hardware-encodings--ranges)
   - [Integer Precision & Formats](#43-integer-precision--formats)
   - [Default Precision Rules by Stage & The Fragment Float Mandate](#44-default-precision-rules-by-stage)
   - [Precision Promotion & Expression Evaluation](#45-precision-promotion--expression-evaluation)
   - [Dual-Issue ALU Packing & Mobile Optimization](#46-dual-issue-alu-packing--mobile-optimization)
5. [Type System & Desktop Divergences](#5-type-system--desktop-divergences)
   - [Scalar & Vector Types](#51-scalar--vector-types)
   - [Matrix Types & Memory Layout](#52-matrix-types--memory-layout)
   - [Opaque Types (Samplers, Images, Atomics)](#53-opaque-types)
   - [Omitted Desktop Types (No `double`, No `sampler1D`)](#54-omitted-desktop-types)
   - [Structs, Arrays, and Dynamic Indexing Limits](#55-structs-arrays--indexing-limits)
   - [Strict Type Casting & Implicit Conversion Rules](#56-strict-type-casting)
6. [Storage, Parameter & Layout Qualifiers](#6-storage-parameter--layout-qualifiers)
   - [Legacy Qualifiers (`attribute`, `varying`) vs Modern (`in`, `out`)](#61-legacy-vs-modern-storage-qualifiers)
   - [Function Parameter Qualifiers (`in`, `out`, `inout`)](#62-function-parameter-qualifiers)
   - [Layout Qualifiers (`layout(...)`) in ES 3.00+](#63-layout-qualifiers)
   - [Interpolation Qualifiers (`smooth`, `flat`, `centroid`, `sample`)](#64-interpolation-qualifiers)
   - [Invariance (`invariant`) and Multi-Pass Z-Fighting Prevention](#65-invariance--exactness)
7. [Expressions, Operators & Swizzling](#7-expressions-operators--swizzling)
   - [Operator Precedence & Integer Bitwise Operator Availability](#71-operator-precedence)
   - [Vector Swizzling Rules](#72-vector-swizzling-rules)
   - [Matrix and Vector Arithmetic Semantics](#73-matrix-and-vector-arithmetic)
8. [Control Flow, Loops & Branching Divergence](#8-control-flow-loops--branching-divergence)
   - [The Strict ES 1.00 Loop Restrictions (Appendix A Rules)](#81-the-strict-es-100-loop-restrictions)
   - [Modern Control Flow in ES 3.00+ (`switch`, Dynamic Loops)](#82-modern-control-flow-in-es-300)
   - [The Hidden Cost of `discard` on Mobile TBDR GPUs](#83-the-hidden-cost-of-discard-on-mobile-tbdr-gpus)
9. [Uniform Buffers (UBO) & Shader Storage Buffers (SSBO)](#9-uniform-buffers-ubo--shader-storage-buffers-ssbo)
   - [Uniform Buffer Objects & `std140` Alignment (ES 3.00+)](#91-uniform-buffer-objects-ubo)
   - [Shader Storage Buffer Objects & `std430` Alignment (ES 3.10+)](#92-shader-storage-buffer-objects-ssbo)
10. [Built-in Variables by Pipeline Stage](#10-built-in-variables-by-pipeline-stage)
    - [Vertex Shader Built-ins](#101-vertex-shader-built-ins)
    - [Fragment Shader Built-ins](#102-fragment-shader-built-ins)
    - [Compute Shader Built-ins (ES 3.10+)](#103-compute-shader-built-ins)
    - [Tessellation & Geometry Shader Built-ins (ES 3.20)](#104-tessellation--geometry-shader-built-ins)
11. [Standard Library Built-in Functions](#11-standard-library-built-in-functions)
    - [Math, Geometric & Relational Functions](#111-math-geometric--relational-functions)
    - [Texture Sampling Function Evolution](#112-texture-sampling-function-evolution)
    - [Screen-Space Derivatives (`dFdx`, `dFdy`, `fwidth`)](#113-screen-space-derivatives)
    - [Compute Synchronization & Memory Barriers (ES 3.10+)](#114-compute-synchronization--memory-barriers)
12. [Subpass & Framebuffer Fetch (`GL_EXT_shader_framebuffer_fetch`)](#12-subpass--framebuffer-fetch)
13. [Comprehensive Comparison Matrix: Desktop GLSL vs. GLSL ES](#13-comprehensive-comparison-matrix-desktop-glsl-vs-glsl-es)
14. [Complete Desktop GLSL to GLSL ES Porting Guide](#14-complete-desktop-glsl-to-glsl-es-porting-guide)
15. [Mobile Performance & Shader Optimization Best Practices](#15-mobile-performance--shader-optimization-best-practices)
16. [Common GLSL ES Compiler Pitfalls, Traps & Diagnostics](#16-common-glsl-es-compiler-pitfalls-traps--diagnostics)

---

# 1. Architectural Overview & The Mobile Paradigm

The OpenGL ES Shading Language (GLSL ES) is a tailored derivative of the desktop OpenGL Shading Language (GLSL), engineered specifically for resource-constrained environments: smartphones, tablets, embedded hardware, automotive consoles, and web browsers (via WebGL).

While Desktop GLSL assumes discrete graphics processing units (GPUs) powered by high-wattage power supplies (150W–450W) and direct, high-bandwidth VRAM buses (hundreds of GB/s to TB/s), GLSL ES is designed for mobile System-on-Chips (SoCs) operating within strict thermal and battery envelopes (2W–15W) with shared Unified Memory Architectures (LPDDR).

```
  ┌──────────────────────────────────────────────────────────────┐
  │                 DESKTOP WORKSTATION / PC                     │
  │  [CPU] <══ PCIe Bus (16-64 GB/s) ══> [Discrete GPU + VRAM]   │
  │  Architecture: Immediate Mode Rendering (IMR)               │
  │  Thermal / Power Envelope: 150W - 450W                       │
  │  VRAM Bandwidth: 500 GB/s - 1000+ GB/s                       │
  │  Precision: 32-bit (FP32) & 64-bit (FP64) standard           │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │                   MOBILE SOC / EMBEDDED                      │
  │  [CPU + GPU + NPU on Single Die] <══> [Unified LPDDR RAM]    │
  │  Architecture: Tile-Based (TBDR / TBR)                       │
  │  Thermal / Power Envelope: 2W - 10W (Strict Passive Cooling) │
  │  Shared Memory Bandwidth: 25 GB/s - 80 GB/s (Shared with OS) │
  │  Precision: Explicit 16-bit (FP16/half) & 32-bit (FP32)      │
  └──────────────────────────────────────────────────────────────┘
```

### 1.1 Desktop IMR vs. Mobile TBDR Architectures

To write performant GLSL ES shaders, a developer must understand how mobile silicon processes graphics compared to desktop GPUs:

1. **Immediate Mode Rendering (IMR - Desktop Nvidia / AMD):**
   - The GPU processes primitives as they are submitted by the application.
   - For every triangle, the rasterizer generates fragments and immediately executes the fragment shader.
   - Pixels are read from and written to external VRAM framebuffers (color, depth, stencil) continuously.
   - If an opaque triangle covers an earlier triangle drawn at the same pixel, the earlier fragment shader work was completely wasted (overdraw), unless Hardware Early-Z successfully rejects it.

2. **Tile-Based Deferred Rendering (TBDR - Apple Silicon, Imagination PowerVR, ARM Mali, Qualcomm Adreno):**
   - The screen is divided into small rectangular tiles (typically 16×16 or 32×32 pixels).
   - **Binning / Tiling Phase:** The vertex shaders execute first for all scene geometry. Triangles are sorted and assigned into per-tile lists ("bins").
   - **Render Phase:** The GPU processes one tile at a time. The entire tile's color, depth, and stencil buffers reside in high-speed, on-chip SRAM cache (Tile Buffer / Local Memory).
   - **Hidden Surface Removal (HSR / Early-Z):** In architectures like PowerVR and Apple Silicon, fragment shaders are deferred until *after* all geometry for that tile has been depth-tested. Fragments that are occluded are discarded *before their fragment shader ever executes*, eliminating overdraw entirely.
   - **Resolve:** Once all fragments within a tile are finished, the final color is written out to main system memory in a single burst.

### 1.2 Why GLSL ES Diverges from Desktop GLSL

Because external memory bandwidth is the single largest consumer of battery power and generator of heat on mobile devices, GLSL ES introduces language features and restrictions specifically designed to minimize memory access and ALU power:

- **Mandatory Precision Qualifiers (`highp`, `mediump`, `lowp`):** Allows mobile ALUs to execute arithmetic at 16-bit half precision (FP16) or 8/10-bit fixed point, doubling instruction throughput and cutting register file power consumption in half.
- **Omission of Double Precision (`double`, `dvec`, `dmat`):** Eliminates silicon area and power draw for 64-bit floating-point ALUs.
- **Omission of 1D Textures (`sampler1D`):** Hardware samplers on mobile silicon only implement 2D, 3D, and Cube sampling logic.
- **Framebuffer Fetch Extensions:** Permits fragment shaders to read the existing tile buffer contents directly from on-chip SRAM without paying the bandwidth penalty of writing out to and re-sampling from external render targets.
- **Stricter Loop & Dynamic Indexing Rules (ES 1.00 / 2.0):** Allowed early mobile silicon without full branch predictors or register stack indirect-addressing to unroll loops at compile-time.

---

# 2. GLSL ES Version Evolution & Compatibility Matrix

GLSL ES has evolved across four major specifications, paired synchronously with the underlying OpenGL ES and WebGL specifications.

### 2.1 Version Matrix

| GLSL ES Version | Host API | Web Standard | Core Stage Capabilities | Primary Defining Features |
| :--- | :--- | :--- | :--- | :--- |
| **`#version 100`** | OpenGL ES 2.0 | **WebGL 1.0** | Vertex, Fragment | Fixed pipeline replaced; `attribute`, `varying`, `uniform`; `gl_FragColor`; precision qualifiers introduced. |
| **`#version 300 es`** | OpenGL ES 3.0 | **WebGL 2.0** | Vertex, Fragment | Unified `in`/`out`; Multiple Render Targets (MRT) via user `out`; Uniform Buffer Objects (UBO); 3D & 2DArray textures; integer bitwise ops; screen derivatives core. |
| **`#version 310 es`** | OpenGL ES 3.1 | — | Vertex, Fragment, **Compute** | **Compute Shaders** (`local_size_x/y/z`); Shader Storage Buffer Objects (SSBO / `std430`); Image load/store; atomic counters; `textureGather`. |
| **`#version 320 es`** | OpenGL ES 3.2 | — | Vertex, **Tessellation**, **Geometry**, Fragment, Compute | **Tessellation Control/Eval**, **Geometry Shaders**; ASTC texture compression; texture buffers (`samplerBuffer`); multisample array textures. |

### 2.2 Desktop GLSL vs. GLSL ES Version Equivalence

When reading or porting shaders between Desktop OpenGL and OpenGL ES, use this direct equivalence mapping:

```
  ┌────────────────────────────────────────────────────────┐
  │           GLSL VERSION CORRESPONDENCE MAPPING          │
  ├────────────────────────────┬───────────────────────────┤
  │ Desktop GLSL Version       │ Equivalent GLSL ES Spec   │
  ├────────────────────────────┼───────────────────────────┤
  │ GLSL 1.10 / 1.20           │ GLSL ES 1.00 (ES 2.0)     │
  │ GLSL 1.30 / 1.40 / 1.50    │ Transitional Desktop era  │
  │ GLSL 3.30 Core             │ GLSL ES 3.00 (ES 3.0)     │
  │ GLSL 4.30 Core             │ GLSL ES 3.10 (ES 3.1)     │
  │ GLSL 4.50 Core             │ GLSL ES 3.20 (ES 3.2)     │
  └────────────────────────────┴───────────────────────────┘
```

> [!IMPORTANT]
> Notice the version declaration tokens:
> - In GLSL ES 1.00: `#version 100` (**no `es` token**).
> - In GLSL ES 3.00+: `#version 300 es`, `#version 310 es`, `#version 320 es` (**the `es` token is mandatory**). If `es` is omitted, the compiler assumes desktop OpenGL Core profile (e.g. GLSL 3.00/3.30).

---

# 3. Source Code Structure & Preprocessor Directives

### 3.1 Version Declaration Syntax Rules

The `#version` directive must appear on the very first non-whitespace, non-comment line of any GLSL ES translation unit.

```glsl
// Valid GLSL ES 1.00 (OpenGL ES 2.0 / WebGL 1.0)
#version 100

// Valid GLSL ES 3.00 (OpenGL ES 3.0 / WebGL 2.0)
#version 300 es

// Valid GLSL ES 3.10 (OpenGL ES 3.1)
#version 310 es

// Valid GLSL ES 3.20 (OpenGL ES 3.2)
#version 320 es
```

If the `#version` directive is absent:
- In OpenGL ES environments, the compiler defaults to **GLSL ES 1.00**.
- In Desktop OpenGL environments, the compiler defaults to **GLSL 1.10**.

### 3.2 Built-in Macros & Feature Detection

The GLSL ES preprocessor defines standardized macros to allow cross-platform source code to adapt between desktop and mobile targets:

| Macro | Defined In | Type | Value / Purpose |
| :--- | :--- | :--- | :--- |
| `GL_ES` | All GLSL ES specifications | Integer | Defined as integer `1` on all OpenGL ES / WebGL implementations. Absent on desktop core profiles. |
| `__VERSION__` | All specifications | Integer | Decimal integer representing language version (`100`, `300`, `310`, `320`). |
| `__LINE__` | All specifications | Integer | The current source line number. |
| `__FILE__` | All specifications | Integer | The current source string / file index number. |
| `GL_FRAGMENT_PRECISION_HIGH` | Fragment stage (ES 1.00 / 3.00+) | Integer | Defined as `1` if the fragment shader hardware natively supports `highp` float precision. |

#### Idiomatic Cross-Platform Header Example:

```glsl
#if defined(GL_ES)
    // Running on mobile OpenGL ES or WebGL
    #if defined(GL_FRAGMENT_PRECISION_HIGH)
        precision highp float;
        precision highp int;
    #else
        precision mediump float;
        precision mediump int;
    #endif
#else
    // Running on desktop OpenGL: precision qualifiers are valid but ignored
    #version 330 core
#endif
```

### 3.3 The Extension System (`#extension`)

Extensions enable optional hardware capabilities or bridge versions. The grammar is strictly defined as:

```glsl
#extension <extension_name> : <behavior>
```

#### Allowed Behaviors:
- `require`: The shader compilation fails immediately if the driver does not support the extension.
- `enable`: Enables the extension if supported; issues a compiler warning if not supported.
- `warn`: Enables the extension if supported; issues a warning on any use of its features.
- `disable`: Disables support for the extension.

#### Crucial GLSL ES Extensions:

```glsl
// Enable screen-space derivatives in GLSL ES 1.00 (WebGL 1.0)
#extension GL_OES_standard_derivatives : enable

// Enable explicit mipmap LOD sampling in GLSL ES 1.00 fragment shaders
#extension GL_EXT_shader_texture_lod : enable

// Enable direct on-chip framebuffer / tile-buffer reads (TBDR subpass emulation)
#extension GL_EXT_shader_framebuffer_fetch : enable

// Enable floating-point texture rendering in ES 2.0 / 3.0
#extension GL_EXT_color_buffer_float : enable
```

---

# 4. The Precision System: The Core Pillar of GLSL ES

The precision system is the most significant semantic difference between Desktop GLSL and GLSL ES. In Desktop GLSL, precision qualifiers (`highp`, `mediump`, `lowp`) are accepted by the compiler for backwards compatibility but are largely treated as no-ops—desktop GPUs execute nearly all calculations at full 32-bit floating-point (FP32).

In GLSL ES, precision qualifiers are **functional hardware directives** that dictate whether calculations run on full 32-bit ALUs, 16-bit half-precision ALUs, or 8-bit fixed-point units.

### 4.1 Precision Qualifiers

GLSL ES defines three precision levels:

```glsl
highp    // Highest precision, standard 32-bit floating point or integer
mediump  // Medium precision, typically 16-bit half-float (FP16) or 16-bit integer
lowp     // Low precision, typically 8-bit to 10-bit fixed-point (normalized colors)
```

Precision qualifiers can be applied to individual variable declarations, function parameters, struct members, or set globally as defaults:

```glsl
highp mat4 modelViewMatrix;
mediump vec3 normal;
lowp vec4 surfaceColor;

mediump float calculateAttenuation(highp vec3 worldPos, mediump float radius);
```

### 4.2 Floating-Point Hardware Encodings & Ranges

The GLSL ES specification establishes minimum mathematical requirements for each qualifier. Mobile GPU vendors implement these in silicon as follows:

| Qualifier | Format Representation | Exponent Range | Mantissa Bits | Decimal Precision | Approximate Magnitude Range | Typical Silicon ALU |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`highp`** | IEEE 754 Single (FP32) | 8-bit (-126 to +127) | 23-bit | ≈ 7.22 digits | ≈ ±1.18e-38 to ±3.40e+38 | Dedicated FP32 Core |
| **`mediump`** | IEEE 754 Half (FP16) | 5-bit (-14 to +15) | 10-bit | ≈ 3.31 digits | ≈ ±6.10e-5 to ±65504.0 | Dual-packed FP16 Core |
| **`lowp`** | Fixed-point / Byte | N/A | 8–10 bit | 2⁻⁸ ≈ 0.0039 | Minimum [-2.0, +2.0] | Packed Color Interpolator |

> [!WARNING]
> **The `mediump` Overflow Trap:** The maximum representable number in standard `mediump` (FP16) is **`65504.0`**.
> - Computing world-space coordinate distances: `length(worldPos - camPos)` will square the distances internally ($x^2 + y^2 + z^2$). If distance exceeds $\sqrt{65504} \approx 256.0$, `mediump` overflows to $+\infty$, turning surfaces pitch black or creating visual artifacts.
> - **Rule:** Always use `highp` for vertex positions, UV texture coordinates, view-space depth, world positions, and projection matrices.

### 4.3 Integer Precision & Formats

Integer precision similarly dictates bit-depth and integer wrapping behavior:

| Qualifier | Signed Range | Unsigned Range | Minimum Bit-Depth |
| :--- | :--- | :--- | :--- |
| **`highp`** | [-2³¹, 2³¹ - 1] | [0, 2³² - 1] | 32-bit two's complement |
| **`mediump`** | [-2¹⁵, 2¹⁵ - 1] (-32768 to 32767) | [0, 2¹⁶ - 1] (0 to 65535) | 16-bit two's complement |
| **`lowp`** | [-256, 255] | [0, 511] | 9-bit signed / 8-bit unsigned |

### 4.4 Default Precision Rules by Stage & The Fragment Float Mandate

To reduce boilerplate, GLSL ES allows specifying default precisions per type using the `precision` statement:

```glsl
precision <precision-qualifier> <type>;
```

#### Built-in Language Defaults:

| Pipeline Stage | Type | Default Precision in GLSL ES 1.00 / 3.00+ |
| :--- | :--- | :--- |
| **Vertex Shader** | `float` | **`highp`** (Built-in default) |
| **Vertex Shader** | `int` | **`highp`** (Built-in default) |
| **Vertex Shader** | `sampler2D`, `samplerCube` | **`lowp`** (Built-in default) |
| **Fragment Shader** | `float` | **NONE! (MANDATORY TO DECLARE MANUALLY)** |
| **Fragment Shader** | `int` | **`mediump`** (Built-in default) |
| **Fragment Shader** | `sampler2D`, `samplerCube` | **`lowp`** (Built-in default) |
| **Compute Shader** | `float` | **`highp`** (Built-in default in ES 3.10+) |
| **Compute Shader** | `int` | **`highp`** (Built-in default in ES 3.10+) |

#### 🚨 The #1 Most Common GLSL ES Compilation Error:
```
ERROR: 0:3: 'float' : No precision specified for (float)
```
**Why this occurs:** In the fragment shader, the specification **does not provide a default precision for floating-point numbers**. Every single fragment shader written in GLSL ES 1.00, 3.00, 3.10, or 3.20 must explicitly declare a default float precision at the top of the file:

```glsl
#version 300 es
precision mediump float; // <-- WITHOUT THIS LINE, COMPILATION WILL FAIL!

in vec2 v_uv;
out vec4 fragColor;
```

> [!NOTE]
> **Fragment `highp` in ES 1.00:** In OpenGL ES 2.0 (GLSL ES 1.00), supporting `highp` in fragment shaders was **optional** for hardware manufacturers. Older chips (e.g. Mali-400) only supported `mediump` in fragment shaders. Starting in GLSL ES 3.00, `highp` support in fragment shaders is **mandatory** for all compliant devices.

### 4.5 Precision Promotion & Expression Evaluation

When two operands in an expression have different precision qualifiers, GLSL ES follows strict precision promotion rules:

1. If one operand is `highp`, the operation is performed at **`highp`**, and the result is `highp`.
2. If one operand is `mediump` and the other is `lowp`, the operation is performed at **`mediump`**, and the result is `mediump`.
3. If an expression involves literal constants (e.g., `2.0 * v_pos`), the literal assumes the precision of the variable it is operating with:
   ```glsl
   highp float a;
   float b = a + 1.0; // 1.0 is treated as highp float
   ```
4. Function return values inherit the precision declared in the function prototype:
   ```glsl
   mediump float computeDiffuse(highp vec3 N, highp vec3 L) {
       return max(dot(N, L), 0.0); // Result truncated to mediump on return!
   }
   ```

### 4.6 Dual-Issue ALU Packing & Mobile Optimization

Modern mobile GPUs (such as ARM Mali Bifrost/Valhall, Qualcomm Adreno 600/700 series, and Apple GPUs) feature hybrid arithmetic logic units. 

An ALU core that can execute one 32-bit operation (FP32) can typically execute **two 16-bit operations (FP16)** in the exact same clock cycle via SIMD-within-a-register (vector packing).

```
  FP32 Mode:
  ┌────────────────────────────────────────────────────────┐
  │         32-bit Float ALU Operation (1 Cycle)           │
  └────────────────────────────────────────────────────────┘

  FP16 Mode (Packed / Dual-Issue):
  ┌───────────────────────────┬────────────────────────────┐
  │ 16-bit Half-Float Op A    │ 16-bit Half-Float Op B     │  <-- 2x Throughput!
  └───────────────────────────┴────────────────────────────┘
```

#### Practical Rules for Precision Selection:
- **`highp`:**
  - Vertex positions and transformed geometry coordinates.
  - UV texture coordinates (especially if tiled, repeating, or sampled with detailed mipmaps).
  - Depth buffer values, camera distance, and world-space lighting vectors.
  - Trigonometric and exponential inputs where precision decay causes banding.
- **`mediump`:**
  - Surface normals, tangents, and bitangents (normalized vectors always sit in [-1.0, 1.0]).
  - Colors, lighting intensities, and specular highlights.
  - Albedo, metallic, roughness, and ambient occlusion parameters.
  - Atmospheric fog factors and local blurs.
- **`lowp`:**
  - Simple 8-bit unlit UI colors, raw vertex color tints, and boolean masks.

---

# 5. Type System & Desktop Divergences

### 5.1 Scalar & Vector Types

GLSL ES supports the core scalar and vector types found in C/GLSL:

```glsl
// Scalars
bool  bVal = true;
int   iVal = -42;
uint  uVal = 100u;      // uint added in GLSL ES 3.00
float fVal = 3.14159;

// Floating-Point Vectors
vec2  v2 = vec2(1.0, 2.0);
vec3  v3 = vec3(v2, 3.0);
vec4  v4 = vec4(v3, 1.0);

// Integer Vectors (GLSL ES 3.00+)
ivec2 iv2 = ivec2(1, -2);
ivec3 iv3 = ivec3(0);
ivec4 iv4 = ivec4(iv3, 4);

// Unsigned Integer Vectors (GLSL ES 3.00+)
uvec2 uv2 = uvec2(1u, 2u);
uvec3 uv3 = uvec3(uv2, 3u);
uvec4 uv4 = uvec4(4u);

// Boolean Vectors
bvec2 bv2 = bvec2(true, false);
bvec3 bv3 = bvec3(bv2, true);
bvec4 bv4 = bvec4(false);
```

### 5.2 Matrix Types & Memory Layout

GLSL ES matrices are **column-major**: `M[col][row]`.

```glsl
// Square Matrices
mat2 m2; // 2x2 matrix
mat3 m3; // 3x3 matrix
mat4 m4; // 4x4 matrix

// Non-Square Matrices (Added in GLSL ES 3.00)
mat2x3 m23; // 2 columns, 3 rows
mat3x2 m32; // 3 columns, 2 rows
mat2x4 m24; // 2 columns, 4 rows
mat4x2 m42; // 4 columns, 2 rows
mat3x4 m34; // 3 columns, 4 rows
mat4x3 m43; // 4 columns, 3 rows
```

> [!NOTE]
> In **GLSL ES 1.00**, only square matrices (`mat2`, `mat3`, `mat4`) exist. Non-square rectangular matrices were only introduced in **GLSL ES 3.00**.

### 5.3 Opaque Types (Samplers, Images, Atomics)

Opaque types represent GPU internal objects (texture bindings, memory images, atomic counters). They cannot be instantiated as local variables; they can only exist as `uniform` declarations or function arguments.

```glsl
// Supported in GLSL ES 1.00:
uniform sampler2D   u_diffuseTexture;
uniform samplerCube u_skyboxTexture;

// Added in GLSL ES 3.00:
uniform sampler3D            u_volumeTexture;
uniform sampler2DArray       u_textureAtlasArray;
uniform sampler2DShadow      u_shadowMap;
uniform samplerCubeShadow    u_cubeShadowMap;
uniform sampler2DArrayShadow u_arrayShadowMap;
uniform isampler2D           u_intTexture;
uniform usampler2D           u_uintTexture;

// Added in GLSL ES 3.10:
layout(rgba8, binding = 0) uniform readonly  image2D  u_inputImage;
layout(rgba8, binding = 1) uniform writeonly image2D  u_outputImage;
layout(binding = 0) uniform atomic_uint               u_globalCounter;

// Added in GLSL ES 3.20:
uniform samplerBuffer        u_bufferTexture;
uniform sampler2DMS          u_multisampleTexture;
```

### 5.4 Omitted Desktop Types (No `double`, No `sampler1D`)

To keep mobile silicon lean and energy-efficient, GLSL ES deliberately omits major portions of the desktop GLSL type system:

1. **NO 64-bit Double Precision:**
   - The types `double`, `dvec2`, `dvec3`, `dvec4`, `dmat2`, `dmat3`, `dmat4` **do not exist** anywhere in GLSL ES (even in 3.20).
   - Attempting to declare `double d = 1.0;` results in an immediate syntax error.
2. **NO 1D Textures:**
   - The types `sampler1D`, `sampler1DShadow`, `sampler1DArray`, and the function `texture1D()` **do not exist** in any GLSL ES version.
   - 1D data lookup must be simulated using a 2D texture with a height of 1 (`sampler2D` with coords `vec2(u, 0.5)`).
3. **NO Rectangle Textures:**
   - `samplerRect` and unnormalized pixel-coordinate texture queries do not exist in standard GLSL ES.
4. **NO Fixed-Function Attributes:**
   - Desktop built-in uniforms (`gl_ModelViewMatrix`, `gl_ProjectionMatrix`, `gl_NormalMatrix`) and legacy attributes (`gl_Vertex`, `gl_Normal`, `gl_MultiTexCoord0`) never existed in OpenGL ES.

### 5.5 Structs, Arrays, and Dynamic Indexing Limits

#### Struct Declarations:

```glsl
struct PointLight {
    highp vec3  position;
    mediump vec3 color;
    mediump float radius;
};

uniform PointLight u_lights[4];
```

#### Dynamic Indexing Restrictions (The ES 1.00 Legacy Trap):
- In **GLSL ES 1.00**, array indexing with non-constant expressions (e.g. `u_lights[i]` where `i` is a variable) was heavily restricted:
  - Dynamic indexing of `uniform` arrays in fragment shaders was frequently unsupported by hardware compilers.
  - Indexing vectors with a variable (`v[i]`) was prohibited or caused software emulation.
- In **GLSL ES 3.00+**, dynamic indexing of arrays, vectors, and matrices with any integer expression is fully supported and standardized.

### 5.6 Strict Type Casting & Implicit Conversion Rules

GLSL ES is an exceptionally strict language regarding types.

```glsl
// INVALID IN ALL GLSL ES VERSIONS:
float x = 1;        // ERROR: Cannot implicitly convert int to float
vec3 v = 0.0;       // ERROR: Cannot implicitly convert float to vec3
int i = 2.0;        // ERROR: Cannot implicitly convert float to int

// CORRECT EXPLICIT CONVERSIONS:
float x = 1.0;      // Or float(1)
vec3 v = vec3(0.0); // Constructor invocation
int i = int(2.0);   // Explicit constructor cast
```

> [!NOTE]
> In **GLSL ES 3.00+**, implicit scalar widening was added for select integer types: `int` can implicitly convert to `uint`. However, `int` **never** implicitly converts to `float`!

---

# 6. Storage, Parameter & Layout Qualifiers

### 6.1 Legacy Qualifiers (`attribute`, `varying`) vs Modern (`in`, `out`)

The syntax for input and output variables changed fundamentally between GLSL ES 1.00 and GLSL ES 3.00:

```
  GLSL ES 1.00 (ES 2.0 / WebGL 1.0):
  ┌────────────────────────┐         ┌────────────────────────┐
  │     VERTEX SHADER      │         │    FRAGMENT SHADER     │
  │ attribute vec3 pos;    │         │                        │
  │ varying vec2 v_uv; ────┼────────>│ varying vec2 v_uv;     │
  │                        │         │ gl_FragColor = ...;    │
  └────────────────────────┘         └────────────────────────┘

  GLSL ES 3.00+ (ES 3.0 / WebGL 2.0):
  ┌────────────────────────┐         ┌────────────────────────┐
  │     VERTEX SHADER      │         │    FRAGMENT SHADER     │
  │ in vec3 pos;           │         │                        │
  │ out vec2 v_uv; ────────┼────────>│ in vec2 v_uv;          │
  │                        │         │ out vec4 fragColor;    │
  └────────────────────────┘         └────────────────────────┘
```

#### Comparative Syntax:

| Concept | GLSL ES 1.00 (Legacy) | GLSL ES 3.00+ (Modern Core) |
| :--- | :--- | :--- |
| **Vertex Input** | `attribute vec3 a_position;` | `in vec3 a_position;` (or with `layout(location = 0) in ...`) |
| **Stage Inter-communication** | `varying vec2 v_texcoord;` | Vertex: `out vec2 v_texcoord;`<br>Fragment: `in vec2 v_texcoord;` |
| **Fragment Output** | Built-in `gl_FragColor` or `gl_FragData[n]` | Explicit user `out vec4 fragColor;` |

### 6.2 Function Parameter Qualifiers (`in`, `out`, `inout`)

Functions use value-result semantics:
- `in` (Default): Value is copied into the function parameter; modifications inside do not affect the caller.
- `out`: Value is uninitialized upon entering the function; whatever value is assigned inside is copied back to the caller upon return.
- `inout`: Value is copied in from the caller, modified, and copied back to the caller upon return.

```glsl
void computeTangentBasis(in vec3 normal, out vec3 tangent, out vec3 bitangent) {
    vec3 c1 = cross(normal, vec3(0.0, 0.0, 1.0));
    vec3 c2 = cross(normal, vec3(0.0, 1.0, 0.0));
    tangent = normalize(length(c1) > length(c2) ? c1 : c2);
    bitangent = cross(normal, tangent);
}
```

### 6.3 Layout Qualifiers (`layout(...)`) in ES 3.00+

GLSL ES 3.00 introduces explicit `layout(...)` qualifiers to eliminate host API lookup roundtrips (`glGetAttribLocation`, `glGetUniformLocation`):

```glsl
#version 300 es

// Explicit Vertex Attribute Locations
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_normal;
layout(location = 2) in vec2 a_texcoord;

// Explicit Fragment Render Target Outputs (MRT)
layout(location = 0) out vec4 o_albedo;
layout(location = 1) out vec4 o_normalRoughness;

// Explicit Uniform Block Bindings (ES 3.10+)
layout(std140, binding = 0) uniform CameraData {
    mat4 viewProjMatrix;
    vec3 cameraPos;
} u_cam;
```

### 6.4 Interpolation Qualifiers (`smooth`, `flat`, `centroid`, `sample`)

Interpolation qualifiers dictate how the rasterizer interpolates vertex stage outputs across the triangle before feeding them into fragment inputs:

```glsl
// smooth (Default): Standard perspective-correct barycentric interpolation
smooth in vec2 v_uv;

// flat: No interpolation. The fragment receives the value from the provoking vertex
flat in int v_materialID;

// centroid: Evaluates the attribute at the centroid of the multisample coverage mask
centroid in vec2 v_sampleUV;
```

> [!WARNING]
> **The `noperspective` Qualifier Is Absent:**
> In Desktop GLSL, `noperspective` performs linear screen-space interpolation without perspective division. In standard GLSL ES, `noperspective` **does not exist** and will trigger a compilation error.

### 6.5 Invariance (`invariant`) and Multi-Pass Z-Fighting Prevention

In multi-pass rendering algorithms (e.g. depth pre-pass, shadow mapping, or additive lighting passes), the exact same geometry is rendered in multiple shader passes.

Because mobile GPU compilers aggressively reorder floating-point instructions to optimize register occupancy, evaluating `gl_Position = u_mvp * vec4(pos, 1.0);` across two different shader programs can result in minor floating-point differences ($10^{-7}$). On mobile GPUs, this causes catastrophic flickering known as **Z-fighting**.

To guarantee identical bit-level results across shaders, use the `invariant` keyword:

```glsl
// Make a specific output invariant:
invariant gl_Position;
invariant out vec4 v_worldPosition;

// Or make ALL vertex outputs invariant globally:
#pragma STDGL invariant(all)
```

---

# 7. Expressions, Operators & Swizzling

### 7.1 Operator Precedence & Integer Bitwise Operator Availability

GLSL ES follows standard C operator precedence:

| Level | Operators | Description | Availability in GLSL ES |
| :---: | :--- | :--- | :--- |
| **1** | `()`, `[]`, `.`, `++`, `--` | Postfix, array indexing, swizzle | All versions |
| **2** | `++`, `--`, `+`, `-`, `!`, `~` | Prefix, unary, logical not, bitwise not | `~` added in **ES 3.00** |
| **3** | `*`, `/`, `%` | Multiplicative, modulus | `%` added in **ES 3.00** |
| **4** | `+`, `-` | Additive | All versions |
| **5** | `<<`, `>>` | Bitwise shift | Added in **ES 3.00** |
| **6** | `<`, `>`, `<=`, `>=` | Relational | All versions |
| **7** | `==`, `!=` | Equality | All versions |
| **8** | `&` | Bitwise AND | Added in **ES 3.00** |
| **9** | `^` | Bitwise XOR | Added in **ES 3.00** |
| **10** | `\|` | Bitwise OR | Added in **ES 3.00** |
| **11** | `&&` | Logical AND | All versions |
| **12** | `^^` | Logical XOR | All versions |
| **13** | `\|\|` | Logical OR | All versions |
| **14** | `?:` | Ternary conditional | All versions |
| **15** | `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `&=`, `^=`, `\|=` | Assignment operators | Bitwise assignments added in **ES 3.00** |

> [!IMPORTANT]
> **No Bitwise Operations in GLSL ES 1.00 (WebGL 1.0):**
> In GLSL ES 1.00, operators `&`, `|`, `^`, `~`, `<<`, `>>`, and `%` **do not exist**. Any bit packing or bit masking on WebGL 1.0 must be mathematically simulated using floating-point `mod()`, `floor()`, and division. In GLSL ES 3.00+, full integer bitwise manipulation is supported.

### 7.2 Vector Swizzling Rules

Vector components can be accessed using three distinct semantic field sets:

```glsl
vec4 color = vec4(1.0, 0.5, 0.25, 1.0);

// Coordinate access: {x, y, z, w}
vec2 xy = color.xy;

// Color access: {r, g, b, a}
vec3 rgb = color.rgb;

// Texture coordinates: {s, t, p, q}
vec2 st = color.st;
```

#### Swizzling Rules:
1. **Never mix sets:** `color.xgr` or `color.stz` is a fatal syntax error.
2. **Maximum 4 components:** An access cannot exceed 4 components: `v.xxxxx` is illegal.
3. **L-Value Swizzle Restrictions:** When swizzling on the left side of an assignment, **no duplicate components are allowed**:
   ```glsl
   color.rg = vec2(0.1, 0.2); // VALID: distinct components
   color.xx = vec2(0.1, 0.2); // ILLEGAL: duplicate component 'x'
   ```

### 7.3 Matrix and Vector Arithmetic Semantics

Multiplication `*` between matrices and vectors represents linear algebraic matrix multiplication, **not** component-wise multiplication:

```glsl
mat4 M, V, P;
vec4 localPos = vec4(a_position, 1.0);

// Correct Column-Vector Transformation Chain:
vec4 clipPos = P * V * M * localPos; // Transforms vector from Right to Left!

// Component-wise multiplication of matrices requires the matrixCompMult() function:
mat3 A, B;
mat3 C = matrixCompMult(A, B);
```

---

# 8. Control Flow, Loops & Branching Divergence

### 8.1 The Strict ES 1.00 Loop Restrictions (Appendix A Rules)

In the early mobile era of OpenGL ES 2.0 (GLSL ES 1.00), GPUs lacked dynamic instruction pointers and hardware loop counters. To ensure that loops could always be unrolled into a flat sequence of instructions by the compiler, the GLSL ES 1.00 specification enforced the infamous **Appendix A loop rules**:

```glsl
// GLSL ES 1.00 Canonical Form Loop:
for (int i = 0; i < 10; ++i) {
    // Loop body
}
```

#### Mandated Constraints in ES 1.00:
1. Exactly one loop index variable must be used.
2. The loop index must be an `int` or `float`.
3. The condition must compare the index against a **compile-time constant expression** (e.g., `i < CONSTANT`). Dynamic conditions like `i < dynamicUniformCount` were strictly prohibited!
4. The step must be one of: `i++`, `i--`, `i += const_expr`, `i -= const_expr`.
5. The index variable could not be modified inside the loop body.

### 8.2 Modern Control Flow in ES 3.00+ (`switch`, Dynamic Loops)

GLSL ES 3.00 removed Appendix A loop restrictions. Modern mobile GPUs support:
- Dynamic loop termination criteria: `for (int i = 0; i < u_lightCount; i++)`.
- `while (...)` and `do { ... } while (...)` loops.
- `switch-case` statements with integer jump tables:

```glsl
#version 300 es
precision mediump float;

flat in int v_type;
out vec4 fragColor;

void main() {
    switch (v_type) {
        case 0:
            fragColor = vec4(1.0, 0.0, 0.0, 1.0);
            break;
        case 1:
            fragColor = vec4(0.0, 1.0, 0.0, 1.0);
            break;
        default:
            fragColor = vec4(0.0, 0.0, 1.0, 1.0);
            break;
    }
}
```

### 8.3 The Hidden Cost of `discard` on Mobile TBDR GPUs

In desktop GPUs, the `discard` keyword simply terminates fragment execution.

On mobile Tile-Based Deferred Renderers (PowerVR, Apple Silicon, Mali, Adreno), `discard` has a **catastrophic performance impact**:

```
  Normal Opaque Pipeline (HSR Active):
  Geometry Rasterized ──> [Hardware HSR / Early-Z Test] ──> Fragment Shader (Zero Overdraw!)
                                    │ (Failed)
                                    └──> Fragment Dropped Before Shader Runs!

  Alpha-Tested / Discard Pipeline:
  Geometry Rasterized ──> [HSR Disabled!] ──> Fragment Shader Must Run First!
                                                      │
                                                      ├──> Checks 'discard'
                                                      └──> Depth written late, stalling tile cache!
```

- When a fragment shader contains `discard`, the hardware **cannot determine whether the fragment will exist** until the shader finishes.
- The GPU must **disable Hidden Surface Removal (Early-Z)** for all geometry drawing with that shader.
- Occluded pixels behind the transparent object can no longer be rejected early, creating severe overdraw and tile-memory cache stalls.

> [!TIP]
> **Mobile Best Practice:** Never use `discard` for large background scenery or terrain meshes. For cutouts (e.g. foliage), keep the cutout alpha geometry tightly bound to the triangle mesh to minimize discarded surface area, or use blending if overdraw is minimal.

---

# 9. Uniform Buffers (UBO) & Shader Storage Buffers (SSBO)

### 9.1 Uniform Buffer Objects & `std140` Alignment (ES 3.00+)

Uniform Buffer Objects (UBOs) allow sharing blocks of uniform data between multiple shaders without binding each variable individually.

Uniform blocks in GLSL ES 3.00 must adhere to the `std140` memory layout rules:

```glsl
#version 300 es
precision highp float;

layout(std140) uniform LightingData {
    vec4  lightPosition;   // Base alignment 16, offset 0
    vec3  lightColor;      // Base alignment 16, offset 16
    float lightIntensity;  // Base alignment 4,  offset 28 (packed into the 16-byte boundary)
    mat4  shadowMatrix;    // Base alignment 16, offset 32 (takes 64 bytes: 4 x vec4)
    float padding[4];      // Arrays in std140 ALWAYS pad each element to 16 bytes!
} u_lighting;
```

#### `std140` Memory Layout Rules:
- `float`, `int`, `uint`, `bool`: 4 bytes.
- `vec2`: 8 bytes (aligned to an 8-byte boundary).
- `vec3` and `vec4`: **16 bytes** (aligned to a 16-byte boundary).
- `mat4`: Equivalent to four `vec4` columns (64 bytes total).
- **Arrays:** Every array element in `std140` is padded to **16 bytes** (4 × float), even if the array is `float arr[4]`!

### 9.2 Shader Storage Buffer Objects & `std430` Alignment (ES 3.10+)

Introduced in GLSL ES 3.10, Shader Storage Buffer Objects (SSBOs) provide read-write buffers capable of storing megabytes of structured data, including unsized dynamic runtime arrays:

```glsl
#version 310 es

struct Particle {
    vec4 position;
    vec4 velocity;
    vec4 color;
};

layout(std430, binding = 0) buffer ParticleBuffer {
    Particle particles[]; // Unsized array dynamically sized by CPU buffer allocation
};
```

> [!NOTE]
> **`std430` vs `std140`:** While UBOs in ES 3.00 require `std140` (which pads array elements to 16 bytes), SSBOs in ES 3.10 support `std430`. Under `std430`, arrays of scalars (`float[]`) or vectors (`vec2[]`) are packed tightly without 16-byte padding!

---

# 10. Built-in Variables by Pipeline Stage

### 10.1 Vertex Shader Built-ins

| Variable | Type | Direction | Version | Description |
| :--- | :--- | :--- | :--- | :--- |
| `gl_Position` | `highp vec4` | **Output** | All | Homogeneous clip-space coordinates of the vertex (**Mandatory output**). |
| `gl_PointSize` | `mediump float` | **Output** | All | Size of rasterized point primitives in pixels. |
| `gl_VertexID` | `highp int` | **Input** | ES 3.00+ | Index of current vertex in the draw call (0-indexed). |
| `gl_InstanceID` | `highp int` | **Input** | ES 3.00+ | Index of current instance in instanced draw calls (`glDrawArraysInstanced`). |

### 10.2 Fragment Shader Built-ins

| Variable | Type | Direction | Version | Description |
| :--- | :--- | :--- | :--- | :--- |
| `gl_FragCoord` | `highp vec4` | **Input** | All | Screen-space window relative coordinates $(x, y, z, 1/w)$. |
| `gl_FrontFacing` | `bool` | **Input** | All | `true` if the current fragment belongs to a front-facing primitive. |
| `gl_PointCoord` | `mediump vec2` | **Input** | All | Normalized $(u, v)$ coordinate $[0.0, 1.0]^2$ within a point sprite. |
| `gl_FragColor` | `mediump vec4` | **Output** | **ES 1.00 only** | Output fragment color (**Removed in ES 3.00+**; use custom `out vec4`). |
| `gl_FragData[n]` | `mediump vec4[]`| **Output** | **ES 1.00 only** | Output color array for MRT (**Removed in ES 3.00+**). |
| `gl_FragDepth` | `highp float` | **Output** | ES 3.00+ | Manually overrides fragment depth written to depth buffer. |

### 10.3 Compute Shader Built-ins (ES 3.10+)

| Variable | Type | Description |
| :--- | :--- | :--- |
| `gl_NumWorkGroups` | `uvec3` | Total number of workgroups dispatched by host API (`glDispatchCompute`). |
| `gl_WorkGroupID` | `uvec3` | 3D index of current workgroup currently executing. |
| `gl_LocalInvocationID`| `uvec3` | 3D index of current thread within local workgroup. |
| `gl_GlobalInvocationID`| `uvec3` | Unique global thread coordinate (`gl_WorkGroupID * gl_WorkGroupSize + gl_LocalInvocationID`). |
| `gl_LocalInvocationIndex`| `uint` | 1D flattened index of thread within local workgroup. |

### 10.4 Tessellation & Geometry Shader Built-ins (ES 3.20)

- **Tessellation:** `gl_TessCoord`, `gl_PatchVerticesIn`, `gl_TessLevelOuter[4]`, `gl_TessLevelInner[2]`.
- **Geometry:** `gl_PrimitiveIDIn`, `gl_InvocationID`, `EmitVertex()`, `EndPrimitive()`.

---

# 11. Standard Library Built-in Functions

### 11.1 Math, Geometric & Relational Functions

GLSL ES implements the core mathematical standard library:

```glsl
// Angle & Trigonometric
radians(deg), degrees(rad), sin(x), cos(x), tan(x), asin(x), acos(x), atan(y, x)

// Exponential & Logarithmic
pow(x, y), exp(x), log(x), exp2(x), log2(x), sqrt(x), inversesqrt(x)

// Common Math
abs(x), sign(x), floor(x), ceil(x), fract(x), mod(x, y), min(x, y), max(x, y),
clamp(x, minVal, maxVal), mix(x, y, a), step(edge, x), smoothstep(edge0, edge1, x)

// Geometric
length(v), distance(p0, p1), dot(x, y), cross(x, y), normalize(v),
faceforward(N, I, Nref), reflect(I, N), refract(I, N, eta)

// Matrix Operations (Added in GLSL ES 3.00)
transpose(m), inverse(m), determinant(m), outerProduct(c, r)

// Vector Relational
equal(x, y), notEqual(x, y), lessThan(x, y), greaterThan(x, y), any(bvec), all(bvec), not(bvec)
```

### 11.2 Texture Sampling Function Evolution

Texture lookup functions underwent a complete syntax overhaul between ES 1.00 and ES 3.00:

```glsl
// ==========================================
// GLSL ES 1.00 (OpenGL ES 2.0 / WebGL 1.0):
// Explicit function name per sampler type:
// ==========================================
vec4 c1 = texture2D(u_diffuse, v_uv);
vec4 c2 = texture2DProj(u_diffuse, v_projectiveCoord);
vec4 c3 = textureCube(u_cubemap, v_direction);

// Mipmap LOD sampling in fragment shader requires extension:
#extension GL_EXT_shader_texture_lod : enable
vec4 c4 = texture2DLodEXT(u_diffuse, v_uv, 2.0);

// ==========================================
// GLSL ES 3.00+ (OpenGL ES 3.0 / WebGL 2.0):
// Unified overloaded texture() function:
// ==========================================
vec4 c1 = texture(u_diffuse, v_uv);
vec4 c2 = textureProj(u_diffuse, v_projectiveCoord);
vec4 c3 = texture(u_cubemap, v_direction);
vec4 c4 = textureLod(u_diffuse, v_uv, 2.0);

// Direct texel fetch by raw integer pixel coordinates (NO filtering):
vec4 rawPixel = texelFetch(u_diffuse, ivec2(gl_FragCoord.xy), 0);

// Query texture dimensions at runtime:
ivec2 size = textureSize(u_diffuse, 0);

// Gather 4 texels for fast bilinear/shadow filtering (GLSL ES 3.10+):
vec4 redFour = textureGather(u_shadowMap, v_uv);
```

### 11.3 Screen-Space Derivatives (`dFdx`, `dFdy`, `fwidth`)

Screen-space derivatives compute the rate of change of any variable across adjacent 2×2 pixel fragment quads.

```glsl
// Computes change along window X-axis
float dX = dFdx(v_worldPos.y);

// Computes change along window Y-axis
float dY = dFdy(v_worldPos.y);

// Computes sum of absolute derivatives: abs(dFdx(p)) + abs(dFdy(p))
float delta = fwidth(v_worldPos.y);
```

#### Analytical Normal Computation from World Position:
```glsl
vec3 computeFlatNormal(vec3 worldPos) {
    vec3 dX = dFdx(worldPos);
    vec3 dY = dFdy(worldPos);
    return normalize(cross(dX, dY));
}
```

> [!NOTE]
> - In **GLSL ES 1.00**, derivatives are not in core; they require:
>   `#extension GL_OES_standard_derivatives : enable`
> - In **GLSL ES 3.00+**, `dFdx()`, `dFdy()`, and `fwidth()` are standard core functions.

### 11.4 Compute Synchronization & Memory Barriers (ES 3.10+)

When executing Compute Shaders, threads within the same workgroup coordinate using shared memory and barriers:

```glsl
#version 310 es
layout(local_size_x = 16, local_size_y = 16) in;

shared float tileDepth[16][16];

void main() {
    ivec2 localID = ivec2(gl_LocalInvocationID.xy);
    tileDepth[localID.x][localID.y] = gl_FragCoord.z;

    // Execution barrier: waits for all 256 threads in the workgroup to reach this point
    barrier();

    // Memory barrier: ensures all shared memory writes are committed and visible
    memoryBarrierShared();
}
```

---

# 12. Subpass & Framebuffer Fetch (`GL_EXT_shader_framebuffer_fetch`)

On mobile Tile-Based Deferred Renderers (TBDR), reading the destination color or depth of the current pixel traditionally required finishing the render pass, resolving tile memory to VRAM, binding the texture, and sampling it back in a separate pass—incurring massive memory bandwidth overhead.

The `GL_EXT_shader_framebuffer_fetch` extension allows the fragment shader to read the existing color, depth, or stencil value **directly from on-chip SRAM tile memory** with zero VRAM bandwidth:

```glsl
#version 300 es
#extension GL_EXT_shader_framebuffer_fetch : enable

precision mediump float;

// Declare inout user fragment output:
layout(location = 0) inout vec4 fragColor;

void main() {
    // fragColor contains the existing color in tile memory at this pixel!
    vec4 existingDstColor = fragColor;
    
    // Perform custom programmable blending on-chip:
    vec4 srcColor = vec4(1.0, 0.5, 0.0, 0.5);
    fragColor = mix(existingDstColor, srcColor, srcColor.a);
}
```

---

# 13. Comprehensive Comparison Matrix: Desktop GLSL vs. GLSL ES

| Technical Feature | Desktop GLSL (3.30 – 4.60 Core) | GLSL ES 1.00 (ES 2.0 / WebGL 1.0) | GLSL ES 3.00 (ES 3.0 / WebGL 2.0) | GLSL ES 3.10 / 3.20 (ES 3.1 / 3.2) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary GPU Target** | Discrete Desktop GPU (IMR) | Mobile SoC / WebGL 1.0 (TBDR) | Mobile SoC / WebGL 2.0 (TBDR) | Modern Mobile / Flagship SoC |
| **Version Token** | `#version 330 core` | `#version 100` | `#version 300 es` | `#version 310 es` / `320 es` |
| **Precision Qualifiers** | Accepted, ignored as no-ops | **Mandatory semantics** | **Mandatory semantics** | **Mandatory semantics** |
| **Fragment Default Float** | Implicit `float` default | **No default (Compilation error!)**| **No default (Compilation error!)**| **No default (Compilation error!)**|
| **Double Precision (`double`)**| **Supported (`dvec`, `dmat`)** | **Omitted completely** | **Omitted completely** | **Omitted completely** |
| **1D Textures (`sampler1D`)** | **Supported** | **Omitted completely** | **Omitted completely** | **Omitted completely** |
| **Input / Output Keywords** | `in` / `out` | `attribute` / `varying` | `in` / `out` | `in` / `out` |
| **Fragment Output Syntax** | `out vec4 fragColor;` | `gl_FragColor` / `gl_FragData` | `out vec4 fragColor;` | `out vec4 fragColor;` |
| **Screen Derivatives** | Built-in Core (`dFdx`, `dFdy`) | Requires `GL_OES_standard_derivatives` | Built-in Core (`dFdx`, `dFdy`) | Built-in Core |
| **Bitwise Operators** | Full support (`&`, `\|`, `^`, `<<`)| **None** | Full support | Full support |
| **Matrix Operations** | `transpose()`, `inverse()` | **None** (Manual calculation) | `transpose()`, `inverse()` | `transpose()`, `inverse()` |
| **Non-Square Matrices** | Supported (`matMxN`) | Square only (`mat2`, `mat3`, `mat4`) | Supported (`matMxN`) | Supported (`matMxN`) |
| **Uniform Buffers (UBO)** | Core (`layout(std140)`) | Unsupported | Supported (`layout(std140)`) | Supported |
| **Storage Buffers (SSBO)** | Core (`layout(std430)`) | Unsupported | Unsupported | Supported (`std430` in ES 3.10+) |
| **Compute Shaders** | Core (GLSL 4.30+) | Unsupported | Unsupported | Supported in ES 3.10+ |
| **Tessellation & Geometry**| Core (GLSL 4.00+ / 1.50+) | Unsupported | Unsupported | Supported in ES 3.20 |

---

# 14. Complete Desktop GLSL to GLSL ES Porting Guide

Follow this systematic 7-step process to port any desktop GLSL shader to clean, compliant, and performant GLSL ES 3.00:

```
  ┌────────────────────────────────────────────────────────┐
  │         DESKTOP GLSL TO GLSL ES PORTING PIPELINE       │
  ├────────────────────────────────────────────────────────┤
  │  Step 1: Set Version Header to '#version 300 es'       │
  │  Step 2: Add Mandatory Fragment Float Precision        │
  │  Step 3: Convert Sampler1D to Sampler2D (Height = 1)   │
  │  Step 4: Strip Double Precision (Convert to Float)     │
  │  Step 5: Apply 'mediump' to Colors, Normals, Lighting  │
  │  Step 6: Replace 'noperspective' with 'smooth'         │
  │  Step 7: Verify Uniform Buffer std140 Struct Alignment │
  └────────────────────────────────────────────────────────┘
```

### Side-by-Side Code Conversion Example

#### Desktop GLSL 330 Core Shader (Before):

```glsl
#version 330 core

in vec3 v_normal;
in vec2 v_uv;
noperspective in float v_depth;

out vec4 FragColor;

uniform sampler1D u_gradientLUT;
uniform sampler2D u_diffuse;
uniform double u_highPrecisionTime;

void main() {
    float lutColor = texture(u_gradientLUT, v_uv.x).r;
    vec4 tex = texture(u_diffuse, v_uv);
    FragColor = tex * lutColor;
}
```

#### Compliant GLSL ES 3.00 Shader (After):

```glsl
#version 300 es

// Step 2: Mandatory default float precision declaration
precision mediump float;
precision highp int;

// Step 5: High precision where needed for depth / UVs
in mediump vec3 v_normal;
in highp vec2   v_uv;

// Step 6: Replace unsupported 'noperspective' with standard 'smooth'
smooth in highp float v_depth;

out vec4 o_fragColor;

// Step 3: Replace sampler1D with sampler2D (height = 1)
uniform sampler2D u_gradientLUT;
uniform sampler2D u_diffuse;

// Step 4: Convert double to float
uniform highp float u_time;

void main() {
    // Sample 1D LUT via 2D texture coordinate (Y fixed at center: 0.5)
    mediump float lutColor = texture(u_gradientLUT, vec2(v_uv.x, 0.5)).r;
    lowp vec4 tex = texture(u_diffuse, v_uv);
    o_fragColor = tex * lutColor;
}
```

---

# 15. Mobile Performance & Shader Optimization Best Practices

1. **Maximize 16-Bit Half Precision (`mediump`):**
   - Use `mediump` for all surface colors, normalized vectors, specular calculations, and lighting.
   - Saves register space, avoids register spilling to external memory, and doubles arithmetic throughput on dual-issue ALUs.
2. **Minimize Dependent Texture Reads:**
   - A dependent texture read occurs when texture coordinates are calculated dynamically inside the fragment shader rather than interpolated directly from vertex outputs (`v_uv`).
   - Dependent texture reads stall the texture cache pipeline on mobile TBDR architectures because the hardware prefetcher cannot predict texel addresses ahead of time.
3. **Avoid Fragment Shader Branching on Dynamic Expressions:**
   - On mobile SIMD warps (16–64 threads), if threads within the same tile diverge in an `if-else` branch, both paths execute for all threads with inactive execution masks, doubling the execution time.
4. **Beware of `discard` and Alpha Testing:**
   - `discard` breaks Tile-Based Hidden Surface Removal (HSR / Early-Z), leading to massive overdraw penalties.
5. **Pre-compute on CPU or Vertex Shader:**
   - Moving a calculation from the fragment shader to the vertex shader reduces execution frequency by 10x to 100x (number of vertices vs. number of rasterized pixels).

---

# 16. Common GLSL ES Compiler Pitfalls, Traps & Diagnostics

### Trap 1: Missing Fragment Float Precision
- **Error:** `'float' : No precision specified for (float)`
- **Solution:** Add `precision mediump float;` or `precision highp float;` at the top of the fragment shader.

### Trap 2: Using Deprecated `gl_FragColor` in `#version 300 es`
- **Error:** `undeclared identifier 'gl_FragColor'`
- **Solution:** In GLSL ES 3.00+, declare an explicit user output: `out vec4 fragColor;` and assign `fragColor = ...;`.

### Trap 3: Using `attribute` or `varying` in `#version 300 es`
- **Error:** `syntax error, unexpected ATTRIBUTE, expecting ...`
- **Solution:** In ES 3.00+, replace `attribute` with `in`, and replace `varying` with `out` (vertex) and `in` (fragment).

### Trap 4: Attempting to Declare `double`
- **Error:** `type 'double' is not supported in this version of GLSL ES`
- **Solution:** Use `highp float`. If extreme precision is needed (e.g. fractal zooms or planetary coordinates), use **float-float emulation** (storing high and low 32-bit floats as a `vec2`).

### Trap 5: `mediump` Coordinate Overflow in Distance Calculations
- **Symptom:** Meshes turn black or vanish when moving away from the world origin.
- **Root Cause:** Squaring coordinates in `mediump` exceeds the 65504.0 maximum value limit.
- **Solution:** Declare world-space vectors and distance variables as `highp vec3` and `highp float`.
