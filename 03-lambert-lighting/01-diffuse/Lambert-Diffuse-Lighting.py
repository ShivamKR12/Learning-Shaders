from direct.showbase.ShowBase import ShowBase
# Import the ShowBase class from Panda3D.
#
# ShowBase is the core application class that:
#   • opens a window
#   • initializes the rendering engine
#   • creates the scene graph
#   • sets up the default camera
#   • manages input, tasks, and timing
#
# By inheriting from ShowBase, our program becomes
# a fully functional Panda3D application.


from panda3d.core import Shader
# Import Panda3D's Shader class.
#
# The Shader class allows us to:
#   • load GLSL shader programs (vertex + fragment)
#   • compile and link them on the GPU
#   • apply them to models in the scene
#
# Using custom shaders replaces Panda3D’s
# built-in fixed-function lighting pipeline.


from panda3d.core import Vec3
# Import Panda3D's Vec3 class for 3D vector math.
# Used here to define the light's direction vector.

from math import sin, cos
# Import sine and cosine functions from Python's math library.
# Used to calculate the light's position as it orbits the model.


from cam import FreeFlyCamera


class App(ShowBase):
    """
    Define a new application class called App.

    This class inherits from ShowBase, meaning:
      • creating an App instance sets up Panda3D
      • we gain access to:
            - self.render (scene graph root)
            - self.loader (model/asset loader)
            - camera and camera controls
            - task manager and input handling
    """


    def __init__(self):
        """
        The constructor for the App class.

        This method runs automatically when we create
        an instance of App.

        Its responsibilities:
          • initialize Panda3D
          • load and position a 3D model
          • load and apply a GLSL shader
        """


        ShowBase.__init__(self)
        # Call the ShowBase constructor.
        #
        # This step is REQUIRED.
        # Without it, Panda3D would NOT:
        #   • create a window
        #   • initialize OpenGL
        #   • create the scene graph
        #   • set up the camera
        #   • prepare asset loading
        #
        # Think of this as "booting" the engine.


        FreeFlyCamera(self)


        self.model = self.loader.load_model('models/teapot')
        # Load a 3D model from disk.
        #
        # 'self.loader' is provided by ShowBase.
        # It searches Panda3D’s model path for:
        #     models/teapot.*
        #
        # The returned object is a NodePath,
        # which represents a node in the scene graph.
        #
        # At this point, the model exists in memory,
        # but it is NOT visible yet.


        self.model.setPos(0, 10, -2)
        # Position the model in 3D space.
        #
        # setPos(x, y, z):
        #   x → left / right
        #   y → forward / backward
        #   z → up / down
        #
        # Panda3D’s default camera looks toward +Y.
        # Moving the model to y = 10 places it
        # in front of the camera.
        #
        # z = -2 lowers the model slightly.


        self.model.setHpr(45, 45, 0)
        # Rotate the model using HPR (Heading, Pitch, Roll).
        #
        # setHpr(h, p, r):
        #   h (heading) → rotation around Z axis (yaw)
        #   p (pitch)   → rotation around X axis
        #   r (roll)    → rotation around Y axis
        #
        # This rotates the teapot so:
        #   • it is turned sideways (heading)
        #   • tilted upward (pitch)
        #
        # Rotation helps demonstrate lighting effects.


        self.model.reparentTo(self.render)
        # Attach the model to the scene graph.
        #
        # 'self.render' is the root node of the 3D world.
        #
        # IMPORTANT:
        #   Objects are NOT rendered unless they are
        #   attached somewhere under self.render.
        #
        # This step makes the model visible.


        self.shader = Shader.load(
            Shader.SL_GLSL,
            'Lambert-Diffuse-Lighting.vert',
            'Lambert-Diffuse-Lighting.frag'
        )
        """
        Load a GLSL shader program.

        Shader.load arguments:
          • Shader.SL_GLSL
                tells Panda3D this is a GLSL shader

          • 'Lambert-Diffuse-Lighting.vert'
                vertex shader file

          • 'Lambert-Diffuse-Lighting.frag'
                fragment shader file

        Panda3D will:
          • compile the vertex shader
          • compile the fragment shader
          • link them into a GPU program
          • report errors if compilation fails

        The resulting Shader object represents
        a complete GPU shading program.
        """


        self.model.setShader(self.shader)
        # Apply the shader to the model.
        #
        # From this point on:
        #   • Panda3D uses your vertex shader
        #   • Panda3D uses your fragment shader
        #
        # The built-in fixed-function lighting
        # is completely bypassed.
        #
        # This allows full control over lighting,
        # shading, and rendering behavior.


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
        light_dir = Vec3(
            cos(self.light_angle),
            0.0,
            sin(self.light_angle)
        )

        self.model.setShaderInput("light_direction", light_dir)
        # Pass the new light direction to the shader.
        # "light_direction" is the name of the uniform in the GLSL shader.
        # The shader will use this updated value for its lighting calculations in the next frame.

        return task.cont
        # Tell the task manager to continue calling this task in the next frame.


app = App()
# Create an instance of the App class.
#
# This immediately:
#   • opens the window
#   • initializes Panda3D
#   • loads the model
#   • applies the shader


app.run()
# Start Panda3D’s main loop.
#
# This loop:
#   • processes input
#   • updates tasks
#   • redraws the scene every frame
#
# The application continues running
# until the window is closed.
