# Solar System Simulation

This project is a realistic simulation of the solar system using OpenGL. It features accurate modeling of the planets, their textures, and their orbits around the sun. The simulation also includes advanced lighting techniques, such as the Phong Reflection Model and moving scene lights, to enhance the visual quality of the scene.

## Features

- Camera that can orbit the solar system
- Accurate textures for each planet
- Phong Reflection Model for realistic lighting
- Moving scene lights that correctly accumulate to light each object
- Additional planets with their own scale and revolution speed
- Cloud texture for Earth that rotates faster than the planet itself
- Starry background for a more immersive experience
- Attenuation and gamma correction for realistic lighting

## Core Requirements

### Camera Orbit

The camera can orbit around the solar system, allowing the user to view the planets from different angles. This is achieved by updating the camera's position based on user input. The camera is always looking at the world origin (0, 0, 0), where the sun is located.

```python
def update_camera(self, keys):
    if keys[pg.K_w]:
        self.camera_rotation_x += self.camera_speed
    if keys[pg.K_s]:
        self.camera_rotation_x -= self.camera_speed
    if keys[pg.K_a]:
        self.camera_rotation_y -= self.camera_speed
    if keys[pg.K_d]:
        self.camera_rotation_y += self.camera_speed
    if keys[pg.K_q]:
        self.camera_rotation_z -= self.camera_speed
    if keys[pg.K_e]:
        self.camera_rotation_z += self.camera_speed
```

### Planet Textures

Each planet has its own unique texture that is accurately mapped onto the sphere geometry. The textures are loaded using the load_texture function, which supports both diffuse and normal textures.

```python
def load_textures(self):
    for planet in self.planets:
        diffuse_texture, normal_texture, cloud_texture = self.load_texture(planet.diffuse_path, planet.normal_path)
        self.diffuse_textures[planet.name] = diffuse_texture
        self.normal_textures[planet.name] = normal_texture

        if planet.name == "Earth":
            self.earth_cloud_texture = cloud_texture
```

### Phong Reflection Model

The Phong Reflection Model is implemented in the fragment shader to achieve realistic lighting. It takes into account the ambient, diffuse, and specular components of the light sources, as well as the material properties of the planets.

```glsl
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
```

### Moving Scene Lights

In addition to the sun, there are two emissive planets (Jupiter and Neptune) that act as moving scene lights. These lights correctly accumulate and contribute to the lighting of each object in the scene.

```glsl
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
    float emissiveIntensity = 1.5;

    // Combine the lighting components
    result += (ambient + diffuse + specular) * lightColors[i] * attenuation * emissiveIntensity;
}
```

To see this effect look at planets close to Jupiter, which will have a reddish tint, and planets close to Neptune, which will have a bluish tint.

## Mastery Work

### Additional Planets

In addition to the core planets, the simulation includes several additional planets with their own scale and revolution speed around the sun. These planets also rotate on their own axes, adding to the realism of the simulation.

```python
self.planets = [
    Planet("Mercury", self.first_planet_distance, 0.2, 20.0, 10.0, "./resources/mercury/diffuse.png", "./resources/mercury/normal.png"),
    Planet("Venus", self.first_planet_distance + 4, 0.4, 15.0, 8.0, "./resources/venus/diffuse.png", "./resources/venus/normal.png", 0.2, [0.8, 0.6, 0.2]),
    Planet("Earth", self.first_planet_distance + 8, 0.5, 10.0, 20.0, "./resources/earth/diffuse.png", "./resources/earth/normal.png", 0.1, [0.0, 0.5, 1.0]),
    Planet("Mars", self.first_planet_distance + 12, 0.3, 8.0, 12.0, "./resources/mars/diffuse.png", "./resources/mars/normal.png", 0.05, [0.8, 0.4, 0.1]),
    Planet("Jupiter", self.first_planet_distance + 20, 1.5, 5.0, 5.0, "./resources/jupiter/diffuse.png", "./resources/jupiter/normal.png", 0.3, [0.8, 0.6, 0.4], [1.0, 0.6, 0.2]),
    Planet("Saturn", self.first_planet_distance + 40, 1.2, 4.0, 4.0, "./resources/saturn/diffuse.png", "./resources/saturn/normal.png", 0.2, [0.8, 0.7, 0.5]),
    Planet("Uranus", self.first_planet_distance + 60, 0.8, 3.0, 3.0, "./resources/uranus/diffuse.png", "./resources/uranus/normal.png", 0.15, [0.6, 0.8, 0.9], [0.2, 0.6, 1.0]),
    Planet("Neptune", self.first_planet_distance + 70, 0.7, 2.0, 2.0, "./resources/neptune/diffuse.png", "./resources/neptune/normal.png", 0.1, [0.2, 0.4, 0.8])
]
```

### Cloud Texture for Earth

The Earth planet features a cloud texture that rotates faster than the planet itself. This cloud texture is blended with the diffuse texture of the Earth, creating a realistic representation of the planet's atmosphere.

```glsl
if (isEarth) {
    // Apply cloud texture for Earth
    vec2 animatedCloudTexCoord = CloudTexCoord + vec2(cloudAnimationTime, 0.0);
    vec4 cloudColor = texture(cloudTexture, animatedCloudTexCoord);

    // Blend the cloud color with the diffuse color based on the cloud alpha
    float cloudAlpha = 0.5; // Adjust this value to control the transparency of the clouds
    diffuseColor.rgb = mix(diffuseColor.rgb, cloudColor.rgb, cloudColor.a * cloudAlpha);
}
```

### Starry Background

To enhance the immersion and realism of the solar system, a starry background has been added. This background is a large sphere that encompasses the entire scene and is textured with a starry sky image.

```python
# Bind the starry background texture
glActiveTexture(GL_TEXTURE0)
glBindTexture(GL_TEXTURE_2D, self.starry_background_texture)
glUniform1i(glGetUniformLocation(self.shader, "diffuseTexture"), 0)

# Create a large sphere encompassing the scene
background_radius = 50
background_model = pyrr.matrix44.create_identity()
background_model = pyrr.matrix44.multiply(background_model, pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0])))
background_model = pyrr.matrix44.create_from_scale(pyrr.Vector3([background_radius, background_radius, background_radius]))

# Draw the starry background sphere
self.draw_object(self.sphere, background_model, None, None, None, None, is_starry_background=True)
```

### Attenuation and Gamma Correction

To further improve the realism of the lighting, attenuation and gamma correction have been implemented. Attenuation ensures that the intensity of the light decreases with distance, while gamma correction corrects the brightness of the final image to match the human eye's perception.

```glsl
// Attenuation based on distance
float attenuation = 1.0 / (1.0 + 0.1 * distance + 0.01 * distance * distance);

// Gamma correction
const float gamma = 2.2;
vec3 gammaCorrectedColor = pow(finalColor, vec3(1.0 / gamma));
```

## Running the Simulation

To run the solar system simulation, follow these steps:

1. Ensure that you have Python and the required dependencies installed.
2. Clone the repository and navigate to the project directory.
3. Run the following command to install the necessary packages:

   ```bash
   make install
   ```

4. Start the simulation by running:

   ```bash
   make run
   ```

**Note:** If you are using python instead of python3, please adjust the Makefile accordingly.

## Controls

- `W`, `S`, `A`, `D`: Orbit the camera around the solar system
- `Q`, `E`: Rotate the camera around its own axis
- `Space`: Toggle the animation on/off

Enjoy exploring the solar system simulation!
