# Blinn-Phong Lighting & Point Light Attenuation

An implementation of Jim Blinn's modification to the classical Phong illumination model, featuring localized point light sources, physical distance attenuation, and the halfway vector ($\mathbf{H}$) specular calculation.

Blinn-Phong is the industry standard for non-PBR real-time rendering, offering superior numerical stability, more plausible highlight shapes at grazing angles, and reduced computational overhead compared to pure Phong reflection.

---

## Quick start

```bash
# Ensure dependencies are installed
pip install -r ../requirements.txt

# Run the interactive point-light Blinn-Phong demo
python BlinnPhong-PointLight-Lighting.py
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

### 1. The Halfway Vector Formulation
Instead of calculating the reflected light vector $\mathbf{R} = 2(\mathbf{N}\cdot\mathbf{L})\mathbf{N} - \mathbf{L}$, Blinn-Phong computes the **halfway vector** $\mathbf{H}$ midway between the light direction $\mathbf{L}$ and the view direction $\mathbf{V}$:

$$\mathbf{H} = \frac{\mathbf{L} + \mathbf{V}}{\|\mathbf{L} + \mathbf{V}\|}$$

The specular intensity is then computed by taking the dot product between the surface normal $\mathbf{N}$ and the halfway vector:

$$I_{spec} = \max(\mathbf{N} \cdot \mathbf{H}, 0.0)^\beta$$

- $\beta$ (Blinn shininess): To achieve an equivalent highlight radius to standard Phong shininess $\alpha$, $\beta \approx 4\alpha$.
- At grazing viewing angles where Phong reflections can produce harsh cutoff artifacts, Blinn-Phong naturally creates a softer, elliptical highlight consistent with microfacet theory.

### 2. Point Light Attenuation
Unlike infinite directional lights (such as sunlight), localized point lights exhibit intensity decay over distance $`d = \|\mathbf{P}_{\text{light}} - \mathbf{P}_{\text{frag}}\|`$:

$$\text{Attenuation} = \frac{1.0}{k_c + k_l \cdot d + k_q \cdot d^2}$$

- $k_c$: Constant attenuation factor (usually $1.0$).
- $k_l$: Linear attenuation factor.
- $k_q$: Quadratic attenuation factor (approximates the inverse-square law $\frac{1}{d^2}$).

---

## Reference

### Script Catalog

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-point-light`**](01-point-light/README.md) | `BlinnPhong-PointLight-Lighting.py` | `BlinnPhong-PointLight-Lighting.frag`, `BlinnPhong-PointLight-Lighting.vert` | Point Light |
| [**`02-directional-halfway`**](02-directional-halfway/README.md) | *(None)* | `BlinnPhong-Diffuse+Ambient+Specular-Lighting.frag` | Directional Halfway |

### Layout

```
05-blinn-phong-lighting/
├── 01-point-light/
│   ├── BlinnPhong-PointLight-Lighting.py
│   ├── BlinnPhong-PointLight-Lighting.frag
│   ├── BlinnPhong-PointLight-Lighting.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-directional-halfway/
│   ├── BlinnPhong-Diffuse+Ambient+Specular-Lighting.frag
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- The point light position in `BlinnPhong-PointLight-Lighting.py` is supplied via uniform `light_position` and can be interactively orbited or translated in Python.
- If $\|\mathbf{L} + \mathbf{V}\| \to 0$ (which only occurs if the light and viewer are in diametrically opposed directions with a back-facing surface), $\mathbf{H}$ evaluates to undefined; the shader uses `max(..., 0.0)` to safeguard against numerical instability.

