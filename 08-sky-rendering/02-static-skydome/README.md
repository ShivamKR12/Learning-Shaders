# Lesson: Static Skydome

Part of the **08-sky-rendering** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates atmospheric sky rendering for **Static Skydome**. It renders panoramic horizons and dynamic sky backgrounds centered on the viewer with proper depth isolation.

## 📂 File Structure

```
02-static-skydome/
├── ShadelessSky-StaticSkydome-Rendering.py
├── ShadelessSky-StaticSkydome-Rendering.vert
├── ShadelessSky-StaticSkydome-Rendering.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `ShadelessSky-StaticSkydome-Rendering.vert`

```glsl
#version 140

in vec4 p3d_Vertex;
in vec3 p3d_MultiTexCoord0;

uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ProjectionMatrix;

out vec2 uv;


void main() {
    // Calculate vertex position
    mat4 skyboxViewMatrix = mat4(mat3(p3d_ViewMatrix));
    gl_Position = p3d_ProjectionMatrix * skyboxViewMatrix * p3d_Vertex;
    gl_Position.z = gl_Position.w;

    // Calculate UV
    uv = p3d_MultiTexCoord0.xy;
}
```

## 🎨 Fragment Shader

File: `ShadelessSky-StaticSkydome-Rendering.frag`

```glsl
#version 140

in vec2 uv;

uniform sampler2D p3d_Texture0;

out vec4 p3d_FragColor;


void main() {
    // Calculate final color
    p3d_FragColor = texture(p3d_Texture0, uv);
}
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python ShadelessSky-StaticSkydome-Rendering.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
