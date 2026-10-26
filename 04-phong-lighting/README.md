# Phong Reflection & Specular Lighting

Implementations of Bui Tuong Phong's empirical illumination model in GLSL and Panda3D. This module introduces view-dependent specular highlights, enabling realistic rendering of glossy and reflective materials such as plastics, varnished surfaces, and polished metals.

The shaders systematically demonstrate the complete classical illumination equation: Ambient + Diffuse + Specular, combined with base colors and 2D textures.

---

## Quick start

```bash
# Ensure dependencies are installed
pip install -r ../requirements.txt

# Run any of the Phong lighting demos
python Phong-Diffuse+Specular-Lighting.py
python Phong-Diffuse+Ambient+Specular-Lighting.py
python Phong-Diffuse+Ambient+Specular+BaseColor-Lighting.py
python Phong-Diffuse+Ambient+Specular+Texture-Lighting.py
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

Phong's model calculates surface color as the linear sum of three independent lighting components:

$$\mathbf{I}_{total} = \mathbf{I}_{ambient} + \mathbf{I}_{diffuse} + \mathbf{I}_{specular}$$

### 1. Specular Reflection Formulation
Unlike diffuse lighting, specular reflections depend critically on the observer's viewing angle. The light ray $\mathbf{L}$ is reflected across the surface normal $\mathbf{N}$ to yield the ideal reflection vector $\mathbf{R}$:

$$\mathbf{R} = \text{reflect}(-\mathbf{L}, \mathbf{N}) = 2(\mathbf{N} \cdot \mathbf{L})\mathbf{N} - \mathbf{L}$$

The highlight intensity is determined by the cosine of the angle between $\mathbf{R}$ and the view vector $\mathbf{V}$ (pointing from the fragment toward the camera), raised to an empirical shininess exponent $\alpha$:

$$I_{spec} = \max(\mathbf{R} \cdot \mathbf{V}, 0.0)^\alpha$$

- $\alpha$ (shininess): Higher values (e.g. $32$ to $128$) produce sharp, pinpoint highlights (glossy glass/metal); lower values (e.g. $4$ to $16$) yield broad, soft highlights (rubber/plastic).

### 2. Full Phong Model (`Phong-Diffuse+Ambient+Specular-Lighting.*`)
$$\mathbf{I}_{final} = k_a + k_d \cdot \max(\mathbf{N} \cdot \mathbf{L}, 0.0) + k_s \cdot \max(\mathbf{R} \cdot \mathbf{V}, 0.0)^\alpha$$

### 3. Material Base Color & Texture Integration
$$\mathbf{C}_{final} = \mathbf{C}_{albedo} \cdot (\mathbf{I}_{ambient} + \mathbf{I}_{diffuse}) + \mathbf{I}_{specular} \cdot \mathbf{C}_{specular}$$
*(Note: In physical dielectrics, specular reflections are predominantly the color of the light source, while diffuse reflections reflect the surface pigment).*

---

## Reference

### Script Catalog

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-diffuse-specular`**](01-diffuse-specular/README.md) | `Phong-Diffuse+Specular-Lighting.py` | `Phong-Diffuse+Specular-Lighting.frag`, `Phong-Diffuse+Specular-Lighting.vert` | Diffuse Specular |
| [**`02-diffuse-ambient-specular`**](02-diffuse-ambient-specular/README.md) | `Phong-Diffuse+Ambient+Specular-Lighting.py` | `Phong-Diffuse+Ambient+Specular-Lighting.frag`, `Phong-Diffuse+Ambient+Specular-Lighting.vert` | Diffuse Ambient Specular |
| [**`03-diffuse-ambient-specular-base-color`**](03-diffuse-ambient-specular-base-color/README.md) | `Phong-Diffuse+Ambient+Specular+BaseColor-Lighting.py` | `Phong-Diffuse+Ambient+Specular+BaseColor-Lighting.frag`, `Phong-Diffuse+Ambient+Specular+BaseColor-Lighting.vert` | Diffuse Ambient Specular Base Color |
| [**`04-diffuse-ambient-specular-texture`**](04-diffuse-ambient-specular-texture/README.md) | `Phong-Diffuse+Ambient+Specular+Texture-Lighting.py` | `Phong-Diffuse+Ambient+Specular+Texture-Lighting.frag`, `Phong-Diffuse+Ambient+Specular+Texture-Lighting.vert` | Diffuse Ambient Specular Texture |

### Layout

```
04-phong-lighting/
├── 01-diffuse-specular/
│   ├── Phong-Diffuse+Specular-Lighting.py
│   ├── Phong-Diffuse+Specular-Lighting.frag
│   ├── Phong-Diffuse+Specular-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-diffuse-ambient-specular/
│   ├── Phong-Diffuse+Ambient+Specular-Lighting.py
│   ├── Phong-Diffuse+Ambient+Specular-Lighting.frag
│   ├── Phong-Diffuse+Ambient+Specular-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 03-diffuse-ambient-specular-base-color/
│   ├── Phong-Diffuse+Ambient+Specular+BaseColor-Lighting.py
│   ├── Phong-Diffuse+Ambient+Specular+BaseColor-Lighting.frag
│   ├── Phong-Diffuse+Ambient+Specular+BaseColor-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 04-diffuse-ambient-specular-texture/
│   ├── Phong-Diffuse+Ambient+Specular+Texture-Lighting.py
│   ├── Phong-Diffuse+Ambient+Specular+Texture-Lighting.frag
│   ├── Phong-Diffuse+Ambient+Specular+Texture-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- The Phong model calculates the reflection vector $\mathbf{R} = \text{reflect}(-\mathbf{L}, \mathbf{N})$. When the angle between $\mathbf{R}$ and $\mathbf{V}$ exceeds $90^\circ$, the highlight terminates abruptly. The Blinn-Phong model (`05-blinn-phong-lighting`) overcomes this limitation by evaluating the halfway vector $\mathbf{H}$.
- All vectors ($\mathbf{N}$, $\mathbf{L}$, $\mathbf{V}$, $\mathbf{R}$) must be re-normalized inside the fragment shader, as linear vertex interpolation reduces vector lengths.

