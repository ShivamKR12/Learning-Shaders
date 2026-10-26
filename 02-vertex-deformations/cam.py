from panda3d.core import WindowProperties, Vec3, getModelPath
from direct.task import Task
import os
import sys

# Ensure current, parent, and models directories are searchable
_this_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_this_dir)

for _p in [_this_dir, _parent_dir]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    _mp = getModelPath()
    _mp.appendPath(".")
    _mp.appendPath("..")
    _mp.appendPath("models")
    _mp.appendPath("../models")
    _mp.appendPath(os.path.join(_parent_dir, "models"))
except Exception:
    pass


class FreeFlyCamera:
    """
    Blender-style free-fly camera for Panda3D.

    Controls:
      - W/S : forward / backward
      - A/D : left / right
      - Q/E : down / up
      - Hold RMB : mouse look
      - Esc : release mouse
    """

    def __init__(self, base, speed=10.0, mouse_sensitivity=0.2):
        self.base = base
        self.speed = speed
        self.mouse_sensitivity = mouse_sensitivity

        # Disable Panda3D's default mouse camera control
        base.disableMouse()

        # Movement state
        self.move = {
            "forward": 0,
            "right": 0,
            "up": 0,
        }

        # Mouse look state
        self.mouse_enabled = False
        self.last_mouse_pos = None

        # Key bindings
        self._bind_keys()

        # Add update task
        base.taskMgr.add(self._update, "FreeFlyCameraUpdate")

    # -------------------------------------------------

    def _bind_keys(self):
        b = self.base

        # Movement keys
        b.accept("w", self._set_move, ["forward", 1])
        b.accept("w-up", self._set_move, ["forward", 0])

        b.accept("s", self._set_move, ["forward", -1])
        b.accept("s-up", self._set_move, ["forward", 0])

        b.accept("a", self._set_move, ["right", -1])
        b.accept("a-up", self._set_move, ["right", 0])

        b.accept("d", self._set_move, ["right", 1])
        b.accept("d-up", self._set_move, ["right", 0])

        b.accept("q", self._set_move, ["up", 1])
        b.accept("q-up", self._set_move, ["up", 0])

        b.accept("e", self._set_move, ["up", -1])
        b.accept("e-up", self._set_move, ["up", 0])

        # Mouse look
        b.accept("mouse3", self._enable_mouse)      # RMB
        b.accept("mouse3-up", self._disable_mouse)

        # Escape releases mouse
        b.accept("escape", self._disable_mouse)

    # -------------------------------------------------

    def _set_move(self, axis, value):
        self.move[axis] = value

    # -------------------------------------------------

    def _enable_mouse(self):
        self.mouse_enabled = True
        self.last_mouse_pos = None

        props = WindowProperties()
        props.setCursorHidden(True)
        self.base.win.requestProperties(props)

    def _disable_mouse(self):
        self.mouse_enabled = False

        props = WindowProperties()
        props.setCursorHidden(False)
        self.base.win.requestProperties(props)

    # -------------------------------------------------

    def _update(self, task):
        dt = globalClock.getDt() # type: ignore

        cam = self.base.camera

        # -------- Movement --------
        direction = Vec3(
            self.move["right"],
            self.move["forward"],
            self.move["up"]
        )

        if direction.lengthSquared() > 0:
            direction.normalize()
            cam.setPos(cam, direction * self.speed * dt)

        # -------- Mouse Look --------
        if self.mouse_enabled and self.base.mouseWatcherNode.hasMouse():
            mw = self.base.mouseWatcherNode
            win = self.base.win

            # Mouse position relative to center (-1 .. +1)
            mx = mw.getMouseX()
            my = mw.getMouseY()

            sensitivity = 600 * self.mouse_sensitivity

            h = cam.getH() - mx * sensitivity
            p = cam.getP() + my * sensitivity
            p = max(-89, min(89, p))

            cam.setHpr(h, p, 0)

            # IMPORTANT: re-center mouse every frame
            win.movePointer(
                0,
                win.getXSize() // 2,
                win.getYSize() // 2
            )

        return Task.cont
