from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    load_prc_file,
    Vec4,
    DepthTestAttrib,
    OmniBoundingVolume,
    Shader
)


# Classes
# =======
class SkyDome(object):
    sky_shader = Shader.load(
        Shader.SL_GLSL,
        "ShadelessSky-StaticSkydome-Rendering.vert",
        "ShadelessSky-StaticSkydome-Rendering.frag"
    )

    def __init__(self, horizon):
        # Set background color
        base.win.set_clear_color(pow(horizon, 2.2 / 1))

        # Load skydome mesh
        self.skydome = base.loader.load_model("models/SkyDome.gltf")
        self.skydome.find("**/SkyDome").node().set_bounds(OmniBoundingVolume())
        self.skydome.set_shader(self.sky_shader)
        self.skydome.set_attrib(DepthTestAttrib.make(DepthTestAttrib.M_less_equal))
        self.skydome.reparent_to(base.render)


# Classes
# =======
class SkyDemo(ShowBase):
    def __init__(self):
        # Load config file
        load_prc_file("settings.prc")

        # Call the base constructor
        ShowBase.__init__(self)

        # Create skydome
        self.skydome = SkyDome(Vec4(0, .61, 1, 1))


# Entry Point
if __name__ == "__main__":
    SkyDemo().run()
