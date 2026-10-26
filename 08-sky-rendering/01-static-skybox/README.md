# Lesson: Static Skybox

Part of the **08-sky-rendering** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates atmospheric sky rendering for **Static Skybox**. It renders panoramic horizons and dynamic sky backgrounds centered on the viewer with proper depth isolation.

## 📂 File Structure

```
01-static-skybox/
├── ShadelessSky-StaticSkybox-Rendering.py
├── ShadelessSky-StaticSkybox-Rendering.vert
├── ShadelessSky-StaticSkybox-Rendering.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `ShadelessSky-StaticSkybox-Rendering.vert`

```glsl
#version 140

in vec4 p3d_Vertex;

uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ProjectionMatrix;

out vec3 uv;


void main() {
    // Calculate vertex position
    mat4 skyboxViewMatrix = mat4(mat3(p3d_ViewMatrix));
    gl_Position = p3d_ProjectionMatrix * skyboxViewMatrix * p3d_Vertex;
    gl_Position.z = gl_Position.w;

    // Calculate UV
    uv = p3d_Vertex.xyz;
}
```

## 🎨 Fragment Shader

File: `ShadelessSky-StaticSkybox-Rendering.frag`

```glsl
#version 140

in vec3 uv;

uniform samplerCube p3d_Texture0;

out vec4 p3d_FragColor;


void main() {
    // Calculate final color
    p3d_FragColor = texture(p3d_Texture0, uv);
}
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python ShadelessSky-StaticSkybox-Rendering.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
