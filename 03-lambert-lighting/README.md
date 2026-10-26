# Lambertian Diffuse Lighting Shaders

Implementations of Johann Heinrich Lambert's cosine emission law (Lambertian reflectance) in GLSL for Panda3D. This module covers the foundation of all matte, non-glossy 3D shading, progressively building from raw diffuse dot-product calculations to ambient fill lighting, material base color modulation, and UV-mapped texture integration.

All lighting calculations occur in View (Eye) Space or World Space using interpolated surface normals and directional light vectors.

---

## Quick start

```bash
# Ensure dependencies are installed
pip install -r ../requirements.txt

# Run any of the Lambert lighting variations
python Lambert-Diffuse-Lighting.py
python Lambert-Diffuse+Ambient-Lighting.py
python Lambert-Diffuse+Ambient+BaseColor-Lighting.py
python Lambert-Diffuse+Ambient+Texture-Lighting.py
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

Lambertian reflectance states that the apparent brightness of an ideal matte surface is directly proportional to the cosine of the angle $\theta$ between the surface normal $\mathbf{N}$ and the incident light direction $\mathbf{L}$.

$$\cos\theta = \frac{\mathbf{N} \cdot \mathbf{L}}{\|\mathbf{N}\| \|\mathbf{L}\|}$$

When both $\mathbf{N}$ and $\mathbf{L}$ are normalized unit vectors, the cosine simplifies directly to the vector dot product:

### 1. Pure Diffuse (`Lambert-Diffuse-Lighting.*`)
$$I_{diff} = \max(\mathbf{N} \cdot \mathbf{L}, 0.0)$$
- Clamped at $0.0$ via $\max()$ to ensure back-facing polygons receiving no light do not evaluate to negative intensity.

### 2. Diffuse + Ambient Fill (`Lambert-Diffuse+Ambient-Lighting.*`)
Adds an ambient constant $k_a$ to prevent unlit regions from dropping into total pitch darkness:
$$I = \max(\mathbf{N} \cdot \mathbf{L}, 0.0) + k_a$$

### 3. Material Base Color Modulation (`Lambert-Diffuse+Ambient+BaseColor-Lighting.*`)
Modulates the total light intensity by a material surface albedo color $\mathbf{C}_{base}$:
$$\mathbf{C}_{final} = \mathbf{C}_{base} \cdot \left(\max(\mathbf{N} \cdot \mathbf{L}, 0.0) + k_a\right)$$

### 4. Diffuse Texture Mapping (`Lambert-Diffuse+Ambient+Texture-Lighting.*`)
Replaces the flat base color with sampled texels from a 2D texture map:
$$\mathbf{C}_{tex} = \text{texture}(u\_tex, \mathbf{uv})$$
$$\mathbf{C}_{final} = \mathbf{C}_{tex} \cdot \left(\max(\mathbf{N} \cdot \mathbf{L}, 0.0) + k_a\right)$$

---

## Reference

### Script Catalog

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-diffuse`**](01-diffuse/README.md) | `Lambert-Diffuse-Lighting.py` | `Lambert-Diffuse-Lighting.frag`, `Lambert-Diffuse-Lighting.vert` | Diffuse |
| [**`02-diffuse-ambient`**](02-diffuse-ambient/README.md) | `Lambert-Diffuse+Ambient-Lighting.py` | `Lambert-Diffuse+Ambient-Lighting.frag`, `Lambert-Diffuse+Ambient-Lighting.vert` | Diffuse Ambient |
| [**`03-diffuse-ambient-base-color`**](03-diffuse-ambient-base-color/README.md) | `Lambert-Diffuse+Ambient+BaseColor-Lighting.py` | `Lambert-Diffuse+Ambient+BaseColor-Lighting.frag`, `Lambert-Diffuse+Ambient+BaseColor-Lighting.vert` | Diffuse Ambient Base Color |
| [**`04-diffuse-ambient-texture`**](04-diffuse-ambient-texture/README.md) | `Lambert-Diffuse+Ambient+Texture-Lighting.py` | `Lambert-Diffuse+Ambient+Texture-Lighting.frag`, `Lambert-Diffuse+Ambient+Texture-Lighting.vert` | Diffuse Ambient Texture |

### Layout

```
03-lambert-lighting/
├── 01-diffuse/
│   ├── Lambert-Diffuse-Lighting.py
│   ├── Lambert-Diffuse-Lighting.frag
│   ├── Lambert-Diffuse-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-diffuse-ambient/
│   ├── Lambert-Diffuse+Ambient-Lighting.py
│   ├── Lambert-Diffuse+Ambient-Lighting.frag
│   ├── Lambert-Diffuse+Ambient-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 03-diffuse-ambient-base-color/
│   ├── Lambert-Diffuse+Ambient+BaseColor-Lighting.py
│   ├── Lambert-Diffuse+Ambient+BaseColor-Lighting.frag
│   ├── Lambert-Diffuse+Ambient+BaseColor-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 04-diffuse-ambient-texture/
│   ├── Lambert-Diffuse+Ambient+Texture-Lighting.py
│   ├── Lambert-Diffuse+Ambient+Texture-Lighting.frag
│   ├── Lambert-Diffuse+Ambient+Texture-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- Lambertian reflectance models completely matte, non-shiny surfaces (like chalk, paper, or unglazed clay). It contains zero specular reflections or gloss highlights (for shiny surfaces, see `04-phong-lighting` and `05-blinn-phong-lighting`).
- Light direction must point toward the light source in the dot product calculation ($`\mathbf{L} = \text{normalize}(\mathbf{P}_{\text{light}} - \mathbf{P}_{\text{frag}})`$ for point lights or $`-\mathbf{D}_{\text{light}}`$ for directional lights).

