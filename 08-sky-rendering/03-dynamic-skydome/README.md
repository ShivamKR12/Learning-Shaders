# Lesson: Dynamic Skydome

Part of the **08-sky-rendering** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates atmospheric sky rendering for **Dynamic Skydome**. It renders panoramic horizons and dynamic sky backgrounds centered on the viewer with proper depth isolation.

## 📂 File Structure

```
03-dynamic-skydome/
├── ShadelessSky-DynamicSkydome-Rendering.py
├── ShadelessSky-DynamicSkydome-Rendering.vert
├── ShadelessSky-DynamicSkydome-Rendering.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `ShadelessSky-DynamicSkydome-Rendering.vert`

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

File: `ShadelessSky-DynamicSkydome-Rendering.frag`

```glsl
#version 140

in vec2 uv;

uniform sampler2D p3d_Texture0;
uniform sampler2D p3d_Texture1;
uniform sampler2D p3d_Texture2;
uniform vec4 horizonColor;
uniform vec4 zenithColor;
uniform vec2 cloudScrollVec;
uniform vec2 cloudScale;
uniform vec2 celestialScrollVec;
uniform float osg_FrameTime;

out vec4 p3d_FragColor;


void main() {
    // Calculate base color
    vec4 baseColor = horizonColor;
    vec4 colorMask = texture(p3d_Texture0, uv);
    vec4 cloudColor = texture(p3d_Texture1, uv / cloudScale + cloudScrollVec * osg_FrameTime);
    vec4 celestialColor = texture(p3d_Texture2, uv / vec2(2, 1) + celestialScrollVec * osg_FrameTime);
    baseColor = mix(baseColor, zenithColor, colorMask.r);
    baseColor = mix(baseColor, celestialColor, celestialColor.a);
    baseColor = mix(baseColor, cloudColor, cloudColor.a);

    // Calculate final color
    p3d_FragColor = baseColor;
}
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python ShadelessSky-DynamicSkydome-Rendering.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
