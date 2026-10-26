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
- Distorts projected screen-space coordinates $(\mathbf{uv}_{refl}', \mathbf{uv}_{refr}')$ to produce dynamic, shimmering wave ripples.
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

| Script | Terrain Shaders | Water Shaders | Key Feature |
|---|---|---|---|
| `LegacyTerrain-SceneSetup-Rendering.py` | *(AutoShader)* | None | Loads `models/Terrain` with directional sunlight |
| `LegacyTerrain-TextureSplatting-Rendering.py` | `*.vert`, `*.frag` | None | Multi-channel splatmap blending across terrain |
| `LegacyTerrain-WaterPlane-Rendering.py` | `*.vert`, `*.frag` | Procedural Quad | Places flat water surface across the lake basin |
| `LegacyTerrain-WaterShader-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Shaded water surface with wave movement |
| `LegacyTerrain-Distortion-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | DuDv wave distortion on screen textures |
| `LegacyTerrain-NormalMapping-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Animated normal maps with sun glints |
| `LegacyTerrain-Fresnel-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Dynamic view-dependent Fresnel factor |
| `LegacyTerrain-ReflectionAndRefraction-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Dual RTT reflection and refraction passes |
| `LegacyTerrain-SoftEdges-Rendering.py` | `*.vert`, `*.frag` | `*-Water.vert`, `*-Water.frag` | Depth buffer comparison for soft shorelines |

### Layout

```
09-legacy-terrain-water/
├── LegacyTerrain-SceneSetup-Rendering.py                     # Baseline terrain setup driver
├── LegacyTerrain-TextureSplatting-Rendering.py               # Splatting driver
├── LegacyTerrain-TextureSplatting-Rendering.vert             # Splatting vertex pass
├── LegacyTerrain-TextureSplatting-Rendering.frag             # RGBA splatmap weight blend
├── LegacyTerrain-WaterPlane-Rendering.py                     # Water geometry driver
├── LegacyTerrain-WaterPlane-Rendering.vert                   # Water plane transform
├── LegacyTerrain-WaterPlane-Rendering.frag                   # Basic water surface output
├── LegacyTerrain-WaterPlane-Rendering-Water.py               # Water plane mesh generator
├── LegacyTerrain-WaterShader-Rendering.py                    # Combined terrain + water driver
├── LegacyTerrain-WaterShader-Rendering.vert                  # Terrain vertex pass
├── LegacyTerrain-WaterShader-Rendering.frag                  # Terrain fragment pass
├── LegacyTerrain-WaterShader-Rendering-Water.py              # Standalone water test
├── LegacyTerrain-WaterShader-Rendering-Water.vert            # Water wave vertex pass
├── LegacyTerrain-WaterShader-Rendering-Water.frag            # Water surface fragment pass
├── LegacyTerrain-Distortion-Rendering.py                     # DuDv distortion driver
├── LegacyTerrain-Distortion-Rendering.vert                   # Terrain transform
├── LegacyTerrain-Distortion-Rendering.frag                   # Terrain shading
├── LegacyTerrain-Distortion-Rendering-Water.vert             # Projected texture coordinates
├── LegacyTerrain-Distortion-Rendering-Water.frag             # DuDv ripple distortion
├── LegacyTerrain-NormalMapping-Rendering.py                  # Normal mapping driver
├── LegacyTerrain-NormalMapping-Rendering.vert                # Terrain transform
├── LegacyTerrain-NormalMapping-Rendering.frag                # Terrain shading
├── LegacyTerrain-NormalMapping-Rendering-Water.vert          # Water normal pass
├── LegacyTerrain-NormalMapping-Rendering-Water.frag          # Tangent-space normal ripples
├── LegacyTerrain-Fresnel-Rendering.py                        # Fresnel driver
├── LegacyTerrain-Fresnel-Rendering.vert                      # Terrain transform
├── LegacyTerrain-Fresnel-Rendering.frag                      # Terrain shading
├── LegacyTerrain-Fresnel-Rendering-Water.vert                # View vector output
├── LegacyTerrain-Fresnel-Rendering-Water.frag                # Evaluates Schlick Fresnel
├── LegacyTerrain-ReflectionAndRefraction-Rendering.py        # Dual RTT reflection/refraction driver
├── LegacyTerrain-ReflectionAndRefraction-Rendering.vert      # Terrain transform
├── LegacyTerrain-ReflectionAndRefraction-Rendering.frag      # Terrain shading
├── LegacyTerrain-ReflectionAndRefraction-Rendering-Water.vert# Screen-space RTT projection
├── LegacyTerrain-ReflectionAndRefraction-Rendering-Water.frag# Mixes reflection and refraction
├── LegacyTerrain-SoftEdges-Rendering.py                      # Soft edge driver
├── LegacyTerrain-SoftEdges-Rendering.vert                    # Terrain transform
├── LegacyTerrain-SoftEdges-Rendering.frag                    # Terrain shading
├── LegacyTerrain-SoftEdges-Rendering-Water.vert              # Depth buffer projection
├── LegacyTerrain-SoftEdges-Rendering-Water.frag              # Depth-based alpha fade
├── cam.py                                                    # Free-fly camera controller
├── Config.prc                                                # Runtime configuration
└── README.md                                                 # Documentation
```

---

## Limitations & Technical Notes

- The offscreen reflection and refraction buffers require Framebuffer Object (FBO) support in Panda3D.
- Screen-space coordinates must be perspective-divided by $w$ in the fragment shader ($\mathbf{uv} = \frac{\mathbf{v}_{clip}.xy}{\mathbf{v}_{clip}.w} \cdot 0.5 + 0.5$) before indexing the RTT textures.
