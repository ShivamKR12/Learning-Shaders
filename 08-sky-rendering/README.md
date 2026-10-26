# Sky Rendering: Skyboxes & Dynamic Skydomes

GLSL shaders and Panda3D drivers for rendering atmospheric skies, background environments, and dynamic celestial horizons. This module progresses from classical static 6-sided skyboxes to spherical panoramic skydomes, and ultimately to a fully procedural, dynamic day/night atmospheric skydome featuring moving clouds, solar transitions, and celestial body tracking.

---

## Quick start

```bash
# Ensure dependencies are installed
pip install -r ../requirements.txt

# Run any of the sky rendering demos
python ShadelessSky-StaticSkybox-Rendering.py
python ShadelessSky-StaticSkydome-Rendering.py
python ShadelessSky-DynamicSkydome-Rendering.py
```

### Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (look around the entire 360° sky horizon) |
| **Esc** | Release Mouse Cursor / Exit |

---

## Technical Overview & Implementation Details

### 1. Static Skybox (`ShadelessSky-StaticSkybox-Rendering.*`)
- Uses a cube geometry encompassing the scene.
- In the vertex shader, depth clamping ensures the sky geometry always renders behind all scene geometry ($z = w$ in homogeneous clip space):
  $$\text{gl\_Position} = (\mathbf{M}_{projection} \cdot \mathbf{M}_{view, un-translated} \cdot \mathbf{v}).xyww$$
- Samples environment textures without showing seams or perspective distortions.

### 2. Static Skydome (`ShadelessSky-StaticSkydome-Rendering.*`)
- Loads a hemispherical/spherical 3D dome mesh (`models/SkyDome.gltf`).
- Maps celestial panoramas seamlessly around the horizon.
- Automatically follows the camera translation, creating the illusion of infinite distance.

### 3. Dynamic Animated Skydome (`ShadelessSky-DynamicSkydome-Rendering.*`)
- Loads a multi-layered skydome mesh (`models/DynamicSkyDome.gltf`).
- **Cloud Layer UV Scrolling**: Procedurally translates cloud texture coordinates over time:
  $$\mathbf{uv}_{cloud}' = \mathbf{uv}_{cloud} + \mathbf{D}_{wind} \cdot (t \cdot s)$$
- **Solar & Lunar Progression**: Calculates sun and moon azimuth and elevation vectors, transitioning sky color gradients from dawn to midday, golden hour, and starry night.
- **Atmospheric Gradient Blending**: Interpolates zenith and horizon colors using vertex elevation angles:
  $$h = \text{clamp}(v_z / r, 0.0, 1.0)$$
  $$\mathbf{C}_{sky} = \text{mix}(\mathbf{C}_{horizon}, \mathbf{C}_{zenith}, h)$$

---

## Reference

### Script Catalog

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-static-skybox`**](01-static-skybox/README.md) | `ShadelessSky-StaticSkybox-Rendering.py` | `ShadelessSky-StaticSkybox-Rendering.frag`, `ShadelessSky-StaticSkybox-Rendering.vert` | Static Skybox |
| [**`02-static-skydome`**](02-static-skydome/README.md) | `ShadelessSky-StaticSkydome-Rendering.py` | `ShadelessSky-StaticSkydome-Rendering.frag`, `ShadelessSky-StaticSkydome-Rendering.vert` | Static Skydome |
| [**`03-dynamic-skydome`**](03-dynamic-skydome/README.md) | `ShadelessSky-DynamicSkydome-Rendering.py` | `ShadelessSky-DynamicSkydome-Rendering.frag`, `ShadelessSky-DynamicSkydome-Rendering.vert` | Dynamic Skydome |

### Layout

```
08-sky-rendering/
├── 01-static-skybox/
│   ├── ShadelessSky-StaticSkybox-Rendering.py
│   ├── ShadelessSky-StaticSkybox-Rendering.frag
│   ├── ShadelessSky-StaticSkybox-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-static-skydome/
│   ├── ShadelessSky-StaticSkydome-Rendering.py
│   ├── ShadelessSky-StaticSkydome-Rendering.frag
│   ├── ShadelessSky-StaticSkydome-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 03-dynamic-skydome/
│   ├── ShadelessSky-DynamicSkydome-Rendering.py
│   ├── ShadelessSky-DynamicSkydome-Rendering.frag
│   ├── ShadelessSky-DynamicSkydome-Rendering.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- Sky models must be rendered with depth-write disabled (`set_depth_write(False)`) and drawn in the background bin (`set_bin('background', 0)`) so they never occlude foreground terrain or characters.
- In `ShadelessSky-StaticSkybox-Rendering.vert`, stripping translation from the view matrix ensures the camera can travel thousands of units across the game world without ever reaching the sky boundary.

