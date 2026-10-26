from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    AmbientLight,
    DirectionalLight,
    SamplerState,
    Shader,
    TextureStage,
    Vec2,
    Vec3,
    Vec4,
    ClipPlaneAttrib,
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    GraphicsOutput,
    Material,
    Plane,
    PlaneNode,
    Texture,
)


# Classes
# =======
class WaterPlane(object):
    water_shader = Shader.load(
        Shader.SL_GLSL,
        "LegacyTerrain-SoftEdges-Rendering-Water.vert",
        "LegacyTerrain-SoftEdges-Rendering-Water.frag"
    )
    water_mat = None
    plane_mesh = None

    def __init__(self, pos=Vec3(), heading=0, scale=Vec3(1, 1, 1)):
        # Initialize water material if necessary
        if self.water_mat is None:
            WaterPlane.water_mat = Material()
            self.water_mat.set_ambient(Vec4(1, 1, 1, 1))
            self.water_mat.set_diffuse(Vec4(.8, .8, .8, 1))
            self.water_mat.set_specular(Vec3(.5, .5, .5))
            self.water_mat.set_shininess(32)

        # Get the default camera lens
        cam_lens = base.cam.node().get_lens()

        # Create refraction buffer. Using (0, 0) for the size indicates that the size of the buffer should
        # be synced with the main window.
        self.refract_buf = base.win.make_texture_buffer("WaterRefractionBuffer", 0, 0)
        self.refract_buf.set_sort(-100)
        self.refract_buf.add_render_texture(
            Texture("RefractionDepth"),
            GraphicsOutput.RTM_bind_or_copy,
            GraphicsOutput.RTP_depth
        )
        self.refract_tex = self.refract_buf.get_texture()
        self.refract_depth_tex = self.refract_buf.get_texture(1)
        self.refract_tex.wrap_u = SamplerState.WM_repeat
        self.refract_tex.wrap_v = SamplerState.WM_repeat
        
        self.refract_cam = base.make_camera(self.refract_buf, lens=cam_lens)
        self.refract_cam.reparent_to(base.render)

        # Create reflection buffer. Using (0, 0) for the size indicates that the size of the buffer should
        # be synced with the main window.
        self.reflect_buf = base.win.make_texture_buffer("WaterReflectionBuffer", 0, 0)
        self.reflect_buf.set_sort(-100)
        self.reflect_tex = self.reflect_buf.get_texture()
        self.reflect_tex.wrap_u = SamplerState.WM_repeat
        self.reflect_tex.wrap_v = SamplerState.WM_repeat
        
        self.reflect_cam = base.make_camera(self.reflect_buf, lens=cam_lens)
        self.reflect_cam.reparent_to(base.render)

        # Register water camera update task
        base.task_mgr.add(self.update_cameras, "update_water_cameras")

        # Initialize plane mesh if necessary
        if self.plane_mesh is None:
            # Get V3N3T2 format
            vtx_format = GeomVertexFormat.get_v3()

            # Allocate vertex data
            vertices = GeomVertexData("WaterPlane", vtx_format, Geom.UH_static)
            vertices.reserve_num_rows(4)

            # Write vertex data
            vertex = GeomVertexWriter(vertices, "vertex")
            vertex.add_data3(-1, 1, 0)
            vertex.add_data3(1, 1, 0)
            vertex.add_data3(-1, -1, 0)
            vertex.add_data3(1, -1, 0)

            # Allocate primitive data
            triangles = GeomTriangles(Geom.UH_static)
            triangles.reserve_num_vertices(6)

            # Write primitive data
            triangles.add_vertices(0, 2, 1)
            triangles.add_vertices(1, 2, 3)

            # Create plane mesh
            WaterPlane.plane_mesh = Geom(vertices)
            self.plane_mesh.add_primitive(triangles)

        # Load textures
        self.dudv_map_tex = base.loader.load_texture("models/maps/WaterDUDV.png")
        self.dudv_map_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.dudv_map_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        self.normal_map_tex = base.loader.load_texture("models/maps/WaterNormal.png")
        self.normal_map_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.normal_map_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        # Create water plane
        self.plane = base.render.attach_new_node(GeomNode("WaterPlane"))
        self.plane.node().add_geom(self.plane_mesh)
        self.plane.set_pos(pos)
        self.plane.set_h(heading)
        self.plane.set_scale(scale)

        self.plane.set_shader(self.water_shader)
        self.plane.set_shader_input("waveSpeed", .01)
        self.plane.set_shader_input("near", cam_lens.get_near())
        self.plane.set_shader_input("far", cam_lens.get_far())

        stage1 = TextureStage("ReflectionTex")
        stage2 = TextureStage("DUDVMap")
        stage3 = TextureStage("NormalMap")
        stage4 = TextureStage("RefractionDepth")

        self.plane.set_texture(self.refract_tex)
        self.plane.set_texture(stage1, self.reflect_tex)
        self.plane.set_texture(stage2, self.dudv_map_tex)
        self.plane.set_texture(stage3, self.normal_map_tex)
        self.plane.set_texture(stage4, self.refract_depth_tex)

        self.plane.set_material(self.water_mat)

        # Configure refraction clipping plane
        self.refract_clip_plane = self.plane.attach_new_node(PlaneNode(
            "WaterRefractClipPlane",
            Plane(0, 0, -1, -.001)
        ))
        clip_state = ClipPlaneAttrib.make_default().add_on_plane(self.refract_clip_plane)
        self.refract_cam.node().set_initial_state(clip_state)

        # Configure reflection clipping plane
        self.reflect_clip_plane = self.plane.attach_new_node(PlaneNode(
            "WaterReflectClipPlane",
            Plane(0, 0, 1, -.001)
        ))
        clip_state = ClipPlaneAttrib.make_default().add_on_plane(self.reflect_clip_plane)
        self.reflect_cam.node().set_initial_state(clip_state)

    def update_cameras(self, task):
        # Update refraction and reflection cameras
        self.refract_cam.set_transform(base.camera.get_transform())

        self.reflect_cam.set_transform(base.camera.get_transform())
        cam_height = base.camera.get_z()
        dist = cam_height - self.plane.get_z()
        self.reflect_cam.set_z(self.reflect_cam.get_z() - dist * 2)
        self.reflect_cam.set_p(-self.reflect_cam.get_p())
        self.reflect_cam.set_r(self.reflect_cam.get_r() + 180)

        # Update window size uniform
        self.plane.set_shader_input("winSize", base.win.get_size())
        return task.cont


# Application Class
# =================
class TerrainDemo(ShowBase):
    def __init__(self):
        # Call base constructor
        ShowBase.__init__(self)

        # Enable auto shaders
        self.render.set_shader_auto()

        # Setup lighting
        self.ambient_light = self.render.attach_new_node(AmbientLight("AmbientLight"))
        self.ambient_light.node().set_color(Vec4(.2, .2, .2, 1))
        self.render.set_light(self.ambient_light)

        self.sun = self.render.attach_new_node(DirectionalLight("Sun"))
        self.sun.set_hpr(45, -45, 0)
        self.render.set_light(self.sun)

        # Load shaders
        self.terrain_shader = Shader.load(
            Shader.SL_GLSL,
            "LegacyTerrain-SoftEdges-Rendering.vert",
            "LegacyTerrain-SoftEdges-Rendering.frag"
        )

        # Load textures
        self.grass_tex = self.loader.load_texture("models/maps/Grass.png")
        self.grass_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.grass_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        self.dirt_tex = self.loader.load_texture("models/maps/Dirt.png")
        self.dirt_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.dirt_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        self.rock_tex = self.loader.load_texture("models/maps/Rock.png")
        self.rock_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.rock_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        self.blank_tex = self.loader.load_texture("models/maps/Blank.png")
        self.blank_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.blank_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        self.color_mask_tex = self.loader.load_texture("models/maps/ColorMask.png")
        self.color_mask_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.color_mask_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        # Load terrain
        self.terrain = self.loader.load_model("models/Terrain")
        self.terrain.set_scale(256, 256, 256)
        self.terrain.set_pos(0, 261, 0)

        self.terrain.set_shader(self.terrain_shader)
        self.terrain.set_shader_input("texScale0", Vec2(.1, .1))
        self.terrain.set_shader_input("texScale1", Vec2(.1, .1))
        self.terrain.set_shader_input("texScale2", Vec2(.1, .1))
        self.terrain.set_shader_input("texScale3", Vec2(.1, .1))

        stage1 = TextureStage("Dirt")
        stage2 = TextureStage("Rock")
        stage3 = TextureStage("Blank")
        stage4 = TextureStage("ColorMask")

        self.terrain.set_texture(self.grass_tex)
        self.terrain.set_texture(stage1, self.dirt_tex)
        self.terrain.set_texture(stage2, self.rock_tex)
        self.terrain.set_texture(stage3, self.blank_tex)
        self.terrain.set_texture(stage4, self.color_mask_tex)

        self.terrain.reparent_to(self.render)

        # Load water plane
        self.water = WaterPlane(
            Vec3(0, 261, -20),
            scale=Vec3(256, 256, 1)
        )

        # Configure buffer viewer
        self.bufferViewer.setPosition("ulcorner")
        self.bufferViewer.setCardSize(.5, 0)
        self.accept("v", self.bufferViewer.toggleEnable)


# Entry Point
# ===========
if __name__ == "__main__":
    TerrainDemo().run()
