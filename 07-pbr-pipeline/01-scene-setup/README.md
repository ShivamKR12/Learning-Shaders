# Lesson: Scene Setup

Part of the **07-pbr-pipeline** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates modern Physically Based Rendering (PBR) for **Scene Setup**. It implements energy-conserving microfacet reflectance using the Cook-Torrance BRDF (GGX distribution, Schlick geometry, and Fresnel reflectivity).

## 📂 File Structure

```
01-scene-setup/
├── Pbr-SceneSetup-Rendering.py
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Pbr-SceneSetup-Rendering.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
