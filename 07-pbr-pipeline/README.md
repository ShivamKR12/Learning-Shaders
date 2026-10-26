# Physically Based Rendering (PBR) & Cook-Torrance BRDF

A complete implementation of the modern Physically Based Rendering (PBR) metallic-roughness workflow and the Cook-Torrance microfacet Bidirectional Reflectance Distribution Function (BRDF) in GLSL for Panda3D.

This module replaces empirical lighting models (like Phong and Blinn-Phong) with rigorous physical principles: energy conservation, microfacet normal distributions (Trowbridge-Reitz GGX), geometric shadowing/masking (Smith Schlick-GGX), and Fresnel reflectivity (Schlick's approximation).

---

## Quick start

```bash
# Ensure dependencies are installed
pip install -r ../requirements.txt

# Run any of the PBR pipeline demos
python Pbr-SceneSetup-Rendering.py
python Pbr-ShadelessRendering-Rendering.py
python Pbr-Texture-Rendering.py
python Pbr-AmbientLighting-Lighting.py
python Pbr-CookTorranceBrdf-Lighting.py
python Pbr-MerMap-Rendering.py
python Pbr-Fog-Rendering.py
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

## Technical Overview & Mathematical Equations

The Cook-Torrance microfacet specular BRDF is formulated as:

$$f_r = k_d \cdot f_{lambert} + k_s \cdot f_{cook-torrance}$$

$$f_{cook-torrance} = \frac{D(\mathbf{H}) \cdot F(\mathbf{V}, \mathbf{H}) \cdot G(\mathbf{L}, \mathbf{V}, \mathbf{H})}{4(\mathbf{N} \cdot \mathbf{L})(\mathbf{N} \cdot \mathbf{V})}$$

### 1. Normal Distribution Function (NDF): Trowbridge-Reitz GGX
Models the statistical orientation of microscopic surface facets relative to the halfway vector $\mathbf{H}$:

$$D(\mathbf{H}) = \frac{\alpha^2}{\pi \left( (\mathbf{N} \cdot \mathbf{H})^2 (\alpha^2 - 1) + 1 \right)^2}$$
- $\alpha = \text{roughness}^2$ (perceptually linear roughness remapping).

### 2. Geometry Function: Smith's Schlick-GGX
Accounts for microscopic self-shadowing (microfacets occluding the light) and masking (microfacets occluding the viewer):

$$G(\mathbf{L}, \mathbf{V}) = G_1(\mathbf{N} \cdot \mathbf{V}) \cdot G_1(\mathbf{N} \cdot \mathbf{L})$$

$$G_1(x) = \frac{x}{x(1 - k) + k}, \quad k = \frac{(\text{roughness} + 1)^2}{8}$$

### 3. Fresnel Reflectance: Schlick's Approximation
Calculates the fraction of reflected versus refracted light as a function of viewing angle:

$$F(\mathbf{V}, \mathbf{H}) = F_0 + (1.0 - F_0)(1.0 - (\mathbf{V} \cdot \mathbf{H}))^5$$
- $F_0$: Base reflectance at normal incidence ($0^\circ$). For dielectrics (plastics, wood, stone), $F_0 \approx 0.04$; for conductors (metals), $F_0$ is tinted by the material albedo.

### 4. Energy Conservation
To ensure surfaces never emit more energy than they receive:
$$k_s = F, \quad k_d = (1.0 - k_s) \cdot (1.0 - \text{metallic})$$

### 5. Metallic-Roughness (MER) Texture Map Unpacking
Adheres to the glTF 2.0 standard:
- **Red channel**: Ambient Occlusion (AO)
- **Green channel**: Roughness ($\alpha$)
- **Blue channel**: Metallic mask ($0 = \text{dielectric}, 1 = \text{metal}$)

---

## Reference

### Script Catalog

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-scene-setup`**](01-scene-setup/README.md) | `Pbr-SceneSetup-Rendering.py` | *(AutoShader)* | Scene Setup |
| [**`02-shadeless-rendering`**](02-shadeless-rendering/README.md) | `Pbr-ShadelessRendering-Rendering.py` | `Pbr-ShadelessRendering-Rendering.frag`, `Pbr-ShadelessRendering-Rendering.vert` | Shadeless Rendering |
| [**`03-ambient-lighting`**](03-ambient-lighting/README.md) | `Pbr-AmbientLighting-Lighting.py` | `Pbr-AmbientLighting-Lighting.frag`, `Pbr-AmbientLighting-Lighting.vert` | Ambient Lighting |
| [**`04-cook-torrance-brdf`**](04-cook-torrance-brdf/README.md) | `Pbr-CookTorranceBrdf-Lighting.py` | `Pbr-CookTorranceBrdf-Lighting.frag`, `Pbr-CookTorranceBrdf-Lighting.vert` | Cook Torrance Brdf |
| [**`05-texture`**](05-texture/README.md) | `Pbr-Texture-Rendering.py` | `Pbr-Texture-Rendering.frag`, `Pbr-Texture-Rendering.vert` | Texture |
| [**`06-fog`**](06-fog/README.md) | `Pbr-Fog-Rendering.py` | `Pbr-Fog-Rendering.frag`, `Pbr-Fog-Rendering.vert` | Fog |
| [**`07-mer-map`**](07-mer-map/README.md) | `Pbr-MerMap-Rendering.py` | `Pbr-MerMap-Rendering.frag`, `Pbr-MerMap-Rendering.vert` | Mer Map |

### Layout

```
07-pbr-pipeline/
├── 01-scene-setup/
│   ├── Pbr-SceneSetup-Rendering.py
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-shadeless-rendering/
│   ├── Pbr-ShadelessRendering-Rendering.py
│   ├── Pbr-ShadelessRendering-Rendering.frag
│   ├── Pbr-ShadelessRendering-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 03-ambient-lighting/
│   ├── Pbr-AmbientLighting-Lighting.py
│   ├── Pbr-AmbientLighting-Lighting.frag
│   ├── Pbr-AmbientLighting-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 04-cook-torrance-brdf/
│   ├── Pbr-CookTorranceBrdf-Lighting.py
│   ├── Pbr-CookTorranceBrdf-Lighting.frag
│   ├── Pbr-CookTorranceBrdf-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 05-texture/
│   ├── Pbr-Texture-Rendering.py
│   ├── Pbr-Texture-Rendering.frag
│   ├── Pbr-Texture-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 06-fog/
│   ├── Pbr-Fog-Rendering.py
│   ├── Pbr-Fog-Rendering.frag
│   ├── Pbr-Fog-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 07-mer-map/
│   ├── Pbr-MerMap-Rendering.py
│   ├── Pbr-MerMap-Rendering.frag
│   ├── Pbr-MerMap-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- All texture lookups from standard sRGB albedo maps must be linearized via $\mathbf{C}_{lin} = \mathbf{C}_{sRGB}^{2.2}$ before lighting calculations, and gamma-corrected via $\mathbf{C}_{out} = \mathbf{C}_{lin}^{1.0 / 2.2}$ prior to display.
- Metallic and Roughness textures are already stored in linear color space and must **not** be gamma-converted.

