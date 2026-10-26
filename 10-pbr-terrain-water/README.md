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

| Script | Terrain Shaders | Water Shaders | Key Feature |
|---|---|---|---|
| `PbrTerrain-SceneSetup-Rendering.py` | *(Built-in)* | None | Baseline PBR landscape environment |
| `PbrTerrain-TextureSplatting-Rendering.py` | `*.vert`, `*.frag` | None | Multi-material PBR terrain splatting |
| `PbrTerrain-WaterPlane-Rendering.py` | `*.vert`, `*.frag` | Procedural Mesh | PBR-lit water plane surface |
| `PbrTerrain-WaterShader-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Dynamic wave motion and surface shaders |
| `PbrTerrain-Distortion-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Flowing DuDv ripple distortion |
| `PbrTerrain-NormalMapping-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Tangent-space normal mapped wave glints |
| `PbrTerrain-Fresnel-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Physical dielectric water Fresnel ($F_0 = 0.02$) |
| `PbrTerrain-ReflectionAndRefraction-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Full RTT reflections with physical absorption |

### Layout

```
10-pbr-terrain-water/
├── PbrTerrain-SceneSetup-Rendering.py                     # Baseline PBR terrain driver
├── PbrTerrain-TextureSplatting-Rendering.py               # PBR terrain splatting driver
├── PbrTerrain-TextureSplatting-Rendering.vert             # Terrain vertex pass
├── PbrTerrain-TextureSplatting-Rendering.frag             # Multi-layer PBR material blend
├── PbrTerrain-WaterPlane-Rendering.py                     # Water surface driver
├── PbrTerrain-WaterPlane-Rendering.vert                   # Water plane transform
├── PbrTerrain-WaterPlane-Rendering.frag                   # PBR water output
├── PbrTerrain-WaterShader-Rendering.py                    # Combined terrain + water driver
├── PbrTerrain-WaterShader-Rendering.vert                  # Terrain vertex pass
├── PbrTerrain-WaterShader-Rendering.frag                  # Terrain fragment pass
├── PbrTerrain-WaterShader-Rendering-Water.vert            # Wave animation vertex pass
├── PbrTerrain-WaterShader-Rendering-Water.frag            # Microfacet water shading
├── PbrTerrain-Distortion-Rendering.py                     # DuDv ripple driver
├── PbrTerrain-Distortion-Rendering.vert                   # Terrain transform
├── PbrTerrain-Distortion-Rendering.frag                   # Terrain shading
├── PbrTerrain-Distortion-Rendering-Water.py               # Standalone distortion test
├── PbrTerrain-Distortion-Rendering-Water.vert             # Screen coordinate projection
├── PbrTerrain-Distortion-Rendering-Water.frag             # Flowing DuDv distortion
├── PbrTerrain-NormalMapping-Rendering.py                  # Normal mapping driver
├── PbrTerrain-NormalMapping-Rendering.vert                # Terrain transform
├── PbrTerrain-NormalMapping-Rendering.frag                # Terrain shading
├── PbrTerrain-NormalMapping-Rendering-Water.py            # Standalone normal test
├── PbrTerrain-NormalMapping-Rendering-Water.vert          # Tangent frame setup
├── PbrTerrain-NormalMapping-Rendering-Water.frag          # Dual normal map ripple glints
├── PbrTerrain-Fresnel-Rendering.py                        # Fresnel driver
├── PbrTerrain-Fresnel-Rendering.vert                      # Terrain transform
├── PbrTerrain-Fresnel-Rendering.frag                      # Terrain shading
├── PbrTerrain-Fresnel-Rendering-Water.py                  # Standalone Fresnel test
├── PbrTerrain-Fresnel-Rendering-Water.vert                # View vector output
├── PbrTerrain-Fresnel-Rendering-Water.frag                # Dielectric water Fresnel evaluation
├── PbrTerrain-ReflectionAndRefraction-Rendering.py        # Dual RTT driver
├── PbrTerrain-ReflectionAndRefraction-Rendering.vert      # Terrain transform
├── PbrTerrain-ReflectionAndRefraction-Rendering.frag      # Terrain shading
├── PbrTerrain-ReflectionAndRefraction-Rendering-Water.vert# Screen-space RTT projection
├── PbrTerrain-ReflectionAndRefraction-Rendering-Water.frag# Mixes RTT textures with physical glints
├── cam.py                                                 # Free-fly camera controller
├── Config.prc                                             # Runtime configuration
└── README.md                                              # Documentation
```

---

## Limitations & Technical Notes

- Water reflection and refraction cameras use clipping planes to prevent rendering unwanted geometry above or below the water plane; this requires hardware clip plane support (`ClipPlaneAttrib`).
- Depth buffer precision affects underwater light extinction; floating-point depth textures provide the cleanest gradient transitions.

