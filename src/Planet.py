import numpy as np

class Planet:
    def __init__(self, name, distance, radius, speed, rotation_speed, diffuse_path, normal_path, atmosphere_thickness=0.0, atmosphere_color=[0.0, 0.0, 0.0], light_color=[0.0, 0.0, 0.0]):
        """
        Initialize a new Planet object.

        Args:
            name (str): The name of the planet.
            distance (float): The distance of the planet from the sun.
            radius (float): The radius of the planet.
            speed (float): The orbital speed of the planet.
            rotation_speed (float): The rotational speed of the planet.
            diffuse_path (str): The path to the diffuse texture of the planet.
            normal_path (str): The path to the normal texture of the planet.
            atmosphere_thickness (float, optional): The thickness of the planet's atmosphere. Defaults to 0.0.
            atmosphere_color (list, optional): The color of the planet's atmosphere. Defaults to [0.0, 0.0, 0.0].
            light_color (list, optional): The color of the planet's light. Defaults to [0.0, 0.0, 0.0].
        """
        self.name = name
        self.distance = distance
        self.radius = radius
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.diffuse_path = diffuse_path
        self.normal_path = normal_path
        self.atmosphere_thickness = atmosphere_thickness
        self.atmosphere_color = np.array(atmosphere_color, dtype=np.float32)
        self.angle = 0.0
        self.rotation_angle = 0.0
        self.light_color = np.array(light_color, dtype=np.float32)

    def update(self, animation_time):
        """
        Update the planet's position and rotation based on the animation time.

        Args:
            animation_time (float): The current animation time.
        """
        self.angle = self.speed * animation_time
        self.rotation_angle = self.rotation_speed * animation_time