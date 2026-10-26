from direct.showbase.ShowBase import ShowBase
# Import the ShowBase class from Panda3D.
# ShowBase is the base application class that:
#   • opens a window
#   • sets up rendering
#   • creates the scene graph
#   • provides input handling
# All Panda3D programs inherit from this class.

from panda3d.core import Shader
# Import Panda3D's Shader class.
# This lets us load GLSL shaders and apply them to models.


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
    Define a new application class called App.
    It inherits from ShowBase, meaning:
        • App becomes a full Panda3D application
        • the constructor (App.__init__) will initialize the engine
    """


    def __init__(self):
        """
        Constructor for the App class.
        Runs automatically when App() is created.
        Sets up the 3D scene, loads the teapot model,
        and applies the GLSL shaders.
        """


        ShowBase.__init__(self)
        # Call the parent class (ShowBase) constructor manually.
        # This step is required — without it, Panda3D will not:
        #   • open a window
        #   • set up the rendering system
        #   • create the scene graph (self.render)
        #   • provide loader, camera, tasks, and input


        FreeFlyCamera(self)
        # Attach a free-fly camera to the application.
        # Replaces Panda3D’s default mouse camera control.
        # Enables movement and mouse-look controls as defined in FreeFlyCamera.


        model = self.loader.load_model('models/teapot')
        # Load a 3D model from Panda3D's model path.
        # "self.loader" is provided by ShowBase.
        # The returned object is a NodePath representing the teapot.


        model.setPos(0, 10, -2)
        # Position the model at (x=0, y=10, z=-2).
        #   x → left/right
        #   y → forward/backward (positive Y goes away from the camera)
        #   z → up/down
        # This places the teapot slightly below the center and 10 units forward.


        model.reparentTo(self.render)
        # Attach the teapot to the render scene graph.
        # A model is not visible until it has a parent node.
        # "self.render" is the root node for everything drawn in 3D.


        shader = Shader.load(
            Shader.SL_GLSL,
            'Minimal-PassThrough-Shader.vert',
            'Minimal-PassThrough-Shader.frag'
        )
        """
        Load a pair of GLSL shaders: vertex + fragment.

        Shader.load arguments:
            • Shader.SL_GLSL
                tells Panda3D we are using GLSL shaders
            • 'Minimal-PassThrough-Shader.vert'
                the vertex shader file
            • 'Minimal-PassThrough-Shader.frag'
                the fragment shader file

        Panda3D will:
            • compile the shaders
            • link them into one GPU program
            • report errors if any line is invalid
        The resulting Shader object is stored in 'shader'.
        """


        model.setShader(shader)
        # Apply the loaded shader to the model.
        # From this point on, the teapot is rendered using:
        #   • the custom vertex shader
        #   • the custom fragment shader
        # instead of Panda3D's default fixed-function shading.


app = App()
# Create an instance of the App class.
# This initializes everything inside App.__init__().


app.run()
# Enter Panda3D's main event loop.
# This loop:
#   • renders each frame
#   • handles input
#   • updates tasks
#   • keeps the window responsive
# The program runs until the window is closed.
