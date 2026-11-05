"""Still potret GLD utuh untuk banner/brosur: memakai adegan shot_gld_core, kamera diganti statis 3/4 depan.
blender -b --factory-startup -P still_gld_hero.py -- --orient portrait --out <png> --still 20 --pct 200
"""
import runpy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy  # noqa: E402
import ht  # noqa: E402

_render = ht.render
CAM = (0.52, -0.95, 0.30)
TGT = (0.02, 0.0, 0.07)


def render():
    sc = bpy.context.scene
    cam = sc.camera
    cam.animation_data_clear()
    cam.location = CAM
    for c in cam.constraints:
        if getattr(c, "target", None) is not None:
            c.target.animation_data_clear()
            c.target.location = TGT
    cam.data.lens = float(__import__("os").environ.get("HERO_LENS", "52"))
    _render()


ht.render = render
runpy.run_path(str(Path(__file__).resolve().parent / "shot_gld_core.py"), run_name="__main__")
