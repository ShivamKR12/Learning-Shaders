# Lesson: Shadeless Rendering

Part of the **07-pbr-pipeline** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates modern Physically Based Rendering (PBR) for **Shadeless Rendering**. It implements energy-conserving microfacet reflectance using the Cook-Torrance BRDF (GGX distribution, Schlick geometry, and Fresnel reflectivity).

## 📂 File Structure

```
02-shadeless-rendering/
├── Pbr-ShadelessRendering-Rendering.py
├── Pbr-ShadelessRendering-Rendering.vert
├── Pbr-ShadelessRendering-Rendering.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Pbr-ShadelessRendering-Rendering.vert`

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

File: `Pbr-ShadelessRendering-Rendering.frag`

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
python Pbr-ShadelessRendering-Rendering.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
