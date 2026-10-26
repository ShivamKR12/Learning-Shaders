# Lesson: Ambient Lighting

Part of the **07-pbr-pipeline** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson demonstrates modern Physically Based Rendering (PBR) for **Ambient Lighting**. It implements energy-conserving microfacet reflectance using the Cook-Torrance BRDF (GGX distribution, Schlick geometry, and Fresnel reflectivity).

## 📂 File Structure

```
03-ambient-lighting/
├── Pbr-AmbientLighting-Lighting.py
├── Pbr-AmbientLighting-Lighting.vert
├── Pbr-AmbientLighting-Lighting.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Pbr-AmbientLighting-Lighting.vert`

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

File: `Pbr-AmbientLighting-Lighting.frag`

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


vec4 applyLighting(vec4 albedo) {
    // Apply lighting to initial color
    vec3 ambient = p3d_LightModel.ambient.rgb * albedo.rgb;
    vec3 color = ambient;
    color = color / (color + vec3(1.0));
    return vec4(color, albedo.a);
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
python Pbr-AmbientLighting-Lighting.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
