from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    load_prc_file,
    SamplerState,
    Vec2,
    Vec4,
    DepthTestAttrib,
    OmniBoundingVolume,
    Shader,
    TextureStage,
)


# Classes
# =======
class SkyDome(object):
    sky_shader = Shader.load(
        Shader.SL_GLSL,
        "ShadelessSky-DynamicSkydome-Rendering.vert",
        "ShadelessSky-DynamicSkydome-Rendering.frag"
    )

    def __init__(self, horizon, zenith, cloud_tex, celestials_tex):
        # Set background color
        base.win.set_clear_color(horizon)

        # Load skydome mesh
        self.skydome = base.loader.load_model("models/DynamicSkyDome.gltf")
        self.skydome.find("**/DynamicSkyDome").node().set_bounds(OmniBoundingVolume())
        self.skydome.set_shader(self.sky_shader)
        self.set_horizon_color(horizon)
        self.set_zenith_color(zenith)
        self.set_cloud_texture(cloud_tex)
        self.set_cloud_scroll_vec(Vec2(.01, 0))
        self.set_cloud_scale(Vec2(1, 1))
        self.set_celestial_texture(celestials_tex)
        self.set_celestial_scroll_vec(Vec2(.001, 0))
        self.skydome.set_attrib(DepthTestAttrib.make(DepthTestAttrib.M_less_equal))
        self.skydome.reparent_to(base.render)

    def set_horizon_color(self, color):
        self.skydome.set_shader_input("horizonColor", color)

    def set_zenith_color(self, color):
        self.skydome.set_shader_input("zenithColor", color)

    def set_cloud_texture(self, tex):
        stage1 = TextureStage("Clouds")
        stage1.set_sort(1)
        self.skydome.set_texture(stage1, tex)

    def set_cloud_scroll_vec(self, vec):
        self.skydome.set_shader_input("cloudScrollVec", vec)

    def set_cloud_scale(self, scale):
        self.skydome.set_shader_input("cloudScale", scale)

    def set_celestial_texture(self, tex):
        stage2 = TextureStage("Celestials")
        stage2.set_sort(2)
        self.skydome.set_texture(stage2, tex)

    def set_celestial_scroll_vec(self, vec):
        self.skydome.set_shader_input("celestialScrollVec", vec)


# Classes
# =======
class SkyDemo(ShowBase):
    def __init__(self):
        # Load config file
        load_prc_file("settings.prc")

        # Call the base constructor
        ShowBase.__init__(self)

        # Load textures
        self.cloud_tex = self.loader.load_texture("models/maps/Clouds.png")
        self.cloud_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.cloud_tex.magfilter = SamplerState.FT_linear_mipmap_linear
        self.cloud_tex.wrap_u = SamplerState.WM_repeat
        self.cloud_tex.wrap_v = SamplerState.WM_repeat

        self.celestials_tex = self.loader.load_texture("models/maps/Celestials.png")
        self.celestials_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.celestials_tex.magfilter = SamplerState.FT_linear_mipmap_linear
        self.celestials_tex.wrap_u = SamplerState.WM_repeat
        self.celestials_tex.wrap_v = SamplerState.WM_repeat

        # Create skydome
        self.skydome = SkyDome(
            Vec4(1, .5, .1, 1),
            Vec4(0, .61, 1, 1),
            self.cloud_tex,
            self.celestials_tex
        )
        self.skydome.set_cloud_scale(Vec2(.5, .5))


# Entry Point
if __name__ == "__main__":
    SkyDemo().run()
