# Lesson: Ambient Lighting

Part of the **06-legacy-pipeline** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson emulates OpenGL fixed-function pipeline behavior for **Ambient Lighting** using programmable GLSL. It demonstrates how traditional hardware graphics pipelines rendered scenes before modern shaders.

## 📂 File Structure

```
03-ambient-lighting/
├── Legacy-AmbientLighting-Lighting.py
├── Legacy-AmbientLighting-Lighting.vert
├── Legacy-AmbientLighting-Lighting.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Legacy-AmbientLighting-Lighting.vert`

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

File: `Legacy-AmbientLighting-Lighting.frag`

```glsl
#version 140

uniform struct p3d_LightModelParameters {
    vec4 ambient;
} p3d_LightModel;
uniform struct p3d_MaterialParameters {
    vec4 ambient;
    vec4 diffuse;
    vec4 emission;
    vec3 specular;
    float shininess;
    
    vec4 baseColor;
    float roughness;
    float metallic;
    float refractiveIndex;
} p3d_Material;

out vec4 p3d_FragColor;


vec4 applyLighting(vec4 color) {
    // Calculate lighting
    vec4 lighting = p3d_LightModel.ambient * p3d_Material.ambient;

    // Apply lighting to initial color
    lighting.a = color.a;
    return color * lighting;
}


void main() {
    // Calculate base color
    vec4 baseColor = vec4(0.0, .225, .8, 1.0);

    // Calculate final color
    p3d_FragColor = applyLighting(baseColor);
}
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python Legacy-AmbientLighting-Lighting.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
