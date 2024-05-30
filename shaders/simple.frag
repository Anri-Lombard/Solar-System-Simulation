#version 330 core

#define NUM_LIGHTS 2

// Input variables
in vec2 DiffuseTexCoord;
in vec2 NormalTexCoord;
in vec2 CloudTexCoord;
in vec3 Normal;
in vec3 FragPos;
in vec3 VertexPos;
in vec3 LightPositions[NUM_LIGHTS];

// Output variable
out vec4 FragColor;

// Uniform variables
uniform sampler2D diffuseTexture;
uniform sampler2D normalTexture;
uniform sampler2D cloudTexture;
uniform float cloudAnimationTime;
uniform bool isEarth;
uniform vec3 sunPosition;
uniform float sunRadius;
uniform vec3 sunColor;
uniform vec3 viewPos;
uniform vec3 ka;
uniform vec3 kd;
uniform vec3 ks;
uniform float shininess;
uniform bool isSun;
uniform float atmosphereThickness;
uniform vec3 atmosphereColor;
uniform bool isStarryBackground;
uniform vec3 lightColors[NUM_LIGHTS];
uniform vec3 lightPositions[NUM_LIGHTS];
uniform float lightRadii[NUM_LIGHTS];

void main() {
    // Sample the diffuse and normal textures
    vec4 diffuseColor = texture(diffuseTexture, DiffuseTexCoord);
    vec3 normal = texture(normalTexture, NormalTexCoord).rgb;
    normal = normalize(normal);

    if (isSun) {
        // Sun: Always fully illuminated
        FragColor = diffuseColor;
    } else if (isStarryBackground) {
        // Starry background: Always fully illuminated
        FragColor = diffuseColor;
    } else {
        // Planets: Apply lighting calculations
        vec3 norm = normalize(Normal);
        norm = normalize(norm + normal);

        vec3 viewDir = normalize(viewPos - FragPos);

        vec3 result = vec3(0.0);

        // Sun lighting with attenuation
        float sunDistance = length(sunPosition - FragPos);
        vec3 lightDir = normalize(sunPosition - FragPos);
        float NdotL = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = kd * NdotL * sunColor;
        vec3 halfDir = normalize(lightDir + viewDir);
        float NdotH = max(dot(norm, halfDir), 0.0);
        vec3 specular = ks * pow(NdotH, shininess) * sunColor;
        float sunAttenuation = 1.0 / (1.0 + 0.01 * sunDistance + 0.001 * sunDistance * sunDistance);
        result += (diffuse + specular) * sunAttenuation;

        // Emissive planets lighting
        for (int i = 0; i < NUM_LIGHTS; i++) {
            // Calculate the distance from the fragment to the light source
            float distance = length(lightPositions[i] - FragPos);

            // Ambient lighting
            vec3 ambient = ka;

            // Diffuse lighting
            vec3 lightDir = normalize(lightPositions[i] - FragPos);
            float NdotL = max(dot(norm, lightDir), 0.0);
            vec3 diffuse = kd * NdotL;

            // Specular lighting
            vec3 halfDir = normalize(lightDir + viewDir);
            float NdotH = max(dot(norm, halfDir), 0.0);
            vec3 specular = ks * pow(NdotH, shininess);

            // Attenuation based on distance
            float attenuation = 1.0 / (1.0 + 0.1 * distance + 0.01 * distance * distance);

            // Increase the intensity of the emissive planets
            float emissiveIntensity = 0.5;

            // Combine the lighting components
            result += (ambient + diffuse + specular) * lightColors[i] * attenuation * emissiveIntensity;
        }

        if (isEarth) {
            // Apply cloud texture for Earth
            vec2 animatedCloudTexCoord = CloudTexCoord + vec2(cloudAnimationTime, 0.0);
            vec4 cloudColor = texture(cloudTexture, animatedCloudTexCoord);
            
            // Blend the cloud color with the diffuse color based on the cloud alpha
            float cloudAlpha = 0.5; // Adjust this value to control the transparency of the clouds
            diffuseColor.rgb = mix(diffuseColor.rgb, cloudColor.rgb, cloudColor.a * cloudAlpha);
        }

        // Apply the lighting to the diffuse color
        vec3 finalColor = result * diffuseColor.rgb;

        // Gamma correction
        const float gamma = 2.2;
        vec3 gammaCorrectedColor = pow(finalColor, vec3(1.0 / gamma));

        // Output the final color
        FragColor = vec4(gammaCorrectedColor, diffuseColor.a);
    }
}