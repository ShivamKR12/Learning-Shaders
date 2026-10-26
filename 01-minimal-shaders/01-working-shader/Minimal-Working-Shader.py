from direct.showbase.ShowBase import ShowBase
# Import the ShowBase class from Panda3D.
# ShowBase is the main application class that sets up:
#     • the window
#     • the rendering engine
#     • the camera
#     • the scene graph
#     • input handling
# By inheriting from ShowBase, the program becomes a Panda3D app.


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
       • we have access to 'loader', 'render', camera, task manager, etc.
    """


    def __init__(self):
        """
        The class constructor.
        This method runs automatically when we create an instance of App.
        It sets up the 3D scene, loads the model, and applies the shader.
        """


        ShowBase.__init__(self)
        # Call the parent class (ShowBase) constructor.
        # This is required — without it, Panda3D would NOT:
        #     • open a window
        #     • create a scene graph
        #     • initialize rendering
        #     • set up the default camera
        #     • prepare the loader and input system


        FreeFlyCamera(self)
        # Attach a free-fly camera to the application.
        # Replaces Panda3D’s default mouse camera control.
        # Enables movement and mouse-look controls as defined in FreeFlyCamera.


        model = self.loader.load_model("models/teapot")
        # Load a 3D model from disk.
        # 'self.loader' is provided by ShowBase.
        # It searches Panda3D's model-path for "models/teapot.*".
        #
        # The returned object is a NodePath, stored in the variable 'model'.


        model.setPos(0, 10, -2)
        # Move the model in the 3D world.
        # setPos(x, y, z):
        #     x = left/right
        #     y = forward/backward (positive Y moves away from the camera)
        #     z = up/down
        #
        # This positions the teapot slightly below the center of the screen
        # and 10 units away from the camera.


        model.reparentTo(self.render)
        # Attach the model to the render scene graph.
        # 'self.render' is the root node of the 3D world.
        #
        # NOTHING is visible until a model is parented somewhere in the scene graph,
        # so this step is mandatory.


        shader = Shader.load(Shader.SL_GLSL,
                             "Minimal-Working-Shader.vert",
                             "Minimal-Working-Shader.frag")
        """
        Load the GLSL shader files.

        Shader.load parameters:
            - Shader.SL_GLSL
                  tells Panda3D to expect GLSL shaders

            - "Minimal-Working-Shader.vert"
                  the vertex shader filename

            - "Minimal-Working-Shader.frag"
                  the fragment shader filename

        Panda3D will:
            • compile both shaders
            • link them into a complete GPU program
            • report errors if something is wrong

        The resulting Shader object is stored in 'shader'.
        """


        model.setShader(shader)
        # Apply the loaded shader to the model.
        #
        # Now, whenever this model is rendered, Panda3D will use:
        #     • Minimal-Working-Shader.vert  (vertex shader)
        #     • Minimal-Working-Shader.frag (fragment shader)
        #
        # This replaces the engine’s default fixed-function lighting/shading.


app = App()
# Create an instance of the App class.
# This triggers App.__init__() and finishes setting up the scene.


app.run()
# Start Panda3D’s main loop.
#
# This loop:
#    • updates the window
#    • handles input
#    • updates tasks
#    • renders every frame
#
# The program continues running until the window is closed.
