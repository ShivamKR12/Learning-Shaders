# Minimal Shaders & GLSL Foundations

A progressive collection of introductory GLSL shaders and Panda3D Python drivers demonstrating the core foundations of modern GPU programming. Each sample isolates a single fundamental concept—from the absolute bare-minimum solid-color pipeline to vertex attribute pass-throughs, CPU-to-GPU uniforms, 2D texture sampling, alpha testing, and UV distortion.

These shaders adhere to modern GLSL standards (GLSL 1.50 / GLSL ES 3.00), utilizing explicit vertex input attributes, custom fragment output targets, and Panda3D's automatic matrix uniforms.

---

## Quick start

```bash
# Ensure dependencies are installed (Panda3D 1.10.13+)
pip install -r ../requirements.txt

# Run any of the foundational shader demos
python Minimal-Working-Shader.py
python Minimal-PassThrough-Shader.py
python Minimal-Tint-Shader.py
python Minimal-Pulse-Shader.py
python Minimal-Texture-Shader.py
python Minimal-Alpha-Cutoff-Shader.py
python Minimal-UVDistortion-Shader.py
```

### Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |

---

## Technical Overview

### 1. Minimal Working Shader (`Minimal-Working-Shader.*`)
- **Vertex Stage**: Receives the raw 3D vertex position `p3d_Vertex` and transforms it to clip space using `p3d_ModelViewProjectionMatrix`:
  $$\mathbf{v}_{clip} = \mathbf{M}_{MVP} \cdot \mathbf{v}_{local}$$
- **Fragment Stage**: Emits a constant solid RGBA color (`vec4(1.0, 0.4, 0.2, 1.0)`) directly to the framebuffer.

### 2. Attribute Pass-Through (`Minimal-PassThrough-Shader.*`)
- Demonstrates inter-stage data communication (`out` in vertex shader matching `in` in fragment shader).
- Interpolates per-vertex color attributes across polygon faces using the GPU hardware rasterizer.

### 3. Uniform Inputs & Animation (`Minimal-Tint-Shader.*`, `Minimal-Pulse-Shader.*`)
- **CPU-to-GPU Uniforms**: Demonstrates `set_shader_input()` in Panda3D.
- **Time Animation**: Samples elapsed time $t$ to compute smooth cyclic intensity oscillations:
  $$I(t) = |\sin(t)|$$

### 4. Texture Sampling & Discard (`Minimal-Texture-Shader.*`, `Minimal-Alpha-Cutoff-Shader.*`)
- Samples 2D image data using normalized texture coordinates:
  $$C = \text{texture}(u\_tex, \mathbf{uv})$$
- Implements alpha cutoff (screen-door transparency / punch-through alpha) using the GLSL `discard` statement:
  $$\text{if } (C.a < 0.1) \implies \text{discard}$$

### 5. UV Wave Distortion (`Minimal-UVDistortion-Shader.*`)
- Dynamically offsets texture lookup coordinates over time to produce fluid ripples:
  $$\mathbf{uv}' = \mathbf{uv} + \begin{pmatrix} \sin(uv_y \cdot 10.0 + t) \cdot 0.02 \\ 0 \end{pmatrix}$$

---

## Reference

### Script Catalog

| Script | Vertex Shader | Fragment Shader | Target Model | Key Feature |
|---|---|---|---|---|
| `Minimal-Working-Shader.py` | `Minimal-Working-Shader.vert` | `Minimal-Working-Shader.frag` | `models/teapot` | MVP transformation, solid color output |
| `Minimal-PassThrough-Shader.py` | `Minimal-PassThrough-Shader.vert` | `Minimal-PassThrough-Shader.frag` | `models/teapot` | Vertex attribute interpolation (`in`/`out`) |
| `Minimal-Tint-Shader.py` | `Minimal-Tint-Shader.vert` | `Minimal-Tint-Shader.frag` | `models/teapot` | Engine-to-shader `uniform vec4` tint |
| `Minimal-Pulse-Shader.py` | `Minimal-Pulse-Shader.vert` | `Minimal-Pulse-Shader.frag` | `models/teapot` | Dynamic time-based pulsing via `taskMgr` |
| `Minimal-Texture-Shader.py` | `Minimal-Texture-Shader.vert` | `Minimal-Texture-Shader.frag` | `models/panda-model` | `sampler2D` lookup with UV mapping |
| `Minimal-Alpha-Cutoff-Shader.py` | `Minimal-Alpha-Cutoff-Shader.vert` | `Minimal-Alpha-Cutoff-Shader.frag` | `models/smiley` | Hard alpha cutoff via fragment `discard` |
| `Minimal-UVDistortion-Shader.py` | `Minimal-UVDistortion-Shader.vert` | `Minimal-UVDistortion-Shader.frag` | `models/panda-model` | Animated sine wave UV texture distortion |

### Layout

```
01-minimal-shaders/
├── Minimal-Working-Shader.py            # Baseline solid color demo
├── Minimal-Working-Shader.vert          # Minimal clip-space transform
├── Minimal-Working-Shader.frag          # Flat color output
├── Minimal-PassThrough-Shader.py        # Color attribute pass-through demo
├── Minimal-PassThrough-Shader.vert      # Passes vertex colors to fragment stage
├── Minimal-PassThrough-Shader.frag      # Renders interpolated vertex color
├── Minimal-Tint-Shader.py               # Uniform tint demo
├── Minimal-Tint-Shader.vert             # Passes UV & position
├── Minimal-Tint-Shader.frag             # Multiplies base color with uniform tint
├── Minimal-Pulse-Shader.py              # Time-varying uniform demo
├── Minimal-Pulse-Shader.vert            # Passes geometry
├── Minimal-Pulse-Shader.frag            # Calculates sin(time) brightness
├── Minimal-Texture-Shader.py            # 2D Texture sampling demo
├── Minimal-Texture-Shader.vert          # Supplies UV coordinates
├── Minimal-Texture-Shader.frag          # Texture sampler lookup
├── Minimal-Alpha-Cutoff-Shader.py       # Alpha test demo
├── Minimal-Alpha-Cutoff-Shader.vert     # UV pass-through
├── Minimal-Alpha-Cutoff-Shader.frag     # Discards fragments below alpha threshold
├── Minimal-UVDistortion-Shader.py       # Animated texture ripple demo
├── Minimal-UVDistortion-Shader.vert     # Passes texture coordinates
├── Minimal-UVDistortion-Shader.frag     # Sine-modulated UV coordinate lookup
├── cam.py                              # Free-fly Blender camera controller
├── Config.prc                           # Panda3D window and model search paths
└── README.md                            # Documentation
```

---

## Limitations & Technical Notes

- Requires an OpenGL 3.2+ Core Profile capable driver.
- Shaders use `#version 150` for desktop OpenGL compatibility; for mobile OpenGLES 3.0, replace `#version 150` with `#version 300 es` and supply precision qualifiers (`precision mediump float;`).

