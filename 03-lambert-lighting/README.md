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

| Script | Vertex Shader | Fragment Shader | Target Model | Lighting Model |
|---|---|---|---|---|
| `Lambert-Diffuse-Lighting.py` | `Lambert-Diffuse-Lighting.vert` | `Lambert-Diffuse-Lighting.frag` | `models/teapot` | Pure Lambertian $\max(\mathbf{N}\cdot\mathbf{L}, 0)$ |
| `Lambert-Diffuse+Ambient-Lighting.py` | `Lambert-Diffuse+Ambient-Lighting.vert` | `Lambert-Diffuse+Ambient-Lighting.frag` | `models/teapot` | Diffuse + constant ambient fill term |
| `Lambert-Diffuse+Ambient+BaseColor-Lighting.py` | `Lambert-Diffuse+Ambient+BaseColor-Lighting.vert` | `Lambert-Diffuse+Ambient+BaseColor-Lighting.frag` | `models/teapot` | Diffuse + Ambient + uniform material color |
| `Lambert-Diffuse+Ambient+Texture-Lighting.py` | `Lambert-Diffuse+Ambient+Texture-Lighting.vert` | `Lambert-Diffuse+Ambient+Texture-Lighting.frag` | `models/panda-model` | Diffuse + Ambient + UV texture map |

### Layout

```
03-lambert-lighting/
├── Lambert-Diffuse-Lighting.py                      # Pure diffuse driver
├── Lambert-Diffuse-Lighting.vert                    # Normal transformation pass
├── Lambert-Diffuse-Lighting.frag                    # Raw N dot L dot-product lighting
├── Lambert-Diffuse+Ambient-Lighting.py              # Diffuse + Ambient driver
├── Lambert-Diffuse+Ambient-Lighting.vert            # View space normal calculation
├── Lambert-Diffuse+Ambient-Lighting.frag            # Evaluates N dot L + ambient factor
├── Lambert-Diffuse+Ambient+BaseColor-Lighting.py    # Diffuse + Ambient + Base Color driver
├── Lambert-Diffuse+Ambient+BaseColor-Lighting.vert  # Transforms normals
├── Lambert-Diffuse+Ambient+BaseColor-Lighting.frag  # Tints with uniform surface albedo
├── Lambert-Diffuse+Ambient+Texture-Lighting.py      # Textured diffuse driver
├── Lambert-Diffuse+Ambient+Texture-Lighting.vert    # Supplies UVs and normals
├── Lambert-Diffuse+Ambient+Texture-Lighting.frag    # Multiplies texel by lighting terms
├── cam.py                                          # Free-fly camera controller
├── Config.prc                                       # Runtime configuration
└── README.md                                        # Documentation
```

---

## Limitations & Technical Notes

- Lambertian reflectance models completely matte, non-shiny surfaces (like chalk, paper, or unglazed clay). It contains zero specular reflections or gloss highlights (for shiny surfaces, see `04-phong-lighting` and `05-blinn-phong-lighting`).
- Light direction must point toward the light source in the dot product calculation ($\mathbf{L} = \text{normalize}(\mathbf{P}_{light} - \mathbf{P}_{frag})$ for point lights or $-\mathbf{D}_{light}$ for directional lights).
