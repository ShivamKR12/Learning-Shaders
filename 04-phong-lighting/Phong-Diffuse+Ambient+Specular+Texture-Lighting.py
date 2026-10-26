from direct.showbase.ShowBase import ShowBase
# Import the ShowBase class from Panda3D.
# ShowBase is the main application class that sets up:
#     • the window
#     • the rendering engine
#     • the default camera
#     • the scene graph
#     • input handling
# By inheriting from ShowBase, this program becomes a Panda3D application.


from panda3d.core import Shader
# Import Panda3D's Shader class.
# This allows us to load GLSL shaders (vertex + fragment programs)
# and apply them to models in the scene.


from panda3d.core import Vec3
# Import Panda3D's Vec3 class for 3D vector math.
# Used here to define the light's direction vector.

from math import sin, cos
# Import sine and cosine functions from Python's math library.
# Used to calculate the light's position as it orbits the model.


from cam import FreeFlyCamera
# Import a custom free-fly camera class.
# Provides Blender-style camera controls:
#     • W/S: forward/backward
#     • A/D: left/right
#     • Q/E: down/up
#     • Hold RMB: mouse look
#     • Esc: release mouse
# The FreeFlyCamera attaches to the ShowBase camera to override default controls.


class App(ShowBase):
    """
    Define a new class called App, which inherits from ShowBase.
    
    By extending ShowBase:
       • the constructor (__init__) creates the Panda3D window
       • we have access to 'loader', 'render', the default camera, task manager, etc.
       • allows straightforward setup of 3D scenes
    """


    def __init__(self):
        """
        The class constructor.
        This method runs automatically when an instance of App is created.
        It sets up the 3D scene, camera, model, texture, and shader.
        """


        ShowBase.__init__(self)
        # Call the parent class (ShowBase) constructor.
        # Without this, Panda3D would NOT:
        #     • open a window
        #     • create a scene graph
        #     • initialize rendering
        #     • set up the default camera
        #     • prepare the loader and input system


        FreeFlyCamera(self)
        # Attach a free-fly camera to the application.
        # Replaces Panda3D’s default mouse camera control.
        # Enables movement and mouse-look controls as defined in FreeFlyCamera.


        self.model = self.loader.load_model("models/panda-model")
        # Load a 3D model from disk.
        # 'self.loader' is provided by ShowBase.
        # Searches Panda3D's model-path for "models/panda-model.*"
        # Returns a NodePath, stored in the variable 'model'.


        self.model.reparentTo(self.render)
        # Attach the model to the scene graph.
        # 'self.render' is the root node of the 3D world.
        # Nothing is visible until a model is parented somewhere in the scene graph.


        self.model.setPos(0, 7, -1)
        # Move the model in the 3D world.
        # setPos(x, y, z):
        #     x = left/right
        #     y = forward/back (positive Y moves away from camera)
        #     z = up/down
        # Positions the panda slightly below center and 7 units away from the camera.


        self.model.setScale(0.002)
        # Scale down the model.
        # The panda model is very large by default, so scaling it to 0.002 makes it visible at normal size.


        self.shader = Shader.load(
            Shader.SL_GLSL,
            "Phong-Diffuse+Ambient+Specular+Texture-Lighting.vert",
            "Phong-Diffuse+Ambient+Specular+Texture-Lighting.frag"
        )
        """
        Load the GLSL shader files.

        Shader.load parameters:
            - Shader.SL_GLSL:
                  instructs Panda3D to expect GLSL shaders
            - "Phong-Diffuse+Ambient+Specular+Texture-Lighting.vert":
                  the vertex shader file
            - "Phong-Diffuse+Ambient+Specular+Texture-Lighting.frag":
                  the fragment shader file

        Panda3D will:
            • compile both shaders
            • link them into a single GPU program
            • report errors if compilation or linking fails

        The resulting Shader object is stored in 'shader'.
        """


        self.model.setShader(self.shader)
        # Apply the loaded shader to the model.
        # Now, whenever this model is rendered, Panda3D will use:
        #     • Phong-Diffuse+Ambient+Specular+Texture-Lighting.vert (vertex shader)
        #     • Phong-Diffuse+Ambient+Specular+Texture-Lighting.frag (fragment shader)
        # This replaces the default fixed-function lighting/shading with our custom shader.


        self.texture = self.loader.load_texture('models/maps/panda-model.jpg')
        # Load a 2D texture from disk.
        # The texture will be applied to the model in the fragment shader.
        # Returns a Texture object stored in 'texture'.


        self.model.setShaderInput('tex', self.texture)
        # Pass the texture to the shader as a uniform input.
        # 'tex' is the uniform name expected by the fragment shader.
        # The shader can now sample this texture per fragment for color information.


        self.light_angle = 0.0
        # Initialize an angle for animating the light source.
        # This will be updated each frame to make the light orbit the model.

        self.taskMgr.add(self.update_light, "UpdateLight")
        # Add a task to the task manager.
        # 'self.update_light' will be called every frame.
        # "UpdateLight" is a unique name for this task.
        # This is how we create animations and per-frame logic in Panda3D.


    def update_light(self, task):
        """
        A task that runs every frame to update the light's direction.

        This function:
          - increments the light's angle over time
          - calculates a new 3D direction vector for the light
          - sends this new direction to the shader as a uniform

        The result is a light that appears to orbit the model.
        """

        self.light_angle += globalClock.getDt() * 0.5 # type: ignore
        # Increment the angle based on elapsed time (dt).
        # globalClock.getDt() returns the time since the last frame.
        # Multiplying by 0.5 slows down the rotation speed.

        # Calculate a new direction vector for the light using trigonometry.
        # The light orbits in the XZ plane (around the Y axis).
        light_direction = Vec3(
            cos(self.light_angle),
            0.0,
            sin(self.light_angle)
        )

        self.model.setShaderInput("light_direction", light_direction)
        # Pass the new light direction to the shader.
        # "light_direction" is the name of the uniform in the GLSL shader.
        # The shader will use this updated value for its lighting calculations in the next frame.

        return task.cont
        # Tell the task manager to continue calling this task in the next frame.


app = App()
# Create an instance of the App class.
# This triggers App.__init__(), setting up the window, camera, model, texture, and shader.


app.run()
# Start Panda3D’s main loop.
#
# This loop:
#     • updates the window
#     • handles input
#     • updates tasks
#     • renders every frame
#
# The program continues running until the window is closed.
