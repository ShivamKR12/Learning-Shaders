GLSL has **very strict grammar rules** — stricter than Python or C — because it is a real compiled language.

---

# 🟥 1. **File Structure Rules**

GLSL has a strict file layout:

### ✔ Rule 1 — The **first non-comment line** must be:

```glsl
#version 150   // or another version
```

### ✔ Rule 2 — You cannot put code before the version line

(No variables, no imports, nothing.)

### ✔ Rule 3 — A GLSL file contains:

* **global variable declarations**
* **uniform declarations**
* **functions**
* **main() function**

Example skeleton:

```glsl
#version 150

uniform float time;
in vec3 pos;

out vec4 fragColor;

void someFunction() {
    // ...
}

void main() {
    // ...
}
```

---

# 🟧 2. **Syntax Rules (Like C Language)**

GLSL uses a C-like syntax:

### ✔ Statements end with **semicolon**

```glsl
float x = 1.0;   // REQUIRED ; 
```

### ✔ Curly braces define blocks

```glsl
void main() {
    // block
}
```

### ✔ Comments follow C rules

```glsl
// single-line comment
/* multi-line comment */
```

### ✔ Case sensitive

`vec3`, `Vec3`, and `VEc3` are all different and only the first is valid.

---

# 🟨 3. **Type System Rules**

GLSL is **strongly typed**:

### Built-in scalar types:

* `float`
* `int`
* `uint`
* `bool`

### Vector types:

* `vec2`, `vec3`, `vec4`
* `ivec2`, etc.

### Matrix types:

* `mat2`, `mat3`, `mat4`

### Samplers (textures):

* `sampler2D`
* `samplerCube`
  (and others, depending on version)

### ✔ You cannot mix types without explicit casting

This is ILLEGAL:

```glsl
float x = 1 + vec3(1);   // ❌ NO
```

You must assign matching types.

### ✔ Constructors look like function calls

```glsl
vec3 color = vec3(1.0, 0.0, 0.0);
```

---

# 🟩 4. **Variable Declaration Rules**

### GLSL variable types must appear **before** usage:

```glsl
float a = 1.0;
vec3 b = vec3(0.1, 0.2, 0.3);
```

### You cannot reassign to `const` variables

```glsl
const float PI = 3.14159;
PI = 2.0;   // ❌ ERROR
```

### Storage qualifiers:

* `in` — input (vertex input, fragment input, uniforms in older GLSL)
* `out` — output (vertex output, fragment output)
* `uniform` — constant per draw-call
* `const` — compile-time constant

---

# 🟦 5. **Function Rules**

### ✔ Every shader must have:

```glsl
void main()
```

### ✔ Functions cannot be nested

NO:

```glsl
void main() {
    void helper() {}  // ❌ ERROR
}
```

### ✔ Functions must have declared types

```glsl
float compute(vec3 v) {
    return v.x * 2.0;
}
```

### ✔ You may forward declare, but rarely needed

---

# 🟪 6. **Vertex Shader–Specific Rules**

Vertex shaders have access to:

```glsl
in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec2 p3d_MultiTexCoord0;
```

They **must** write:

```glsl
gl_Position = ...;
```

Other optional outputs:

```glsl
out vec3 normal;
out vec2 uv;
```

Vertex shaders cannot read textures (in older GLSL versions)
though modern GLSL **can**.

---

# 🟫 7. **Fragment Shader–Specific Rules**

Fragment shaders:

### ✔ Receive varyings from vertex shader using `in`

```glsl
in vec2 uv;
```

### ✔ Must have at least one output

```glsl
out vec4 fragColor;
```

### ✔ Cannot write `gl_Position` (that’s vertex-only)

### ✔ Cannot modify geometry — only color

### ✔ Can sample textures

Example:

```glsl
uniform sampler2D tex;
vec4 color = texture(tex, uv);
```

---

# 🔵 8. **The Rules for `in`, `out`, and `uniform`**

### ✔ In vertex shader:

```glsl
in vec4 p3d_Vertex;   // from Mesh
out vec2 uv;
```

### ✔ In fragment shader:

```glsl
in vec2 uv;           // from vertex shader
out vec4 fragColor;
```

### ✔ Uniforms: same in both shaders

```glsl
uniform float time;
uniform sampler2D tex;
```

Uniforms:

* cannot be assigned inside the shader
* are set from your Python code (Panda3D)

---

# 🟣 9. **Common Mistakes That Break GLSL**

### ❌ Forgetting semicolon

### ❌ Using wrong variable type

### ❌ Writing shader code before #version

### ❌ Not matching vertex outputs to fragment inputs

### ❌ Output name mismatch

Example:

```glsl
// vertex
out vec2 uv;    // must match EXACTLY

// fragment
in vec2 UV;     // ❌ mismatch — breaks
```

### ❌ Missing gl_Position in vertex shader

### ❌ No output in fragment shader

### ❌ Swizzling incorrectly (e.g. mix using xyz, w)

---

# 🔴 1. FILE STRUCTURE RULES

A GLSL shader MUST follow this structure:

```
#version <number>

[global variable declarations]
[uniform declarations]
[in/out declarations]
[function definitions]

void main() {
    ...
}
```

### ✔ **#version line must be first non-comment**

❌ NO code before it.

---

# 🟠 2. COMMENTS

```glsl
// single-line comment
/* multi-line
   comment */
```

---

# 🟡 3. SEMICOLONS & STATEMENTS

EVERY statement ends with a semicolon:

```glsl
float x = 3.0;
vec3 y = vec3(1.0);
```

---

# 🟢 4. BASIC TYPES

GLSL is strongly typed.

### Scalars:

```
float
int
uint
bool
```

### Vectors:

```
vec2, vec3, vec4
ivec2, uvec2, bvec3, ...
```

### Matrices:

```
mat2, mat3, mat4
```

### Samplers (textures):

```
sampler1D
sampler2D
sampler3D
samplerCube
```

---

# 🔵 5. VARIABLE DECLARATION GRAMMAR

General form:

```glsl
[qualifier] type name [ = initial_value ];
```

Examples:

```glsl
uniform float time;
in vec3 p3d_Vertex;
out vec2 uv;
vec3 color = vec3(1.0, 0.5, 0.2);
```

### Qualifiers:

| Qualifier | Meaning                     |
| --------- | --------------------------- |
| `in`      | Input to shader stage       |
| `out`     | Output to next stage        |
| `uniform` | Constant value set from CPU |
| `const`   | Compile-time constant       |
| `flat`    | Disable interpolation       |
| `smooth`  | Default interpolation       |

---

# 🟣 6. CONSTRUCTORS

GLSL types can be constructed like functions:

```glsl
vec3 a = vec3(1.0, 0.5, 0.2);
mat4 m = mat4(1.0);
```

---

# 🟤 7. OPERATORS

GLSL supports:

### Arithmetic:

```
+  -  *  /  
```

### Component-wise vector operations:

```glsl
vec3 a = vec3(1) * vec3(2);  // OK
```

### Dot and cross:

```glsl
dot(a,b)
cross(a,b)
```

### Comparison:

```
== != < > <= >=
```

### Logical:

```
&& || !
```

---

# ⚫ 8. SWIZZLING

Rearrange vector components:

```glsl
vec3 v = vec3(1,2,3);

v.xy   // vec2
v.zx   // vec2
v.xxx  // vec3
v.bgra // allowed with color-style names
```

---

# 🟩 9. FUNCTIONS

### Declaration:

```glsl
float add(float a, float b) {
    return a + b;
}
```

### Overloading allowed.

### No nested functions allowed.

### Must have a `void main()`.

---

# 🟥 10. CONTROL STRUCTURES

### If / else:

```glsl
if (x > 0.5) {
    ...
} else {
    ...
}
```

### For loop:

```glsl
for (int i = 0; i < 10; i++) {
    ...
}
```

### While loop:

```glsl
while (x < 5.0) {
    ...
}
```

---

# 🟧 11. QUALIFIER RULES (VERY IMPORTANT)

## Vertex shader:

```glsl
in vec4 position;
out vec2 uv;
gl_Position = ...;   // MUST be set
```

## Fragment shader:

```glsl
in vec2 uv;
out vec4 fragColor;  // MUST be set
```

## Uniforms:

```glsl
uniform float time;
uniform sampler2D texture0;
```

Uniforms:

* cannot be assigned values inside the shader
* must be set from CPU code (Panda3D Python)

---

# 🟨 12. TEXTURE SAMPLING

Valid texture functions:

```glsl
texture(sampler2D, vec2)         // main one
texture(samplerCube, vec3)
```

Example:

```glsl
uniform sampler2D tex;
in vec2 uv;
out vec4 fragColor;

void main(){
    fragColor = texture(tex, uv);
}
```

---

# 🟩 13. INTERPOLATION RULES

Vertex → fragment interpolation is automatic.

```glsl
// vertex
out vec3 normal;

// fragment
in vec3 normal;
```

To disable interpolation:

```glsl
flat out int id;
flat in int id;
```

---

# 🟦 14. BUILT-IN VARIABLES

### In vertex shader:

```
gl_Position     (must be written)
```

### In fragment shader:

```
gl_FragCoord     (pixel coordinates)
gl_FrontFacing   (bool)
```

---

# 🟪 15. GLSL KEYWORDS (Do NOT use as variable names)

```
attribute break buffer bvec2 bvec3 bvec4 
case cast centroid class const continue 
default discard do else enum extern 
flat float for highp if in inout inline 
invariant layout lowp mat2 mat3 mat4 
mediump out precision return sampler2D 
sampler3D samplerCube struct switch 
uint uniform varying vec2 vec3 vec4 
void while
```

---

# ⚡ 16. COMMON GRAMMAR ERRORS TO AVOID

❌ Missing semicolon
❌ Mismatched in/out names (must match EXACTLY)
❌ Wrong type assignment
❌ Using ints where floats required (`1` vs `1.0`)
❌ Declaring code before `#version`
❌ Not writing to `gl_Position` in vertex shader
❌ Not writing to an `out` variable in fragment shader
❌ Using tabs/spaces inside `#version` (not allowed in some drivers!)

---
