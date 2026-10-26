# OpenGL Shading Language (GLSL): The Complete Grammar, Syntax & Specification Reference

A comprehensive, authoritative specification and reference manual for the **OpenGL Shading Language (GLSL)**. This document covers the complete grammar, type system, qualifiers, operators, built-in functions, memory models, and execution semantics across desktop OpenGL (GLSL 1.10 through 4.60) and mobile OpenGL ES (GLSL ES 1.00 through 3.20).

---

## 📑 Table of Contents

1. [Architectural Overview & Pipeline Model](#1-architectural-overview--pipeline-model)
2. [Source Code Structure & Preprocessor](#2-source-code-structure--preprocessor)
3. [Lexical Conventions & Reserved Keywords](#3-lexical-conventions--reserved-keywords)
4. [The GLSL Type System](#4-the-glsl-type-system)
   - [Scalar Types](#41-scalar-types)
   - [Vector Types & Vector Constructors](#42-vector-types)
   - [Matrix Types & Memory Layout](#43-matrix-types)
   - [Opaque Types (Samplers, Images, Atomics)](#44-opaque-types)
   - [Structures & User-Defined Types](#45-structures)
   - [Arrays & Unsized Arrays](#46-arrays)
   - [Type Conversion & Explicit Casting](#47-type-conversion--casting)
5. [Storage, Parameter & Layout Qualifiers](#5-qualifiers--storage-classes)
   - [Storage Qualifiers (`in`, `out`, `uniform`, `buffer`, `shared`)](#51-storage-qualifiers)
   - [Function Parameter Qualifiers (`in`, `out`, `inout`)](#52-parameter-qualifiers)
   - [Layout Qualifiers (`layout(...)`)](#53-layout-qualifiers)
   - [Interpolation & Auxiliary Qualifiers (`flat`, `smooth`, `noperspective`, `centroid`, `sample`)](#54-interpolation-qualifiers)
   - [Precision Qualifiers (`highp`, `mediump`, `lowp`)](#55-precision-qualifiers)
   - [Invariance & Exactness Qualifiers (`invariant`, `precise`)](#56-invariance-and-exactness)
6. [Expressions, Operators & Swizzling](#6-expressions-operators--swizzling)
   - [Operator Precedence & Associativity Table](#61-operator-precedence)
   - [Vector Swizzling Rules & Field Sets](#62-swizzling)
   - [Vector and Matrix Arithmetic](#63-vector-and-matrix-algebra)
7. [Statements & Control Flow](#7-statements--control-flow)
   - [Selection (`if-else`, `switch-case`)](#71-selection-statements)
   - [Iteration (`for`, `while`, `do-while`)](#72-iteration-loops)
   - [Jumps & Discard (`break`, `continue`, `return`, `discard`)](#73-jump-statements--discard)
   - [GPU Branching & Divergence](#74-gpu-execution-divergence)
8. [Functions & Scope Rules](#8-functions--scope-rules)
   - [Function Declarations & Overloading](#81-declarations--overloading)
   - [Entry Point: `void main()`](#82-the-entry-point)
   - [Scoping & Variable Shadowing](#83-scoping-rules)
9. [Uniform Buffer Objects (UBO) & Shader Storage (SSBO)](#9-uniform-buffers-and-storage-buffers)
   - [Uniform Blocks & Memory Layouts (`std140`, `std430`)](#91-uniform-blocks)
   - [Shader Storage Buffer Objects (SSBOs)](#92-shader-storage-buffer-objects)
10. [Built-in Variables by Pipeline Stage](#10-built-in-variables-by-stage)
    - [Vertex Shader](#101-vertex-shader)
    - [Tessellation Control & Evaluation](#102-tessellation-stages)
    - [Geometry Shader](#103-geometry-shader)
    - [Fragment Shader](#104-fragment-shader)
    - [Compute Shader](#105-compute-shader)
11. [Built-in Functions (Standard Library)](#11-built-in-functions-standard-library)
    - [Trigonometric & Angle Functions](#111-trigonometric-functions)
    - [Exponential & Power Functions](#112-exponential-functions)
    - [Common Mathematical Functions](#113-common-functions)
    - [Geometric Functions](#114-geometric-functions)
    - [Matrix Functions](#115-matrix-functions)
    - [Vector Relational Functions](#116-vector-relational-functions)
    - [Integer & Bit Manipulation Functions](#117-integer--bit-manipulation)
    - [Texture Sampling & Query Functions](#118-texture-sampling--queries)
    - [Derivative Functions (Fragment Only)](#119-screen-space-derivatives)
    - [Synchronization & Memory Barriers](#1110-compute-synchronization)
12. [Evolution & Migration: Legacy to Modern GLSL](#12-version-matrix--migration-guide)
13. [Common Compiler Errors & Diagnostic Checklist](#13-common-compiler-errors--debugging)

---

# 1. Architectural Overview & Pipeline Model

GLSL is a statically typed, C-based data-parallel language designed to execute natively on graphics processing units (GPUs). Unlike CPU programs that execute instructions sequentially on a small number of complex cores, GLSL programs execute in lockstep across thousands of SIMD/SIMT (Single Instruction, Multiple Data / Single Instruction, Multiple Threads) vector ALUs.

```
       [Host CPU / Application]
                  │
        Draw Call / Dispatch
                  ▼
       ┌─────────────────────┐
       │    Vertex Shader    │  <-- Transforms vertices (local -> clip space)
       └──────────┬──────────┘
                  ▼
       ┌─────────────────────┐
       │ Tessellation Stage  │  <-- Optional: Procedural subdivision (TCS + TES)
       └──────────┬──────────┘
                  ▼
       ┌─────────────────────┐
       │   Geometry Shader   │  <-- Optional: Primitive amplification / modification
       └──────────┬──────────┘
                  ▼
       ┌─────────────────────┐
       │   Rasterization     │  <-- Hardware stage: Clipping, viewport, interpolation
       └──────────┬──────────┘
                  ▼
       ┌─────────────────────┐
       │   Fragment Shader   │  <-- Evaluates per-pixel color, depth, lighting
       └──────────┬──────────┘
                  ▼
       ┌─────────────────────┐
       │ Per-Sample Tests    │  <-- Hardware stage: Scissor, Stencil, Depth, Blending
       └─────────────────────┘
```

A standalone GLSL program object is created by compiling one or more shader stages (translation units) and linking them together into an executable GPU program pipeline via the host API (OpenGL, Vulkan via SPIR-V, or game engines like Panda3D).

---

# 2. Source Code Structure & Preprocessor

## 2.1 The `#version` Directive
Every GLSL shader source file must specify the version of the language on the **first non-comment, non-whitespace line**:

```glsl
#version <version-number> [profile]
```

- **Rules**:
  1. No executable code, variable declarations, or preprocessor conditionals may precede `#version`.
  2. Only comments and empty lines are permitted before `#version`.
  3. The `profile` specifier is required for desktop GLSL versions 150 and above. Valid profiles: `core` (default), `compatibility`, or `es` (for embedded systems).

### Version Correspondence Table

| Desktop OpenGL | GLSL Version | Profile Required? | Mobile OpenGL ES | GLSL ES Version |
| :--- | :--- | :--- | :--- | :--- |
| **OpenGL 2.0** | `#version 110` | No | **OpenGL ES 2.0** | `#version 100` |
| **OpenGL 2.1** | `#version 120` | No | — | — |
| **OpenGL 3.0** | `#version 130` | No | — | — |
| **OpenGL 3.1** | `#version 140` | No | — | — |
| **OpenGL 3.2** | `#version 150 core` | Yes (`core` / `compatibility`) | — | — |
| **OpenGL 3.3** | `#version 330 core` | Yes | — | — |
| **OpenGL 4.0** | `#version 400 core` | Yes | — | — |
| **OpenGL 4.1** | `#version 410 core` | Yes | — | — |
| **OpenGL 4.2** | `#version 420 core` | Yes | — | — |
| **OpenGL 4.3** | `#version 430 core` | Yes | **OpenGL ES 3.0** | `#version 300 es` |
| **OpenGL 4.4** | `#version 440 core` | Yes | **OpenGL ES 3.1** | `#version 310 es` |
| **OpenGL 4.5** | `#version 450 core` | Yes | **OpenGL ES 3.2** | `#version 320 es` |
| **OpenGL 4.6** | `#version 460 core` | Yes | — | — |

## 2.2 Extension Management (`#extension`)
Extensions enable vendor-specific or hardware-specific GPU capabilities:

```glsl
#extension <extension_name> : <behavior>
#extension all : <behavior>
```

Valid behaviors:
- `require`: Compilation halts with an error if the extension is unsupported.
- `enable`: Enables the extension if supported; emits a warning if unsupported.
- `warn`: Emits a warning on compilation; warns if unsupported.
- `disable`: Disables the extension completely.

```glsl
#version 330 core
#extension GL_ARB_gpu_shader5 : require
#extension GL_EXT_shader_image_load_store : enable
```

## 2.3 Preprocessor Directives & Macros
GLSL implements a standard C-like macro preprocessor:

```glsl
#define IDENTIFIER value
#undef IDENTIFIER

#if condition
#elif condition
#else
#endif

#ifdef IDENTIFIER
#ifndef IDENTIFIER

#error "Custom compilation error message"
#pragma optimize(on)
#pragma debug(off)
#line <line_number> [source_string_number]
```

### Pre-defined Built-in Macros
- `__LINE__`: Current line number in source string.
- `__FILE__`: Current source string number (integer index).
- `__VERSION__`: Integer representing GLSL version (e.g., `460` for 4.60, `300` for ES 3.00).
- `GL_core_profile`: Defined as `1` when targeting the Core Profile.
- `GL_compatibility_profile`: Defined as `1` when targeting the Compatibility Profile.
- `GL_ES`: Defined as `1` when compiling for OpenGL ES environments (`#version 100`, `#version 300 es`, etc.).

---

# 3. Lexical Conventions & Reserved Keywords

- **Case Sensitivity**: GLSL is strictly case-sensitive. `vec3`, `Vec3`, and `VEC3` are distinct tokens; only `vec3` is recognized as the keyword type.
- **Semicolons**: Every statement and structure declaration must terminate with a semicolon `;`.
- **Comments**:
  ```glsl
  // Single-line comment continues to end of line
  /* Multi-line block comments
     cannot be nested */
  ```
- **Identifiers**: Begin with an ASCII letter or underscore `_`, followed by letters, digits, or underscores. Identifiers starting with `gl_` or containing two consecutive underscores `__` are strictly reserved for internal GPU runtime use.

### Reserved Keywords Table
Variables may not use any of the following reserved words:

```
attribute    break        buffer       bvec2        bvec3        bvec4
case         cast         centroid     coherent     common       const
continue     default      discard      dmat2        dmat3        dmat4
do           double       dvec2        dvec3        dvec4        else
enum         extern       false        filter       fixed        flat
float        for          fvec2        fvec3        fvec4        goto
half         highp        hvec2        hvec3        hvec4        if
iimage2D     image2D      in           inline       inout        input
int          invariant    isampler2D   ivec2        ivec3        ivec4
layout       long         lowp         mat2         mat3         mat4
mediump      noperspective noinline    out          output       packed
partition    patch        precise      precision    public       readonly
resource     restrict     return       sample       sampler2D    samplerCube
shared       short        sizeof       smooth       static       struct
subroutine   superp       switch       template     this         true
typedef      uimage2D     uint         uniform      union        unsigned
usampler2D   using        uvec2        uvec3        uvec4        varying
vec2         vec3         vec4         void         volatile     while
writeonly
```

---

# 4. The GLSL Type System

GLSL is strongly and statically typed. There are no void pointers, dynamic types, or runtime duck typing.

## 4.1 Scalar Types

| Type | Size / Precision | Description | Example Literal |
| :--- | :--- | :--- | :--- |
| `void` | 0 bits | Function returning no value | — |
| `bool` | 1 bit (logical) | Boolean truth value | `true`, `false` |
| `int` | 32 bits (two's complement) | Signed integer | `-42`, `0`, `0x1A` |
| `uint` | 32 bits | Unsigned integer | `0u`, `128u`, `0xFFu` |
| `float` | 32 bits (IEEE 754 single) | Single-precision floating point | `1.0`, `0.5f`, `1e-4` |
| `double` | 64 bits (IEEE 754 double) | Double-precision float (GLSL 4.0+) | `1.0lf`, `0.25LF` |

> [!IMPORTANT]
> Floating-point literals **must** include a decimal point or exponent to prevent type mismatch errors in older compilers: `float f = 1;` is illegal in GLSL 1.10/1.20; write `float f = 1.0;`.

## 4.2 Vector Types
Vectors represent geometric coordinates, colors, normals, and homogeneous positions.

| Type | Component Type | Dimensions | Common Uses |
| :--- | :--- | :--- | :--- |
| `vec2`, `vec3`, `vec4` | 32-bit `float` | 2, 3, 4 | Positions, normals, UVs, RGBA colors |
| `dvec2`, `dvec3`, `dvec4` | 64-bit `double` | 2, 3, 4 | High-precision astronomical/CAD coordinates |
| `ivec2`, `ivec3`, `ivec4` | 32-bit signed `int` | 2, 3, 4 | Grid coordinates, texel coordinates |
| `uvec2`, `uvec3`, `uvec4` | 32-bit unsigned `uint`| 2, 3, 4 | Bitmasks, invocation IDs, cluster bins |
| `bvec2`, `bvec3`, `bvec4` | `bool` | 2, 3, 4 | Component-wise boolean condition masks |

### Vector Constructors
Vectors can be constructed from scalars, lower-dimensional vectors, or combinations:

```glsl
vec3 a = vec3(1.0);                     // vec3(1.0, 1.0, 1.0) - scalar splat
vec2 uv = vec2(0.5, 0.2);
vec4 rgba = vec4(uv, 1.0, 0.8);         // Concatenation: vec4(0.5, 0.2, 1.0, 0.8)
vec3 rgb = vec3(rgba);                   // Truncation: grabs first 3 components
ivec2 tile = ivec2(16, 32);
bvec3 mask = bvec3(true, false, true);
```

## 4.3 Matrix Types
GLSL supports standard linear algebra transformations. **All matrices in GLSL are column-major by default.**

| Type | Dimensions (Cols x Rows) | Element Type | Memory Size |
| :--- | :--- | :--- | :--- |
| `mat2` or `mat2x2` | 2 columns, 2 rows | `float` | 4 floats |
| `mat3` or `mat3x3` | 3 columns, 3 rows | `float` | 9 floats (Normal matrix) |
| `mat4` or `mat4x4` | 4 columns, 4 rows | `float` | 16 floats (MVP transform) |
| `mat2x3` | 2 columns, 3 rows | `float` | 6 floats |
| `mat3x2` | 3 columns, 2 rows | `float` | 6 floats |
| `mat2x4`, `mat4x2` | Non-square | `float` | 8 floats |
| `mat3x4`, `mat4x3` | Non-square | `float` | 12 floats |
| `dmat2`, `dmat3`, `dmat4` | Square double | `double` | 64-bit per element |

### Matrix Constructors
```glsl
// Diagonal / Identity constructor (scalar on diagonal, 0 elsewhere):
mat4 identity = mat4(1.0);

// Explicit component specification (column by column!):
mat2 m = mat2(
    1.0, 2.0,   // Column 0: (x=1, y=2)
    3.0, 4.0    // Column 1: (x=3, y=4)
);

// Constructed from vectors (each vector is a column!):
vec4 col0 = vec4(1, 0, 0, 0);
vec4 col1 = vec4(0, 1, 0, 0);
vec4 col2 = vec4(0, 0, 1, 0);
vec4 col3 = vec4(0, 0, 0, 1);
mat4 m4 = mat4(col0, col1, col2, col3);
```

## 4.4 Opaque Types
Opaque variables handle hardware GPU resources (textures, framebuffers, compute memory) and cannot be constructed or directly manipulated as data numbers. They must be declared as `uniform` or function parameters.

```glsl
// Standard 2D / 3D / Cube textures
uniform sampler2D u_albedoMap;
uniform sampler3D u_volumeData;
uniform samplerCube u_skybox;

// Shadow comparison samplers (perform hardware depth comparison)
uniform sampler2DShadow u_shadowMap;
uniform samplerCubeShadow u_pointShadow;

// Integer textures
uniform isampler2D u_stencilIndex;
uniform usampler2D u_materialID;

// Multisample samplers (MSAA)
uniform sampler2DMS u_msaaColorBuffer;

// Read-Write Image Buffers (Compute / Storage)
layout(rgba32f, binding = 0) uniform image2D u_outputImage;

// Atomic Counters
layout(binding = 0) uniform atomic_uint u_hitCounter;
```

## 4.5 Structures
User-defined compound types encapsulate related data:

```glsl
struct PointLight {
    vec3 position;
    float intensity;
    vec4 color;
};

// Instantiation & Constructor:
PointLight light = PointLight(vec3(0.0, 5.0, 0.0), 100.0, vec4(1.0, 0.9, 0.7, 1.0));
vec3 p = light.position;
```

## 4.6 Arrays
Arrays can store sequences of any built-in or user-defined type:

```glsl
float kernel[9];                           // Explicitly sized array
vec3 positions[] = vec3[](vec3(0), vec3(1), vec3(2)); // Implicit size via constructor

// Querying array size:
int count = kernel.length();               // Built-in method returns constant integer
```

## 4.7 Type Conversion & Casting
GLSL does **not** perform automatic lossy or implicit type conversions in older versions. Conversions must be explicit:

```glsl
int i = 5;
float f = float(i);     // Explicit cast constructor
uint u = uint(i);       // int to uint

// Widening conversions permitted in GLSL 1.30+ and GLSL 4.0+:
// int -> uint -> float -> double
float fine = 4;         // Legal in modern GLSL (widens int 4 to float 4.0)
```

---

# 5. Qualifiers & Storage Classes

## 5.1 Storage Qualifiers

```glsl
in        // Vertex input attribute or fragment interpolated varying
out       // Stage output
uniform   // Constant per draw-call, bound from host CPU application
buffer    // Shader Storage Buffer Object (SSBO), unbounded read/write
shared    // Compute shader workgroup local memory shared across threads
const     // Compile-time immutable constant expression
```

- `const`: Evaluated at shader compilation time.
  ```glsl
  const float PI = 3.14159265359;
  ```
- `uniform`: Read-only value constant across the entire primitive draw invocation. Passed from CPU (`glUniform*`, Panda3D `set_shader_input`).
- `in` / `out`: Link adjacent shader pipeline stages. A vertex shader output `out vec3 v_normal;` must match the fragment shader input `in vec3 v_normal;` in type, name, and interpolation qualifier.

## 5.2 Parameter Qualifiers
Control parameter passing semantics in function calls:

| Qualifier | Direction | Semantics |
| :--- | :--- | :--- |
| `in` | Caller $\to$ Callee | Value copied into function (default). Callee modifications do not affect caller. |
| `out` | Callee $\to$ Caller | Uninitialized on entry. Final value copied back to caller on return. |
| `inout` | Caller $\leftrightarrow$ Callee | Initialized on entry; modifications copied back to caller on return (pass-by-reference). |

```glsl
void computeTangent(in vec3 norm, out vec3 tangent, inout vec3 seed) {
    tangent = cross(norm, seed);
    seed = normalize(tangent + seed); // updates caller variable
}
```

## 5.3 Layout Qualifiers (`layout(...)`)
Introduced in modern GLSL to explicitly assign bindings, locations, and memory constraints directly in shader source code:

```glsl
// 1. Explicit Attribute Locations (Vertex Inputs):
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_normal;
layout(location = 2) in vec2 a_texCoord;

// 2. Explicit Framebuffer Render Targets (Fragment Outputs):
layout(location = 0) out vec4 out_color;
layout(location = 1) out vec4 out_normal_depth; // Multiple Render Targets (MRT)

// 3. Texture Unit Binding (OpenGL 4.2+ / GLSL 420):
layout(binding = 0) uniform sampler2D u_albedo;
layout(binding = 1) uniform sampler2D u_normalMap;

// 4. Compute Workgroup Dimensions:
layout(local_size_x = 16, local_size_y = 16, local_size_z = 1) in;

// 5. Early Fragment Depth Testing:
layout(early_fragment_tests) in; // Forces depth test before fragment shader runs
```

## 5.4 Interpolation Qualifiers
Define how per-vertex output values are rasterized across fragment triangles:

| Qualifier | Behavior |
| :--- | :--- |
| `smooth` | **Default**: Perspective-correct barycentric interpolation across the primitive. |
| `flat` | **No interpolation**: The fragment receives the value from the provoking vertex (typically the first or last vertex of the triangle). Required for integer/uint attributes. |
| `noperspective` | Screen-space linear interpolation without hyperbolic perspective divide. Useful for 2D UI elements. |

```glsl
// Vertex Shader:
flat out int v_materialID;
smooth out vec3 v_worldNormal;
noperspective out vec2 v_screenUV;

// Fragment Shader (MUST match qualifiers):
flat in int v_materialID;
smooth in vec3 v_worldNormal;
noperspective in vec2 v_screenUV;
```

### Auxiliary Qualifiers
- `centroid`: Forces interpolation to evaluate at a point guaranteed to lie inside the geometric boundary of the primitive, preventing multisample edge bleeding.
- `sample`: Forces per-sample evaluation when executing under Multi-Sample Anti-Aliasing (MSAA).

## 5.5 Precision Qualifiers
Essential in mobile hardware (GLSL ES) to balance arithmetic accuracy with battery, thermal, and silicon performance:

```glsl
precision highp float;      // 32-bit floating point (vertices, positions)
precision mediump float;    // 16-bit half-float (colors, normals, UVs)
precision lowp float;       // 8-bit to 10-bit fixed-point (normalized values [0..1])
```

- In **GLSL ES Fragment Shaders**, floating-point precision has no default; a global `precision mediump float;` or `precision highp float;` **must** be declared at the top of the file.

## 5.6 Invariance and Exactness
- `invariant`: Guarantees identical numerical calculation across multiple shaders. Essential for multi-pass rendering (e.g. shadow passes vs. color passes) to avoid Z-fighting:
  ```glsl
  invariant gl_Position;
  ```
- `precise`: Prevents aggressive compiler optimization (such as fused multiply-add `FMA` contractions) that could alter numerical evaluation order.

---

# 6. Expressions, Operators & Swizzling

## 6.1 Operator Precedence

| Precedence | Operator | Description | Associativity |
| :--- | :--- | :--- | :--- |
| **1 (Highest)** | `()` `[]` `.` `++` `--` | Call, subscript, swizzle/field, postfix | Left-to-Right |
| **2** | `++` `--` `+` `-` `!` `~` | Prefix inc/dec, unary signs, logical NOT, bitwise NOT | Right-to-Left |
| **3** | `*` `/` `%` | Multiplicative (multiply, divide, modulus) | Left-to-Right |
| **4** | `+` `-` | Additive (addition, subtraction) | Left-to-Right |
| **5** | `<<` `>>` | Bitwise shift left, shift right | Left-to-Right |
| **6** | `<` `>` `<=` `>=` | Relational inequality | Left-to-Right |
| **7** | `==` `!=` | Equality and inequality | Left-to-Right |
| **8** | `&` | Bitwise AND | Left-to-Right |
| **9** | `^` | Bitwise XOR | Left-to-Right |
| **10** | `\|` | Bitwise OR | Left-to-Right |
| **11** | `&&` | Logical AND (short-circuiting) | Left-to-Right |
| **12** | `^^` | Logical XOR | Left-to-Right |
| **13** | `\|\|` | Logical OR (short-circuiting) | Left-to-Right |
| **14** | `? :` | Ternary conditional | Right-to-Left |
| **15 (Lowest)**| `=` `+=` `-=` `*=` `/=` `%=` `<<=` `>>=` `&=` `^=` `\|=` | Assignment | Right-to-Left |

## 6.2 Swizzling
Vectors can access, replicate, and reorder their components using three interchangeable naming sets:

- **Coordinate set**: `{x, y, z, w}` (used for positions, directions)
- **Color set**: `{r, g, b, a}` (used for colors, channels)
- **Texture set**: `{s, t, p, q}` (used for texture coordinates)

```glsl
vec4 p = vec4(1.0, 2.0, 3.0, 4.0);

vec2 xy = p.xy;            // vec2(1.0, 2.0)
vec3 zyx = p.zyx;          // vec3(3.0, 2.0, 1.0) - Reordering
vec4 xxxx = p.xxxx;        // vec4(1.0, 1.0, 1.0, 1.0) - Replication
vec3 bgr = p.bgr;          // Valid using color set

// L-Value Swizzling (Assignment target):
vec3 v = vec3(0.0);
v.xy = vec2(1.0, 2.0);     // v is now vec3(1.0, 2.0, 0.0)
v.z = 3.0;                 // v is now vec3(1.0, 2.0, 3.0)
```

### Swizzling Rules
1. **Never mix sets in a single swizzle**: `p.xyr` or `p.rgz` is a compile error.
2. **Never duplicate components on the left side of an assignment (L-value)**:
   ```glsl
   p.xx = vec2(1.0, 2.0);  // ❌ ILLEGAL: Compiler cannot assign two different values to 'x'
   p.xz = vec2(1.0, 2.0);  // ✔ LEGAL: Assigns x=1.0 and z=2.0
   ```
3. A swizzle can never select more than 4 components.

## 6.3 Vector and Matrix Algebra
Arithmetic operators act **component-wise** on vectors, but execute **true linear algebra products** between matrices and vectors:

```glsl
vec3 a = vec3(1.0, 2.0, 3.0);
vec3 b = vec3(4.0, 5.0, 6.0);

// Component-wise multiplication:
vec3 c = a * b; // vec3(4.0, 10.0, 18.0)

// Matrix-Vector Multiplication:
mat4 M = ...;
vec4 pos = vec4(1.0, 0.0, 0.0, 1.0);
vec4 transformed = M * pos; // Linear algebraic matrix multiplication

// Vector-Matrix Multiplication (Row-vector):
vec4 rowTransformed = pos * M;

// Matrix-Matrix Multiplication:
mat4 MVP = projection * view * model; // Evaluates right-to-left transformations
```

---

# 7. Statements & Control Flow

## 7.1 Selection Statements
```glsl
// If-Else:
if (intensity > 0.8) {
    fragColor = vec4(1.0);
} else if (intensity > 0.4) {
    fragColor = vec4(0.6);
} else {
    fragColor = vec4(0.2);
}

// Switch-Case (Requires integer/uint expression):
switch (int(materialType)) {
    case 0:
        albedo = vec3(1.0, 0.0, 0.0);
        break;
    case 1:
        albedo = vec3(0.0, 1.0, 0.0);
        break;
    default:
        albedo = vec3(0.5);
        break;
}
```

## 7.2 Iteration Loops
```glsl
// For Loop:
for (int i = 0; i < 4; i++) {
    totalLight += computeLight(i);
}

// While Loop:
while (rayDistance < maxDistance) {
    rayDistance += marchStep();
}

// Do-While:
do {
    samples++;
} while (samples < 16);
```

## 7.3 Jump Statements & `discard`
- `continue`: Skips remainder of current loop iteration.
- `break`: Terminates the innermost loop or `switch`.
- `return [value]`: Exits function.
- `discard`: **Fragment shader only.** Halts processing of the current pixel fragment immediately. No pixel color is written, and the depth/stencil buffers remain unchanged.
  ```glsl
  if (texColor.a < 0.1) {
      discard; // Alpha cutoff punch-through
  }
  ```

## 7.4 GPU Execution Divergence
On physical GPU hardware, threads execute in lockstep groups called **Warps** (NVIDIA: 32 threads) or **Wavefronts** (AMD: 32/64 threads).
- If adjacent pixels take different paths of an `if-else` branch, the hardware **serializes** the execution: both branches run sequentially, with threads inactive on the alternate path masked out.
- **Tip**: Keep loop bounds uniform or use branchless arithmetic functions (`mix`, `step`, `clamp`) where performance is paramount.

---

# 8. Functions & Scope Rules

## 8.1 Declarations & Overloading
- Functions cannot be nested inside other functions.
- Functions must have an explicit return type (`void` if returning nothing).
- Overloading by argument type is fully supported.
- Recursion is **strictly prohibited** by the GLSL specification (GPUs lack a dynamic execution stack).

```glsl
// Function Prototype:
vec3 evaluateLighting(vec3 N, vec3 L, vec3 V, float roughness);

// Function Definition:
vec3 evaluateLighting(vec3 N, vec3 L, vec3 V, float roughness) {
    float NdotL = max(dot(N, L), 0.0);
    return vec3(NdotL * (1.0 - roughness));
}
```

## 8.2 The Entry Point
Every shader stage must implement a parameterless entry point:
```glsl
void main() {
    // Stage logic
}
```

## 8.3 Scoping Rules
- Variables declared inside a block `{ ... }` exist only within that block.
- Identifiers declared in an inner block shadow identically named identifiers in outer blocks.

---

# 9. Uniform Buffers and Storage Buffers

## 9.1 Uniform Blocks (UBO)
Uniform blocks group related uniform parameters into shared memory buffers backed by hardware Uniform Buffer Objects (UBOs):

```glsl
layout(std140, binding = 0) uniform CameraData {
    mat4 u_view;
    mat4 u_projection;
    mat4 u_viewProjection;
    vec3 u_cameraWorldPos;
    float u_nearPlane;
};
```

### The `std140` Memory Layout Rules
To guarantee memory parity between C++ host code and GPU shader memory, `std140` enforces strict alignment:
1. **Scalars** (`float`, `int`, `uint`): Aligned to 4 bytes.
2. **`vec2`**: Aligned to 8 bytes.
3. **`vec3` and `vec4`**: Aligned to **16 bytes**. *(Caution: `vec3` takes 16 bytes!)*
4. **Matrices** (`mat4`): Treated as an array of column vectors (each column vector aligned to 16 bytes).
5. **Arrays & Structs**: Every element is rounded up to a base alignment of **16 bytes**.

## 9.2 Shader Storage Buffer Objects (SSBO)
Available in OpenGL 4.3+ (`#version 430 core`) and compute shaders. SSBOs can be written to by shaders, can be unbounded in length, and follow the tighter `std430` packing rules:

```glsl
struct Particle {
    vec4 position;
    vec4 velocity;
};

layout(std430, binding = 1) buffer ParticleSystem {
    Particle particles[]; // Unbounded runtime array
};
```

---

# 10. Built-in Variables by Stage

## 10.1 Vertex Shader
- **Inputs**:
  - `gl_VertexID`: Integer index of the vertex being processed.
  - `gl_InstanceID`: Instance index when rendering via instanced draw calls (`glDrawArraysInstanced`).
- **Outputs**:
  - `gl_Position`: **Mandatory output.** Homogeneous clip-space position (`vec4`).
  - `gl_PointSize`: Size of rasterized point primitives in pixels (`float`).
  - `gl_ClipDistance[]`: Array of distances to user-defined clipping planes (`float`).

## 10.2 Tessellation Stages
- **Tessellation Control Shader (TCS)**:
  - Inputs: `gl_PatchVerticesIn`, `gl_PrimitiveID`, `gl_InvocationID`, `gl_in[]`.
  - Outputs: `gl_TessLevelOuter[4]`, `gl_TessLevelInner[2]`, `gl_out[]`.
- **Tessellation Evaluation Shader (TES)**:
  - Inputs: `gl_TessCoord` (`vec3` barycentric coordinates), `gl_TessLevelOuter`, `gl_TessLevelInner`, `gl_in[]`.
  - Outputs: `gl_Position`.

## 10.3 Geometry Shader
- Inputs: `gl_PrimitiveIDIn`, `gl_InvocationID`, `gl_in[]`.
- Outputs: `gl_Position`, `gl_PointSize`, `gl_Layer` (cubemap/array layer), `gl_ViewportIndex`.
- Primitive Generation: `EmitVertex()`, `EndPrimitive()`.

## 10.4 Fragment Shader
- **Inputs**:
  - `gl_FragCoord`: Window-space fragment coordinates $(x, y, z, 1/w)$. `xy` are pixel offsets; `z` is depth in range $[0..1]$.
  - `gl_FrontFacing`: Boolean; `true` if the fragment belongs to a front-facing primitive.
  - `gl_PointCoord`: 2D coordinates within a point sprite $[0..1]$.
  - `gl_SampleID`, `gl_SamplePosition`: Per-sample identifiers under MSAA.
- **Outputs**:
  - `gl_FragDepth`: Explicitly overwrites the hardware-computed fragment depth.

## 10.5 Compute Shader
- Inputs:
  - `gl_NumWorkGroups`: Total number of workgroups dispatched (`uvec3`).
  - `gl_WorkGroupID`: Index of the current workgroup within the dispatch grid (`uvec3`).
  - `gl_LocalInvocationID`: Local thread coordinate within current workgroup (`uvec3`).
  - `gl_GlobalInvocationID`: Unique 3D thread coordinate across all workgroups (`uvec3`):
    $$\text{GlobalID} = \text{WorkGroupID} \times \text{WorkGroupSize} + \text{LocalInvocationID}$$
  - `gl_LocalInvocationIndex`: Flattened 1D local invocation index within workgroup.

---

# 11. Built-in Functions (Standard Library)

All GLSL mathematical built-ins operate on scalars or component-wise on vectors.

## 11.1 Trigonometric Functions
*Angles are measured in radians.*
- `radians(deg)`, `degrees(rad)`: Conversion.
- `sin(x)`, `cos(x)`, `tan(x)`: Standard trigonometric ratios.
- `asin(x)`, `acos(x)`, `atan(y, x)`: Inverse trigonometry.
- `sinh(x)`, `cosh(x)`, `tanh(x)`: Hyperbolic functions.

## 11.2 Exponential Functions
- `pow(x, y)`: Calculates $x^y$ (undefined if $x < 0$).
- `exp(x)`: Natural exponential $e^x$.
- `log(x)`: Natural logarithm $\ln(x)$.
- `exp2(x)`, `log2(x)`: Base-2 exponential and logarithm.
- `sqrt(x)`: $\sqrt{x}$.
- `inversesqrt(x)`: Fast reciprocal square root $\frac{1}{\sqrt{x}}$.

## 11.3 Common Functions
- `abs(x)`: Absolute value $|x|$.
- `sign(x)`: Returns `-1.0` if $x < 0$, `0.0` if $x == 0$, `1.0` if $x > 0$.
- `floor(x)`, `ceil(x)`: Rounds down/up to nearest integer.
- `fract(x)`: Fractional part: $x - \text{floor}(x)$.
- `mod(x, y)`: Modulo / remainder: $x - y \cdot \text{floor}(x / y)$.
- `min(x, y)`, `max(x, y)`: Minimum / maximum bounds.
- `clamp(x, minVal, maxVal)`: Constrains $x$ within $[\text{minVal}, \text{maxVal}]$.
- `mix(x, y, a)`: Linear interpolation: $x(1 - a) + ya$.
- `step(edge, x)`: Returns `0.0` if $x < \text{edge}$, else `1.0`.
- `smoothstep(edge0, edge1, x)`: Hermite cubic interpolation between 0 and 1:
  $$t = \text{clamp}\left(\frac{x - \text{edge0}}{\text{edge1} - \text{edge0}}, 0.0, 1.0\right), \quad 3t^2 - 2t^3$$
- `isnan(x)`, `isinf(x)`: Checks for IEEE floating point NaN and infinity.
- `fma(a, b, c)`: Fused Multiply-Add: computes $(a \cdot b) + c$ with single rounding.

## 11.4 Geometric Functions
- `length(x)`: Euclidean vector magnitude: $\sqrt{x \cdot x}$.
- `distance(p0, p1)`: Euclidean distance between points: $\|p_0 - p_1\|$.
- `dot(x, y)`: Vector dot product: $x_1 y_1 + x_2 y_2 + \dots$
- `cross(x, y)`: 3D vector cross product ($\mathbf{x} \times \mathbf{y}$).
- `normalize(x)`: Returns unit vector in same direction: $\frac{x}{\|x\|}$.
- `faceforward(N, I, Nref)`: Flips normal if $\text{dot}(N_{ref}, I) > 0$.
- `reflect(I, N)`: Computes reflection vector:
  $$\mathbf{R} = \mathbf{I} - 2(\mathbf{N} \cdot \mathbf{I})\mathbf{N}$$
- `refract(I, N, eta)`: Snell's law refraction vector for ratio of refractive indices $\eta = \frac{\eta_1}{\eta_2}$.

## 11.5 Matrix Functions
- `matrixCompMult(A, B)`: Component-wise matrix multiplication (not linear algebra product).
- `transpose(M)`: Matrix transpose $\mathbf{M}^T$.
- `determinant(M)`: Scalar determinant $\det(\mathbf{M})$.
- `inverse(M)`: Matrix inverse $\mathbf{M}^{-1}$.
- `outerProduct(c, r)`: Computes outer product matrix: $\mathbf{c} \cdot \mathbf{r}^T$.

## 11.6 Vector Relational Functions
Perform component-wise comparisons, returning boolean vectors (`bvec`):
- `lessThan(x, y)`, `lessThanEqual(x, y)`
- `greaterThan(x, y)`, `greaterThanEqual(x, y)`
- `equal(x, y)`, `notEqual(x, y)`
- `any(bvec)`: Returns `true` if any component is true.
- `all(bvec)`: Returns `true` only if all components are true.
- `not(bvec)`: Component-wise boolean inversion.

## 11.7 Integer & Bit Manipulation
- `bitfieldExtract(value, offset, bits)`: Extracts range of bits.
- `bitfieldInsert(base, insert, offset, bits)`: Overwrites range of bits.
- `bitfieldReverse(value)`: Reverses bit order.
- `bitCount(value)`: Counts set bits (population count).
- `findLSB(value)`, `findMSB(value)`: Finds least/most significant set bit.

## 11.8 Texture Sampling & Queries
Modern GLSL unifies all texture queries under overloaded `texture(...)` functions:

```glsl
// Basic sampling:
vec4 color = texture(sampler2D sampler, vec2 uv);
vec4 cube   = texture(samplerCube sampler, vec3 dir);

// Explicit Level of Detail (LOD):
vec4 lodTex = textureLod(sampler2D sampler, vec2 uv, float lodLevel);

// Texel Fetch (Integer pixel coordinates without filtering or normalization):
vec4 rawPixel = texelFetch(sampler2D sampler, ivec2 pixelCoord, int lodLevel);

// Texture Size Query:
ivec2 dims = textureSize(sampler2D sampler, int lodLevel);

// Texture Offset:
vec4 offsetPixel = textureOffset(sampler2D sampler, vec2 uv, ivec2(-1, 0));

// Texture Gather (Samples 2x2 footprint of single channel without bilinear blend):
vec4 redFourTap = textureGather(sampler2D sampler, vec2 uv, 0); // 0 = Red channel
```

## 11.9 Screen-Space Derivatives (Fragment Stage Only)
Evaluate the hardware finite rate of change across neighboring $2 \times 2$ pixel quads:
- `dFdx(p)`: Partial derivative $\frac{\partial p}{\partial x}$ in window coordinates.
- `dFdy(p)`: Partial derivative $\frac{\partial p}{\partial y}$ in window coordinates.
- `fwidth(p)`: Absolute sum of derivatives: $|dFdx(p)| + |dFdy(p)|$. Essential for procedural anti-aliasing.

### Example: Procedural Analytic Normal Generation
```glsl
vec3 calculateFlatNormal(vec3 worldPos) {
    vec3 dX = dFdx(worldPos);
    vec3 dY = dFdy(worldPos);
    return normalize(cross(dX, dY));
}
```

## 11.10 Compute Synchronization
- `barrier()`: Synchronizes all compute invocations in the current workgroup. No invocation proceeds past the barrier until all have arrived.
- `memoryBarrier()`: Enforces memory visibility order across memory accesses.

---

# 12. Version Matrix & Migration Guide

### Legacy vs. Modern GLSL Cheat Sheet

| Feature | Legacy GLSL (1.10 - 1.20) | Modern GLSL (1.50+ / 330+) |
| :--- | :--- | :--- |
| **Vertex Inputs** | `attribute vec4 gl_Vertex;` | `in vec4 in_position;` |
| **Vertex-to-Fragment**| `varying vec3 v_normal;` | `out vec3 v_normal;` (VS) / `in vec3 v_normal;` (FS) |
| **Fragment Output** | `gl_FragColor = color;` | `out vec4 out_color;` |
| **Texture 2D** | `texture2D(tex, uv)` | `texture(tex, uv)` |
| **Cube Map Texture** | `textureCube(env, dir)` | `texture(env, dir)` |
| **Built-in Matrices** | `gl_ModelViewProjectionMatrix` | Custom uniform / UBO (`p3d_ModelViewProjectionMatrix`) |
| **Integer bitwise ops**| ❌ Not supported | `&`, `\|`, `^`, `<<`, `>>` fully supported |
| **Uniform layouts** | Uniform locations driver-dependent | `layout(location = 0)`, `layout(binding = 0)` |

---

# 13. Common Compiler Errors & Debugging

| Error / Symptom | Root Cause | Fix |
| :--- | :--- | :--- |
| **`#version must occur before any other statement`** | Comments, empty lines, or characters placed before `#version`. | Move `#version` to line 1 without leading whitespace. |
| **`Cannot convert 'int' to 'float'`** | Passing integer literal where float is expected in older GLSL. | Append `.0` or `f`: write `2.0` instead of `2`. |
| **`Varying 'foo' not written / read mismatch`** | Name, type, or qualifier mismatch between vertex `out` and fragment `in`. | Verify that vertex output matches fragment input name, type (`vec3`), and interpolation (`flat`/`smooth`) identically. |
| **`Undeclared identifier: gl_FragColor`** | Using deprecated `gl_FragColor` under `#version 150` or `#version 330 core`. | Declare custom fragment output: `out vec4 fragColor;` and assign to it. |
| **`Non-constant array index in sampler lookup`** | Older GPUs cannot index arrays of samplers with dynamic variables. | Use compile-time constant indices or uniform arrays. |
| **`Swizzle duplicate component assignment`** | Attempting to write to repeated components (`v.xx = ...`). | Target each vector component at most once on the left-hand side. |
| **Black screen / No render** | Missing `gl_Position` assignment in vertex shader. | Ensure `gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;` is executed on all execution paths. |
| **Z-fighting across multiple passes** | Floating-point rounding discrepancies between passes. | Mark clip position as `invariant gl_Position;` in both passes. |
