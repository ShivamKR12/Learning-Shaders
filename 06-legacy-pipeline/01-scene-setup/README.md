# Lesson: Scene Setup

Part of the **06-legacy-pipeline** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson emulates OpenGL fixed-function pipeline behavior for **Scene Setup** using programmable GLSL. It demonstrates how traditional hardware graphics pipelines rendered scenes before modern shaders.

## 📂 File Structure

```
01-scene-setup/
├── Legacy-SceneSetup-Rendering.py
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Legacy-SceneSetup-Rendering.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
