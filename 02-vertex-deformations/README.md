# Vertex Shader Deformations & Mesh Manipulation

Procedural vertex displacement and geometric deformation shaders implemented with GLSL and Panda3D. This module focuses exclusively on the vertex processing stage, demonstrating how to animate, twist, extrude, and deform 3D meshes directly on the GPU without CPU mesh re-computation or buffer transfers.

All transformations manipulate vertex positions in model space before applying the Model-View-Projection (MVP) matrix, achieving 60+ FPS procedurally driven geometry.

---

## Quick start

```bash
# Ensure dependencies are installed
pip install -r ../requirements.txt

# Run any of the vertex deformation demos
python Minimal-YWave-Deformation.py
python Minimal-DirectionalWave-Deformation.py
python Minimal-HeightTwist-Deformation.py
python Minimal-NormalPulse-Deformation.py
python Minimal-RadialExplosion-Deformation.py
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

## Technical Overview & Mathematical Models

### 1. Sinusoidal Y-Wave (`Minimal-YWave-Deformation.*`)
Displaces vertex vertical coordinates along the Y axis using a traveling sine wave parameterized by spatial frequency and time:
$$y' = y + \sin(x \cdot \omega + t \cdot s) \cdot A$$
- $\omega$: Spatial frequency across the mesh surface.
- $s$: Wave travel speed.
- $A$: Wave displacement amplitude.

### 2. 2D Directional Wave (`Minimal-DirectionalWave-Deformation.*`)
Extends 1D oscillation into a directional traveling wave across a specified 2D vector $\mathbf{D}$:
$$\mathbf{v}' = \mathbf{v} + \mathbf{N} \cdot \left(\sin((\mathbf{v} \cdot \mathbf{D}) \cdot \omega + t \cdot s) \cdot A\right)$$
Simulates ocean swells, undulating flags, and rippling fabric.

### 3. Height-Based Torsional Twist (`Minimal-HeightTwist-Deformation.*`)
Applies a variable angle rotation $\theta(z)$ around the vertical axis proportional to vertex elevation:
$$\theta = z \cdot k_{twist} \cdot \sin(t)$$
$$\begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix}$$
Generates twisting pillars, vortex distortions, and jelly-like torsional elasticity.

### 4. Normal Extrusion / Breathing Pulse (`Minimal-NormalPulse-Deformation.*`)
Displaces each vertex along its outward-facing surface normal vector $\mathbf{n}$:
$$\mathbf{v}' = \mathbf{v} + \mathbf{n} \cdot \left(\sin(t \cdot s) \cdot A\right)$$
Produces breathing, heartbeat, and organic pulsing effects while preserving topology.

### 5. Radial Explosion (`Minimal-RadialExplosion-Deformation.*`)
Displaces vertices radially away from the local origin $(0, 0, 0)$:
$$\mathbf{d} = \frac{\mathbf{v}}{\|\mathbf{v}\|}, \quad \mathbf{v}' = \mathbf{v} + \mathbf{d} \cdot \left(|\sin(t \cdot s)| \cdot A_{max}\right)$$
Simulates explosive dispersal and reassembly cycles.

---

## Reference

### Script Catalog

### 📚 Sub-Directory Lessons

| Lesson Directory | Python Driver | Shaders | Key Feature |
|---|---|---|---|
| [**`01-y-wave`**](01-y-wave/README.md) | `Minimal-YWave-Deformation.py` | `Minimal-YWave-Deformation.frag`, `Minimal-YWave-Deformation.vert` | Y Wave |
| [**`02-directional-wave`**](02-directional-wave/README.md) | `Minimal-DirectionalWave-Deformation.py` | `Minimal-DirectionalWave-Deformation.frag`, `Minimal-DirectionalWave-Deformation.vert` | Directional Wave |
| [**`03-height-twist`**](03-height-twist/README.md) | `Minimal-HeightTwist-Deformation.py` | `Minimal-HeightTwist-Deformation.frag`, `Minimal-HeightTwist-Deformation.vert` | Height Twist |
| [**`04-normal-pulse`**](04-normal-pulse/README.md) | `Minimal-NormalPulse-Deformation.py` | `Minimal-NormalPulse-Deformation.frag`, `Minimal-NormalPulse-Deformation.vert` | Normal Pulse |
| [**`05-radial-explosion`**](05-radial-explosion/README.md) | `Minimal-RadialExplosion-Deformation.py` | `Minimal-RadialExplosion-Deformation.frag`, `Minimal-RadialExplosion-Deformation.vert` | Radial Explosion |

### Layout

```
02-vertex-deformations/
├── 01-y-wave/
│   ├── Minimal-YWave-Deformation.py
│   ├── Minimal-YWave-Deformation.frag
│   ├── Minimal-YWave-Deformation.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 02-directional-wave/
│   ├── Minimal-DirectionalWave-Deformation.py
│   ├── Minimal-DirectionalWave-Deformation.frag
│   ├── Minimal-DirectionalWave-Deformation.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 03-height-twist/
│   ├── Minimal-HeightTwist-Deformation.py
│   ├── Minimal-HeightTwist-Deformation.frag
│   ├── Minimal-HeightTwist-Deformation.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 04-normal-pulse/
│   ├── Minimal-NormalPulse-Deformation.py
│   ├── Minimal-NormalPulse-Deformation.frag
│   ├── Minimal-NormalPulse-Deformation.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── 05-radial-explosion/
│   ├── Minimal-RadialExplosion-Deformation.py
│   ├── Minimal-RadialExplosion-Deformation.frag
│   ├── Minimal-RadialExplosion-Deformation.vert
│   ├── cam.py
│   ├── Config.prc
│   └── README.md
├── cam.py
├── Config.prc
└── README.md
```

---

## Limitations & Technical Notes

- Vertex shader deformations do not automatically recalculate lighting normals. For accurate dynamic lighting on heavily deformed surfaces, the tangent frame or analytical surface derivatives ($\frac{\partial \mathbf{v}'}{\partial u}, \frac{\partial \mathbf{v}'}{\partial v}$) should be used to recalculate perturbed normals.
- Meshes with low polygon densities will produce faceted or rigid deformations; tessellated models (like the Panda3D `smiley` or subdivision spheres) yield the smoothest results.

