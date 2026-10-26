from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    DepthTestAttrib,
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    OmniBoundingVolume,
    Shader,
    SamplerState
)


# Classes
# =======
class SkyBox(object):
    skybox_shader = Shader.load(
        Shader.SL_GLSL,
        "ShadelessSky-StaticSkybox-Rendering.vert",
        "ShadelessSky-StaticSkybox-Rendering.frag"
    )
    skybox_mesh = None

    def __init__(self, texture):
        # Create skybox mesh
        if self.skybox_mesh is None:
            # Get vertex format
            vtx_format = GeomVertexFormat.get_v3()

            # Allocate vertex data
            vertices = GeomVertexData("Skybox", vtx_format, Geom.UH_static)
            vertices.reserve_num_rows(8)

            # Write vertex data
            vertex = GeomVertexWriter(vertices, "vertex")

            vertex.add_data3(-1, -1, -1)
            vertex.add_data3(1, -1, -1)
            vertex.add_data3(-1, 1, -1)
            vertex.add_data3(1, 1, -1)
            vertex.add_data3(-1, -1, 1)
            vertex.add_data3(1, -1, 1)
            vertex.add_data3(-1, 1, 1)
            vertex.add_data3(1, 1, 1)

            # Allocate primitive data
            triangles = GeomTriangles(Geom.UH_static)
            triangles.reserve_num_vertices(12)

            # Write primitive data
            triangles.add_vertices(4, 5, 1)
            triangles.add_vertices(1, 0, 4)
            triangles.add_vertices(2, 3, 7)
            triangles.add_vertices(7, 6, 2)
            triangles.add_vertices(2, 6, 4)
            triangles.add_vertices(4, 0, 2)
            triangles.add_vertices(1, 5, 7)
            triangles.add_vertices(7, 3, 1)
            triangles.add_vertices(4, 6, 7)
            triangles.add_vertices(7, 5, 4)
            triangles.add_vertices(0, 1, 3)
            triangles.add_vertices(3, 2, 0)

            # Create skybox mesh
            SkyBox.skybox_mesh = Geom(vertices)
            self.skybox_mesh.add_primitive(triangles)

        # Create skybox
        self.skybox = base.render.attach_new_node(GeomNode("Skybox"))
        self.skybox.node().add_geom(self.skybox_mesh)
        self.skybox.node().set_bounds(OmniBoundingVolume())
        self.skybox.set_shader(self.skybox_shader)
        self.skybox.set_texture(texture)
        depth_test_attrib = DepthTestAttrib.make(DepthTestAttrib.M_less_equal)
        self.skybox.set_attrib(depth_test_attrib)


# Classes
# =======
class SkyDemo(ShowBase):
    def __init__(self):
        # Call the base constructor
        ShowBase.__init__(self)

        # Load cubemap sky texture
        self.sky_tex = self.loader.load_cube_map("models/maps/TestSky-#.png")
        self.sky_tex.minfilter = SamplerState.FT_linear_mipmap_linear
        self.sky_tex.magfilter = SamplerState.FT_linear_mipmap_linear

        # Create sky
        self.sky = SkyBox(self.sky_tex)


# Entry Point
if __name__ == "__main__":
    SkyDemo().run()
