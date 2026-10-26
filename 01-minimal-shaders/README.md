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

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-working-shader`**](01-working-shader/README.md) | `Minimal-Working-Shader.py` | `Minimal-Working-Shader.frag`, `Minimal-Working-Shader.vert` | Working Shader |
| [**`02-pass-through`**](02-pass-through/README.md) | `Minimal-PassThrough-Shader.py` | `Minimal-PassThrough-Shader.frag`, `Minimal-PassThrough-Shader.vert` | Pass Through |
| [**`03-tint`**](03-tint/README.md) | `Minimal-Tint-Shader.py` | `Minimal-Tint-Shader.frag`, `Minimal-Tint-Shader.vert` | Tint |
| [**`04-pulse`**](04-pulse/README.md) | `Minimal-Pulse-Shader.py` | `Minimal-Pulse-Shader.frag`, `Minimal-Pulse-Shader.vert` | Pulse |
| [**`05-texture`**](05-texture/README.md) | `Minimal-Texture-Shader.py` | `Minimal-Texture-Shader.frag`, `Minimal-Texture-Shader.vert` | Texture |
| [**`06-alpha-cutoff`**](06-alpha-cutoff/README.md) | `Minimal-Alpha-Cutoff-Shader.py` | `Minimal-Alpha-Cutoff-Shader.frag`, `Minimal-Alpha-Cutoff-Shader.vert` | Alpha Cutoff |
| [**`07-uv-distortion`**](07-uv-distortion/README.md) | `Minimal-UVDistortion-Shader.py` | `Minimal-UVDistortion-Shader.frag`, `Minimal-UVDistortion-Shader.vert` | Uv Distortion |

### Layout

```
01-minimal-shaders/
├── 01-working-shader/
│   ├── Minimal-Working-Shader.py
│   ├── Minimal-Working-Shader.frag
│   ├── Minimal-Working-Shader.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-pass-through/
│   ├── Minimal-PassThrough-Shader.py
│   ├── Minimal-PassThrough-Shader.frag
│   ├── Minimal-PassThrough-Shader.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 03-tint/
│   ├── Minimal-Tint-Shader.py
│   ├── Minimal-Tint-Shader.frag
│   ├── Minimal-Tint-Shader.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 04-pulse/
│   ├── Minimal-Pulse-Shader.py
│   ├── Minimal-Pulse-Shader.frag
│   ├── Minimal-Pulse-Shader.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 05-texture/
│   ├── Minimal-Texture-Shader.py
│   ├── Minimal-Texture-Shader.frag
│   ├── Minimal-Texture-Shader.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 06-alpha-cutoff/
│   ├── Minimal-Alpha-Cutoff-Shader.py
│   ├── Minimal-Alpha-Cutoff-Shader.frag
│   ├── Minimal-Alpha-Cutoff-Shader.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 07-uv-distortion/
│   ├── Minimal-UVDistortion-Shader.py
│   ├── Minimal-UVDistortion-Shader.frag
│   ├── Minimal-UVDistortion-Shader.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- Requires an OpenGL 3.2+ Core Profile capable driver.
- Shaders use `#version 150` for desktop OpenGL compatibility; for mobile OpenGLES 3.0, replace `#version 150` with `#version 300 es` and supply precision qualifiers (`precision mediump float;`).

