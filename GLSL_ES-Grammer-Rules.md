
---

# 🔵 1. FILE STRUCTURE RULES

### ✔ First non-comment line **must** be:

```glsl
#version 300 es
```

### ✔ A typical file contains:

```glsl
#version 300 es

precision mediump float;   // required for fragment shaders

// global variables
// uniforms
// in/out declarations
// function definitions

void main() {
    // required function
}
```

---

# 🔵 2. COMMENTS

```glsl
// single-line comment
/* multi-line
   comment */
```

---

# 🔵 3. PRECISION RULES (ES 3.00)

### ✔ Fragment shaders **must** define a default float precision:

```glsl
precision mediump float;
```

### ✔ Valid precisions:

```
lowp
mediump
highp
```

Example:

```glsl
precision highp float;
precision mediump int;
```

---

# 🔵 4. DATA TYPES

### Scalars:

```
float
int
uint
bool
```

### Vectors:

```
vec2  vec3  vec4
ivec2 ivec3 ivec4
uvec2 uvec3 uvec4
bvec2 bvec3 bvec4
```

### Matrices:

```
mat2 mat3 mat4
mat2x3 mat3x4 mat4x3 mat2x4 mat4x2
```

### Samplers:

```
sampler2D
sampler3D
samplerCube
sampler2DShadow
sampler2DArray
sampler2DArrayShadow
samplerCubeShadow
```

Example:

```glsl
uniform sampler2D diffuseMap;
```

---

# 🔵 5. VARIABLE DECLARATION SYNTAX

### General grammar:

```glsl
[qualifier] type name [ = value ];
```

### Allowed qualifiers:

```
in
out
uniform
const
flat
smooth
noperspective
```

Examples:

```glsl
in vec3 position;
out vec2 uv;
uniform float time;
const float PI = 3.14159;
```

---

# 🔵 6. SWIZZLING (Vector component access)

### Valid component sets:

```
.xyzw
.rgba
.stpq
```

Examples:

```glsl
vec3 v = vec3(1.0, 2.0, 3.0);
float a = v.x;      // 1.0
vec2 b = v.yz;      // vec2(2.0, 3.0)
vec3 c = v.xxx;     // vec3(1.0,1.0,1.0)
```

---

# 🔵 7. OPERATORS

### Arithmetic:

```
+  -  *  /  %
```

### Logical:

```
&&  ||  !
```

### Comparison:

```
==  !=  <  >  <=  >=
```

Example:

```glsl
if (dot(n, l) > 0.0) { ... }
```

---

# 🔵 8. CONTROL STRUCTURES

### if/else:

```glsl
if (x > 0.5) {
    ...
} else {
    ...
}
```

### for:

```glsl
for (int i = 0; i < 10; i++) {
    ...
}
```

### while:

```glsl
while (x < 1.0) {
    x += 0.1;
}
```

### do/while:

```glsl
do {
    x++;
} while (x < 5);
```

---

# 🔵 9. FUNCTIONS

### Grammar:

```glsl
returnType functionName(argType argName, ...) {
    ...
}
```

Example:

```glsl
float saturate(float x) {
    return clamp(x, 0.0, 1.0);
}
```

### Rules:

* No nested functions
* Overloading allowed
* No recursion

---

# 🔵 10. THE `main()` FUNCTION

Required:

```glsl
void main() {
}
```

Vertex shaders must write **gl_Position**.
Fragment shaders must write to at least one **user-defined output**.

---

# 🔵 11. INTERFACE VARIABLES (in/out)

## Vertex Shader → Fragment Shader

```glsl
// Vertex shader:
out vec3 normal;

// Fragment shader:
in vec3 normal;
```

Names must match exactly (case sensitive).

---

# 🔵 12. UNIFORMS (CPU → GPU)

Syntax:

```glsl
uniform type name;
```

Examples:

```glsl
uniform float time;
uniform vec3 lightPos;
uniform sampler2D diffuseMap;
```

### Rules:

* Cannot be assigned inside the shader.
* Same in both vertex and fragment shaders.

---

# 🔵 13. VERTEX SHADER–SPECIFIC GRAMMAR

### Required output:

```glsl
gl_Position = ...;
```

### Input attributes from the application:

```glsl
in vec3 position;
in vec3 normal;
in vec2 texcoord;
```

### Example valid ES 3.00 vertex shader:

```glsl
#version 300 es
precision highp float;

in vec3 position;
in vec2 texcoord;

out vec2 v_uv;

uniform mat4 mvp;

void main() {
    v_uv = texcoord;
    gl_Position = mvp * vec4(position, 1.0);
}
```

---

# 🔵 14. FRAGMENT SHADER–SPECIFIC GRAMMAR

### Must define float precision:

```glsl
precision mediump float;
```

### Must declare a color output:

```glsl
out vec4 fragColor;
```

### Example valid ES 3.00 fragment shader:

```glsl
#version 300 es
precision mediump float;

in vec2 v_uv;
out vec4 fragColor;

uniform sampler2D tex;

void main() {
    fragColor = texture(tex, v_uv);
}
```

---

# 🔵 15. TEXTURE SAMPLING

### Modern ES 3.00 function:

```glsl
texture(sampler, coords)
```

Examples:

```glsl
vec4 c = texture(diffuseMap, uv);
float depth = texture(depthMap, uv).r;
```

---

# 🔵 16. INTERPOLATION QUALIFIERS

```glsl
smooth in vec3 normal;        // default
flat in int instanceID;       // no interpolation
noperspective in vec3 pos;    // linear interpolation without perspective correction
```

---

# 🔵 17. DISCARD (fragment shader only)

Stops the fragment from being drawn:

```glsl
if (alpha < 0.1) {
    discard;
}
```

---

# 🔵 18. STRUCTS

Grammar:

```glsl
struct Light {
    vec3 color;
    vec3 dir;
};

uniform Light sun;
```

---

# 🔵 19. ARRAYS

```glsl
float values[3];
values[0] = 1.0;
```

---

# 🔵 20. COMMON ES 3.00 ERRORS

❌ Missing precision declaration in fragment shader
❌ Using "gl_FragColor" (not allowed in ES 3.00)
❌ Using "attribute" or "varying" (removed)
❌ Mismatched `in`/`out` between shader stages
❌ Assigning to a uniform
❌ Missing semicolon
❌ Using desktop-only functions

---
