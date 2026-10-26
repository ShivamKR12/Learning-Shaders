# Legacy Terrain & Water Shading Pipeline

A production-grade terrain and real-time water rendering pipeline implemented with GLSL and Panda3D. This module covers multi-texture terrain splatting, dynamic water surface geometry, DuDv ripple distortion, tangent-space normal mapping, Fresnel reflection/refraction blending, offscreen render-to-texture (RTT) buffers, and depth-tested soft shoreline edges.

The implementation utilizes dual clip planes, offscreen render buffers (`GraphicsOutput`), and secondary reflection/refraction virtual cameras synchronized with the main viewer.

---

## Quick start

```bash
# Ensure dependencies are installed
pip install -r ../requirements.txt

# Run any of the terrain or water demos
python LegacyTerrain-SceneSetup-Rendering.py
python LegacyTerrain-TextureSplatting-Rendering.py
python LegacyTerrain-WaterPlane-Rendering.py
python LegacyTerrain-WaterShader-Rendering.py
python LegacyTerrain-Distortion-Rendering.py
python LegacyTerrain-NormalMapping-Rendering.py
python LegacyTerrain-Fresnel-Rendering.py
python LegacyTerrain-ReflectionAndRefraction-Rendering.py
python LegacyTerrain-SoftEdges-Rendering.py
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

### 1. Multi-Texture Terrain Splatting (`LegacyTerrain-TextureSplatting-Rendering.*`)
Blends multiple terrain textures (grass, dirt, rock, sand) using a multi-channel RGBA splatmap / weightmap:
$$\mathbf{C}_{terrain} = \mathbf{C}_{grass} \cdot w_R + \mathbf{C}_{dirt} \cdot w_G + \mathbf{C}_{rock} \cdot w_B + \mathbf{C}_{sand} \cdot (1 - (w_R + w_G + w_B))$$
Eliminates tiling repetition and produces rich, varied landscape topography across `models/Terrain.egg`.

### 2. Offscreen Reflection & Refraction Buffers (RTT)
- **Reflection Camera**: Mirrored across the water plane $z = z_{water}$ with an inverted pitch and a user clip plane clipping geometry below the water surface.
- **Refraction Camera**: Positioned at the main camera with a clip plane clipping geometry above the water surface.
- Both cameras render into offscreen textures passed to the water fragment shader.

### 3. DuDv & Normal Map Ripple Distortion (`LegacyTerrain-Distortion-Rendering.*`, `LegacyTerrain-NormalMapping-Rendering.*`)
- Samples animated DuDv offset maps scrolled over time:
  $$\mathbf{D} = (\text{texture}(u\_dudv, \mathbf{uv} + \vec{v}_{flow} \cdot t).rg \times 2.0 - 1.0) \times \text{distortion\_factor}$$
- Distorts projected screen-space coordinates $`(\mathbf{uv}'_{\text{refl}}, \mathbf{uv}'_{\text{refr}})`$ to produce dynamic, shimmering wave ripples.
- Samples normal maps $\mathbf{N}_{water}$ to compute sharp specular sun glints using Blinn-Phong highlights.

### 4. Fresnel Reflection vs. Refraction Factor (`LegacyTerrain-Fresnel-Rendering.*`)
Approximates the physical Fresnel equation for water ($n_1 = 1.0, n_2 = 1.33$):
$$F = \text{clamp}(F_0 + (1.0 - F_0)(1.0 - (\mathbf{N} \cdot \mathbf{V}))^5, 0.0, 1.0)$$
- Glancing angles ($\mathbf{N} \cdot \mathbf{V} \approx 0$) reflect the sky and terrain.
- Direct downward angles ($\mathbf{N} \cdot \mathbf{V} \approx 1$) look directly through into the lake/seabed.
$$\mathbf{C}_{water} = \text{mix}(\mathbf{C}_{refraction}, \mathbf{C}_{reflection}, F) + \mathbf{I}_{sun\_specular}$$

### 5. Soft Shoreline Edge Blending (`LegacyTerrain-SoftEdges-Rendering.*`)
- Compares water plane depth $z_{water}$ with the underwater terrain depth $z_{terrain}$ from the scene depth buffer:
  $$\Delta z = z_{terrain} - z_{water}$$
$$\alpha_{edge} = \text{clamp}\left(\frac{\Delta z}{\text{shore\_fade\_distance}}, 0.0, 1.0\right)$$
- Gradually fades water opacity to zero at the shoreline, eliminating harsh geometric intersections.

---

## Reference

### Script Catalog

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-scene-setup`**](01-scene-setup/README.md) | `LegacyTerrain-SceneSetup-Rendering.py` | *(AutoShader)* | Scene Setup |
| [**`02-texture-splatting`**](02-texture-splatting/README.md) | `LegacyTerrain-TextureSplatting-Rendering.py` | `LegacyTerrain-TextureSplatting-Rendering.frag`, `LegacyTerrain-TextureSplatting-Rendering.vert` | Texture Splatting |
| [**`03-water-plane`**](03-water-plane/README.md) | `LegacyTerrain-WaterPlane-Rendering-Water.py` | `LegacyTerrain-WaterPlane-Rendering.frag`, `LegacyTerrain-WaterPlane-Rendering.vert` | Water Plane |
| [**`04-water-shader`**](04-water-shader/README.md) | `LegacyTerrain-WaterShader-Rendering-Water.py` | `LegacyTerrain-WaterShader-Rendering-Water.frag`, `LegacyTerrain-WaterShader-Rendering-Water.vert`, `LegacyTerrain-WaterShader-Rendering.frag`, `LegacyTerrain-WaterShader-Rendering.vert` | Water Shader |
| [**`05-reflection-and-refraction`**](05-reflection-and-refraction/README.md) | `LegacyTerrain-ReflectionAndRefraction-Rendering.py` | `LegacyTerrain-ReflectionAndRefraction-Rendering-Water.frag`, `LegacyTerrain-ReflectionAndRefraction-Rendering-Water.vert`, `LegacyTerrain-ReflectionAndRefraction-Rendering.frag`, `LegacyTerrain-ReflectionAndRefraction-Rendering.vert` | Reflection And Refraction |
| [**`06-distortion`**](06-distortion/README.md) | `LegacyTerrain-Distortion-Rendering.py` | `LegacyTerrain-Distortion-Rendering-Water.frag`, `LegacyTerrain-Distortion-Rendering-Water.vert`, `LegacyTerrain-Distortion-Rendering.frag`, `LegacyTerrain-Distortion-Rendering.vert` | Distortion |
| [**`07-normal-mapping`**](07-normal-mapping/README.md) | `LegacyTerrain-NormalMapping-Rendering.py` | `LegacyTerrain-NormalMapping-Rendering-Water.frag`, `LegacyTerrain-NormalMapping-Rendering-Water.vert`, `LegacyTerrain-NormalMapping-Rendering.frag`, `LegacyTerrain-NormalMapping-Rendering.vert` | Normal Mapping |
| [**`08-fresnel`**](08-fresnel/README.md) | `LegacyTerrain-Fresnel-Rendering.py` | `LegacyTerrain-Fresnel-Rendering-Water.frag`, `LegacyTerrain-Fresnel-Rendering-Water.vert`, `LegacyTerrain-Fresnel-Rendering.frag`, `LegacyTerrain-Fresnel-Rendering.vert` | Fresnel |
| [**`09-soft-edges`**](09-soft-edges/README.md) | `LegacyTerrain-SoftEdges-Rendering.py` | `LegacyTerrain-SoftEdges-Rendering-Water.frag`, `LegacyTerrain-SoftEdges-Rendering-Water.vert`, `LegacyTerrain-SoftEdges-Rendering.frag`, `LegacyTerrain-SoftEdges-Rendering.vert` | Soft Edges |

### Layout

```
09-legacy-terrain-water/
├── 01-scene-setup/
│   ├── LegacyTerrain-SceneSetup-Rendering.py
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-texture-splatting/
│   ├── LegacyTerrain-TextureSplatting-Rendering.py
│   ├── LegacyTerrain-TextureSplatting-Rendering.frag
│   ├── LegacyTerrain-TextureSplatting-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 03-water-plane/
│   ├── LegacyTerrain-WaterPlane-Rendering-Water.py
│   ├── LegacyTerrain-WaterPlane-Rendering.py
│   ├── LegacyTerrain-WaterPlane-Rendering.frag
│   ├── LegacyTerrain-WaterPlane-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 04-water-shader/
│   ├── LegacyTerrain-WaterShader-Rendering-Water.py
│   ├── LegacyTerrain-WaterShader-Rendering.py
│   ├── LegacyTerrain-WaterShader-Rendering-Water.frag
│   ├── LegacyTerrain-WaterShader-Rendering-Water.vert
│   ├── LegacyTerrain-WaterShader-Rendering.frag
│   ├── LegacyTerrain-WaterShader-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 05-reflection-and-refraction/
│   ├── LegacyTerrain-ReflectionAndRefraction-Rendering.py
│   ├── LegacyTerrain-ReflectionAndRefraction-Rendering-Water.frag
│   ├── LegacyTerrain-ReflectionAndRefraction-Rendering-Water.vert
│   ├── LegacyTerrain-ReflectionAndRefraction-Rendering.frag
│   ├── LegacyTerrain-ReflectionAndRefraction-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 06-distortion/
│   ├── LegacyTerrain-Distortion-Rendering.py
│   ├── LegacyTerrain-Distortion-Rendering-Water.frag
│   ├── LegacyTerrain-Distortion-Rendering-Water.vert
│   ├── LegacyTerrain-Distortion-Rendering.frag
│   ├── LegacyTerrain-Distortion-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 07-normal-mapping/
│   ├── LegacyTerrain-NormalMapping-Rendering.py
│   ├── LegacyTerrain-NormalMapping-Rendering-Water.frag
│   ├── LegacyTerrain-NormalMapping-Rendering-Water.vert
│   ├── LegacyTerrain-NormalMapping-Rendering.frag
│   ├── LegacyTerrain-NormalMapping-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 08-fresnel/
│   ├── LegacyTerrain-Fresnel-Rendering.py
│   ├── LegacyTerrain-Fresnel-Rendering-Water.frag
│   ├── LegacyTerrain-Fresnel-Rendering-Water.vert
│   ├── LegacyTerrain-Fresnel-Rendering.frag
│   ├── LegacyTerrain-Fresnel-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 09-soft-edges/
│   ├── LegacyTerrain-SoftEdges-Rendering.py
│   ├── LegacyTerrain-SoftEdges-Rendering-Water.frag
│   ├── LegacyTerrain-SoftEdges-Rendering-Water.vert
│   ├── LegacyTerrain-SoftEdges-Rendering.frag
│   ├── LegacyTerrain-SoftEdges-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- The offscreen reflection and refraction buffers require Framebuffer Object (FBO) support in Panda3D.
- Screen-space coordinates must be perspective-divided by $w$ in the fragment shader ($`\mathbf{uv} = \frac{\mathbf{v}_{\text{clip}}.xy}{\mathbf{v}_{\text{clip}}.w} \cdot 0.5 + 0.5`$) before indexing the RTT textures.

