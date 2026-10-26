# Lesson: Water Plane

Part of the **09-legacy-terrain-water** module in the Panda3D GLSL Shader Laboratory.

## 📖 Overview

This lesson implements landscape and hydrological shading for **Water Plane**. It handles complex multi-texture splatting, dynamic water surface geometry, ripple distortion, and depth-tested shoreline effects.

## 📂 File Structure

```
03-water-plane/
├── LegacyTerrain-WaterPlane-Rendering-Water.py
├── LegacyTerrain-WaterPlane-Rendering.py
├── LegacyTerrain-WaterPlane-Rendering.vert
├── LegacyTerrain-WaterPlane-Rendering.frag
├── cam.py                 # Free-fly Blender camera controller
├── Config.prc              # Panda3D runtime configuration
└── README.md               # Lesson documentation
```

## 🔺 Vertex Shader

File: `LegacyTerrain-WaterPlane-Rendering.vert`

```glsl
#version 140

in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec3 p3d_MultiTexCoord0;

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat3 p3d_NormalMatrix;

out vec3 fragPos;
out vec3 normal;
out vec2 uv;


void main() {
    // Calculate vertex position, fragment position, and surface normal
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    fragPos = vec3(p3d_ModelViewMatrix * p3d_Vertex);
    normal = p3d_NormalMatrix * p3d_Normal;

    // Calculate UV
    uv = p3d_MultiTexCoord0.xy;
}
```

## 🎨 Fragment Shader

File: `LegacyTerrain-WaterPlane-Rendering.frag`

```glsl
#version 140

in vec3 fragPos;
in vec3 normal;
in vec2 uv;

uniform mat4 p3d_ViewMatrix;
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
uniform struct p3d_FogParameters {
    vec4 color;
    float density;
    float start;
    float end;
    float scale; // 1.0 / (end - start)
} p3d_Fog;
uniform sampler2D p3d_Texture0;
uniform sampler2D p3d_Texture1;
uniform sampler2D p3d_Texture2;
uniform sampler2D p3d_Texture3;
uniform sampler2D p3d_Texture4;
uniform vec2 texScale0;
uniform vec2 texScale1;
uniform vec2 texScale2;
uniform vec2 texScale3;

out vec4 p3d_FragColor;


vec4 applyLighting(vec4 color) {
    // Normalize normal and extract camera position from view matrix
    vec3 norm = normalize(normal);
    vec3 cameraPos = p3d_ViewMatrix[3].xyz;

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
        float nxDir = max(0.0, dot(norm, lightVector));
        vec4 diffuse = p3d_LightSource[i].color * nxDir * attenuation;

        // Calculate specular lighting
        vec3 cameraVector = normalize(cameraPos - fragPos);
        vec3 halfVector = normalize(lightVector + cameraVector);
        float nxHalf = max(0.0, dot(norm, halfVector));
        float specularPower = pow(nxHalf, p3d_Material.shininess);
        vec4 specular = p3d_LightSource[i].color * specularPower * 
            attenuation * int(nxDir != 0.0);

        // Calculate total lighting
        lighting += (p3d_LightModel.ambient * p3d_Material.ambient + 
            (diffuse * p3d_Material.diffuse) + 
            (specular * vec4(p3d_Material.specular, 1.0)));
    }

    // Apply lighting to initial color
    lighting.a = color.a;
    return color * lighting;
}


vec4 applyFog(vec4 color) {
    // If fog is disabled, skip fog calculations
    if(p3d_Fog.start == p3d_Fog.end) {
        return color;
    }

    // Calculate linear fog
    float dist = length(fragPos);
    float fogFactor = (p3d_Fog.end - dist) / (p3d_Fog.end - p3d_Fog.start);
    fogFactor = clamp(fogFactor, 0, 1);
    return mix(p3d_Fog.color, color, fogFactor);
}


void main() {
    // Calculate base color
    vec4 baseColor = texture(p3d_Texture0, uv / texScale0);
    vec4 layer1 = texture(p3d_Texture1, uv / texScale1);
    vec4 layer2 = texture(p3d_Texture2, uv / texScale2);
    vec4 layer3 = texture(p3d_Texture3, uv / texScale3);
    vec4 mask0 = texture(p3d_Texture4, uv);
    baseColor = mix(baseColor, layer1, mask0.r);
    baseColor = mix(baseColor, layer2, mask0.g);
    baseColor = mix(baseColor, layer3, mask0.b);

    // Calculate final color
    p3d_FragColor = applyFog(applyLighting(baseColor));
}
```

## 🚀 Quick start

```bash
# Run this specific lesson demo
python LegacyTerrain-WaterPlane-Rendering-Water.py
```

## 🕹️ Controls

| Key | Action |
|---|---|
| **W / S** | Move Camera Forward / Backward |
| **A / D** | Strafe Camera Left / Right |
| **Q / E** | Move Camera Down / Up |
| **Hold RMB + Move Mouse** | Free-fly Mouse Look (pitch & yaw) |
| **Esc** | Release Mouse Cursor / Exit |
