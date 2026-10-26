# Lesson: Diffuse Lighting

Part of the **06-legacy-pipeline** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson emulates OpenGL fixed-function pipeline behavior for **Diffuse Lighting** using programmable GLSL. It demonstrates how traditional hardware graphics pipelines rendered scenes before modern shaders.

## 📂 File Structure

```
04-diffuse-lighting/
├── Legacy-DiffuseLighting-Lighting.py
├── Legacy-DiffuseLighting-Lighting.vert
├── Legacy-DiffuseLighting-Lighting.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `Legacy-DiffuseLighting-Lighting.vert`

```glsl
#version 140

in vec4 p3d_Vertex;
in vec3 p3d_Normal;

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat3 p3d_NormalMatrix;

out vec3 fragPos;
out vec3 normal;


void main() {
    // Calculate vertex position, fragment position, and surface normal
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    fragPos = vec3(p3d_ModelViewMatrix * p3d_Vertex);
    normal = p3d_NormalMatrix * p3d_Normal;
}
```

## 🎨 Fragment Shader

File: `Legacy-DiffuseLighting-Lighting.frag`

```glsl
#version 140

in vec3 fragPos;
in vec3 normal;

uniform struct p3d_LightModelParameters {
    vec4 ambient;
} p3d_LightModel;
uniform struct p3d_LightSourceParameters {
    // Primary light color.
    vec4 color;

    // Light color broken up into components, for compatibility with legacy
    // shaders. These are now deprecated.
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;

    // View-space position. If w=0, this is a directional light, with the xyz
    // being -direction.
    vec4 position;

    // Spotlight-only settings
    vec3 spotDirection;
    float spotExponent;
    float spotCutoff;
    float spotCosCutoff;

    // Individual attenuation constants
    float constantAttenuation;
    float linearAttenuation;
    float quadraticAttenuation;

    // constant, linear, quadratic attenuation in one vector
    vec3 attenuation;

    // Shadow map for this light source
    sampler2DShadow shadowMap;

    // Transforms view-space coordinates to shadow map coordinates
    mat4 shadowViewMatrix;
} p3d_LightSource[2];
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
    // Normalize normal
    vec3 norm = normalize(normal);

    // Calculate lighting
    vec4 lighting = vec4(0.0);

    for(int i = 0; i < p3d_LightSource.length(); i++) {
        // Calculate light vector
        vec3 lightVector = p3d_LightSource[i].position.xyz - fragPos * 
            p3d_LightSource[i].position.w;

        // Calculate attenuation
        float dist = length(lightVector);
        float attenuation = 1.0 / (p3d_LightSource[i].constantAttenuation + 
            p3d_LightSource[i].linearAttenuation * dist + 
            p3d_LightSource[i].quadraticAttenuation * dist * dist);

        // Normalize light vector
        lightVector = normalize(lightVector);

        // Calculate diffuse lighting
        float nxDir = max(0.0, dot(normal, lightVector));
        vec4 diffuse = p3d_LightSource[i].color * nxDir * attenuation;

        // Calculate total lighting
        lighting += (p3d_LightModel.ambient * p3d_Material.ambient + 
            (diffuse * p3d_Material.diffuse));
    }

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
python Legacy-DiffuseLighting-Lighting.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
