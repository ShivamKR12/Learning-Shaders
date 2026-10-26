# Lesson: Shadeless Rendering

Part of the **06-legacy-pipeline** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson emulates OpenGL fixed-function pipeline behavior for **Shadeless Rendering** using programmable GLSL. It demonstrates how traditional hardware graphics pipelines rendered scenes before modern shaders.

## 📂 File Structure

```
02-shadeless-rendering/
├── Legacy-ShadelessRendering-Rendering.py
├── Legacy-ShadelessRendering-Rendering.vert
├── Legacy-ShadelessRendering-Rendering.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Legacy-ShadelessRendering-Rendering.vert`

```glsl
#version 140

in vec4 p3d_Vertex;

uniform mat4 p3d_ModelViewProjectionMatrix;


void main() {
    // Calculate vertex position
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
```

## 🎨 Fragment Shader

File: `Legacy-ShadelessRendering-Rendering.frag`

```glsl
#version 140

out vec4 p3d_FragColor;


void main() {
    // Calculate fragment color
    p3d_FragColor = vec4(0.0, .225, .8, 1.0);
}
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Legacy-ShadelessRendering-Rendering.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
