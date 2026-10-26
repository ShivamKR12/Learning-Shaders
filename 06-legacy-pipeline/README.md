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

| Script | Vertex Shader | Fragment Shader | Target Model | Emulated Legacy Feature |
|---|---|---|---|---|
| `Legacy-SceneSetup-Rendering.py` | *(Built-in AutoShader)* | *(Built-in AutoShader)* | `models/Sphere` | Baseline scene structure with lighting |
| `Legacy-ShadelessRendering-Rendering.py` | `Legacy-ShadelessRendering-Rendering.vert` | `Legacy-ShadelessRendering-Rendering.frag` | `models/Sphere` | Unlit / flat shading (`GL_LIGHTING` disabled) |
| `Legacy-Texture-Rendering.py` | `Legacy-Texture-Rendering.vert` | `Legacy-Texture-Rendering.frag` | `models/Sphere` | Fixed-function texture stage modulation |
| `Legacy-AmbientLighting-Lighting.py` | `Legacy-AmbientLighting-Lighting.vert` | `Legacy-AmbientLighting-Lighting.frag` | `models/Sphere` | Scene ambient light reflection |
| `Legacy-DiffuseLighting-Lighting.py` | `Legacy-DiffuseLighting-Lighting.vert` | `Legacy-DiffuseLighting-Lighting.frag` | `models/Sphere` | Single directional light source diffuse |
| `Legacy-SpecularLighting-Lighting.py` | `Legacy-SpecularLighting-Lighting.vert` | `Legacy-SpecularLighting-Lighting.frag` | `models/Sphere` | View-dependent specular reflection |
| `Legacy-Fog-Rendering.py` | `Legacy-Fog-Rendering.vert` | `Legacy-Fog-Rendering.frag` | `models/Sphere` | Distance-based depth fog interpolation |

### Layout

```
06-legacy-pipeline/
├── Legacy-SceneSetup-Rendering.py              # Baseline scene setup driver
├── Legacy-ShadelessRendering-Rendering.py      # Flat unlit shader driver
├── Legacy-ShadelessRendering-Rendering.vert    # Basic MVP transformation
├── Legacy-ShadelessRendering-Rendering.frag    # Emits constant color
├── Legacy-Texture-Rendering.py                 # Texture modulation driver
├── Legacy-Texture-Rendering.vert               # Passes UV coordinates
├── Legacy-Texture-Rendering.frag               # Samples 2D texture
├── Legacy-AmbientLighting-Lighting.py          # Ambient lighting driver
├── Legacy-AmbientLighting-Lighting.vert        # Passes vertex attributes
├── Legacy-AmbientLighting-Lighting.frag        # Applies uniform ambient term
├── Legacy-DiffuseLighting-Lighting.py          # Fixed-function diffuse driver
├── Legacy-DiffuseLighting-Lighting.vert        # Transforms normals to view space
├── Legacy-DiffuseLighting-Lighting.frag        # Computes N dot L
├── Legacy-SpecularLighting-Lighting.py         # Specular highlight driver
├── Legacy-SpecularLighting-Lighting.vert       # View and reflection vector setup
├── Legacy-SpecularLighting-Lighting.frag       # Evaluates specular exponent
├── Legacy-Fog-Rendering.py                     # Distance fog driver
├── Legacy-Fog-Rendering.vert                   # Passes camera-distance metric
├── Legacy-Fog-Rendering.frag                   # Blends surface color into fog color
├── cam.py                                      # Free-fly camera controller
├── Config.prc                                  # Runtime configuration
└── README.md                                   # Documentation
```

---

## Limitations & Technical Notes

- Unlike genuine fixed-function OpenGL drivers which evaluated lighting at every vertex (Gouraud shading), these GLSL implementations evaluate lighting per-fragment (Phong shading) to avoid polygon faceting and interpolation artifacts on low-poly spheres.
- All fog calculations use true eye-space Euclidean distance $\|\mathbf{P}_{eye}\|$ rather than planar $Z$ depth, preventing distortion when rotating the camera.

