# Physically Based (PBR) Terrain & Advanced Water Rendering

An advanced, physically based landscape and hydrological rendering pipeline built with GLSL and Panda3D. This module unifies Physically Based Rendering (PBR) material workflows (Albedo, Roughness, Normal, Ambient Occlusion) with realistic multi-layer terrain splatting, dynamic water wave synthesis, microfacet Cook-Torrance water reflections, DuDv ripple displacement, dielectric Fresnel transmittance, and underwater light extinction (Beer-Lambert law absorption).

---

## Quick start

```bash
# Ensure dependencies are installed
pip install -r ../requirements.txt

# Run any of the PBR terrain and water demos
python PbrTerrain-SceneSetup-Rendering.py
python PbrTerrain-TextureSplatting-Rendering.py
python PbrTerrain-WaterPlane-Rendering.py
python PbrTerrain-WaterShader-Rendering.py
python PbrTerrain-Distortion-Rendering.py
python PbrTerrain-NormalMapping-Rendering.py
python PbrTerrain-Fresnel-Rendering.py
python PbrTerrain-ReflectionAndRefraction-Rendering.py
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

## Technical Overview & Physical Models

### 1. PBR Multi-Material Terrain Splatting (`PbrTerrain-TextureSplatting-Rendering.*`)
Blends multiple physical materials across terrain elevation and slopes:
- **Albedo / Base Color**: Linearized sRGB texture maps.
- **Roughness & Normal Maps**: Blended per-channel based on the splatmap weights:
  $$\mathbf{N}_{surface} = \text{normalize}\left(\sum_{i=1}^n w_i \cdot \mathbf{N}_i\right), \quad \alpha = \sum_{i=1}^n w_i \cdot \text{roughness}_i$$
- Applies the Cook-Torrance microfacet BRDF across the entire landscape.

### 2. Physical Dielectric Water Fresnel
Water is treated as an ideal optical dielectric with refractive index $\eta = 1.333$ (air $\eta = 1.0$), yielding a base reflectance at normal incidence ($0^\circ$) of:

$$F_0 = \left(\frac{\eta_1 - \eta_2}{\eta_1 + \eta_2}\right)^2 = \left(\frac{1.0 - 1.333}{1.0 + 1.333}\right)^2 \approx 0.02$$

Schlick's approximation models the rapid increase in mirror-like reflectivity toward grazing angles:

$$F(\theta) = 0.02 + 0.98 \cdot (1.0 - \cos\theta)^5$$

### 3. Microfacet Specular Sun Highlights
Specular glints from the sun and sky on the water surface are calculated using the Trowbridge-Reitz GGX distribution function:

$$D(\mathbf{H}) = \frac{\alpha^2}{\pi \left( (\mathbf{N} \cdot \mathbf{H})^2 (\alpha^2 - 1) + 1 \right)^2}$$
- Low water roughness ($\alpha \approx 0.01 - 0.05$) creates intense, razor-sharp sun streaks across undulating waves.

### 4. Underwater Light Absorption (Beer-Lambert Law)
As light penetrates through water of depth $d$, shorter wavelengths (blue/green) survive longer while red wavelengths are absorbed rapidly:

$$\mathbf{T}(d) = e^{-\boldsymbol{\sigma}_a \cdot d}$$
- $\boldsymbol{\sigma}_a$: Spectral absorption coefficients ($`\sigma_{\text{red}} > \sigma_{\text{green}} > \sigma_{\text{blue}}`$).
- Produces deep turquoise and sapphire color shifts in deep basins while maintaining crystal-clear clarity in shallow shore waters.

---

## Reference

### Script Catalog

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-scene-setup`**](01-scene-setup/README.md) | `PbrTerrain-SceneSetup-Rendering.py` | *(AutoShader)* | Scene Setup |
| [**`02-texture-splatting`**](02-texture-splatting/README.md) | `PbrTerrain-TextureSplatting-Rendering.py` | `PbrTerrain-TextureSplatting-Rendering.frag`, `PbrTerrain-TextureSplatting-Rendering.vert` | Texture Splatting |
| [**`03-water-plane`**](03-water-plane/README.md) | `PbrTerrain-WaterPlane-Rendering.py` | `PbrTerrain-WaterPlane-Rendering.frag`, `PbrTerrain-WaterPlane-Rendering.vert` | Water Plane |
| [**`04-water-shader`**](04-water-shader/README.md) | `PbrTerrain-WaterShader-Rendering.py` | `PbrTerrain-WaterShader-Rendering-Water.frag`, `PbrTerrain-WaterShader-Rendering-Water.vert`, `PbrTerrain-WaterShader-Rendering.frag`, `PbrTerrain-WaterShader-Rendering.vert` | Water Shader |
| [**`05-reflection-and-refraction`**](05-reflection-and-refraction/README.md) | `PbrTerrain-ReflectionAndRefraction-Rendering.py` | `PbrTerrain-ReflectionAndRefraction-Rendering-Water.frag`, `PbrTerrain-ReflectionAndRefraction-Rendering-Water.vert`, `PbrTerrain-ReflectionAndRefraction-Rendering.frag`, `PbrTerrain-ReflectionAndRefraction-Rendering.vert` | Reflection And Refraction |
| [**`06-distortion`**](06-distortion/README.md) | `PbrTerrain-Distortion-Rendering-Water.py` | `PbrTerrain-Distortion-Rendering-Water.frag`, `PbrTerrain-Distortion-Rendering-Water.vert`, `PbrTerrain-Distortion-Rendering.frag`, `PbrTerrain-Distortion-Rendering.vert` | Distortion |
| [**`07-normal-mapping`**](07-normal-mapping/README.md) | `PbrTerrain-NormalMapping-Rendering.py` | `PbrTerrain-NormalMapping-Rendering-Water.frag`, `PbrTerrain-NormalMapping-Rendering-Water.vert`, `PbrTerrain-NormalMapping-Rendering.frag`, `PbrTerrain-NormalMapping-Rendering.vert` | Normal Mapping |
| [**`08-fresnel`**](08-fresnel/README.md) | `PbrTerrain-Fresnel-Rendering-Water.py` | `PbrTerrain-Fresnel-Rendering-Water.frag`, `PbrTerrain-Fresnel-Rendering-Water.vert`, `PbrTerrain-Fresnel-Rendering.frag`, `PbrTerrain-Fresnel-Rendering.vert` | Fresnel |

### Layout

```
10-pbr-terrain-water/
├── 01-scene-setup/
│   ├── PbrTerrain-SceneSetup-Rendering.py
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-texture-splatting/
│   ├── PbrTerrain-TextureSplatting-Rendering.py
│   ├── PbrTerrain-TextureSplatting-Rendering.frag
│   ├── PbrTerrain-TextureSplatting-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 03-water-plane/
│   ├── PbrTerrain-WaterPlane-Rendering.py
│   ├── PbrTerrain-WaterPlane-Rendering.frag
│   ├── PbrTerrain-WaterPlane-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 04-water-shader/
│   ├── PbrTerrain-WaterShader-Rendering.py
│   ├── PbrTerrain-WaterShader-Rendering-Water.frag
│   ├── PbrTerrain-WaterShader-Rendering-Water.vert
│   ├── PbrTerrain-WaterShader-Rendering.frag
│   ├── PbrTerrain-WaterShader-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 05-reflection-and-refraction/
│   ├── PbrTerrain-ReflectionAndRefraction-Rendering.py
│   ├── PbrTerrain-ReflectionAndRefraction-Rendering-Water.frag
│   ├── PbrTerrain-ReflectionAndRefraction-Rendering-Water.vert
│   ├── PbrTerrain-ReflectionAndRefraction-Rendering.frag
│   ├── PbrTerrain-ReflectionAndRefraction-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 06-distortion/
│   ├── PbrTerrain-Distortion-Rendering-Water.py
│   ├── PbrTerrain-Distortion-Rendering.py
│   ├── PbrTerrain-Distortion-Rendering-Water.frag
│   ├── PbrTerrain-Distortion-Rendering-Water.vert
│   ├── PbrTerrain-Distortion-Rendering.frag
│   ├── PbrTerrain-Distortion-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 07-normal-mapping/
│   ├── PbrTerrain-NormalMapping-Rendering.py
│   ├── PbrTerrain-NormalMapping-Rendering-Water.frag
│   ├── PbrTerrain-NormalMapping-Rendering-Water.vert
│   ├── PbrTerrain-NormalMapping-Rendering.frag
│   ├── PbrTerrain-NormalMapping-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 08-fresnel/
│   ├── PbrTerrain-Fresnel-Rendering-Water.py
│   ├── PbrTerrain-Fresnel-Rendering.py
│   ├── PbrTerrain-Fresnel-Rendering-Water.frag
│   ├── PbrTerrain-Fresnel-Rendering-Water.vert
│   ├── PbrTerrain-Fresnel-Rendering.frag
│   ├── PbrTerrain-Fresnel-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- Water reflection and refraction cameras use clipping planes to prevent rendering unwanted geometry above or below the water plane; this requires hardware clip plane support (`ClipPlaneAttrib`).
- Depth buffer precision affects underwater light extinction; floating-point depth textures provide the cleanest gradient transitions.

