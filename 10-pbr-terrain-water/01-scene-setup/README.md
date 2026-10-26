# Lesson: Scene Setup

Part of the **10-pbr-terrain-water** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson implements landscape and hydrological shading for **Scene Setup**. It handles complex multi-texture splatting, dynamic water surface geometry, ripple distortion, and depth-tested shoreline effects.

## 📂 File Structure

```
01-scene-setup/
├── PbrTerrain-SceneSetup-Rendering.py
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python PbrTerrain-SceneSetup-Rendering.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
