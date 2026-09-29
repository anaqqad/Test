"""History-documentary globe shot, built entirely from code: the Mongol Empire spreading from Karakorum, 1206-1279.

  blender -b --factory-startup -P globe_mongols.py -- [--preview] [--still 1,60,120] [--frames 1-192] [--engine EEVEE|CYCLES] [--gpu] [--out file.mp4]

Output goes to blender/out/ by default. --preview renders at 50% size; --still renders only those frames as PNGs.

Needs assets/globe_plain.png (map), assets/globe_mask.png (empire extent, white on black), assets/Cinzel.ttf
(regenerate the textures for another empire with globe_tex.mjs).
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default


PREVIEW = "--preview" in argv
ENGINE = arg("--engine", "CYCLES").upper()  # CYCLES: fastest on CPU; with --gpu, uses NVIDIA OptiX
F0, F1 = (int(x) for x in arg("--frames", "1-192").split("-"))
OUT = os.path.abspath(arg("--out", os.path.join(HERE, "out", "globe_preview.mp4" if PREVIEW else "globe_mongols.mp4")))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
FPS = 24

KARAKORUM = (102.8, 47.2)  # lon, lat
C = {"red": (0.702, 0.149, 0.118), "gold": (1.0, 0.82, 0.40), "cream": (1.0, 0.96, 0.86),
     "space": (0.020, 0.043, 0.075), "atmo": (0.55, 0.80, 1.0)}


def srgb(c):  # sRGB -> linear, so colours match the 2D artwork exactly
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c) + (1.0,)


def unit(lon, lat):
    lo, la = math.radians(lon), math.radians(lat)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def key(obj_or_socket, path, frame, value, interp="BEZIER"):
    setattr(obj_or_socket, path, value)
    obj_or_socket.keyframe_insert(path, frame=frame)


# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.frame_start, sc.frame_end, sc.render.fps = F0, F1, FPS
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.resolution_percentage = 50 if PREVIEW else 100
sc.view_settings.view_transform = "Standard"
if ENGINE == "CYCLES":
    sc.render.engine = "CYCLES"
    # the scene is unlit (emission only), so samples only anti-alias edges: few are enough
    sc.cycles.samples = int(arg("--samples", 4 if PREVIEW else 8))
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 1
    sc.cycles.transparent_max_bounces = 6
    sc.render.use_persistent_data = True
    sc.cycles.device = "CPU"
    if "--gpu" in argv:  # NVIDIA card (e.g. RTX 3090 Ti): OptiX ray tracing + OptiX denoiser
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "OPTIX"
        prefs.get_devices()
        for d in prefs.devices:
            d.use = d.type == "OPTIX"
        sc.cycles.device = "GPU"
        sc.cycles.denoiser = "OPTIX"
        print("GPU devices:", [d.name for d in prefs.devices if d.use])
else:  # EEVEE uses the graphics card automatically when one is present
    sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.eevee.taa_render_samples = 8 if PREVIEW else 32

# world: deep navy space with faint stars
world = bpy.data.worlds.new("space"); sc.world = world; world.use_nodes = True
wn, wl = world.node_tree.nodes, world.node_tree.links
wn.clear()
tc = wn.new("ShaderNodeTexCoord"); vor = wn.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 260
ramp = wn.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
ramp.color_ramp.elements[1].position = 0.05; ramp.color_ramp.elements[1].color = srgb(C["space"])
bg = wn.new("ShaderNodeBackground"); out = wn.new("ShaderNodeOutputWorld")
wl.new(tc.outputs["Window"], vor.inputs["Vector"]); wl.new(vor.outputs["Distance"], ramp.inputs["Fac"])
wl.new(ramp.outputs["Color"], bg.inputs["Color"]); wl.new(bg.outputs["Background"], out.inputs["Surface"])

# ------------------------------------------------------------------ globe material (unlit map + limb shading)
bpy.ops.mesh.primitive_uv_sphere_add(segments=256, ring_count=128, radius=1.0)
globe = bpy.context.object; globe.name = "Globe"
bpy.ops.object.shade_smooth()
mat = bpy.data.materials.new("globe"); mat.use_nodes = True; globe.data.materials.append(mat)
N, L = mat.node_tree.nodes, mat.node_tree.links
N.clear()


def node(t, **inputs):
    n = N.new(t)
    for k, v in inputs.items():
        if k.startswith("_"):
            setattr(n, k[1:], v)
        else:
            n.inputs[k].default_value = v
    return n


def math_node(op, a=None, b=None):
    n = node("ShaderNodeMath", _operation=op)
    for i, v in enumerate((a, b)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            n.inputs[i].default_value = v
        else:
            L.new(v, n.inputs[i])
    return n.outputs[0]


tco = node("ShaderNodeTexCoord")
norm = node("ShaderNodeVectorMath", _operation="NORMALIZE"); L.new(tco.outputs["Object"], norm.inputs[0])
sep = node("ShaderNodeSeparateXYZ"); L.new(norm.outputs["Vector"], sep.inputs[0])
lon = math_node("ARCTAN2", sep.outputs["Y"], sep.outputs["X"])
lat = math_node("ARCSINE", sep.outputs["Z"])
u = math_node("ADD", math_node("DIVIDE", lon, 2 * math.pi), 0.5)
v = math_node("ADD", math_node("DIVIDE", lat, math.pi), 0.5)
uv = node("ShaderNodeCombineXYZ"); L.new(u, uv.inputs["X"]); L.new(v, uv.inputs["Y"])
tex = node("ShaderNodeTexImage", _interpolation="Cubic"); tex.image = bpy.data.images.load(os.path.join(ASSETS, "globe_plain.png"))
msk = node("ShaderNodeTexImage", _interpolation="Linear"); msk.image = bpy.data.images.load(os.path.join(ASSETS, "globe_mask.png"))
msk.image.colorspace_settings.name = "Non-Color"
L.new(uv.outputs[0], tex.inputs["Vector"]); L.new(uv.outputs[0], msk.inputs["Vector"])

# empire reveal: every point whose angular distance to Karakorum < R(t) turns red; a gold front line rides the edge
kvec = node("ShaderNodeCombineXYZ", X=unit(*KARAKORUM)[0], Y=unit(*KARAKORUM)[1], Z=unit(*KARAKORUM)[2])
dot = node("ShaderNodeVectorMath", _operation="DOT_PRODUCT"); L.new(norm.outputs["Vector"], dot.inputs[0]); L.new(kvec.outputs[0], dot.inputs[1])
radius = node("ShaderNodeValue"); radius.name = "reveal"
ang = math_node("ARCCOSINE", math_node("MINIMUM", dot.outputs["Value"], 1.0))  # angular distance to Karakorum
edge_w = 0.022  # radians
r_plus = math_node("ADD", radius.outputs[0], edge_w)
r_minus = math_node("SUBTRACT", radius.outputs[0], edge_w)
inside = node("ShaderNodeMapRange", _clamp=True); L.new(ang, inside.inputs["Value"])  # 1 inside R, 0 beyond R+w
L.new(r_plus, inside.inputs["From Min"]); L.new(radius.outputs[0], inside.inputs["From Max"])
deep = node("ShaderNodeMapRange", _clamp=True); L.new(ang, deep.inputs["Value"])  # 1 inside R-w
L.new(radius.outputs[0], deep.inputs["From Min"]); L.new(r_minus, deep.inputs["From Max"])
front = math_node("SUBTRACT", inside.outputs["Result"], deep.outputs["Result"])
m = msk.outputs["Color"]
emp = math_node("MULTIPLY", inside.outputs["Result"], m)
frn = math_node("MULTIPLY", math_node("MULTIPLY", front, m), 1.6)

mix1 = node("ShaderNodeMix", _data_type="RGBA"); L.new(emp, mix1.inputs["Factor"]); L.new(tex.outputs["Color"], mix1.inputs[6])
mix1.inputs[7].default_value = srgb(C["red"])
mix2 = node("ShaderNodeMix", _data_type="RGBA"); L.new(math_node("MINIMUM", frn, 1.0), mix2.inputs["Factor"])
L.new(mix1.outputs[2], mix2.inputs[6]); mix2.inputs[7].default_value = srgb(C["gold"])

lw = node("ShaderNodeLayerWeight", Blend=0.5)
shade = math_node("SUBTRACT", 1.0, math_node("MULTIPLY", math_node("POWER", lw.outputs["Facing"], 1.6), 0.75))
mul = node("ShaderNodeMix", _data_type="RGBA", _blend_type="MULTIPLY", Factor=1.0)
L.new(mix2.outputs[2], mul.inputs[6]); sh = node("ShaderNodeCombineColor"); L.new(shade, sh.inputs[0]); L.new(shade, sh.inputs[1]); L.new(shade, sh.inputs[2])
L.new(sh.outputs[0], mul.inputs[7])
em = node("ShaderNodeEmission", Strength=1.0); L.new(mul.outputs[2], em.inputs["Color"])
mo = node("ShaderNodeOutputMaterial"); L.new(em.outputs[0], mo.inputs["Surface"])

# atmosphere rim
bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=1.03)
atm = bpy.context.object; bpy.ops.object.shade_smooth()
am = bpy.data.materials.new("atmo"); am.use_nodes = True; atm.data.materials.append(am)
if hasattr(am, "surface_render_method"):
    am.surface_render_method = "BLENDED"
an, al = am.node_tree.nodes, am.node_tree.links
an.clear()
alw = an.new("ShaderNodeLayerWeight"); alw.inputs["Blend"].default_value = 0.35
apw = an.new("ShaderNodeMath"); apw.operation = "POWER"; apw.inputs[1].default_value = 2.2
aem = an.new("ShaderNodeEmission"); aem.inputs["Color"].default_value = srgb(C["atmo"]); aem.inputs["Strength"].default_value = 1.4
atr = an.new("ShaderNodeBsdfTransparent"); amx = an.new("ShaderNodeMixShader"); aout = an.new("ShaderNodeOutputMaterial")
al.new(alw.outputs["Facing"], apw.inputs[0]); al.new(apw.outputs[0], amx.inputs["Fac"])
al.new(atr.outputs[0], amx.inputs[1]); al.new(aem.outputs[0], amx.inputs[2]); al.new(amx.outputs[0], aout.inputs["Surface"])

# Karakorum marker (parented to the globe so it turns with it)
kx, ky, kz = unit(*KARAKORUM)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.018, location=(kx * 1.002, ky * 1.002, kz * 1.002))
pin = bpy.context.object; pin.parent = globe
pm = bpy.data.materials.new("pin"); pm.use_nodes = True; pin.data.materials.append(pm)
pe = pm.node_tree.nodes.new("ShaderNodeEmission"); pe.inputs["Color"].default_value = srgb(C["gold"]); pe.inputs["Strength"].default_value = 3
pm.node_tree.links.new(pe.outputs[0], pm.node_tree.nodes["Material Output"].inputs["Surface"])

# ------------------------------------------------------------------ camera + animation
cam_data = bpy.data.cameras.new("cam"); cam_data.lens = 35
cam = bpy.data.objects.new("cam", cam_data); sc.collection.objects.link(cam); sc.camera = cam
target = bpy.data.objects.new("target", None); sc.collection.objects.link(target)
tr = cam.constraints.new("TRACK_TO"); tr.target = target; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"


def cam_at(frame, dist, lat_deg):
    la = math.radians(lat_deg)
    key(cam, "location", frame, (0.0, -dist * math.cos(la), dist * math.sin(la)))


def face_lon(frame, lon_deg):  # rotate the globe so this longitude faces the camera (camera sits on -Y)
    key(globe, "rotation_euler", frame, (0.0, 0.0, math.radians(-90 - lon_deg)))


face_lon(1, 15); cam_at(1, 4.6, 30)
face_lon(70, 88); cam_at(70, 3.2, 40)
face_lon(192, 80); cam_at(192, 2.75, 40)

key(pin, "scale", 1, (0, 0, 0)); key(pin, "scale", 34, (0, 0, 0)); key(pin, "scale", 44, (1.4, 1.4, 1.4)); key(pin, "scale", 50, (1, 1, 1))

sock = radius.outputs[0]
for f, deg in ((1, 0.0), (44, 0.0), (175, 60.0)):
    sock.default_value = math.radians(deg)
    sock.keyframe_insert("default_value", frame=f)

# ------------------------------------------------------------------ titles (children of the camera)
font = bpy.data.fonts.load(os.path.join(ASSETS, "Cinzel.ttf"))


def label(text, y, size, color, depth=0.5, name=None):
    k = depth / 2.0  # sizes are given for a plane 2 units in front of the camera
    cu = bpy.data.curves.new(name or text, "FONT"); cu.body = text; cu.font = font; cu.size = size * k
    cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.extrude = 0.0
    ob = bpy.data.objects.new(name or text, cu); sc.collection.objects.link(ob)
    ob.parent = cam; ob.location = (0.004 * k if name else 0, y * k - (0.006 * k if name else 0), -depth)
    tm = bpy.data.materials.new(name or text); tm.use_nodes = True
    tn, tl = tm.node_tree.nodes, tm.node_tree.links
    e = tn.new("ShaderNodeEmission"); e.inputs["Color"].default_value = srgb(color)
    t = tn.new("ShaderNodeBsdfTransparent"); mx = tn.new("ShaderNodeMixShader"); mx.name = "fade"
    tl.new(t.outputs[0], mx.inputs[1]); tl.new(e.outputs[0], mx.inputs[2])
    tl.new(mx.outputs[0], tn["Material Output"].inputs["Surface"]); cu.materials.append(tm)
    return ob, mx.inputs["Fac"]


title, tfade = label("THE MONGOL EMPIRE", 0.45, 0.13, C["cream"])
tsh, tsfade = label("THE MONGOL EMPIRE", 0.45, 0.13, (0.02, 0.03, 0.05), depth=0.5005, name="title_shadow")
year, yfade = label("1206", -0.43, 0.17, C["gold"])
ysh, ysfade = label("1206", -0.43, 0.17, (0.02, 0.03, 0.05), depth=0.5005, name="year_shadow")
fades = ((1, 0.0), (12, 0.0), (30, 1.0)), ((1, 0.0), (36, 0.0), (48, 1.0))
for s, frames in ((tfade, fades[0]), (tsfade, fades[0]), (yfade, fades[1]), (ysfade, fades[1])):
    for f, val in frames:
        s.default_value = val
        s.keyframe_insert("default_value", frame=f)


def set_year(scene, *_):  # year counter synced to the reveal
    f = scene.frame_current
    t = min(1.0, max(0.0, (f - 44) / (175 - 44)))
    t = t * t * (3 - 2 * t)
    year.data.body = ysh.data.body = str(round(1206 + t * (1279 - 1206)))


bpy.app.handlers.frame_change_pre.append(set_year)

# ------------------------------------------------------------------ output
sc.render.image_settings.file_format = "FFMPEG"
sc.render.ffmpeg.format = "MPEG4"; sc.render.ffmpeg.codec = "H264"
sc.render.ffmpeg.constant_rate_factor = "HIGH"; sc.render.ffmpeg.ffmpeg_preset = "GOOD"
sc.render.filepath = OUT
if "--still" in argv:
    sc.render.image_settings.file_format = "PNG"
    for f in (int(x) for x in arg("--still", "1").split(",")):
        sc.frame_set(f); sc.render.filepath = os.path.join(os.path.dirname(OUT), f"globe_f{f:03d}.png")
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
print("DONE", OUT)
