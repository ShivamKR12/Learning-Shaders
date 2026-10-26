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


from cam import FreeFlyCamera
# Import a custom free-fly camera class.
# Provides Blender-style camera controls:
#     • W/S: move forward/backward
#     • A/D: move left/right
#     • Q/E: move down/up
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
        It sets up the 3D scene, camera, model, and normal-pulse deformation shader.
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


        model = self.loader.load_model('models/smiley')
        # Load a 3D model from disk.
        # 'self.loader' is provided by ShowBase.
        # Searches Panda3D's model-path for "models/smiley.*"
        # Returns a NodePath, stored in the variable 'model'.


        model.setPos(0, 10, 0)
        # Move the model in the 3D world.
        # setPos(x, y, z):
        #     x = left/right
        #     y = forward/back (positive Y moves away from camera)
        #     z = up/down
        # Positions the smiley directly in front of the camera, 10 units away.


        model.setScale(2)
        # Scale the model uniformly by a factor of 2.
        # Makes the smiley appear larger in the scene.


        model.reparentTo(self.render)
        # Attach the model to the scene graph.
        # 'self.render' is the root node of the 3D world.
        # Nothing is visible until a model is parented somewhere in the scene graph.


        shader = Shader.load(
            Shader.SL_GLSL,
            'Minimal-NormalPulse-Deformation.vert',
            'Minimal-NormalPulse-Deformation.frag'
        )
        """
        Load the GLSL shader files for normal-pulse deformation.

        Shader.load parameters:
            - Shader.SL_GLSL:
                  instructs Panda3D to expect GLSL shaders
            - "Minimal-NormalPulse-Deformation.vert":
                  vertex shader file
            - "Minimal-NormalPulse-Deformation.frag":
                  fragment shader file

        Panda3D will:
            • compile both shaders
            • link them into a single GPU program
            • report errors if compilation/linking fails

        The resulting Shader object is stored in 'shader'.
        """


        model.setShader(shader)
        # Apply the loaded shader to the model.
        # Now, whenever this model is rendered, Panda3D will use:
        #     • Minimal-NormalPulse-Deformation.vert (vertex shader)
        #     • Minimal-NormalPulse-Deformation.frag (fragment shader)
        # This replaces the default fixed-function rendering with our animated normal-pulse deformation.


app = App()
# Create an instance of the App class.
# This triggers App.__init__(), setting up the window, camera, model, and shader.


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
