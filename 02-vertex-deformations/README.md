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

| Script | Vertex Shader | Fragment Shader | Target Model | Deformation Mechanism |
|---|---|---|---|---|
| `Minimal-YWave-Deformation.py` | `Minimal-YWave-Deformation.vert` | `Minimal-YWave-Deformation.frag` | `models/smiley` | Sinusoidal vertical displacement |
| `Minimal-DirectionalWave-Deformation.py` | `Minimal-DirectionalWave-Deformation.vert` | `Minimal-DirectionalWave-Deformation.frag` | `models/smiley` | Directional surface wave modulation |
| `Minimal-HeightTwist-Deformation.py` | `Minimal-HeightTwist-Deformation.vert` | `Minimal-HeightTwist-Deformation.frag` | `models/box` | Height-dependent rotational shear (twist) |
| `Minimal-NormalPulse-Deformation.py` | `Minimal-NormalPulse-Deformation.vert` | `Minimal-NormalPulse-Deformation.frag` | `models/smiley` | Inflation/deflation along vertex normals |
| `Minimal-RadialExplosion-Deformation.py` | `Minimal-RadialExplosion-Deformation.vert` | `Minimal-RadialExplosion-Deformation.frag` | `models/smiley` | Origin-centered radial vertex dispersal |

### Layout

```
02-vertex-deformations/
├── Minimal-YWave-Deformation.py              # Sine wave displacement driver
├── Minimal-YWave-Deformation.vert            # Modifies vertex Y coordinate
├── Minimal-YWave-Deformation.frag            # Surface shading pass
├── Minimal-DirectionalWave-Deformation.py    # Directional wave driver
├── Minimal-DirectionalWave-Deformation.vert  # Vector dot-product wave equation
├── Minimal-DirectionalWave-Deformation.frag  # Shading pass
├── Minimal-HeightTwist-Deformation.py        # Torsional twist driver
├── Minimal-HeightTwist-Deformation.vert      # 2D rotation matrix applied along Z
├── Minimal-HeightTwist-Deformation.frag      # Shading pass
├── Minimal-NormalPulse-Deformation.py        # Normal inflation driver
├── Minimal-NormalPulse-Deformation.vert      # Extrudes position along vertex normal
├── Minimal-NormalPulse-Deformation.frag      # Shading pass
├── Minimal-RadialExplosion-Deformation.py    # Radial explosion driver
├── Minimal-RadialExplosion-Deformation.vert  # Pushes vertices outwards from origin
├── Minimal-RadialExplosion-Deformation.frag  # Shading pass
├── cam.py                                    # Free-fly camera controller
├── Config.prc                                 # Runtime configuration
└── README.md                                  # Documentation
```

---

## Limitations & Technical Notes

- Vertex shader deformations do not automatically recalculate lighting normals. For accurate dynamic lighting on heavily deformed surfaces, the tangent frame or analytical surface derivatives ($\frac{\partial \mathbf{v}'}{\partial u}, \frac{\partial \mathbf{v}'}{\partial v}$) should be used to recalculate perturbed normals.
- Meshes with low polygon densities will produce faceted or rigid deformations; tessellated models (like the Panda3D `smiley` or subdivision spheres) yield the smoothest results.
