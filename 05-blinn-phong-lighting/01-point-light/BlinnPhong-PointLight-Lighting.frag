#version 150

in vec3 v_fragPos;
in vec3 v_normal;

out vec4 fragColor;

uniform mat4 p3d_ViewMatrix;
/*
   "p3d_ViewMatrix"
   Converts World Space coordinates into View Space coordinates.
*/

uniform vec3 light_pos_world;
/*
   "light_pos_world"
   The 3D position of the point light, sent from Python.
   Because Python uses Panda3D's root 'render' node, this position 
   is in World Space.
*/

uniform vec3 light_color;


void main() {
    
    vec3 N = normalize(v_normal);
    
    /*
       1. Transform Light to View Space
       --------------------------------
       Our fragment position and normal are in View Space.
       The Light Position passed from Python is in World Space.
       We MUST convert the light to View Space using the View Matrix!
    */
    vec3 lightPosView = (p3d_ViewMatrix * vec4(light_pos_world, 1.0)).xyz;


    /*
       2. Calculate Distance and Light Vector
       --------------------------------------
       Subtracting the Fragment position from the Light position gives us 
       a vector that points FROM the fragment TO the light.
    */
    vec3 lightDir = lightPosView - v_fragPos;
    
    // length() gets the actual physical distance between the two points
    float distance = length(lightDir);
    
    // Now that we have the distance, we normalize the direction vector 
    // so we can use it in dot products.
    vec3 L = normalize(lightDir);


    /*
       3. Calculate the View Vector
       ----------------------------
       Because we are in View Space, the camera is exactly at (0, 0, 0).
       The vector from the fragment to the camera is just (0,0,0) - v_fragPos.
       Therefore, -v_fragPos points directly at the camera!
    */
    vec3 V = normalize(-v_fragPos);


    /*
       4. Calculate Attenuation (Inverse Square Law)
       ---------------------------------------------
       Real light falls off quadratically over distance.
       The formula used below is standard in game engines (like Unity/Unreal).
       
       - constant: usually 1.0 so denominator is never less than 1
       - linear:   reduces intensity linearly
       - quadratic: reduces intensity exponentially
    */
    float constant = 1.0;
    float linear = 0.09;
    float quadratic = 0.032;
    
    float attenuation = 1.0 / (constant + (linear * distance) + (quadratic * (distance * distance)));


    /*
       5. Blinn-Phong Lighting
       -----------------------
    */
    // Halfway Vector
    vec3 H = normalize(L + V);

    // Diffuse
    float diff = max(dot(N, L), 0.0);
    
    // Specular (Using Blinn-Phong)
    float shininess = 64.0;
    float spec = pow(max(dot(N, H), 0.0), shininess);


    /*
       6. Combine everything
       ---------------------
       We apply the attenuation multiplier to both diffuse and specular.
       As the distance grows, attenuation approaches 0.0, fading the light out.
    */
    vec3 ambient = vec3(0.05); // Global dim ambient light so the scene isn't pitch black
    
    vec3 diffuse = diff * light_color * attenuation;
    vec3 specular = spec * light_color * attenuation;

    // Sum the lighting components
    vec3 finalColor = ambient + diffuse + specular;
    
    // We map our object as a pure white base color, so we just output the light directly.
    fragColor = vec4(finalColor, 1.0);
}