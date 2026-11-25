"""Kaktus-style 3D reconstruction kit for Blender 4.2 (run with blender -b -P shot.py).

Look: miniature diorama tiles floating in a black void, faceted clay mannequins colour-coded by role,
low-poly vehicles, soft key light + spotlight pools, shallow depth of field, AgX grade.
Everything is procedural: no downloaded models.
"""
import bpy, bmesh, math, random, sys, os
from mathutils import Vector, Euler
from math import radians as R

FPS = 24
ROLE = {  # colour code used across a video (keep it fixed for a whole episode)
    'blue':   (0.06, 0.20, 0.95),   # protagonists / victims / friendly force
    'red':    (0.80, 0.03, 0.03),   # hostile / perpetrator (head + hands only, body clothed)
    'yellow': (0.95, 0.72, 0.08),   # third party / civilians / negotiators
    'white':  (0.82, 0.82, 0.80),   # dead / neutral crowd
    'grey':   (0.35, 0.36, 0.38),
    'black':  (0.025, 0.025, 0.028),
    'olive':  (0.16, 0.18, 0.11),
    'sand':   (0.55, 0.45, 0.30),
    'navy':   (0.30, 0.32, 0.34),
}

# ---------------------------------------------------------------- scene / render

def reset(frames=120, res=(1920, 1080), engine='EEVEE', samples=64):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, frames
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    if engine == 'CYCLES':
        sc.render.engine = 'CYCLES'
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'OPTIX'; prefs.get_devices()
        for d in prefs.devices: d.use = d.type == 'OPTIX'
        sc.cycles.device = 'GPU'; sc.cycles.samples = samples
        sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPTIX'
    else:
        sc.render.engine = 'BLENDER_EEVEE_NEXT'
        e = sc.eevee
        e.taa_render_samples = samples
        e.use_shadows = True
        e.use_raytracing = True
        e.ray_tracing_options.resolution_scale = '2'
        e.use_volumetric_shadows = True
        e.volumetric_tile_size = '8'; e.volumetric_samples = 48
    sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.view_settings.exposure = 0.0
    w = bpy.data.worlds.new('void'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.004, 0.004, 0.005, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 1.0
    sc.render.image_settings.file_format = 'PNG'
    sc.render.film_transparent = False
    return sc


def world(color=(0.004, 0.004, 0.005), strength=1.0):
    n = bpy.context.scene.world.node_tree.nodes['Background']
    n.inputs[0].default_value = (*color, 1); n.inputs[1].default_value = strength


def glare_comp(threshold=1.2, mix=-0.75, vignette=0.35, grain=0.03):
    """Compositor: soft bloom on lights/fire, vignette, light grain (Kaktus frames are clean but filmic)."""
    sc = bpy.context.scene; sc.use_nodes = True
    t = sc.node_tree; t.nodes.clear()
    rl = t.nodes.new('CompositorNodeRLayers')
    gl = t.nodes.new('CompositorNodeGlare'); gl.glare_type = 'FOG_GLOW'; gl.quality = 'HIGH'
    gl.threshold = threshold; gl.mix = mix; gl.size = 8
    # vignette: ellipse mask -> blur -> multiply
    em = t.nodes.new('CompositorNodeEllipseMask'); em.width = 1.05; em.height = 0.95
    bl = t.nodes.new('CompositorNodeBlur'); bl.filter_type = 'FAST_GAUSS'
    bl.use_relative = True; bl.factor_x = bl.factor_y = 0.35
    mx = t.nodes.new('CompositorNodeMixRGB'); mx.blend_type = 'MULTIPLY'
    inv = t.nodes.new('CompositorNodeMath'); inv.operation = 'MULTIPLY_ADD'
    inv.inputs[1].default_value = vignette; inv.inputs[2].default_value = 1 - vignette
    out = t.nodes.new('CompositorNodeComposite')
    t.links.new(rl.outputs['Image'], gl.inputs['Image'])
    t.links.new(em.outputs['Mask'], bl.inputs['Image'])
    t.links.new(bl.outputs['Image'], inv.inputs[0])
    t.links.new(gl.outputs['Image'], mx.inputs[1]); t.links.new(inv.outputs[0], mx.inputs[2])
    mx.inputs[0].default_value = 1.0
    t.links.new(mx.outputs['Image'], out.inputs['Image'])


# ---------------------------------------------------------------- materials

_MATS = {}
REG = {}  # python-side handles (props, rotors) by object name

def mat(name, color=(0.5, 0.5, 0.5), rough=0.65, metal=0.0, emit=None, emit_strength=0.0, alpha=1.0):
    key = (name, color, rough, metal, emit, emit_strength)
    if key in _MATS: return _MATS[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1)
        b.inputs['Emission Strength'].default_value = emit_strength
    _MATS[key] = m
    return m


def noise_mat(name, c1, c2, scale=8.0, rough=0.9, bump=0.25, detail=6.0):
    """Ground / terrain material: two-tone noise with bump (salt flat, dirt, concrete)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale
    nz.inputs['Detail'].default_value = detail; nz.inputs['Roughness'].default_value = 0.6
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].color = (*c1, 1); cr.color_ramp.elements[1].color = (*c2, 1)
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = rough
    return m


def set_mat(obj, m):
    obj.data.materials.clear(); obj.data.materials.append(m)
    return obj

# ---------------------------------------------------------------- primitives

def _link(o, parent=None):
    if o.name not in bpy.context.scene.collection.objects:
        try: bpy.context.scene.collection.objects.link(o)
        except RuntimeError: pass
    if parent is not None:
        o.parent = parent
    return o


def box(name, size, loc=(0, 0, 0), m=None, parent=None, bevel=0.0, rot=(0, 0, 0)):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); _link(o, parent)
    o.location = loc; o.rotation_euler = Euler([R(a) for a in rot])
    if bevel:
        bv = o.modifiers.new('bv', 'BEVEL'); bv.width = bevel; bv.segments = 2
    if m: set_mat(o, m)
    return o


def cyl(name, r1, r2, depth, verts=8, loc=(0, 0, 0), m=None, parent=None, rot=(0, 0, 0), smooth=False, axis_down=False):
    """Cone/cylinder. axis_down=True: base at origin, extends along -Z (limb style)."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r1, radius2=r2, depth=depth)
    if axis_down:
        for v in bm.verts: v.co.z -= depth / 2
        # flip so r1 is at top (joint) and r2 at the bottom
        for v in bm.verts: v.co.z = -depth - v.co.z
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); _link(o, parent)
    o.location = loc; o.rotation_euler = Euler([R(a) for a in rot])
    for p in me.polygons: p.use_smooth = smooth
    if m: set_mat(o, m)
    return o


def sphere(name, r, loc=(0, 0, 0), scale=(1, 1, 1), m=None, parent=None, seg=10, rings=7, smooth=False):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); _link(o, parent)
    o.location = loc; o.scale = scale
    for p in me.polygons: p.use_smooth = smooth
    if m: set_mat(o, m)
    return o


def empty(name, loc=(0, 0, 0), parent=None, rot=(0, 0, 0)):
    o = bpy.data.objects.new(name, None); o.empty_display_size = 0.05
    _link(o, parent); o.location = loc; o.rotation_euler = Euler([R(a) for a in rot])
    return o

# ---------------------------------------------------------------- mannequin

JOINTS = ['pelvis', 'spine', 'chest', 'neck', 'head',
          'shoulder_L', 'elbow_L', 'wrist_L', 'shoulder_R', 'elbow_R', 'wrist_R',
          'hip_L', 'knee_L', 'ankle_L', 'hip_R', 'knee_R', 'ankle_R']


class Figure:
    """Faceted clay mannequin (1.8 m). Faces +Y. Joint empties take Euler XYZ in degrees.
    Limb +X rotation swings forward; knee bends with negative X; elbow bends with positive X.
    kit: 'plain' | 'soldier' (helmet, vest) | 'tactical' (black body, coloured head+hands) | 'masked'
    """

    def __init__(self, name, role='blue', loc=(0, 0, 0), heading=0, kit='plain', height=1.8, accent=None):
        self.name = name; s = height / 1.8; self.s = s
        body = mat(f'{name}_body', ROLE[role] if kit in ('plain',) else ROLE.get(accent or 'black'), rough=0.55)
        skin = mat(f'{name}_skin', ROLE[role], rough=0.5)
        if kit == 'soldier':
            body = mat(f'{name}_fat', ROLE.get(accent or 'olive'), rough=0.85)
            skin = mat(f'{name}_skin', ROLE[role], rough=0.5)
        self.root = empty(f'{name}_root', loc); self.root.rotation_euler.z = R(heading)
        J = self.j = {}
        J['pelvis'] = empty(f'{name}_pelvis', (0, 0, 0.98 * s), self.root)
        J['spine'] = empty(f'{name}_spine', (0, 0, 0.10 * s), J['pelvis'])
        J['chest'] = empty(f'{name}_chest', (0, 0, 0.24 * s), J['spine'])
        J['neck'] = empty(f'{name}_neck', (0, 0, 0.30 * s), J['chest'])
        J['head'] = empty(f'{name}_head', (0, 0, 0.07 * s), J['neck'])
        # pelvis + abdomen + chest blocks (tapered, faceted)
        cyl(f'{name}_pelvis_m', 0.16 * s, 0.15 * s, 0.20 * s, 8, (0, 0, 0.02 * s), body, J['pelvis']).scale = (1, 0.72, 1)
        cyl(f'{name}_abd_m', 0.135 * s, 0.15 * s, 0.22 * s, 8, (0, 0, 0.11 * s), body, J['spine']).scale = (1, 0.7, 1)
        ch = cyl(f'{name}_chest_m', 0.14 * s, 0.20 * s, 0.32 * s, 8, (0, 0, 0.15 * s), body, J['chest']); ch.scale = (1, 0.62, 1)
        cyl(f'{name}_neck_m', 0.05 * s, 0.055 * s, 0.10 * s, 6, (0, 0, 0.0), skin, J['neck'])
        hd = sphere(f'{name}_head_m', 0.105 * s, (0, 0.01 * s, 0.10 * s), (0.86, 0.95, 1.18), skin, J['head'], seg=10, rings=7)
        self.parts = [ch, hd]
        for side, sx in (('L', 1), ('R', -1)):
            J[f'shoulder_{side}'] = empty(f'{name}_shoulder_{side}', (sx * 0.20 * s, 0, 0.27 * s), J['chest'])
            J[f'elbow_{side}'] = empty(f'{name}_elbow_{side}', (0, 0, -0.29 * s), J[f'shoulder_{side}'])
            J[f'wrist_{side}'] = empty(f'{name}_wrist_{side}', (0, 0, -0.26 * s), J[f'elbow_{side}'])
            sphere(f'{name}_shball_{side}', 0.062 * s, (0, 0, 0), m=body, parent=J[f'shoulder_{side}'], seg=8, rings=5)
            cyl(f'{name}_uarm_{side}', 0.055 * s, 0.045 * s, 0.29 * s, 7, m=body, parent=J[f'shoulder_{side}'], axis_down=True)
            cyl(f'{name}_farm_{side}', 0.045 * s, 0.035 * s, 0.26 * s, 7, m=skin if kit == 'plain' else body, parent=J[f'elbow_{side}'], axis_down=True)
            hand = box(f'{name}_hand_{side}', (0.035 * s, 0.075 * s, 0.17 * s), (0, 0, -0.085 * s), skin, J[f'wrist_{side}'])
            J[f'hip_{side}'] = empty(f'{name}_hip_{side}', (sx * 0.095 * s, 0, -0.04 * s), J['pelvis'])
            J[f'knee_{side}'] = empty(f'{name}_knee_{side}', (0, 0, -0.45 * s), J[f'hip_{side}'])
            J[f'ankle_{side}'] = empty(f'{name}_ankle_{side}', (0, 0, -0.44 * s), J[f'knee_{side}'])
            cyl(f'{name}_thigh_{side}', 0.085 * s, 0.06 * s, 0.45 * s, 8, m=body, parent=J[f'hip_{side}'], axis_down=True)
            cyl(f'{name}_shin_{side}', 0.06 * s, 0.045 * s, 0.44 * s, 8, m=body, parent=J[f'knee_{side}'], axis_down=True)
            foot_m = mat(f'{name}_boot', ROLE['black'] if kit != 'plain' else ROLE[role], rough=0.7)
            box(f'{name}_foot_{side}', (0.09 * s, 0.24 * s, 0.07 * s), (0, 0.06 * s, -0.045 * s), foot_m, J[f'ankle_{side}'], bevel=0.01)
        if kit in ('soldier', 'tactical'):
            gear = mat(f'{name}_gear', ROLE['black'] if kit == 'tactical' else (0.10, 0.11, 0.07), rough=0.8)
            sphere(f'{name}_helmet', 0.125 * s, (0, 0.0, 0.13 * s), (0.95, 1.05, 0.8), gear, J['head'], seg=10, rings=6)
            box(f'{name}_vest', (0.36 * s, 0.25 * s, 0.30 * s), (0, 0.0, 0.16 * s), gear, J['chest'], bevel=0.02)
        self.pose('stand')

    # ---- posing
    POSES = {
        'stand': {'shoulder_L': (0, -6, 0), 'shoulder_R': (0, 6, 0), 'elbow_L': (8, 0, 0), 'elbow_R': (8, 0, 0)},
        'rifle': {'shoulder_L': (62, 0, -18), 'elbow_L': (40, 0, 0), 'shoulder_R': (40, 0, 30), 'elbow_R': (75, 0, 0),
                  'neck': (8, 0, 0), 'chest': (4, 0, 8)},
        'hands_up': {'shoulder_L': (0, -150, 0), 'shoulder_R': (0, 150, 0), 'elbow_L': (0, 0, 0), 'elbow_R': (0, 0, 0)},
        'point': {'shoulder_R': (85, 0, 0), 'elbow_R': (5, 0, 0)},
        'kneel': {'hip_L': (85, 0, 0), 'knee_L': (-95, 0, 0), 'hip_R': (-5, 0, 0), 'knee_R': (-85, 0, 0), 'ankle_R': (30, 0, 0)},
        'crouch': {'hip_L': (70, 0, 0), 'knee_L': (-120, 0, 0), 'hip_R': (70, 0, 0), 'knee_R': (-120, 0, 0),
                   'ankle_L': (45, 0, 0), 'ankle_R': (45, 0, 0), 'chest': (25, 0, 0)},
        'hands_head': {'shoulder_L': (60, -120, 0), 'shoulder_R': (60, 120, 0), 'elbow_L': (120, 0, 0), 'elbow_R': (120, 0, 0), 'neck': (20, 0, 0)},
        'lie': {},
        'brace': {'shoulder_L': (50, -30, 0), 'shoulder_R': (50, 30, 0), 'elbow_L': (60, 0, 0), 'elbow_R': (60, 0, 0),
                  'chest': (20, 0, 0), 'hip_L': (20, 0, 0), 'hip_R': (-10, 0, 0), 'knee_L': (-30, 0, 0), 'knee_R': (-20, 0, 0)},
        'wave': {'shoulder_R': (0, 150, 0), 'elbow_R': (0, 0, -30)},
    }

    def pose(self, name_or_dict, frame=None, blend=None):
        p = self.POSES.get(name_or_dict, {}) if isinstance(name_or_dict, str) else name_or_dict
        for jn, e in self.j.items():
            if jn == 'pelvis': continue
            rot = p.get(jn, (0, 0, 0))
            e.rotation_euler = Euler([R(a) for a in rot])
            if frame is not None: e.keyframe_insert('rotation_euler', frame=frame)
        if isinstance(name_or_dict, str) and name_or_dict == 'lie':
            self.j['pelvis'].rotation_euler = Euler((R(-90), 0, 0)); self.j['pelvis'].location.z = 0.12 * self.s
            if frame is not None:
                self.j['pelvis'].keyframe_insert('rotation_euler', frame=frame); self.j['pelvis'].keyframe_insert('location', frame=frame)

    def key_root(self, frame, loc=None, heading=None):
        if loc is not None: self.root.location = loc
        if heading is not None: self.root.rotation_euler.z = R(heading)
        self.root.keyframe_insert('location', frame=frame); self.root.keyframe_insert('rotation_euler', frame=frame)

    def walk(self, f0, f1, p0, p1, speed='walk', upper=None):
        """Walk/run from p0 to p1 between frames f0..f1 with a procedural gait. upper: pose dict kept on the arms."""
        p0, p1 = Vector(p0), Vector(p1)
        d = p1 - p0; heading = math.degrees(math.atan2(-d.x, d.y))
        stride = 1.5 if speed == 'walk' else 2.6           # metres per full cycle (2 steps)
        dist = d.length; cycles = max(1, dist / stride)
        amp = (26, 35, 22) if speed == 'walk' else (45, 80, 55)  # hip, knee, arm swing
        lean = 3 if speed == 'walk' else 14
        steps = int((f1 - f0)); keystep = 2
        for f in range(f0, f1 + 1, keystep):
            t = (f - f0) / max(1, (f1 - f0)); ph = t * cycles * 2 * math.pi
            self.root.location = p0 + d * t; self.root.rotation_euler.z = R(heading)
            self.root.keyframe_insert('location', frame=f); self.root.keyframe_insert('rotation_euler', frame=f)
            s = math.sin(ph); c = math.cos(ph)
            P = {'hip_L': (amp[0] * s, 0, 0), 'hip_R': (-amp[0] * s, 0, 0),
                 'knee_L': (-amp[1] * max(0, -c) - 6, 0, 0), 'knee_R': (-amp[1] * max(0, c) - 6, 0, 0),
                 'ankle_L': (10 * max(0, -c), 0, 0), 'ankle_R': (10 * max(0, c), 0, 0),
                 'shoulder_L': (-amp[2] * s, -6, 0), 'shoulder_R': (amp[2] * s, 6, 0),
                 'elbow_L': (15 + 10 * max(0, s), 0, 0), 'elbow_R': (15 + 10 * max(0, -s), 0, 0),
                 'spine': (lean, 0, 0), 'chest': (0, 0, 4 * s)}
            if upper: P.update(upper)
            self.pose(P, frame=f)
            self.j['pelvis'].location.z = 0.98 * self.s + 0.025 * abs(c) * self.s
            self.j['pelvis'].keyframe_insert('location', frame=f)

    def hold(self, frame, pose='stand', loc=None, heading=None):
        if loc is not None or heading is not None: self.key_root(frame, loc, heading)
        self.pose(pose, frame=frame)

# ---------------------------------------------------------------- vehicles

def c130(name='c130', loc=(0, 0, 0), heading=0, color=(0.30, 0.31, 0.30), props_spin=True, frames=240):
    """Lockheed C-130 at 1:1 (span 40.4 m, length 29.8 m, height 11.6 m), low-poly. Nose faces +Y."""
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    skin = mat(f'{name}_skin', color, rough=0.55, metal=0.15)
    dark = mat(f'{name}_dark', (0.03, 0.03, 0.035), rough=0.4)
    glass = mat(f'{name}_glass', (0.02, 0.03, 0.04), rough=0.1, metal=0.4)
    fz = 3.0  # fuselage centre height
    cyl(f'{name}_fus', 2.1, 2.1, 21.0, 16, (0, 0, fz), skin, root, rot=(90, 0, 0), smooth=True)
    nose = sphere(f'{name}_nose', 2.1, (0, 10.5, fz), (1, 1.9, 0.95), skin, root, seg=16, rings=10, smooth=True)
    sphere(f'{name}_cockpit', 1.5, (0, 10.8, fz + 0.9), (1.05, 1.2, 0.6), glass, root, seg=14, rings=8, smooth=True)
    tail = cyl(f'{name}_tailcone', 2.1, 0.5, 8.5, 16, (0, -14.6, fz + 1.4), skin, root, rot=(-81, 0, 0), smooth=True)
    # high wing + engines + props
    box(f'{name}_wing', (40.4, 4.2, 0.45), (0, 1.0, fz + 2.15), skin, root, bevel=0.15)
    props = []
    for x in (-10.1, -5.2, 5.2, 10.1):
        cyl(f'{name}_nac{x}', 0.75, 0.6, 6.5, 12, (x, 2.6, fz + 1.7), skin, root, rot=(90, 0, 0), smooth=True)
        hub = empty(f'{name}_prop{x}', (x, 6.0, fz + 1.7), root)
        sphere(f'{name}_spin{x}', 0.45, (0, 0, 0), (1, 1.4, 1), dark, hub, seg=10, rings=6, smooth=True)
        for k in range(4):
            bl = box(f'{name}_blade{x}_{k}', (0.32, 0.08, 2.05), (0, 0, 1.0), dark, empty(f'{name}_bp{x}_{k}', (0, 0, 0), hub, rot=(0, k * 90, 0)))
        if props_spin:
            hub.rotation_euler.y = 0; hub.keyframe_insert('rotation_euler', frame=1)
            hub.rotation_euler.y = R(360 * 17 * frames / FPS); hub.keyframe_insert('rotation_euler', frame=frames + 1)
            for fc in hub.animation_data.action.fcurves:
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
        props.append(hub)
    REG[name] = {'props': props}
    # tail surfaces
    box(f'{name}_fin', (0.4, 5.5, 6.2), (0, -15.5, fz + 5.3), skin, root, bevel=0.1, rot=(-12, 0, 0))
    box(f'{name}_hstab', (16.0, 3.2, 0.3), (0, -16.3, fz + 2.6), skin, root, bevel=0.1)
    # gear sponsons + wheels
    for sx in (-1, 1):
        box(f'{name}_sponson{sx}', (1.2, 6.5, 1.6), (sx * 2.05, -0.5, 1.4), skin, root, bevel=0.3)
        for y in (-1.6, 0.9):
            cyl(f'{name}_wheel{sx}{y}', 0.6, 0.6, 0.5, 14, (sx * 2.1, y, 0.6), dark, root, rot=(0, 90, 0), smooth=True)
    cyl(f'{name}_nosewheel', 0.45, 0.45, 0.4, 12, (0, 9.0, 0.45), dark, root, rot=(0, 90, 0), smooth=True)
    return root


def rh53(name='rh53', loc=(0, 0, 0), heading=0, color=(0.47, 0.40, 0.29), rotor_rpm=180, frames=240, spin=True, alt=0.0):
    """Sikorsky RH-53D Sea Stallion (rotor 22 m, 7 blades; fuselage ~20 m), low-poly. Nose +Y."""
    root = empty(name, (loc[0], loc[1], loc[2] + alt)); root.rotation_euler.z = R(heading)
    skin = mat(f'{name}_skin', color, rough=0.75)
    dark = mat(f'{name}_dark', (0.025, 0.025, 0.03), rough=0.5)
    glass = mat(f'{name}_glass', (0.02, 0.03, 0.04), rough=0.08, metal=0.5)
    box(f'{name}_body', (2.7, 12.0, 3.0), (0, 0.5, 2.4), skin, root, bevel=0.55)
    box(f'{name}_nose', (2.5, 3.0, 2.3), (0, 7.4, 2.0), skin, root, bevel=0.7)
    box(f'{name}_wind', (2.3, 1.2, 1.0), (0, 8.2, 2.85), glass, root, bevel=0.3, rot=(30, 0, 0))
    box(f'{name}_hump', (1.8, 5.0, 1.2), (0, 0.8, 4.3), skin, root, bevel=0.4)
    boom = cyl(f'{name}_boom', 1.1, 0.45, 8.0, 10, (0, -8.6, 3.6), skin, root, rot=(-80, 0, 0), smooth=True)
    box(f'{name}_pylon', (0.35, 1.8, 3.6), (0, -12.6, 5.6), skin, root, bevel=0.1, rot=(-15, 0, 0))
    for sx in (-1, 1):
        box(f'{name}_spon{sx}', (1.1, 4.0, 1.0), (sx * 1.85, 0.6, 1.3), skin, root, bevel=0.35)
        cyl(f'{name}_mw{sx}', 0.38, 0.38, 0.3, 12, (sx * 1.9, 0.8, 0.4), dark, root, rot=(0, 90, 0), smooth=True)
    cyl(f'{name}_nw', 0.3, 0.3, 0.25, 12, (0, 6.8, 0.32), dark, root, rot=(0, 90, 0), smooth=True)
    mast = empty(f'{name}_mast', (0, 1.0, 5.15), root)
    cyl(f'{name}_hub', 0.5, 0.35, 0.5, 10, (0, 0, 0), dark, mast)
    for k in range(7):
        a = empty(f'{name}_ba{k}', (0, 0, 0.1), mast, rot=(0, 0, k * 360 / 7))
        box(f'{name}_blade{k}', (0.6, 10.8, 0.06), (0, 5.6, 0), dark, a)
    tr = empty(f'{name}_trotor', (-0.5, -13.2, 6.6), root, rot=(0, 0, 0))
    for k in range(4):
        a = empty(f'{name}_tb{k}', (0, 0, 0), tr, rot=(k * 90, 0, 0))
        box(f'{name}_tblade{k}', (0.06, 0.3, 2.0), (0, 0, 1.0), dark, a)
    REG[name] = {'mast': mast, 'trotor': tr}
    if spin:
        for e, axis, turns in ((mast, 2, rotor_rpm / 60 * frames / FPS), (tr, 0, rotor_rpm * 4.6 / 60 * frames / FPS)):
            e.keyframe_insert('rotation_euler', frame=1)
            e.rotation_euler[axis] = R(360 * turns); e.keyframe_insert('rotation_euler', frame=frames + 1)
            for fc in e.animation_data.action.fcurves:
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    return root


def bus(name='bus', loc=(0, 0, 0), heading=0, color=(0.75, 0.70, 0.55)):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    skin = mat(f'{name}_skin', color, rough=0.6); dark = mat(f'{name}_d', (0.03, 0.03, 0.03), rough=0.3)
    box(f'{name}_b', (2.5, 11.0, 2.6), (0, 0, 1.9), skin, root, bevel=0.25)
    box(f'{name}_win', (2.55, 9.5, 0.8), (0, 0.3, 2.55), dark, root, bevel=0.05)
    for y in (-3.5, 3.6):
        for sx in (-1, 1): cyl(f'{name}_w{y}{sx}', 0.5, 0.5, 0.35, 12, (sx * 1.2, y, 0.5), dark, root, rot=(0, 90, 0), smooth=True)
    hl = mat(f'{name}_hl', (1, 0.9, 0.7), emit=(1, 0.85, 0.6), emit_strength=30)
    for sx in (-0.85, 0.85): box(f'{name}_hl{sx}', (0.35, 0.05, 0.2), (sx, 5.52, 1.1), hl, root)
    return root


def truck(name='truck', loc=(0, 0, 0), heading=0, color=(0.55, 0.12, 0.08)):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    skin = mat(f'{name}_s', color, rough=0.5); dark = mat(f'{name}_d', (0.03, 0.03, 0.03), rough=0.3)
    box(f'{name}_cab', (2.3, 2.2, 2.3), (0, 3.2, 1.6), skin, root, bevel=0.15)
    cyl(f'{name}_tank', 1.1, 1.1, 5.0, 16, (0, -0.6, 1.8), mat(f'{name}_t', (0.7, 0.7, 0.68), rough=0.35, metal=0.5), root, rot=(90, 0, 0), smooth=True)
    for y in (-2.2, 0.5, 3.2):
        for sx in (-1, 1): cyl(f'{name}_w{y}{sx}', 0.5, 0.5, 0.35, 12, (sx * 1.1, y, 0.5), dark, root, rot=(0, 90, 0), smooth=True)
    return root

# ---------------------------------------------------------------- sets

def diorama(name='tile', size=(140, 100), thick=4.0, top=None, side=(0.035, 0.03, 0.025), loc=(0, 0, 0), bevel=1.5):
    """Floating diorama tile: textured top, dark earth sides, rounded edges, sits with top at z=0."""
    top = top or noise_mat(f'{name}_top', (0.50, 0.46, 0.40), (0.68, 0.64, 0.57), scale=0.08, bump=0.15)
    o = box(name, (size[0], size[1], thick), (loc[0], loc[1], loc[2] - thick / 2), top, bevel=bevel)
    o.modifiers['bv'].segments = 4
    # side material via second slot on side faces
    sm = mat(f'{name}_side', side, rough=0.95)
    o.data.materials.append(sm)
    for p in o.data.polygons:
        if abs(p.normal.z) < 0.5: p.material_index = 1
    return o


def ground_marks(n=40, area=(120, 80), seed=3, m=None):
    """Tyre tracks / scuffs on the salt flat: thin dark strips."""
    random.seed(seed); m = m or mat('tracks', (0.30, 0.27, 0.23), rough=0.95)
    for i in range(n):
        x = random.uniform(-area[0] / 2, area[0] / 2); y = random.uniform(-area[1] / 2, area[1] / 2)
        box(f'trk{i}', (0.35, random.uniform(8, 30), 0.01), (x, y, 0.006), m, rot=(0, 0, random.uniform(-25, 25)))


def dust(name='dust', size=(160, 120, 30), loc=(0, 0, 12), density=0.015, color=(0.75, 0.62, 0.45), anim_frames=None):
    """Haboob / rotor-wash dust: volume box with drifting noise density."""
    o = box(name, size, loc)
    m = bpy.data.materials.new(name + '_vol'); m.use_nodes = True; nt = m.node_tree
    nt.nodes.remove(nt.nodes['Principled BSDF'])
    pv = nt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Color'].default_value = (*color, 1)
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.06; nz.inputs['Detail'].default_value = 4
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.35; mr.inputs['From Max'].default_value = 0.75
    mr.inputs['To Max'].default_value = density
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    nt.links.new(nz.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], pv.inputs['Density'])
    nt.links.new(pv.outputs['Volume'], nt.nodes['Material Output'].inputs['Volume'])
    if anim_frames:
        mp.inputs['Location'].default_value = (0, 0, 0); mp.inputs['Location'].keyframe_insert('default_value', frame=1)
        mp.inputs['Location'].default_value = (anim_frames * 0.25, 0, 0); mp.inputs['Location'].keyframe_insert('default_value', frame=anim_frames)
    set_mat(o, m)
    return o


def fireball(name='fire', loc=(0, 0, 0), f0=1, f1=40, r=6.0, light=True):
    """Stylised fire: emissive faceted blob that swells and flickers + flickering point light."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (1, 0.4, 0.05, 1)
    b.inputs['Emission Color'].default_value = (1.0, 0.42, 0.08, 1); b.inputs['Emission Strength'].default_value = 18
    o = sphere(name, 1.0, loc, (0.01, 0.01, 0.01), m, seg=12, rings=8)
    o.keyframe_insert('scale', frame=f0)
    o.scale = (r, r, r * 1.3); o.keyframe_insert('scale', frame=f0 + 6)
    o.scale = (r * 0.8, r * 0.8, r * 1.6); o.keyframe_insert('scale', frame=f1)
    if light:
        L = bpy.data.lights.new(name + '_L', 'POINT'); L.color = (1, 0.55, 0.2); L.shadow_soft_size = 2
        lo = bpy.data.objects.new(name + '_L', L); _link(lo); lo.location = (loc[0], loc[1], loc[2] + 3)
        random.seed(7)
        L.energy = 0; L.keyframe_insert('energy', frame=f0 - 1)
        for f in range(f0, f1 + 60, 2):
            L.energy = (2.5e6 if f < f0 + 8 else 6e5) * random.uniform(0.6, 1.0); L.keyframe_insert('energy', frame=f)
    return o

# ---------------------------------------------------------------- lights & camera

def area(name, loc, target=(0, 0, 0), energy=2000, size=10, color=(1, 1, 1)):
    L = bpy.data.lights.new(name, 'AREA'); L.energy = energy; L.size = size; L.color = color
    o = bpy.data.objects.new(name, L); _link(o); o.location = loc; aim(o, target)
    return o


def spot(name, loc, target=(0, 0, 0), energy=5e5, angle=40, blend=0.6, color=(1, 0.95, 0.85), soft=1.0):
    L = bpy.data.lights.new(name, 'SPOT'); L.energy = energy; L.spot_size = R(angle); L.spot_blend = blend
    L.color = color; L.shadow_soft_size = soft
    o = bpy.data.objects.new(name, L); _link(o); o.location = loc; aim(o, target)
    return o


def sun(name='moon', rot=(50, 0, 30), energy=0.6, color=(0.75, 0.82, 1.0), angle=2.0):
    L = bpy.data.lights.new(name, 'SUN'); L.energy = energy; L.color = color; L.angle = R(angle)
    o = bpy.data.objects.new(name, L); _link(o); o.rotation_euler = Euler([R(a) for a in rot])
    return o


def aim(o, target):
    d = Vector(target) - o.location
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def camera(lens=35, fstop=None, focus=None, sensor=36):
    c = bpy.data.cameras.new('cam'); c.lens = lens; c.sensor_width = sensor; c.clip_end = 5000; c.clip_start = 0.1
    o = bpy.data.objects.new('cam', c); _link(o); bpy.context.scene.camera = o
    if fstop:
        c.dof.use_dof = True; c.dof.aperture_fstop = fstop
        if isinstance(focus, (int, float)): c.dof.focus_distance = focus
        elif focus is not None: c.dof.focus_object = focus
    return o


def cam_key(cam, frame, loc, target, lens=None, focus=None):
    cam.location = loc; aim(cam, target); cam.keyframe_insert('location', frame=frame); cam.keyframe_insert('rotation_euler', frame=frame)
    if lens: cam.data.lens = lens; cam.data.keyframe_insert('lens', frame=frame)
    if isinstance(focus, (int, float)): cam.data.dof.focus_distance = focus; cam.data.dof.keyframe_insert('focus_distance', frame=frame)


def ease_all(kind='BEZIER', ease='EASE_IN_OUT'):
    for o in bpy.data.objects:
        ad = o.animation_data
        if ad and ad.action:
            for fc in ad.action.fcurves:
                for kp in fc.keyframe_points:
                    if kp.interpolation != 'LINEAR':
                        kp.interpolation = kind; kp.easing = ease


def orbit(cam, f0, f1, center, radius, height, a0, a1, lens=None, target_z=0.0, step=4):
    for f in range(f0, f1 + 1, step):
        t = (f - f0) / max(1, f1 - f0); a = R(a0 + (a1 - a0) * (3 * t * t - 2 * t * t * t))
        cam_key(cam, f, (center[0] + radius * math.sin(a), center[1] - radius * math.cos(a), height), (center[0], center[1], target_z), lens)


def render(out_dir, frames=None, still=None):
    sc = bpy.context.scene
    os.makedirs(out_dir, exist_ok=True)
    if still is not None:
        for f in (still if isinstance(still, (list, tuple)) else [still]):
            sc.frame_set(f); sc.render.filepath = os.path.join(out_dir, f'still_{f:04d}.png')
            bpy.ops.render.render(write_still=True)
        return
    sc.render.filepath = os.path.join(out_dir, 'f_')
    bpy.ops.render.render(animation=True)


def args():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    out = a[0] if a else os.path.join(os.getcwd(), 'out')
    still = None
    if len(a) > 1 and a[1] != 'anim':
        still = [int(x) for x in a[1].split(',')]
    return out, still


def fire(name='fire', loc=(0, 0, 0), size=(6, 6, 9), f0=1, f1=240, strength=60.0, light=True, smoke=True, grow=8, body=0.42, nscale=None, light_k=1.0):
    """Volumetric fire: 4D noise drives density + emission, rising and flickering, plus optional dark smoke column."""
    o = box(name, size, (loc[0], loc[1], loc[2] + size[2] / 2))
    m = bpy.data.materials.new(name + '_vol'); m.use_nodes = True; nt = m.node_tree
    nt.nodes.remove(nt.nodes['Principled BSDF'])
    pv = nt.nodes.new('ShaderNodeVolumePrincipled')
    pv.inputs['Color'].default_value = (0.05, 0.03, 0.02, 1)
    pv.inputs['Emission Color'].default_value = (1.0, 0.38, 0.06, 1)
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'
    nz.inputs['Scale'].default_value = nscale or 14.0 / max(size); nz.inputs['Detail'].default_value = 6; nz.inputs['Roughness'].default_value = 0.6
    shape = nt.nodes.new('ShaderNodeTexGradient'); shape.gradient_type = 'SPHERICAL'
    mp2 = nt.nodes.new('ShaderNodeMapping'); mp2.inputs['Location'].default_value = (-0.5, -0.5, -0.15)
    mp2.inputs['Scale'].default_value = (2.0, 2.0, 1.1)
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = body; mr.inputs['From Max'].default_value = body + 0.4
    dens = nt.nodes.new('ShaderNodeMath'); dens.operation = 'MULTIPLY'; dens.inputs[1].default_value = 6.0
    emi = nt.nodes.new('ShaderNodeMath'); emi.operation = 'MULTIPLY'; emi.inputs[1].default_value = strength
    L = nt.links
    L.new(tc.outputs['Object'], mp.inputs['Vector']); L.new(mp.outputs['Vector'], nz.inputs['Vector'])
    L.new(tc.outputs['Generated'], mp2.inputs['Vector']); L.new(mp2.outputs['Vector'], shape.inputs['Vector'])
    L.new(nz.outputs['Fac'], mul.inputs[0]); L.new(shape.outputs['Fac'], mul.inputs[1])
    L.new(mul.outputs['Value'], mr.inputs['Value'])
    L.new(mr.outputs['Result'], dens.inputs[0]); L.new(mr.outputs['Result'], emi.inputs[0])
    L.new(dens.outputs['Value'], pv.inputs['Density']); L.new(emi.outputs['Value'], pv.inputs['Emission Strength'])
    L.new(pv.outputs['Volume'], nt.nodes['Material Output'].inputs['Volume'])
    nz.inputs['W'].default_value = 0; nz.inputs['W'].keyframe_insert('default_value', frame=f0)
    nz.inputs['W'].default_value = (f1 - f0) / FPS * 1.6; nz.inputs['W'].keyframe_insert('default_value', frame=f1)
    mp.inputs['Location'].default_value = (0, 0, 0); mp.inputs['Location'].keyframe_insert('default_value', frame=f0)
    mp.inputs['Location'].default_value = (0, 0, -(f1 - f0) / FPS * 3.0); mp.inputs['Location'].keyframe_insert('default_value', frame=f1)
    for fc in m.node_tree.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    o.scale = (0.05, 0.05, 0.05); o.keyframe_insert('scale', frame=max(1, f0 - 1))
    o.scale = (1, 1, 1); o.keyframe_insert('scale', frame=f0 + grow)
    set_mat(o, m)
    if light:
        Lt = bpy.data.lights.new(name + '_L', 'POINT'); Lt.color = (1, 0.5, 0.18); Lt.shadow_soft_size = size[0] / 3
        lo = bpy.data.objects.new(name + '_L', Lt); _link(lo); lo.location = (loc[0], loc[1], loc[2] + size[2] * 0.35)
        random.seed(sum(map(ord, name)))
        Lt.energy = 0; Lt.keyframe_insert('energy', frame=max(1, f0 - 1))
        for f in range(f0, f1 + 1, 2):
            Lt.energy = (1.5e5 if f < f0 + 6 else 3.5e4) * random.uniform(0.65, 1.0) * (size[0] / 6) * light_k
            Lt.keyframe_insert('energy', frame=f)
    if smoke:
        s = dust(name + '_smoke', (size[0] * 2.0, size[1] * 2.0, size[2] * 3), (loc[0], loc[1], loc[2] + size[2] * 2.6),
                 density=0.0, color=(0.02, 0.02, 0.02), anim_frames=f1)
        mrs = [n for n in s.material_slots[0].material.node_tree.nodes if n.type == 'MAP_RANGE'][0]
        mrs.inputs['To Max'].default_value = 0.0; mrs.inputs['To Max'].keyframe_insert('default_value', frame=max(1, f0 - 1))
        mrs.inputs['To Max'].default_value = 0.12; mrs.inputs['To Max'].keyframe_insert('default_value', frame=f0 + 48)
    return o
