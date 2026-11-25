"""3D reconstruction shots for the Missouri surrender episode (WWII Frontlines, Nov 2026).

blender -b -P scene.py -- <out_dir> <shot> [anim|stills:<f1,f2>]

Our own look (not Immersive Past's teal, not Kaktus's black void): an overcast morning, slate-grey sea, warm grey
steel, teak deck, ink-black and khaki faceless mannequins. Sizes in metres, real proportions where known.
Shots are kept short (6-14 s at 30 fps) and are rendered with EEVEE on the GPU.
"""
import sys, os, math, random, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
import kit
kit.FPS = 30
from kit import *
from math import radians as R

_kit_reset = reset
def reset(frames=120, res=(1920, 1080), engine='EEVEE', samples=24):
    """kit.reset without motion blur (EEVEE re-renders each frame per blur step: ~10 s/frame) and at most 24 samples."""
    sc = _kit_reset(frames, res, engine, min(samples, 24))
    sc.render.use_motion_blur = False
    sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 95  # disk is tight: ~0.4 MB/frame instead of 2.6
    return sc

_a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = _a[0] if len(_a) > 0 else os.path.join(HERE, 'out')
SHOT = _a[1] if len(_a) > 1 else 'test_deck'
MODE = _a[2] if len(_a) > 2 else 'stills:1'

# ---------------------------------------------------------------- palette
SEA = (0.10, 0.12, 0.13)
STEEL = (0.36, 0.37, 0.38)
STEEL_DK = (0.20, 0.21, 0.22)
TEAK = (0.42, 0.33, 0.24)
KHAKI = (0.50, 0.44, 0.30)
NAVYWHITE = (0.80, 0.80, 0.77)
INK = (0.03, 0.03, 0.035)
JPN = (0.30, 0.29, 0.22)   # Japanese army uniform, olive-brown
BAIZE = (0.10, 0.22, 0.12)


def sky(top=(0.42, 0.45, 0.48), strength=1.0):
    """Overcast sky: world colour + a soft sun."""
    world(top, strength)


def sea(size=(4000, 4000), z=0.0):
    m = noise_mat('sea', (SEA[0] * 0.8, SEA[1] * 0.8, SEA[2] * 0.8), (SEA[0] * 1.3, SEA[1] * 1.3, SEA[2] * 1.35), scale=0.02, rough=0.25, bump=0.05)
    return box('sea', (size[0], size[1], 0.2), (0, 0, z - 0.1), m)


def _hull_mesh(name, L=270.0, B=33.0, parent=None, m_side=None, m_deck=None):
    """Hull from a plan outline: pointed bow (+Y), rounded stern, sheer rising to the bow. Deck = top face."""
    import bmesh
    hw = B / 2
    ys, half = [], []
    for i in range(41):
        t = i / 40; y = -L / 2 + t * L
        if y < -L / 2 + 30:   # rounded stern
            u = (y + L / 2) / 30; w = hw * (0.55 + 0.45 * math.sin(u * math.pi / 2))
        elif y < L / 2 - 95:
            w = hw
        else:                 # fine entry to a sharp bow
            u = (y - (L / 2 - 95)) / 95; w = hw * (1 - u ** 1.6)
        ys.append(y); half.append(max(w, 0.05))
    def deck_z(y):
        u = (y + L / 2) / L
        return 9.0 + 4.5 * max(0, u - 0.55) / 0.45 + 0.8 * max(0, 0.15 - u) / 0.15
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    top, bot = [], []
    pts = [(half[i], ys[i]) for i in range(41)] + [(-half[i], ys[i]) for i in reversed(range(41))]
    for x, y in pts:
        top.append(bm.verts.new((x, y, deck_z(y))))
        bot.append(bm.verts.new((x * 0.8, y, -3.0)))
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    ft = bm.faces.new(top); fb_ = bm.faces.new(list(reversed(bot)))
    bm.normal_update(); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    if parent: o.parent = parent
    me.materials.append(m_side); me.materials.append(m_deck)
    for p in me.polygons:
        p.material_index = 1 if p.normal.z > 0.7 else 0
    return o, deck_z


# ---------------------------------------------------------------- battleship (Iowa class, 270 m x 33 m), low-poly
def battleship(name='bb', loc=(0, 0, 0), heading=0, detail=True):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    hull = mat(f'{name}_hull', STEEL, rough=0.6, metal=0.1)
    dk = mat(f'{name}_deck', TEAK, rough=0.85)
    sup = mat(f'{name}_sup', (0.40, 0.41, 0.42), rough=0.6, metal=0.1)
    dark = mat(f'{name}_dark', STEEL_DK, rough=0.5)
    L, B = 270.0, 33.0
    _, dz = _hull_mesh(f'{name}_hull', L, B, root, hull, dk)
    fb = dz(0) + 3.0   # legacy offset: superstructure code below uses fb - 3 as deck height
    # superstructure block amidships
    box(f'{name}_sup1', (16, 46, 8), (0, 4, fb - 3 + 4), sup, root, bevel=0.4)
    box(f'{name}_sup2', (12, 30, 7), (0, 8, fb - 3 + 11.5), sup, root, bevel=0.4)
    box(f'{name}_bridge', (9, 10, 6), (0, 18, fb - 3 + 18), sup, root, bevel=0.3)
    cyl(f'{name}_mast', 0.8, 0.5, 26, 8, (0, 14, fb - 3 + 30), dark, root)
    for i, y in enumerate((-2, -14)):
        cyl(f'{name}_funnel{i}', 4.2, 3.6, 12, 12, (0, y, fb - 3 + 19), sup, root, smooth=True).scale = (0.9, 1.4, 1)
        cyl(f'{name}_cap{i}', 3.8, 3.8, 0.8, 12, (0, y, fb - 3 + 25.2), dark, root).scale = (0.9, 1.4, 1)
    # three triple 16-inch turrets: two forward, one aft
    for i, (y, z, hd) in enumerate(((74, 0, 0), (56, 2.6, 0), (-74, 0, 180))):
        t = empty(f'{name}_tur{i}', (0, y, dz(y) + 0.3 + z), root, rot=(0, 0, hd))
        box(f'{name}_turb{i}', (13, 16, 4.2), (0, 0, 2.1), sup, t, bevel=0.8)
        for k, x in enumerate((-2.8, 0, 2.8)):
            cyl(f'{name}_gun{i}{k}', 0.45, 0.35, 20, 8, (x, 17, 2.6), dark, t, rot=(-90, 0, 0))
        if z: box(f'{name}_barb{i}', (11, 11, z), (0, 0, -z / 2), sup, t)
    if detail:
        # secondary 5-inch mounts and AA tubs along the sides
        for side in (-1, 1):
            for j, y in enumerate((28, 16, 4, -8, -20)):
                m = box(f'{name}_sec{side}{j}', (4.6, 5.2, 2.4), (side * 10.5, y, fb - 3 + 9.2), sup, root, bevel=0.3)
                cyl(f'{name}_secg{side}{j}', 0.16, 0.14, 6, 6, (side * 10.5, y + 4.5, fb - 3 + 9.8), dark, root, rot=(-90, 0, 0))
    return root


# ---------------------------------------------------------------- C-54 Skymaster (span 35.8 m, length 28.6 m), low-poly
def c54(name='c54', loc=(0, 0, 0), heading=0, color=(0.62, 0.63, 0.64), frames=300, spin=True):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    skin = mat(f'{name}_skin', color, rough=0.35, metal=0.55)
    dark = mat(f'{name}_dark', (0.03, 0.03, 0.035), rough=0.4)
    glass = mat(f'{name}_glass', (0.02, 0.03, 0.04), rough=0.1, metal=0.4)
    fz = 3.4
    cyl(f'{name}_fus', 1.75, 1.75, 20.0, 16, (0, 0, fz), skin, root, rot=(90, 0, 0), smooth=True)
    sphere(f'{name}_nose', 1.75, (0, 10.0, fz), (1, 1.8, 0.95), skin, root, seg=16, rings=10, smooth=True)
    sphere(f'{name}_cockpit', 1.2, (0, 11.0, fz + 0.75), (1.1, 1.3, 0.55), glass, root, seg=14, rings=8, smooth=True)
    cyl(f'{name}_tailcone', 1.75, 0.35, 8.0, 16, (0, -13.9, fz + 0.6), skin, root, rot=(-84, 0, 0), smooth=True)
    box(f'{name}_wing', (35.8, 4.6, 0.5), (0, 1.0, fz - 1.2), skin, root, bevel=0.2)   # low wing
    props = []
    for x in (-10.5, -5.0, 5.0, 10.5):
        cyl(f'{name}_nac{x}', 0.8, 0.55, 5.0, 12, (x, 2.8, fz - 0.9), skin, root, rot=(90, 0, 0), smooth=True)
        hub = empty(f'{name}_prop{x}', (x, 5.5, fz - 0.9), root)
        sphere(f'{name}_spin{x}', 0.4, (0, 0, 0), (1, 1.4, 1), dark, hub, seg=10, rings=6, smooth=True)
        for k in range(3):
            box(f'{name}_blade{x}_{k}', (0.28, 0.06, 1.9), (0, 0, 0.95), dark, empty(f'{name}_bp{x}_{k}', (0, 0, 0), hub, rot=(0, k * 120, 0)))
        if spin:
            hub.rotation_euler.y = 0; hub.keyframe_insert('rotation_euler', frame=1)
            hub.rotation_euler.y = R(360 * 9 * frames / kit.FPS); hub.keyframe_insert('rotation_euler', frame=frames + 1)
            for fc in hub.animation_data.action.fcurves:
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
        props.append(hub)
    box(f'{name}_fin', (0.35, 4.5, 6.0), (0, -15.0, fz + 3.4), skin, root, bevel=0.1, rot=(-10, 0, 0))
    box(f'{name}_hstab', (13.0, 3.0, 0.3), (0, -15.6, fz + 0.9), skin, root, bevel=0.1)
    for sx in (-1, 1):
        cyl(f'{name}_leg{sx}', 0.12, 0.12, 2.2, 6, (sx * 5.0, 2.0, 1.3), dark, root)
        cyl(f'{name}_wheel{sx}', 0.6, 0.6, 0.45, 14, (sx * 5.0, 2.0, 0.6), dark, root, rot=(0, 90, 0), smooth=True)
    cyl(f'{name}_nleg', 0.1, 0.1, 2.0, 6, (0, 9.0, 1.2), dark, root)
    cyl(f'{name}_nosewheel', 0.42, 0.42, 0.35, 12, (0, 9.0, 0.42), dark, root, rot=(0, 90, 0), smooth=True)
    return root


# ---------------------------------------------------------------- faceless figures (simple clay, no MakeHuman needed)
def person(name, loc, heading=0, body=KHAKI, head=(0.62, 0.55, 0.47), hat=None, height=1.78, pose='stand'):
    """Faceted clay figure from kit.Figure, recoloured: body = uniform/suit colour, head+hands = neutral clay."""
    f = Figure(name, 'grey', loc, heading=heading, kit='plain', height=height)
    bm = mat(f'{name}_b', body, rough=0.8); hm = mat(f'{name}_h', head, rough=0.6)
    for o in bpy.data.objects:
        if o.name.startswith(name + '_') and o.type == 'MESH':
            n = o.name
            skin = any(k in n for k in ('head_m', 'neck_m', 'hand_', 'farm_'))
            set_mat(o, hm if skin and 'farm_' not in n else bm)
    if hat == 'top':
        black = mat(f'{name}_hat', INK, rough=0.5)
        cyl(f'{name}_brim', 0.17, 0.17, 0.02, 14, (0, 0, 0.20), black, f.j['head'])
        cyl(f'{name}_crown', 0.11, 0.115, 0.17, 14, (0, 0, 0.29), black, f.j['head'], smooth=True)
    elif hat == 'cap':
        c = mat(f'{name}_cap', body, rough=0.8)
        cyl(f'{name}_capm', 0.12, 0.125, 0.08, 12, (0, 0.0, 0.19), c, f.j['head'], smooth=True)
        box(f'{name}_visor', (0.16, 0.08, 0.015), (0, 0.10, 0.165), mat(f'{name}_vis', INK), f.j['head'])
    if pose != 'stand': f.pose(pose)
    return f


def deck_set(width=40, depth=30):
    """A patch of the Missouri's starboard deck (veranda deck, 01 level): teak, turret 2 face behind, rails."""
    dk = noise_mat('teak', (0.36, 0.28, 0.20), (0.47, 0.37, 0.27), scale=0.9, rough=0.85, bump=0.05)
    box('deck', (width, depth, 0.4), (0, 0, -0.2), dk)
    # planking lines
    seam = mat('seam', (0.16, 0.12, 0.09), rough=0.9)
    for i in range(-int(width / 2), int(width / 2), 1):
        box(f'seam{i}', (0.02, depth, 0.01), (i + 0.5, 0, 0.005), seam)
    sup = mat('wall', (0.40, 0.41, 0.42), rough=0.6, metal=0.1)
    box('bulkhead', (width, 1.0, 6.0), (0, depth / 2 - 0.5, 3.0), sup)
    rail = mat('rail', (0.55, 0.56, 0.57), rough=0.5, metal=0.4)
    for x in range(-int(width / 2), int(width / 2) + 1, 2):
        cyl(f'stan{x}', 0.03, 0.03, 1.0, 6, (x, -depth / 2 + 0.3, 0.5), rail)
    for z in (0.45, 0.95):
        cyl(f'rail{z}', 0.02, 0.02, width, 6, (0, -depth / 2 + 0.3, z), rail, rot=(0, 90, 0))


def table(loc=(0, 0, 0)):
    """The mess table with a cloth, two copies of the Instrument, chairs either side."""
    root = empty('table', loc); root.rotation_euler.z = R(90)
    cl = mat('cloth', BAIZE, rough=0.95)
    box('top', (1.4, 3.0, 0.06), (0, 0, 0.76), cl, root)
    box('skirt', (1.42, 3.02, 0.5), (0, 0, 0.50), cl, root)
    paper = mat('paper', (0.88, 0.86, 0.78), rough=0.9)
    box('doc1', (0.32, 0.45, 0.02), (0.15, 0.55, 0.80), paper, root)
    box('doc2', (0.32, 0.45, 0.02), (0.15, -0.55, 0.80), paper, root)
    wood = mat('chair', (0.20, 0.15, 0.11), rough=0.7)
    for sx in (-1, 1):
        c = empty(f'chair{sx}', (sx * 1.05, 0, 0), root, rot=(0, 0, 90 if sx > 0 else -90))
        box(f'seat{sx}', (0.45, 0.45, 0.05), (0, 0, 0.46), wood, c)
        box(f'back{sx}', (0.45, 0.05, 0.5), (0, -0.22, 0.72), wood, c)
        for lx in (-0.2, 0.2):
            for ly in (-0.2, 0.2):
                box(f'leg{sx}{lx}{ly}', (0.04, 0.04, 0.46), (lx, ly, 0.23), wood, c)
    return root


# ---------------------------------------------------------------- shots
SHOTS = {}


def shot(fn):
    SHOTS[fn.__name__] = fn
    return fn


@shot
def test_deck():
    reset(frames=60, samples=48)
    glare_comp(threshold=1.2, mix=-0.8, vignette=0.0)
    sky((0.40, 0.43, 0.46), 0.9)
    sun('sun', (55, 0, 140), 3.2, color=(1.0, 0.95, 0.88), angle=8)
    deck_set()
    table((0, 2, 0))
    # Japanese delegation: three rows facing the table (+Y), civilians in black with top hats
    xs = [-2.4, -1.2, 0.0, 1.2, 2.4]
    for i, x in enumerate(xs[1:4]):
        person(f'jc{i}', (x, -2.0, 0), heading=180, body=INK, hat='top')
    for i, x in enumerate(xs):
        person(f'jm{i}', (x, -3.2, 0), heading=180, body=JPN, hat='cap')
    for i, x in enumerate(xs[:3]):
        person(f'jr{i}', (x + 0.6, -4.4, 0), heading=180, body=JPN if i else INK, hat='cap' if i else 'top')
    # MacArthur at the microphone, Allied officers in a line behind
    person('mac', (0, 4.0, 0), heading=0, body=KHAKI, hat='cap')
    cyl('mic', 0.015, 0.015, 1.5, 6, (0, 3.4, 0.75), mat('micm', INK))
    for i, x in enumerate([-6, -5, -4, -3, 3, 4, 5, 6]):
        person(f'al{i}', (x, 5.6, 0), heading=0, body=KHAKI if i % 3 else NAVYWHITE, hat='cap')
    cam = camera(lens=35, fstop=4.0, focus=11)
    cam_key(cam, 1, (9, -9, 5.5), (0, 0.5, 1.2))
    cam_key(cam, 60, (7.5, -7.5, 4.8), (0, 0.5, 1.2))


@shot
def test_ship():
    reset(frames=60, samples=48)
    glare_comp(threshold=1.2, mix=-0.8, vignette=0.0)
    sky((0.40, 0.43, 0.46), 0.9)
    sun('sun', (55, 0, 140), 3.2, color=(1.0, 0.95, 0.88), angle=8)
    sea()
    battleship('missouri', (0, 0, 0), heading=0)
    c54('bataan', (-90, -60, 40), heading=60, frames=60)
    cam = camera(lens=35)
    cam_key(cam, 1, (170, 150, 45), (0, 10, 12))


# ================================================================ more models
OLIVE_JP = (0.27, 0.26, 0.18)
POWCLOTH = (0.58, 0.55, 0.46)
GRASS = ((0.20, 0.22, 0.14), (0.30, 0.31, 0.20))
EARTH = ((0.26, 0.23, 0.19), (0.36, 0.32, 0.26))


def lin(o, path='location'):
    ad = o.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            if fc.data_path == path:
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'


def destroyer(name='dd', loc=(0, 0, 0), heading=0):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    hull = mat(f'{name}_h', (0.30, 0.31, 0.32), rough=0.6); dk = mat(f'{name}_d', (0.24, 0.25, 0.26), rough=0.8)
    sup = mat(f'{name}_s', (0.38, 0.39, 0.40), rough=0.6); dark = mat(f'{name}_k', STEEL_DK)
    import bmesh
    _hull_mesh(f'{name}_hull', 115, 12, root, hull, dk)
    root.scale = (1, 1, 0.55)
    box(f'{name}_sup', (7, 18, 7), (0, 18, 14), sup, root, bevel=0.3)
    for i, y in enumerate((2, -12)):
        cyl(f'{name}_fun{i}', 1.6, 1.4, 10, 10, (0, y, 16), sup, root, smooth=True).scale = (1, 1.5, 1)
    for i, y in enumerate((38, -40)):
        box(f'{name}_gun{i}', (3.5, 4.5, 3.5), (0, y, 12), sup, root, bevel=0.3)
    cyl(f'{name}_mast', 0.3, 0.2, 14, 6, (0, 14, 24), dark, root)
    return root


def launch(name='launch', loc=(0, 0, 0), heading=0):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    m = mat(f'{name}_m', (0.33, 0.34, 0.35), rough=0.6); w = mat(f'{name}_w', (0.75, 0.74, 0.70), rough=0.7)
    box(f'{name}_hull', (3.2, 11, 1.4), (0, 0, 0.3), m, root, bevel=0.4)
    box(f'{name}_cab', (2.4, 3.5, 1.4), (0, 1.0, 1.6), w, root, bevel=0.2)
    return root


def lcvp(name='lcvp', loc=(0, 0, 0), heading=0):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    m = mat(f'{name}_m', (0.30, 0.33, 0.30), rough=0.7)
    box(f'{name}_hull', (3.2, 11, 1.6), (0, 0, 0.4), m, root, bevel=0.2)
    box(f'{name}_ramp', (3.0, 0.3, 1.8), (0, 5.5, 0.7), m, root)
    box(f'{name}_cox', (1.2, 1.4, 1.0), (0, -4.6, 1.6), m, root)
    return root


def fighter(name='zero', loc=(0, 0, 0), heading=0, color=(0.30, 0.31, 0.24), props=False, scale=1.0, under=None):
    root = empty(name, loc); root.rotation_euler.z = R(heading); root.scale = (scale, scale, scale)
    m = mat(f'{name}_m', color, rough=0.6, metal=0.1); u = mat(f'{name}_u', under or color, rough=0.6)
    dark = mat(f'{name}_k', INK)
    cyl(f'{name}_f', 0.6, 0.25, 9.0, 10, (0, 0, 1.7), m, root, rot=(90, 0, 0), smooth=True)
    sphere(f'{name}_cow', 0.62, (0, 4.3, 1.7), (1, 0.7, 1), m, root, seg=12, rings=6)
    box(f'{name}_w', (12.0, 2.2, 0.18), (0, 1.0, 1.25), u, root, bevel=0.05)
    box(f'{name}_hs', (4.2, 1.0, 0.12), (0, -4.0, 1.85), m, root)
    box(f'{name}_vs', (0.12, 1.3, 1.4), (0, -4.2, 2.4), m, root, rot=(-10, 0, 0))
    sphere(f'{name}_cp', 0.42, (0, 0.6, 2.2), (0.8, 1.8, 0.7), mat(f'{name}_g', (0.05, 0.06, 0.07), rough=0.15, metal=0.4), root, seg=10, rings=6)
    for sx in (-1, 1):
        cyl(f'{name}_wh{sx}', 0.32, 0.32, 0.2, 10, (sx * 1.5, 1.2, 0.32), dark, root, rot=(0, 90, 0))
        cyl(f'{name}_lg{sx}', 0.06, 0.06, 1.0, 6, (sx * 1.5, 1.2, 0.8), dark, root)
    if props:
        for k in range(3):
            box(f'{name}_bl{k}', (0.2, 0.05, 1.4), (0, 0, 0.7), dark, empty(f'{name}_bp{k}', (0, 4.75, 1.7), root, rot=(0, k * 120, 0)))
    return root


def plane_small(name, loc, color=(0.18, 0.22, 0.30)):
    """F6F/F4U-sized carrier plane for the flyover (13 m span)."""
    root = empty(name, loc)
    m = mat('cvplane', color, rough=0.5, metal=0.2)
    cyl(f'{name}_f', 0.7, 0.3, 10, 8, (0, 0, 0), m, root, rot=(90, 0, 0))
    box(f'{name}_w', (13, 2.4, 0.2), (0, 0.8, -0.2), m, root)
    box(f'{name}_hs', (4.5, 1.0, 0.15), (0, -4.6, 0.1), m, root)
    box(f'{name}_vs', (0.15, 1.2, 1.6), (0, -4.6, 0.8), m, root)
    return root


def b29(name='b29', loc=(0, 0, 0), heading=0, frames=300, spin=True):
    """Boeing B-29 (span 43 m, length 30 m), bare metal."""
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    skin = mat(f'{name}_s', (0.66, 0.67, 0.68), rough=0.3, metal=0.7); dark = mat(f'{name}_k', INK)
    glass = mat(f'{name}_g', (0.05, 0.06, 0.07), rough=0.1, metal=0.5)
    cyl(f'{name}_f', 1.45, 1.45, 24, 16, (0, 0, 0), skin, root, rot=(90, 0, 0), smooth=True)
    sphere(f'{name}_n', 1.45, (0, 12, 0), (1, 1.5, 1), glass, root, seg=16, rings=10, smooth=True)
    cyl(f'{name}_tc', 1.45, 0.5, 6, 16, (0, -15, 0.2), skin, root, rot=(-88, 0, 0), smooth=True)
    box(f'{name}_w', (43, 4.6, 0.45), (0, 1.5, -0.3), skin, root, bevel=0.15)
    box(f'{name}_hs', (14, 3.0, 0.3), (0, -16.5, 0.4), skin, root)
    box(f'{name}_vs', (0.4, 5.0, 7.0), (0, -16.5, 3.6), skin, root, rot=(-14, 0, 0))
    for x in (-13, -6.5, 6.5, 13):
        cyl(f'{name}_nac{x}', 0.9, 0.6, 5.5, 12, (x, 3.6, -0.3), skin, root, rot=(90, 0, 0), smooth=True)
        hub = empty(f'{name}_p{x}', (x, 6.4, -0.3), root)
        for k in range(4):
            box(f'{name}_bl{x}{k}', (0.3, 0.06, 2.3), (0, 0, 1.15), dark, empty(f'{name}_bp{x}{k}', (0, 0, 0), hub, rot=(0, k * 90, 0)))
        if spin:
            hub.rotation_euler.y = 0; hub.keyframe_insert('rotation_euler', frame=1)
            hub.rotation_euler.y = R(360 * 12 * frames / kit.FPS); hub.keyframe_insert('rotation_euler', frame=frames + 1)
            lin(hub, 'rotation_euler')
    return root


def sedan(name='car', loc=(0, 0, 0), heading=0, color=(0.08, 0.08, 0.09)):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    m = mat(f'{name}_m', color, rough=0.35, metal=0.4); dark = mat(f'{name}_k', INK)
    glass = mat(f'{name}_g', (0.12, 0.14, 0.16), rough=0.1, metal=0.4)
    box(f'{name}_b', (1.8, 4.9, 0.75), (0, 0, 0.75), m, root, bevel=0.2)
    box(f'{name}_c', (1.6, 2.4, 0.65), (0, -0.4, 1.38), glass, root, bevel=0.2)
    box(f'{name}_r', (1.62, 2.0, 0.08), (0, -0.4, 1.72), m, root, bevel=0.04)
    for sx in (-1, 1):
        for y in (-1.5, 1.6):
            cyl(f'{name}_w{sx}{y}', 0.38, 0.38, 0.25, 12, (sx * 0.85, y, 0.38), dark, root, rot=(0, 90, 0), smooth=True)
    return root


def barracks(name, loc, size=(30, 8), heading=0, roof_text=None):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    wall = mat('bwall', (0.33, 0.30, 0.26), rough=0.95); roof = mat('broof', (0.20, 0.19, 0.18), rough=0.9)
    box(f'{name}_w', (size[1], size[0], 3.0), (0, 0, 1.5), wall, root)
    r = box(f'{name}_r', (size[1] + 0.8, size[0] + 0.6, 0.25), (0, 0, 3.6), roof, root, rot=(0, 0, 0))
    if roof_text:
        bpy.ops.object.text_add(location=(0, 0, 3.75)); t = bpy.context.object; t.name = f'{name}_txt'
        t.data.body = roof_text; t.data.size = size[1] * 0.75; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'
        t.data.extrude = 0.02; t.parent = root; t.rotation_euler.z = R(90)
        set_mat(t, mat('rooftxt', (0.85, 0.84, 0.78), rough=0.9))
    return root


def fence(name, p0, p1, h=2.4, spacing=4.0):
    m = mat('fence', (0.22, 0.20, 0.17), rough=0.9)
    a, b = Vector(p0), Vector(p1); d = b - a; n = max(1, int(d.length / spacing))
    for i in range(n + 1):
        q = a + d * (i / n); cyl(f'{name}_p{i}', 0.08, 0.08, h, 6, (q.x, q.y, h / 2), m)
    ang = math.degrees(math.atan2(d.y, d.x))
    for z in (0.6, 1.3, 2.0):
        box(f'{name}_wire{z}', (d.length, 0.02, 0.02), ((a.x + b.x) / 2, (a.y + b.y) / 2, z), m, rot=(0, 0, ang))


def flag(name, parent_obj, kind='us', loc=(0.1, 0.0, 0.55)):
    """A small hand-held flag on a stick (US, UK, NL in simplified colours)."""
    stick = mat('stick', (0.35, 0.28, 0.2)); cols = {'us': [(0.70, 0.08, 0.08), (0.92, 0.92, 0.90)], 'uk': [(0.08, 0.15, 0.45), (0.75, 0.08, 0.10)],
                                                       'nl': [(0.70, 0.08, 0.08), (0.92, 0.92, 0.90), (0.10, 0.20, 0.55)]}[kind]
    holder = empty(f'{name}_fh', loc, parent_obj)
    cyl(f'{name}_st', 0.012, 0.012, 1.0, 5, (0, 0, 0.5), stick, holder)
    for i, c in enumerate(cols):
        box(f'{name}_fl{i}', (0.02, 0.6, 0.38 / len(cols)), (0, 0.32, 0.82 - i * 0.38 / len(cols)), mat(f'flag{kind}{i}', c, rough=0.9), holder)
    return holder


def parachute(name, loc, f0, f1, z0, z1, drift=(6, 0)):
    root = empty(name, (loc[0], loc[1], z0))
    canopy = mat('chute', (0.85, 0.80, 0.62), rough=0.9); drum = mat('drum', (0.25, 0.27, 0.22), rough=0.6)
    sphere(f'{name}_c', 3.0, (0, 0, 6), (1, 1, 0.45), canopy, root, seg=14, rings=5)
    cyl(f'{name}_d', 0.35, 0.35, 0.9, 10, (0, 0, 0), drum, root)
    for k in range(4):
        a = k * math.pi / 2
        box(f'{name}_l{k}', (0.02, 0.02, 6.2), (1.4 * math.cos(a), 1.4 * math.sin(a), 3.1), mat('line', (0.6, 0.6, 0.6)), root,
            rot=(math.degrees(-0.22 * math.sin(a)), math.degrees(0.22 * math.cos(a)), 0))
    root.scale = (0.01, 0.01, 0.01); root.keyframe_insert('scale', frame=max(1, f0 - 1))
    root.scale = (1, 1, 1); root.keyframe_insert('scale', frame=f0 + 8)
    root.location = (loc[0], loc[1], z0); root.keyframe_insert('location', frame=f0)
    root.location = (loc[0] + drift[0], loc[1] + drift[1], z1); root.keyframe_insert('location', frame=f1)
    lin(root)
    return root


def overcast(sun_e=3.0):
    sky((0.40, 0.43, 0.46), 0.9)
    sun('sun', (55, 0, 140), sun_e, color=(1.0, 0.95, 0.88), angle=8)


def ground(size=(800, 800), c=GRASS, z=0.0, name='ground'):
    m = noise_mat(name, c[0], c[1], scale=0.05, rough=0.95, bump=0.1)
    return box(name, (size[0], size[1], 0.2), (0, 0, z - 0.1), m)


# ================================================================ final shots (30 fps)
@shot
def s_atsugi():
    """28 Aug 1945, 0828: a twin-engine transport lands at Atsugi between rows of Japanese planes with no propellers."""
    N = 330; reset(frames=N, samples=48); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0); overcast()
    ground((1600, 1600))
    tar = mat('tarmac', (0.22, 0.22, 0.21), rough=0.9)
    box('runway', (50, 1200, 0.06), (0, 0, 0.03), tar)
    for i in range(-14, 15):
        box(f'mark{i}', (0.8, 18, 0.01), (0, i * 40, 0.07), mat('mark', (0.6, 0.6, 0.55)))
    box('apron', (120, 260, 0.05), (-110, 40, 0.025), tar)
    for r, x in enumerate((-80, -120)):
        for i in range(10):
            fighter(f'z{r}_{i}', (x, -60 + i * 22, 0), heading=90, props=False)
    hang = mat('hangar', (0.35, 0.34, 0.32), rough=0.8)
    for i, y in enumerate((150, 210)):
        box(f'hangar{i}', (40, 50, 14), (-150, y, 7), hang)
        cyl(f'hroof{i}', 25, 25, 50, 24, (-150, y, 6), hang, rot=(90, 0, 0)).scale = (0.8, 1, 0.45)
    # wind sock (blowing towards +Y: the plane lands towards -Y, i.e. downwind, as Arisue wrote)
    pole = mat('pole', (0.5, 0.5, 0.5)); cyl('wpole', 0.12, 0.12, 8, 6, (40, 60, 4), pole)
    sock = mat('sock', (0.85, 0.42, 0.15), rough=0.9)
    cyl('sock', 0.8, 0.35, 4, 10, (40, 62.2, 7.6), sock, rot=(-95, 0, 0), smooth=True)
    for i in range(6):
        person(f'jo{i}', (-60 + i * 1.6, 120, 0), heading=-80, body=OLIVE_JP, hat='cap')
    p = c54('c46', (0, 700, 60), heading=180, color=(0.42, 0.44, 0.38), frames=N)
    # remove two inner engines' props for a twin look (C-46): hide them
    for o in bpy.data.objects:
        if o.name.startswith('c46_') and re.search(r'(nac|prop|spin|blade|bp)-?5\.0', o.name):
            o.hide_render = True
    p.location = (0, 520, 45); p.rotation_euler.x = R(-3); p.keyframe_insert('location', frame=1); p.keyframe_insert('rotation_euler', frame=1)
    p.location = (0, 120, 0.0); p.rotation_euler.x = 0; p.keyframe_insert('location', frame=200); p.keyframe_insert('rotation_euler', frame=200)
    p.location = (0, -60, 0.0); p.keyframe_insert('location', frame=N)
    cam = camera(lens=40)
    cam_key(cam, 1, (70, -40, 9), (0, 400, 30))
    cam_key(cam, 200, (62, -10, 8), (0, 110, 3))
    cam_key(cam, N, (58, -20, 7), (0, -40, 2))


@shot
def s_road():
    """30 Aug 1945: the convoy drives to Yokohama between soldiers standing with their backs to the road."""
    N = 360; reset(frames=N, samples=48); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0); overcast()
    ground((1600, 400), EARTH)
    rd = mat('road', (0.30, 0.28, 0.25), rough=0.95)
    box('road', (1600, 7, 0.06), (0, 0, 0.03), rd)
    # fields and a few ruined walls
    random.seed(3)
    ruin = mat('ruin', (0.36, 0.33, 0.29), rough=0.95)
    for i in range(40):
        x = random.uniform(-300, 400); y = random.choice((-1, 1)) * random.uniform(20, 120)
        box(f'ruin{i}', (random.uniform(3, 9), random.uniform(3, 9), random.uniform(0.8, 4)), (x, y, 1), ruin, rot=(0, 0, random.uniform(0, 90)))
    for i in range(30):
        x = random.uniform(-300, 400); y = random.choice((-1, 1)) * random.uniform(25, 140)
        cyl(f'tree{i}', 0.2, 0.2, 5, 6, (x, y, 2.5), mat('trunk', (0.15, 0.12, 0.10)))
        sphere(f'crown{i}', 2.4, (x, y, 6), (1, 1, 0.8), mat('leaf', (0.13, 0.16, 0.10), rough=0.95), seg=8, rings=5)
    # soldiers every 12 m on both sides, facing AWAY from the road
    k = 0
    for x in range(-120, 330, 8):
        for side in (-1, 1):
            person(f's{k}', (x + random.uniform(-1, 1), side * 6.0, 0), heading=(0 if side > 0 else 180), body=OLIVE_JP, hat='cap')
            k += 1
    cars = []
    for i in range(4):
        c = sedan(f'car{i}', (-60 - i * 14, -1.6, 0), heading=-90, color=[(0.08, 0.08, 0.09), (0.12, 0.12, 0.10), (0.25, 0.24, 0.20), (0.08, 0.08, 0.09)][i])
        c.keyframe_insert('location', frame=1); c.location.x += 230; c.keyframe_insert('location', frame=N); lin(c); cars.append(c)
    cam = camera(lens=35)
    for f, cx in ((1, -110), (N, 120)):
        cam_key(cam, f, (cx - 22, -15, 6.5), (cx + 28, 0, 1.2))


@shot
def s_drop():
    """27 Aug 1945 on: a B-29 drops supplies by parachute over a prison camp with PW painted on the roofs."""
    N = 330; reset(frames=N, samples=48); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0); overcast()
    ground((1600, 1600), EARTH)
    yard = mat('yard', (0.33, 0.30, 0.25), rough=0.95); box('yard', (120, 90, 0.05), (0, 0, 0.025), yard)
    for i in range(4):
        barracks(f'bk{i}', (-42 + i * 28, 22, 0), size=(40, 10), roof_text='P W' if i in (1, 2) else None)
    fence('f1', (-60, -40), (60, -40)); fence('f2', (-60, -40), (-60, 45)); fence('f3', (60, -40), (60, 45))
    random.seed(5); figs = []
    for i in range(26):
        h = person(f'p{i}', (random.uniform(-35, 35), random.uniform(-28, 2), 0), heading=random.uniform(150, 210), body=POWCLOTH)
        h.pose('wave' if i % 3 == 0 else ('hands_up' if i % 5 == 0 else 'stand'))
        figs.append(h)
    b = b29('b29', (0, 0, 0), heading=-90, frames=N)
    b.location = (-500, 10, 95); b.keyframe_insert('location', frame=1)
    b.location = (520, 10, 95); b.keyframe_insert('location', frame=N); lin(b)
    for i in range(5):
        f0 = 120 + i * 12
        bx = -500 + 1020 * (f0 - 1) / (N - 1)
        parachute(f'ch{i}', (bx, 8 + (i % 2) * 6, 0), f0, N + 90, 88, 0.0, drift=(10, -6))
    cam = camera(lens=28)
    cam_key(cam, 1, (70, -110, 30), (-30, 10, 30))
    cam_key(cam, 170, (62, -100, 28), (10, 10, 45))
    cam_key(cam, N, (55, -92, 24), (0, 5, 20))


@shot
def s_omori():
    """29 Aug 1945, afternoon: landing boats come up to the Omori camp on the waterfront; prisoners wave flags."""
    N = 300; reset(frames=N, samples=48); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0); overcast()
    sea((3000, 3000))
    land = noise_mat('island', EARTH[0], EARTH[1], scale=0.05, rough=0.95)
    box('island', (160, 90, 3.0), (0, 60, 1.4), land, bevel=1.0)
    for i in range(3):
        barracks(f'bk{i}', (-40 + i * 40, 75, 2.9), size=(30, 9), heading=90)
    fence('fw', (-70, 40), (70, 40))
    random.seed(9); kinds = ['us', 'uk', 'nl']
    for i in range(30):
        h = person(f'p{i}', (random.uniform(-55, 55), random.uniform(28, 38), 2.9), heading=180 + random.uniform(-20, 20), body=POWCLOTH)
        if i % 4 == 0:
            h.pose('wave'); flag(f'fl{i}', h.j['wrist_R'], kinds[i % 3], loc=(0, 0, -0.2))
        elif i % 3 == 0: h.pose('hands_up')
    boats = []
    for i in range(3):
        bt = lcvp(f'lcvp{i}', (-14 + i * 14, -95 - i * 12, 0.2), heading=0)
        bt.keyframe_insert('location', frame=1); bt.location.y += 95; bt.keyframe_insert('location', frame=N); lin(bt)
        boats.append(bt)
    cam = camera(lens=35)
    cam_key(cam, 1, (30, -170, 16), (0, -40, 2))
    cam_key(cam, N, (22, -90, 10), (0, 20, 3))


@shot
def s_arrive():
    """2 Sep 1945, 0856: a launch brings the Japanese delegation from the destroyer to the Missouri."""
    N = 300; reset(frames=N, samples=48); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0); overcast()
    sea((5000, 5000))
    battleship('missouri', (0, 0, 0), heading=0)
    destroyer('lansdowne', (120, -40, 0), heading=10)
    for i, (x, y, h) in enumerate(((-420, 300, 30), (-600, -200, 80), (500, 520, -20), (900, -300, 50))):
        destroyer(f'dd{i}', (x, y, 0), heading=h)
    for i, (x, y, h) in enumerate(((-900, 700, 10), (1200, 900, -40))):
        battleship(f'bb{i}', (x, y, 0), heading=h, detail=False)
    l = launch('launch', (100, -30, 0.3), heading=-60)
    l.keyframe_insert('location', frame=1); l.location = (24, 20, 0.3); l.keyframe_insert('location', frame=N - 30); lin(l)
    cam = camera(lens=35)
    cam_key(cam, 1, (230, -170, 34), (40, 20, 6))
    cam_key(cam, N, (150, -110, 24), (25, 20, 8))


def deck_scene(N):
    reset(frames=N, samples=48); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0); overcast(2.6)
    sea((2000, 2000), z=-6)
    deck_set(width=44, depth=34)
    # the bulkhead with a row of little Rising Sun kill flags (Kase counted them)
    white = mat('kf_w', (0.88, 0.87, 0.82), rough=0.8); red = mat('kf_r', (0.72, 0.08, 0.07), rough=0.8)
    for i in range(14):
        x = -9 + i * 1.3
        box(f'kf{i}', (0.9, 0.05, 0.6), (x, 15.97, 4.6), white)
        cyl(f'kfd{i}', 0.16, 0.16, 0.06, 12, (x, 15.93, 4.6), red, rot=(90, 0, 0))
    table((0, 2, 0))
    return


DELEG = [(-2.4, -2.0, 'top'), (-1.2, -2.0, 'top'), (0.0, -2.0, 'top'), (1.2, -2.0, 'cap'), (2.4, -2.0, 'cap'),
         (-2.4, -3.2, 'cap'), (-1.2, -3.2, 'top'), (0.0, -3.2, 'cap'), (1.2, -3.2, 'cap'), (2.4, -3.2, 'cap'), (0.6, -4.4, 'cap')]


@shot
def s_deck_plan():
    """0856-0902: the eleven walk to their places in front of the table; the Allied officers in lines behind it."""
    N = 360; deck_scene(N)
    for i, x in enumerate([-12 + k * 1.1 for k in range(9)] + [3 + k * 1.1 for k in range(9)]):
        person(f'al{i}', (x, 6.0 if i % 2 else 7.2, 0), heading=180 if False else 0, body=KHAKI if i % 3 else NAVYWHITE, hat='cap')
    for i, (x, y, hat) in enumerate(DELEG):
        body = INK if hat == 'top' else JPN
        f = person(f'jd{i}', (x, y, 0), heading=0, body=body, hat=hat)
        start = (18 + i * 0.9, -10 - (i % 3), 0); f0 = 10 + i * 12; f1 = f0 + 150
        f.key_root(1, start, 90); f.key_root(f0, start, 90)
        f.walk(f0, f1, start, (x, y, 0)); f.hold(f1 + 2, 'stand', (x, y, 0), 0)
        if i == 0: f.pose({'shoulder_R': (20, 0, 0)}, frame=f1 + 2)
    cam = camera(lens=30)
    cam_key(cam, 1, (16, -22, 26), (2, 0, 0))
    cam_key(cam, N, (12, -17, 19), (0, 0, 0))


@shot
def s_deck_sign():
    """~0906-0908: MacArthur sits at the table; Wainwright and Percival step forward and stand behind him."""
    N = 300; deck_scene(N)
    for i, x in enumerate([-12 + k * 1.1 for k in range(9)] + [3 + k * 1.1 for k in range(9)]):
        person(f'al{i}', (x, 6.0 if i % 2 else 7.2, 0), heading=0, body=KHAKI if i % 3 else NAVYWHITE, hat='cap')
    for i, (x, y, hat) in enumerate(DELEG):
        person(f'jd{i}', (x, y, 0), heading=0, body=INK if hat == 'top' else JPN, hat=hat)
    mac = person('mac', (0, 3.05, 0), heading=180, body=KHAKI, hat='cap')
    mac.pose({'hip_L': (85, 0, 0), 'hip_R': (85, 0, 0), 'knee_L': (-85, 0, 0), 'knee_R': (-85, 0, 0),
              'shoulder_R': (45, 0, 0), 'elbow_R': (60, 0, 0), 'shoulder_L': (40, 0, 0), 'elbow_L': (60, 0, 0)})
    mac.j['pelvis'].location.z = 0.52
    # light glow on the two men who step forward (role highlight, not a face)
    for nm, x0, x1 in (('wainwright', -3.0, -0.9), ('percival', 3.2, 0.9)):
        f = person(nm, (x0, 6.0, 0), heading=180, body=KHAKI, hat='cap', height=1.82)
        f.key_root(1, (x0, 6.0, 0), 180); f.key_root(70, (x0, 6.0, 0), 180)
        f.walk(70, 160, (x0, 6.0, 0), (x1, 4.2, 0)); f.hold(162, 'stand', (x1, 4.2, 0), 180)
    spot('key', (0, -10, 14), (0, 3.5, 1.2), energy=3e4, angle=30, blend=0.9, soft=2, color=(1, 0.96, 0.88))
    cam = camera(lens=45, fstop=4.0, focus=10)
    cam_key(cam, 1, (6, -8, 4.2), (0, 3.4, 1.3))
    cam_key(cam, N, (3.5, -5.5, 3.4), (0, 3.6, 1.4))


@shot
def s_flyover():
    """0925: hundreds of carrier planes pass over the Missouri, mast high; the B-29s follow."""
    N = 330; reset(frames=N, samples=48); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0); overcast()
    sea((6000, 6000))
    battleship('missouri', (0, 0, 0), heading=-20)
    for i, (x, y, h) in enumerate(((-300, 400, 20), (420, 650, -10), (-700, -300, 60))):
        destroyer(f'dd{i}', (x, y, 0), heading=h)
    form = empty('form', (0, -900, 90))
    k = 0
    for row in range(8):
        for col in range(-4, 5):
            if abs(col) > row // 2 + 2: continue
            plane_small(f'pl{k}', (col * 22 + (row % 2) * 8, -row * 26, random.uniform(-2, 2))).parent = form; k += 1
    form.keyframe_insert('location', frame=1); form.location.y = 900; form.keyframe_insert('location', frame=N - 60); lin(form)
    bomb = empty('bform', (0, -1600, 260))
    for i, (x, y) in enumerate(((0, 0), (-60, -50), (60, -50), (-120, -100), (120, -100))):
        b29(f'b{i}', (x, y, 0), heading=0, frames=N).parent = bomb
    bomb.keyframe_insert('location', frame=120); bomb.location.y = 500; bomb.keyframe_insert('location', frame=N); lin(bomb)
    cam = camera(lens=24)
    cam_key(cam, 1, (90, -260, 14), (0, 0, 40))
    cam_key(cam, N, (80, -240, 12), (0, 120, 110))


exec(open(os.path.join(HERE, 'cowra_shots.py'), encoding='utf8').read())  # Cowra breakout shots (share helpers + SHOTS)


if __name__ == '__main__':
    SHOTS[SHOT]()
    if MODE.startswith('stills:'):
        render(OUT, still=[int(x) for x in MODE.split(':')[1].split(',')])
    else:
        render(os.path.join(OUT, SHOT))
