#version 330 core

#define NUM_LIGHTS 2

// Input variables
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoord;
layout (location = 2) in vec3 normal;

// Output variables
out vec2 DiffuseTexCoord;
out vec2 NormalTexCoord;
out vec3 Normal;
out vec3 FragPos;
out vec2 RingTexCoord;
out vec3 VertexPos;
out vec2 CloudTexCoord;
out vec3 LightPositions[NUM_LIGHTS];

// Uniform variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat3 normalMatrix;
uniform bool isSaturnRing;
uniform bool isStarryBackground;
uniform bool isEarth;
uniform bool invertNormals;
uniform vec3 lightPositions[NUM_LIGHTS];

void main() {
    // Calculate the fragment position in world space
    FragPos = vec3(model * vec4(position, 1.0));
    VertexPos = position;

    if (isSaturnRing) {
        // Calculate texture coordinates for Saturn's ring based on the angle around the ring
        float angle = atan(position.z, position.x);
        float radius = length(position.xz);
        DiffuseTexCoord = vec2(radius / 2.0, angle / (2.0 * 3.14159265359));
    } else {
        // Use the UV coordinates from the model
        DiffuseTexCoord = texCoord;
        NormalTexCoord = texCoord;

        if (isEarth) {
            CloudTexCoord = texCoord;
        }
    }

    // Calculate the normal vector in world space
    if (invertNormals) {
        Normal = -normalMatrix * normal;
    } else {
        Normal = normalMatrix * normal;
    }
    
    // Pass the light positions to the fragment shader
    for (int i = 0; i < NUM_LIGHTS; i++) {
        LightPositions[i] = vec3(view * vec4(lightPositions[i], 1.0));
    }

    // Calculate the vertex position in clip space
    gl_Position = projection * view * model * vec4(position, 1.0);
}