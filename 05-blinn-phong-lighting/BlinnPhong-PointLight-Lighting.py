import math
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Shader, Vec3
from cam import FreeFlyCamera


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        FreeFlyCamera(self)


        # 1. Load the Blinn-Phong Point Light Shader
        self.shader = Shader.load(
            Shader.SL_GLSL,
            "BlinnPhong-PointLight-Lighting.vert",
            "BlinnPhong-PointLight-Lighting.frag"
        )


        # 2. Setup a Floor
        # We need a large surface to clearly see how the point light 
        # creates a localized circle of illumination.
        self.floor = self.loader.load_model("models/box")
        self.floor.set_scale(10.0, 10.0, 0.5)
        self.floor.set_pos(0, 10, -3)
        self.floor.set_shader(self.shader)
        self.floor.reparent_to(self.render)


        # 3. Setup a Subject
        self.model = self.loader.load_model("models/teapot")
        self.model.set_pos(0, 10, -2)
        self.model.set_shader(self.shader)
        self.model.reparent_to(self.render)


        # 4. Setup a Visual Light Bulb
        # We use a small sphere to visually represent where the light source is in 3D space.
        self.light_bulb = self.loader.load_model("models/Sphere")
        self.light_bulb.set_scale(0.2)
        self.light_bulb.reparent_to(self.render)
        
        # We give the bulb a bright neon green color.
        # Since we DO NOT apply our shader to the bulb, it will render 
        # unshaded (flat), which makes it look like it's glowing!
        self.light_color = Vec3(0.2, 1.0, 0.2)
        self.light_bulb.set_color(self.light_color.x, self.light_color.y, self.light_color.z, 1.0)


        # 5. Send static uniform data to the shaders
        # Send the light color to both the floor and the teapot
        self.floor.set_shader_input("light_color", self.light_color)
        self.model.set_shader_input("light_color", self.light_color)


        # 6. Start the animation loop
        self.light_angle = 0.0
        self.taskMgr.add(self.update_light, "UpdateLight")


    def update_light(self, task):
        """
        Animates the point light, moving it in an orbiting, bouncing pattern.
        """
        
        self.light_angle += globalClock.getDt() * 1.5 # type: ignore

        # Calculate a dynamic 3D position for the light
        x = math.cos(self.light_angle) * 6.0
        y = 10.0 + math.sin(self.light_angle) * 6.0
        
        # Bounce up and down using sine on a faster frequency
        z = math.sin(self.light_angle * 3.0) * 3.0 + 1.0

        light_pos = Vec3(x, y, z)

        # Physically move the visual glowing bulb mesh
        self.light_bulb.set_pos(light_pos)

        # Send the mathematical World Space position of the light to the shaders
        self.floor.set_shader_input("light_pos_world", light_pos)
        self.model.set_shader_input("light_pos_world", light_pos)

        return task.cont


app = App()
app.run()