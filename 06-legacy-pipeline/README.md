# Legacy Fixed-Function Pipeline Emulation

GLSL shader recreations of the classical OpenGL 1.x / 2.x fixed-function graphics pipeline. This module demonstrates how traditional graphics hardware computed rendering before programmable shaders existed—including flat unlit rendering, texture modulation, ambient fill, directional diffuse, specular highlights, and hardware distance fog.

Each stage is implemented as a standalone programmable GLSL program, giving full visibility into legacy rendering mechanics while maintaining compatibility with modern OpenGL core profiles.

---

## Quick start

```bash
# Ensure dependencies are installed
pip install -r ../requirements.txt

# Run any of the legacy pipeline stages
python Legacy-SceneSetup-Rendering.py
python Legacy-ShadelessRendering-Rendering.py
python Legacy-Texture-Rendering.py
python Legacy-AmbientLighting-Lighting.py
python Legacy-DiffuseLighting-Lighting.py
python Legacy-SpecularLighting-Lighting.py
python Legacy-Fog-Rendering.py
```

### Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look |
| **Esc** | Release Mouse Cursor / Exit |

---

## Technical Overview & Pipeline Stages

### 1. Shadeless / Unlit Rendering (`Legacy-ShadelessRendering-Rendering.*`)
- Emulates `glDisable(GL_LIGHTING)`.
- Ignores surface normals and light sources, rendering flat geometry directly from vertex colors or uniform material tint.

### 2. Texture Mapping (`Legacy-Texture-Rendering.*`)
- Emulates `glTexEnv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)`.
- Samples texels from a 2D texture unit and multiplies with the incoming fragment color:
  $$\mathbf{C}_{fragment} = \mathbf{C}_{vertex} \times \mathbf{C}_{texture}$$

### 3. Ambient & Diffuse Lighting (`Legacy-AmbientLighting-Lighting.*`, `Legacy-DiffuseLighting-Lighting.*`)
- Emulates standard OpenGL light models (`GL_LIGHT0`, `GL_AMBIENT`, `GL_DIFFUSE`):
  $$\mathbf{C} = \mathbf{A}_{scene} \cdot \mathbf{M}_{ambient} + (\mathbf{N} \cdot \mathbf{L}) \cdot \mathbf{D}_{light} \cdot \mathbf{M}_{diffuse}$$

### 4. Specular Highlights (`Legacy-SpecularLighting-Lighting.*`)
- Emulates `GL_SPECULAR` and `GL_SHININESS`:
  $$\mathbf{C}_{spec} = (\mathbf{R} \cdot \mathbf{V})^{s} \cdot \mathbf{S}_{light} \cdot \mathbf{M}_{specular}$$

### 5. Distance Fog (`Legacy-Fog-Rendering.*`)
- Emulates hardware fog modes (`glFogi(GL_FOG_MODE, ...)`):
  - **Linear Fog**:
    $$f = \frac{d_{end} - d}{d_{end} - d_{start}}$$
  - **Exponential Fog**:
    $$f = e^{-(\text{density} \cdot d)}$$
  - **Exponential Squared Fog**:
    $$f = e^{-(\text{density} \cdot d)^2}$$
- Final color blends between the lit surface and background fog color:
  $$\mathbf{C}_{final} = \text{mix}(\mathbf{C}_{fog}, \mathbf{C}_{surface}, \text{clamp}(f, 0.0, 1.0))$$

---

## Reference

### Script Catalog

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-scene-setup`**](01-scene-setup/README.md) | `Legacy-SceneSetup-Rendering.py` | *(AutoShader)* | Scene Setup |
| [**`02-shadeless-rendering`**](02-shadeless-rendering/README.md) | `Legacy-ShadelessRendering-Rendering.py` | `Legacy-ShadelessRendering-Rendering.frag`, `Legacy-ShadelessRendering-Rendering.vert` | Shadeless Rendering |
| [**`03-ambient-lighting`**](03-ambient-lighting/README.md) | `Legacy-AmbientLighting-Lighting.py` | `Legacy-AmbientLighting-Lighting.frag`, `Legacy-AmbientLighting-Lighting.vert` | Ambient Lighting |
| [**`04-diffuse-lighting`**](04-diffuse-lighting/README.md) | `Legacy-DiffuseLighting-Lighting.py` | `Legacy-DiffuseLighting-Lighting.frag`, `Legacy-DiffuseLighting-Lighting.vert` | Diffuse Lighting |
| [**`05-specular-lighting`**](05-specular-lighting/README.md) | `Legacy-SpecularLighting-Lighting.py` | `Legacy-SpecularLighting-Lighting.frag`, `Legacy-SpecularLighting-Lighting.vert` | Specular Lighting |
| [**`06-texture`**](06-texture/README.md) | `Legacy-Texture-Rendering.py` | `Legacy-Texture-Rendering.frag`, `Legacy-Texture-Rendering.vert` | Texture |
| [**`07-fog`**](07-fog/README.md) | `Legacy-Fog-Rendering.py` | `Legacy-Fog-Rendering.frag`, `Legacy-Fog-Rendering.vert` | Fog |

### Layout

```
06-legacy-pipeline/
├── 01-scene-setup/
│   ├── Legacy-SceneSetup-Rendering.py
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-shadeless-rendering/
│   ├── Legacy-ShadelessRendering-Rendering.py
│   ├── Legacy-ShadelessRendering-Rendering.frag
│   ├── Legacy-ShadelessRendering-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 03-ambient-lighting/
│   ├── Legacy-AmbientLighting-Lighting.py
│   ├── Legacy-AmbientLighting-Lighting.frag
│   ├── Legacy-AmbientLighting-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 04-diffuse-lighting/
│   ├── Legacy-DiffuseLighting-Lighting.py
│   ├── Legacy-DiffuseLighting-Lighting.frag
│   ├── Legacy-DiffuseLighting-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 05-specular-lighting/
│   ├── Legacy-SpecularLighting-Lighting.py
│   ├── Legacy-SpecularLighting-Lighting.frag
│   ├── Legacy-SpecularLighting-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 06-texture/
│   ├── Legacy-Texture-Rendering.py
│   ├── Legacy-Texture-Rendering.frag
│   ├── Legacy-Texture-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 07-fog/
│   ├── Legacy-Fog-Rendering.py
│   ├── Legacy-Fog-Rendering.frag
│   ├── Legacy-Fog-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- Unlike genuine fixed-function OpenGL drivers which evaluated lighting at every vertex (Gouraud shading), these GLSL implementations evaluate lighting per-fragment (Phong shading) to avoid polygon faceting and interpolation artifacts on low-poly spheres.
- All fog calculations use true eye-space Euclidean distance $\|\mathbf{P}_{eye}\|$ rather than planar $Z$ depth, preventing distortion when rotating the camera.

