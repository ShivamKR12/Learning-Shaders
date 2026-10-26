# Learning Shaders: The Comprehensive Panda3D GLSL Laboratory

An end-to-end curriculum and interactive laboratory for learning real-time Computer Graphics and GLSL shaders using Python and the [Panda3D](https://www.panda3d.org/) game engine.

The repository spans from bare-minimum programmable pipeline foundations to advanced Physically Based Rendering (PBR), Cook-Torrance microfacet BRDFs, procedural vertex wave simulations, dynamic atmospheric skydomes, multi-layer terrain texture splatting, and complete real-time water shaders with offscreen render-to-texture (RTT) reflections and refractions.

---

## 🗂️ Curriculum & Module Index

The repository is organized into 10 structured, progressive modules. Each sub-directory includes its own dedicated runnable scripts, vertex/fragment shaders, and comprehensive technical documentation:

| # | Module Directory | Focus & Core Techniques | Key Mathematical Models |
|---|---|---|---|
| **01** | [**`01-minimal-shaders`**](01-minimal-shaders/README.md) | GLSL program structure, MVP matrix transform, vertex attributes, uniforms, texture sampling, alpha testing, UV distortion. | $`\mathbf{v}_{\text{clip}} = \mathbf{M}_{\text{MVP}} \cdot \mathbf{v}`$ |
| **02** | [**`02-vertex-deformations`**](02-vertex-deformations/README.md) | Procedural vertex shader displacement, sine waves, directional waves, height-dependent torsional twists, normal extrusion, radial explosions. | $`y' = y + \sin(x\omega + ts)A, \quad \mathbf{R}_{\text{twist}}(z)`$ |
| **03** | [**`03-lambert-lighting`**](03-lambert-lighting/README.md) | Matte surface reflectance, Johann Heinrich Lambert's cosine law, ambient light fill, material base color modulation, textured diffuse shading. | $`I = \max(\mathbf{N} \cdot \mathbf{L}, 0.0) + k_a`$ |
| **04** | [**`04-phong-lighting`**](04-phong-lighting/README.md) | Bui Tuong Phong's classical illumination model: Ambient, Diffuse, and view-dependent Specular highlights via reflection vectors. | $`I_{\text{spec}} = \max(\mathbf{R} \cdot \mathbf{V}, 0)^\alpha`$ |
| **05** | [**`05-blinn-phong-lighting`**](05-blinn-phong-lighting/README.md) | Jim Blinn's halfway vector formulation ($\mathbf{H}$), localized 3D point lights, inverse-square physical distance attenuation. | $`I_{\text{spec}} = \max(\mathbf{N} \cdot \mathbf{H}, 0)^\beta, \quad \frac{1}{d^2}`$ |
| **06** | [**`06-legacy-pipeline`**](06-legacy-pipeline/README.md) | GLSL emulations of OpenGL 1.x / 2.x fixed-function pipeline: unlit/shadeless, texture stage modulation, directional lights, linear & exponential depth fog. | $`f = e^{-(\text{density} \cdot d)}`$ |
| **07** | [**`07-pbr-pipeline`**](07-pbr-pipeline/README.md) | Modern Physically Based Rendering (PBR) metallic-roughness workflow, Cook-Torrance microfacet BRDF, GGX distribution, Schlick geometry & Fresnel, MER texture unpacking. | $`f_r = \frac{D \cdot F \cdot G}{4(\mathbf{N}\cdot\mathbf{L})(\mathbf{N}\cdot\mathbf{V})}`$ |
| **08** | [**`08-sky-rendering`**](08-sky-rendering/README.md) | Cubic static skyboxes, hemispherical panoramic skydomes, and dynamic atmospheric skies with animated scrolling clouds and solar day/night tracking. | $`\text{mix}(\mathbf{C}_{\text{horizon}}, \mathbf{C}_{\text{zenith}}, h)`$ |
| **09** | [**`09-legacy-terrain-water`**](09-legacy-terrain-water/README.md) | Multi-texture terrain splatting, lake basin placement, DuDv flow distortion, normal mapped ripple glints, Fresnel mixing, dual RTT reflection/refraction, soft depth shoreline edges. | $`F(\theta), \quad \Delta z = z_{\text{terr}} - z_{\text{water}}`$ |
| **10** | [**`10-pbr-terrain-water`**](10-pbr-terrain-water/README.md) | Physically based landscape splatting, Cook-Torrance water reflections, dielectric Fresnel ($F_0 = 0.02$), microfacet sun streaks, and underwater light absorption (Beer-Lambert law). | $`\mathbf{T}(d) = e^{-\boldsymbol{\sigma}_a \cdot d}`$ |

---

## 🚀 Quick start

### Prerequisites

- Python 3.8+ installed on your system.
- An OpenGL 3.2+ Core Profile capable GPU.

### 1. Installation

Clone this repository and create a virtual environment:

```bash
git clone https://github.com/ShivamKR12/Learning-Shaders.git
cd Learning-Shaders
```

Create and activate a virtual environment:

```bash
# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS:
python3 -m venv venv
source venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

---

### 2. Running the Demos

You can run any demo directly from the root directory or by navigating into its subfolder:

```bash
# Example 1: Run the minimal working shader
cd 01-minimal-shaders
python Minimal-Working-Shader.py

# Example 2: Run Phong specular reflections
cd ../04-phong-lighting
python Phong-Diffuse+Ambient+Specular-Lighting.py

# Example 3: Run the Cook-Torrance PBR BRDF
cd ../07-pbr-pipeline
python Pbr-CookTorranceBrdf-Lighting.py

# Example 4: Run the advanced real-time water simulation
cd ../09-legacy-terrain-water
python LegacyTerrain-ReflectionAndRefraction-Rendering.py
```

---

## 🕹️ Global Camera & Viewport Controls

All interactive 3D demos are equipped with a Blender-style free-fly camera controller ([`cam.py`](cam.py)):

| Input | Action |
|---|---|
| **W / S** | Fly Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up vertically |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch and yaw rotation) |
| **Esc** | Release Mouse Pointer / Unlock cursor |

---

## 🛠️ Repository Layout

```
Learning-Shaders/
├── 01-minimal-shaders/          # Basic GLSL pipeline, uniforms, textures, discard
├── 02-vertex-deformations/      # GPU vertex animations, waves, twists, pulses
├── 03-lambert-lighting/         # Matte diffuse Lambertian cosine reflectance
├── 04-phong-lighting/           # Glossy specular highlights via reflection vectors
├── 05-blinn-phong-lighting/     # Halfway vector formulation & 3D point lights
├── 06-legacy-pipeline/          # Fixed-function pipeline emulation & hardware fog
├── 07-pbr-pipeline/             # Physically Based Rendering & Cook-Torrance BRDF
├── 08-sky-rendering/            # Static skyboxes, skydomes, and dynamic skies
├── 09-legacy-terrain-water/     # Terrain splatting, DuDv water, RTT reflections
├── 10-pbr-terrain-water/        # PBR terrain splatting, microfacet water, Beer's law
├── models/                      # Shared 3D models (glTF/egg), terrain, textures, maps
├── cam.py                       # Blender-style free-fly camera module
├── Config.prc                   # Panda3D runtime configuration
├── requirements.txt             # Python dependencies (panda3d)
├── RoadMap.md                   # Complete pedagogical roadmap & learning syllabus
├── GLSL-Grammer-Rules.md        # Desktop GLSL syntax and grammar specification
├── GLSL_ES-Grammer-Rules.md     # Embedded Systems GLSL ES syntax rules
└── README.md                    # Root documentation and laboratory index
```

---

## 📚 Supplementary Documentation

- [`RoadMap.md`](RoadMap.md): Step-by-step 16-stage learning curriculum from beginner to advanced shader authoring.
- [`GLSL-Grammer-Rules.md`](GLSL-Grammer-Rules.md): Detailed reference guide on GLSL variables, types, swizzling, vector operations, and built-in functions.
- [`GLSL_ES-Grammer-Rules.md`](GLSL_ES-Grammer-Rules.md): Reference guide covering OpenGL ES qualifiers, precision statements, and mobile GPU constraints.

---

## 📜 Credits & Tech Stack

- **Game Engine**: [Panda3D](https://www.panda3d.org/)
- **Shading Language**: OpenGL Shading Language (GLSL 1.50 / GLSL ES 3.00)
- **Programming Language**: Python 3
