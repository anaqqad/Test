"""Faceted anatomical mannequins from MPFB (MakeHuman, CC0 base mesh) - the Kaktus figure look.

One template body is generated per Blender run, helpers removed, decimated to ~2k faces (flat facets),
then every Figure is a cheap copy (shared mesh, own armature, own colours).
Front of the body = -Y in rest pose. Heading 0 means facing -Y; use face_to() / walk() for directions.
"""
import bpy, math, random
from mathutils import Vector, Euler
from math import radians as R
import kit
from kit import ROLE, mat, box, sphere, cyl, FPS

_T = {}
OUTFITS = []          # set before the first Human() of a run, e.g. human.OUTFITS = ['male_casualsuit03', 'shoes01']
import os as _os
SMOOTH = _os.environ.get('KK_SMOOTH') == '1'   # 2026-11-15 ref look: smooth glossy mannequins, denser mesh
CLOTH_RATIO = 0.6 if SMOOTH else 0.25
CLOTHES_DIR = r'C:/Users/anass/AppData/Roaming/Blender Foundation/Blender/4.2/extensions/.user/blender_org/mpfb/data/clothes'


def cloth_mat(oname, tint, rough=0.85):
    """Principled material: MPFB diffuse texture x tint (glTF-friendly multiply = baseColorFactor)."""
    key = f'cl_{oname}_{tint[0]:.2f}_{tint[1]:.2f}_{tint[2]:.2f}'
    if key in bpy.data.materials: return bpy.data.materials[key]
    m = bpy.data.materials.new(key); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = rough
    import os
    png = f'{CLOTHES_DIR}/{oname}/{oname}_diffuse.png'
    if os.path.exists(png):
        img = bpy.data.images.load(png, check_existing=True)
        if tuple(tint) != (1, 1, 1):   # bake the tint into a copy (glTF drops Mix nodes): out = tint * (0.5 + luminance)
            import numpy as np
            w, hgt = img.size
            px = np.empty(w * hgt * 4, dtype=np.float32); img.pixels.foreach_get(px); px = px.reshape(-1, 4)
            lum = px[:, :3] @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
            for c in range(3): px[:, c] = np.clip(tint[c] * (0.5 + lum), 0, 1)
            img = bpy.data.images.new(key, w, hgt, alpha=True); img.pixels.foreach_set(px.ravel())
            img.filepath_raw = os.path.join(os.environ.get('TEMP', 'C:/Temp'), key + '.png'); img.file_format = 'PNG'; img.save()
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = img
        nt.links.new(t.outputs['Color'], b.inputs['Base Color'])
    else:
        b.inputs['Base Color'].default_value = (*tint, 1)
    return m
SKIN_GROUPS = ('head', 'neck', 'jaw', 'eye', 'wrist', 'finger', 'metacarpal', 'special', 'oris', 'levator',
               'orbicularis', 'temporalis', 'oculi', 'risorius', 'tongue')


def _apply(obj, mod_name):
    with bpy.context.temp_override(object=obj, active_object=obj, selected_objects=[obj], selected_editable_objects=[obj]):
        bpy.ops.object.modifier_apply(modifier=mod_name)


def template(ratio=0.10, height=1.8):
    if 'h' in _T: return _T['h'], _T['rig']
    if SMOOTH: ratio = 0.35
    from bl_ext.blender_org.mpfb.services.humanservice import HumanService
    macro = {"gender": 1.0, "age": 0.5, "muscle": 0.62, "weight": 0.55, "proportions": 0.6, "height": 0.6,
             "cupsize": 0.5, "firmness": 0.5, "race": {"asian": 0.33, "caucasian": 0.34, "african": 0.33}}
    h = HumanService.create_human(scale=0.1, macro_detail_dict=macro)
    rig = HumanService.add_builtin_rig(h, 'default')
    clothes = {}
    helper_masks = {m.name for m in h.modifiers if m.type == 'MASK'}   # MPFB's own helper mask (keep applying it)
    for oname in OUTFITS:   # MPFB CC0 clothes, fitted on the full base mesh (mhclo needs the original vertex ids)
        before = set(bpy.data.objects)
        try:
            HumanService.add_mhclo_asset(f"{CLOTHES_DIR}/{oname}/{oname}.mhclo", h, asset_type="Clothes", subdiv_levels=0,
                                         material_type="MAKESKIN", set_up_rigging=True, interpolate_weights=True)
        except Exception as e:
            print('[human] clothes failed', oname, e); continue
        new = [o for o in bpy.data.objects if o not in before and o.type == 'MESH']
        if new:
            clothes[oname] = new[0]
    if h.data.shape_keys:
        with bpy.context.temp_override(object=h, active_object=h):
            bpy.ops.object.shape_key_remove(all=True, apply_mix=True)
    # remove helper geometry: move mask first, apply it
    mask = [m for m in h.modifiers if m.type == 'MASK']
    for m in mask:
        if m.name not in helper_masks:   # clothes delete-masks: drop them (dressed exports drop the body faces anyway,
            h.modifiers.remove(m)        # and undressed figures - the white dead - need the whole body)
            continue
        with bpy.context.temp_override(object=h, active_object=h):
            bpy.ops.object.modifier_move_to_index(modifier=m.name, index=0)
        _apply(h, m.name)
    dec = h.modifiers.new('dec', 'DECIMATE'); dec.ratio = ratio; dec.use_collapse_triangulate = False
    with bpy.context.temp_override(object=h, active_object=h):
        bpy.ops.object.modifier_move_to_index(modifier='dec', index=0)
    _apply(h, 'dec')
    for p in h.data.polygons: p.use_smooth = SMOOTH
    # material slots: 0 body, 1 skin (head/neck/hands); faces assigned once from vertex groups
    h.data.materials.clear()
    h.data.materials.append(mat('tpl_body', (0.5, 0.5, 0.5))); h.data.materials.append(mat('tpl_skin', (0.5, 0.5, 0.5)))
    bones = {b.name for b in rig.data.bones}
    deform = {g.index for g in h.vertex_groups if g.name in bones}
    skin_idx = {g.index for g in h.vertex_groups if g.index in deform and g.name.split('.')[0].rstrip('0123456789-').lower().startswith(SKIN_GROUPS)}
    vskin = []
    for v in h.data.vertices:
        w_skin = sum(g.weight for g in v.groups if g.group in skin_idx); w_all = sum(g.weight for g in v.groups if g.group in deform) or 1
        vskin.append(w_skin / w_all > 0.5)
    for p in h.data.polygons:
        p.material_index = 1 if sum(vskin[i] for i in p.vertices) * 2 > len(p.vertices) else 0
    for oname, c in clothes.items():   # same faceted look: decimate, flat shading, own textured material
        for m in [m for m in c.modifiers if m.type not in ('ARMATURE',)]:
            try:
                _apply(c, m.name)
            except Exception:
                c.modifiers.remove(m)
        if c.data.shape_keys:
            with bpy.context.temp_override(object=c, active_object=c):
                bpy.ops.object.shape_key_remove(all=True, apply_mix=True)
        d = c.modifiers.new('dec', 'DECIMATE'); d.ratio = CLOTH_RATIO; d.use_collapse_triangulate = False
        with bpy.context.temp_override(object=c, active_object=c):
            bpy.ops.object.modifier_move_to_index(modifier='dec', index=0)
        _apply(c, 'dec')
        for p in c.data.polygons: p.use_smooth = SMOOTH
        c.data.materials.clear(); c.data.materials.append(cloth_mat(oname, (1, 1, 1)))
        c.hide_render = True
    s = height / max(0.01, h.dimensions.z)
    rig.scale = (s, s, s)
    rig.hide_render = True; h.hide_render = True
    _T['clothes'] = clothes
    rig.location = (0, 0, -1000); _T.update(h=h, rig=rig, faces=len(h.data.polygons))
    print('[human] template faces', len(h.data.polygons))
    return h, rig


class Human:
    """A posable faceted mannequin. role colours: see kit.ROLE.
    kit: 'plain' (whole body role colour), 'clothed' (body=cloth colour, head/hands=role colour),
         'soldier' (cloth=olive + helmet + vest), 'tactical' (cloth=black + helmet), 'masked' (head=white hood)."""

    def __init__(self, name, role='blue', loc=(0, 0, 0), heading=0, kit_='plain', cloth=None, height=1.8, ratio=0.10,
                 outfit=None):
        """outfit: [(mpfb clothes name, tint rgb), ...] - real fitted clothes (template must have them in OUTFITS);
        the body faces under them (slot 0) are dropped at export (self.dressed)."""
        h, rig = template(ratio)
        self.name = name
        self.rig = rig.copy(); self.rig.data = rig.data.copy(); self.rig.name = name + '_rig'
        bpy.context.scene.collection.objects.link(self.rig)
        self.rig.hide_render = False
        self.mesh = h.copy(); self.mesh.name = name + '_mesh'
        bpy.context.scene.collection.objects.link(self.mesh)
        self.mesh.hide_render = False
        self.mesh.parent = self.rig
        for m in self.mesh.modifiers:
            if m.type == 'ARMATURE': m.object = self.rig
        sk = ROLE[role]
        cl = {'plain': sk, 'clothed': ROLE.get(cloth or 'grey'), 'soldier': (0.17, 0.17, 0.12),
              'tactical': ROLE['black'], 'masked': ROLE.get(cloth or 'sand')}.get(kit_, sk)
        if cloth and kit_ in ('soldier', 'tactical'): cl = ROLE.get(cloth, cl)
        body_m = mat(f'{name}_b', cl, rough=0.62); skin_m = mat(f'{name}_s', sk, rough=0.28 if SMOOTH else 0.5)
        self.mesh.material_slots[0].link = 'OBJECT'; self.mesh.material_slots[0].material = body_m
        self.mesh.material_slots[1].link = 'OBJECT'; self.mesh.material_slots[1].material = skin_m
        self.rig.location = loc; self.rig.rotation_euler = Euler((0, 0, R(heading)))
        for pb in self.rig.pose.bones: pb.rotation_mode = 'XYZ'
        if kit_ in ('soldier', 'tactical'):
            gear = mat(f'{name}_g', (0.09, 0.10, 0.07) if kit_ == 'soldier' else (0.02, 0.02, 0.022), rough=0.8)
            hm = sphere(f'{name}_helmet', 0.112, (0, 0, 0), (0.98, 0.82, 1.08), gear, seg=14, rings=7)
            self._bone_child(hm, 'head', (0, 0.10, -0.012))
        if kit_ == 'masked':
            hood = mat(f'{name}_hood', (0.85, 0.84, 0.80), rough=0.8)
            hm = sphere(f'{name}_hood', 0.118, (0, 0, 0), (0.92, 1.0, 1.15), hood, seg=12, rings=8)
            self._bone_child(hm, 'head', (0, 0.085, -0.01))
        self.dressed = False
        for oname, tint in (outfit or []):
            src = _T.get('clothes', {}).get(oname)
            if src is None:
                print('[human] outfit not in template', oname); continue
            c = src.copy(); c.data = src.data; c.name = f'{name}_cl_{oname}'
            bpy.context.scene.collection.objects.link(c)
            c.hide_render = False
            par = self.mesh if src.parent is _T['h'] else self.rig
            c.parent = par; c.matrix_parent_inverse = src.matrix_parent_inverse.copy()
            for m in c.modifiers:
                if m.type == 'ARMATURE': m.object = self.rig
            c.material_slots[0].link = 'OBJECT'; c.material_slots[0].material = cloth_mat(oname, tint)
            if not oname.startswith(('shoes', 'fedora')): self.dressed = True
        if not self.dressed:   # the template's clothes mask hides the body under them: undressed figures need it off
            for m in self.mesh.modifiers:
                if m.type == 'MASK': m.show_viewport = m.show_render = False
        self.pose('stand')

    def _bone_child(self, obj, bone, offset=(0, 0, 0)):
        """Attach obj to a bone. offset is in the bone's rest frame relative to the bone HEAD
        (x: right, y: along the bone, z: bone Z). Works at rest pose; follows the bone afterwards."""
        from mathutils import Matrix
        bpy.context.view_layer.update()
        b = self.rig.data.bones[bone]
        rest = self.rig.matrix_world @ b.matrix_local            # bone head frame in world (rest)
        tail = rest @ Matrix.Translation((0, b.length, 0))        # BONE parenting is relative to the tail
        obj.parent = self.rig; obj.parent_type = 'BONE'; obj.parent_bone = bone
        obj.matrix_parent_inverse = tail.inverted()
        obj.matrix_world = rest @ Matrix.Translation(offset) @ Matrix.Diagonal((*obj.scale, 1.0)).to_4x4() if False else rest @ Matrix.Translation(offset)
        return obj

    def prop(self, obj, bone='wrist.R', offset=(0, 0.05, 0), rot=(0, 0, 0)):
        self._bone_child(obj, bone, offset); obj.rotation_euler = Euler([R(a) for a in rot]); return obj

    # ----- pose library (degrees, bone-local XYZ; legs: -X forward, knee +X bends; arms: +X forward, L Z- lowers, R Z+ lowers)
    POSES = {
        'stand': {'upperarm01.L': (0, 0, -38), 'upperarm01.R': (0, 0, 38), 'lowerarm01.L': (12, 0, 0), 'lowerarm01.R': (12, 0, 0)},
        'rifle': {'upperarm01.L': (65, 0, -15), 'lowerarm01.L': (35, 0, 0), 'upperarm01.R': (45, 0, 10), 'lowerarm01.R': (95, 0, 0),
                  'spine03': (6, 0, 0), 'head': (8, 0, 0)},
        'hands_up': {'upperarm01.L': (0, 0, 118), 'upperarm01.R': (0, 0, -118), 'lowerarm01.L': (25, 0, 0), 'lowerarm01.R': (25, 0, 0)},
        'hands_head': {'upperarm01.L': (20, 0, 55), 'upperarm01.R': (20, 0, -55), 'lowerarm01.L': (130, 0, 0), 'lowerarm01.R': (130, 0, 0), 'head': (18, 0, 0)},
        'point': {'upperarm01.L': (0, 0, -38), 'lowerarm01.L': (12, 0, 0), 'upperarm01.R': (80, 0, 15), 'lowerarm01.R': (5, 0, 0)},
        'wave': {'upperarm01.L': (0, 0, -38), 'upperarm01.R': (10, 0, -70), 'lowerarm01.R': (40, 0, 0)},
        'kneel': {'upperleg01.L': (-80, 0, 0), 'lowerleg01.L': (90, 0, 0), 'upperleg01.R': (10, 0, 0), 'lowerleg01.R': (95, 0, 0),
                  'upperarm01.L': (0, 0, -38), 'upperarm01.R': (0, 0, 38), 'root': (0, 0, 0)},
        'crouch': {'upperleg01.L': (-75, 0, 0), 'lowerleg01.L': (120, 0, 0), 'upperleg01.R': (-75, 0, 0), 'lowerleg01.R': (120, 0, 0),
                   'foot.L': (-40, 0, 0), 'foot.R': (-40, 0, 0), 'spine03': (25, 0, 0), 'upperarm01.L': (40, 0, -30), 'upperarm01.R': (40, 0, 30)},
        'brace': {'upperarm01.L': (60, 0, -10), 'upperarm01.R': (60, 0, 10), 'lowerarm01.L': (70, 0, 0), 'lowerarm01.R': (70, 0, 0),
                  'spine03': (22, 0, 0), 'head': (20, 0, 0), 'upperleg01.L': (-20, 0, 0), 'lowerleg01.L': (30, 0, 0)},
        'radio': {'upperarm01.L': (0, 0, -38), 'upperarm01.R': (40, 0, -20), 'lowerarm01.R': (135, 0, 0), 'head': (-5, 0, 10)},
        'sit': {'upperleg01.L': (-90, 0, 0), 'lowerleg01.L': (90, 0, 0), 'upperleg01.R': (-90, 0, 0), 'lowerleg01.R': (90, 0, 0),
                'upperarm01.L': (20, 0, -35), 'upperarm01.R': (20, 0, 35), 'lowerarm01.L': (40, 0, 0), 'lowerarm01.R': (40, 0, 0)},
        'lie': {'upperarm01.L': (0, 0, -20), 'upperarm01.R': (0, 0, 20)},
        # ---- story poses (embassy rebuild, static tableaux)
        'sit_head': {'upperleg01.L': (-90, 0, 0), 'lowerleg01.L': (90, 0, 0), 'upperleg01.R': (-90, 0, 0), 'lowerleg01.R': (90, 0, 0), 'head': (12, 0, 0)},
        'sit_tied': {'upperleg01.L': (-90, 0, 0), 'lowerleg01.L': (90, 0, 0), 'upperleg01.R': (-90, 0, 0), 'lowerleg01.R': (90, 0, 0), 'spine03': (-4, 0, 0), 'head': (15, 0, 0)},
        'sit_phone': {'upperleg01.L': (-90, 0, 0), 'lowerleg01.L': (90, 0, 0), 'upperleg01.R': (-90, 0, 0), 'lowerleg01.R': (90, 0, 0), 'head': (-5, 0, 10)},
        'sit_floor': {'upperleg01.L': (-80, 0, 8), 'lowerleg01.L': (115, 0, 0), 'upperleg01.R': (-80, 0, -8), 'lowerleg01.R': (115, 0, 0), 'spine03': (18, 0, 0), 'head': (10, 0, 0)},
        'kneel_head': {'upperleg01.L': (-5, 0, 0), 'lowerleg01.L': (100, 0, 0), 'upperleg01.R': (-5, 0, 0), 'lowerleg01.R': (100, 0, 0), 'foot.L': (35, 0, 0), 'foot.R': (35, 0, 0), 'head': (15, 0, 0)},
        'aim_down': {'upperleg01.L': (-18, 0, 0), 'lowerleg01.L': (10, 0, 0), 'upperleg01.R': (12, 0, 0), 'spine03': (12, 0, 0), 'head': (22, 0, 0)},
        'rifle_down': {'upperleg01.L': (-18, 0, 0), 'lowerleg01.L': (10, 0, 0), 'upperleg01.R': (12, 0, 0), 'spine03': (16, 0, 0), 'head': (26, 0, 0)},
        'tackle': {'upperleg01.L': (-55, 0, 0), 'lowerleg01.L': (65, 0, 0), 'upperleg01.R': (28, 0, 0), 'lowerleg01.R': (25, 0, 0), 'spine03': (32, 0, 0), 'spine01': (10, 0, 0), 'head': (-10, 0, 0)},
        'fall': {'upperleg01.L': (-35, 0, 0), 'lowerleg01.L': (45, 0, 0), 'upperleg01.R': (10, 0, 0), 'spine03': (-22, 0, 0), 'head': (-25, 0, 0)},
        'throw': {'upperleg01.L': (-32, 0, 0), 'lowerleg01.L': (22, 0, 0), 'upperleg01.R': (18, 0, 0), 'lowerleg01.R': (10, 0, 0), 'spine03': (-6, 0, -10)},
        'swing': {'upperleg01.L': (-25, 0, 0), 'lowerleg01.L': (15, 0, 0), 'upperleg01.R': (15, 0, 0), 'spine03': (-12, 0, 0), 'head': (-10, 0, 0)},
        'run': {'upperleg01.L': (-58, 0, 0), 'lowerleg01.L': (35, 0, 0), 'upperleg01.R': (32, 0, 0), 'lowerleg01.R': (85, 0, 0), 'foot.R': (-20, 0, 0), 'spine03': (16, 0, 0)},
        'run_rifle': {'upperleg01.L': (-50, 0, 0), 'lowerleg01.L': (35, 0, 0), 'upperleg01.R': (30, 0, 0), 'lowerleg01.R': (75, 0, 0), 'spine03': (14, 0, 0), 'head': (-8, 0, 0)},
        'walk_hands': {'upperleg01.L': (-24, 0, 0), 'lowerleg01.L': (8, 0, 0), 'upperleg01.R': (20, 0, 0), 'lowerleg01.R': (30, 0, 0), 'head': (12, 0, 0)},
        'crouch_cover': {'upperleg01.L': (-80, 0, 0), 'lowerleg01.L': (125, 0, 0), 'upperleg01.R': (-80, 0, 0), 'lowerleg01.R': (125, 0, 0), 'foot.L': (-40, 0, 0), 'foot.R': (-40, 0, 0), 'spine03': (45, 0, 0), 'head': (30, 0, 0)},
        'abseil': {'upperleg01.L': (-82, 0, 6), 'lowerleg01.L': (15, 0, 0), 'upperleg01.R': (-82, 0, -6), 'lowerleg01.R': (15, 0, 0), 'spine03': (-8, 0, 0), 'head': (-15, 0, 0)},
        'lie_back': {'upperleg01.R': (-25, 0, 0), 'lowerleg01.R': (40, 0, 0), 'head': (0, 0, 25)},
        'lie_sprawl': {'upperleg01.L': (-35, 0, 10), 'lowerleg01.L': (60, 0, 0), 'head': (0, 0, -30)},
        'lie_side': {'upperleg01.L': (-55, 0, 0), 'lowerleg01.L': (70, 0, 0), 'upperleg01.R': (-35, 0, 0), 'lowerleg01.R': (50, 0, 0), 'spine03': (15, 0, 0)},
    }

    # Arm aims in BODY space: x = character's LEFT, -y = FORWARD, +z = UP. Chains are aimed upper -> lower.
    DIRS = {
        'stand':      {'upperarm01.L': (0.20, 0.02, -1), 'lowerarm01.L': (0.10, -0.18, -1), 'upperarm01.R': (-0.20, 0.02, -1), 'lowerarm01.R': (-0.10, -0.18, -1)},
        'rifle':      {'upperarm01.R': (-0.55, -0.25, -0.55), 'lowerarm01.R': (0.55, -0.75, 0.30), 'upperarm01.L': (0.15, -0.80, -0.45), 'lowerarm01.L': (-0.30, -0.95, 0.10)},
        'rifle_low':  {'upperarm01.R': (-0.30, -0.15, -0.95), 'lowerarm01.R': (0.55, -0.80, -0.15), 'upperarm01.L': (0.20, -0.45, -0.85), 'lowerarm01.L': (-0.35, -0.90, 0.05)},
        'hands_up':   {'upperarm01.L': (0.45, 0.0, 1), 'lowerarm01.L': (0.15, 0.0, 1), 'upperarm01.R': (-0.45, 0.0, 1), 'lowerarm01.R': (-0.15, 0.0, 1)},
        'hands_head': {'upperarm01.L': (0.6, 0.1, 0.8), 'lowerarm01.L': (-0.8, 0.1, 0.6), 'upperarm01.R': (-0.6, 0.1, 0.8), 'lowerarm01.R': (0.8, 0.1, 0.6)},
        'point':      {'upperarm01.L': (0.20, 0.02, -1), 'lowerarm01.L': (0.10, -0.18, -1), 'upperarm01.R': (-0.20, -1.0, 0.12), 'lowerarm01.R': (-0.15, -1.0, 0.15)},
        'radio':      {'upperarm01.L': (0.20, 0.02, -1), 'lowerarm01.L': (0.10, -0.18, -1), 'upperarm01.R': (-0.55, -0.35, -0.45), 'lowerarm01.R': (0.25, -0.15, 1.0)},
        'wave':       {'upperarm01.L': (0.20, 0.02, -1), 'lowerarm01.L': (0.10, -0.18, -1), 'upperarm01.R': (-0.85, -0.1, 0.45), 'lowerarm01.R': (-0.15, -0.15, 1.0)},
        'brace':      {'upperarm01.L': (0.30, -0.80, 0.20), 'lowerarm01.L': (-0.55, -0.35, 0.75), 'upperarm01.R': (-0.30, -0.80, 0.20), 'lowerarm01.R': (0.55, -0.35, 0.75)},
        'kneel':      {'upperarm01.L': (0.15, -0.30, -0.95), 'lowerarm01.L': (0.0, -0.75, -0.6), 'upperarm01.R': (-0.15, -0.20, -1), 'lowerarm01.R': (-0.1, -0.5, -0.85)},
        'crouch':     {'upperarm01.L': (0.20, -0.60, -0.75), 'lowerarm01.L': (-0.1, -0.95, -0.2), 'upperarm01.R': (-0.20, -0.60, -0.75), 'lowerarm01.R': (0.1, -0.95, -0.2)},
        'sit':        {'upperarm01.L': (0.20, -0.30, -0.95), 'lowerarm01.L': (0.0, -1.0, -0.15), 'upperarm01.R': (-0.20, -0.30, -0.95), 'lowerarm01.R': (0.0, -1.0, -0.15)},
        'lie':        {'upperarm01.L': (0.35, 0.0, -1), 'lowerarm01.L': (0.35, 0.0, -1), 'upperarm01.R': (-0.35, 0.0, -1), 'lowerarm01.R': (-0.35, 0.0, -1)},
        'sit_head':   {'upperarm01.L': (0.6, 0.1, 0.8), 'lowerarm01.L': (-0.8, 0.1, 0.6), 'upperarm01.R': (-0.6, 0.1, 0.8), 'lowerarm01.R': (0.8, 0.1, 0.6)},
        'sit_tied':   {'upperarm01.L': (0.25, 0.45, -0.85), 'lowerarm01.L': (-0.75, 0.55, -0.1), 'upperarm01.R': (-0.25, 0.45, -0.85), 'lowerarm01.R': (0.75, 0.55, -0.1)},
        'sit_phone':  {'upperarm01.L': (0.20, -0.30, -0.95), 'lowerarm01.L': (0.0, -1.0, -0.15), 'upperarm01.R': (-0.55, -0.35, -0.45), 'lowerarm01.R': (0.25, -0.15, 1.0)},
        'sit_floor':  {'upperarm01.L': (0.2, -0.55, -0.75), 'lowerarm01.L': (-0.55, -0.75, 0.1), 'upperarm01.R': (-0.2, -0.55, -0.75), 'lowerarm01.R': (0.55, -0.75, 0.1)},
        'kneel_head': {'upperarm01.L': (0.6, 0.1, 0.8), 'lowerarm01.L': (-0.8, 0.1, 0.6), 'upperarm01.R': (-0.6, 0.1, 0.8), 'lowerarm01.R': (0.8, 0.1, 0.6)},
        'aim_down':   {'upperarm01.R': (-0.15, -0.85, -0.5), 'lowerarm01.R': (-0.05, -0.85, -0.52), 'upperarm01.L': (0.25, -0.75, -0.6), 'lowerarm01.L': (-0.55, -0.7, -0.35)},
        'rifle_down': {'upperarm01.R': (-0.55, -0.25, -0.75), 'lowerarm01.R': (0.5, -0.7, -0.3), 'upperarm01.L': (0.15, -0.75, -0.65), 'lowerarm01.L': (-0.3, -0.85, -0.4)},
        'tackle':     {'upperarm01.L': (0.3, -0.92, 0.15), 'lowerarm01.L': (-0.35, -0.85, 0.35), 'upperarm01.R': (-0.3, -0.92, 0.15), 'lowerarm01.R': (0.35, -0.85, 0.35)},
        'fall':       {'upperarm01.L': (0.75, 0.15, 0.65), 'lowerarm01.L': (0.3, -0.2, 0.95), 'upperarm01.R': (-0.75, 0.15, 0.65), 'lowerarm01.R': (-0.3, -0.2, 0.95)},
        'throw':      {'upperarm01.R': (-0.45, 0.55, 0.7), 'lowerarm01.R': (-0.1, -0.25, 1.0), 'upperarm01.L': (0.25, -0.9, 0.25), 'lowerarm01.L': (0.05, -0.9, 0.4)},
        'swing':      {'upperarm01.L': (0.2, 0.15, 1.0), 'lowerarm01.L': (-0.3, 0.45, 0.85), 'upperarm01.R': (-0.2, 0.15, 1.0), 'lowerarm01.R': (0.3, 0.45, 0.85)},
        'run':        {'upperarm01.L': (0.15, -0.65, -0.7), 'lowerarm01.L': (0.0, -0.9, 0.45), 'upperarm01.R': (-0.15, 0.6, -0.75), 'lowerarm01.R': (0.0, 0.1, -1.0)},
        'run_rifle':  {'upperarm01.R': (-0.30, -0.15, -0.95), 'lowerarm01.R': (0.55, -0.80, -0.15), 'upperarm01.L': (0.20, -0.45, -0.85), 'lowerarm01.L': (-0.35, -0.90, 0.05)},
        'walk_hands': {'upperarm01.L': (0.6, 0.1, 0.8), 'lowerarm01.L': (-0.8, 0.1, 0.6), 'upperarm01.R': (-0.6, 0.1, 0.8), 'lowerarm01.R': (0.8, 0.1, 0.6)},
        'crouch_cover': {'upperarm01.L': (0.75, -0.55, 0.35), 'lowerarm01.L': (-0.6, -0.2, 0.75), 'upperarm01.R': (-0.75, -0.55, 0.35), 'lowerarm01.R': (0.6, -0.2, 0.75)},
        'abseil':     {'upperarm01.L': (0.2, -0.55, 0.8), 'lowerarm01.L': (-0.15, -0.7, 0.7), 'upperarm01.R': (-0.2, -0.55, 0.8), 'lowerarm01.R': (0.15, -0.7, 0.7)},
        'lie_back':   {'upperarm01.L': (0.8, 0.0, -0.6), 'lowerarm01.L': (0.6, -0.3, -0.75), 'upperarm01.R': (-0.45, 0.0, -0.9), 'lowerarm01.R': (-0.2, -0.4, -0.9)},
        'lie_sprawl': {'upperarm01.L': (1.0, -0.2, 0.15), 'lowerarm01.L': (0.8, -0.5, 0.3), 'upperarm01.R': (-0.9, -0.3, 0.4), 'lowerarm01.R': (-0.5, -0.4, 0.75)},
        'lie_side':   {'upperarm01.L': (0.2, -0.8, -0.5), 'lowerarm01.L': (0.1, -0.9, 0.3), 'upperarm01.R': (-0.2, -0.8, -0.5), 'lowerarm01.R': (-0.1, -0.9, 0.3)},
    }

    def aim(self, bone, direction):
        """Rotate a pose bone so its Y axis points along `direction` (armature/body space)."""
        pb = self.rig.pose.bones[bone]
        pb.rotation_euler = Euler((0, 0, 0)); bpy.context.view_layer.update()
        M = pb.matrix.copy(); y = Vector(M.col[1][:3]).normalized()
        q = y.rotation_difference(Vector(direction).normalized())
        rot = (q.to_matrix() @ M.to_3x3()).to_4x4(); rot.translation = M.translation
        pb.matrix = rot; bpy.context.view_layer.update()

    def pose(self, p, frame=None):
        d = self.POSES.get(p, {}) if isinstance(p, str) else p
        for pb in self.rig.pose.bones:
            if pb.name in d or pb.name in self._touched():
                pb.rotation_euler = Euler([R(a) for a in d.get(pb.name, (0, 0, 0))])
                if frame is not None: pb.keyframe_insert('rotation_euler', frame=frame)
        if isinstance(p, str) and p in self.DIRS:
            for b, dv in self.DIRS[p].items():
                self.aim(b, dv)
                if frame is not None: self.rig.pose.bones[b].keyframe_insert('rotation_euler', frame=frame)
        if isinstance(p, str) and p in ('lie_back', 'lie_sprawl', 'lie_side'):
            if p == 'lie_back': self.rig.rotation_euler.x = R(-90)
            elif p == 'lie_sprawl': self.rig.rotation_euler.x = R(90)
            else: self.rig.rotation_euler.y = R(90)
        if p == 'lie':
            self.rig.rotation_euler.x = R(90); self.rig.location.z = 0.14
            if frame is not None:
                self.rig.keyframe_insert('rotation_euler', frame=frame); self.rig.keyframe_insert('location', frame=frame)

    _T_BONES = None

    def _touched(self):
        if Human._T_BONES is None:
            s = set()
            for d in self.POSES.values(): s |= set(d)
            s |= {'upperleg01.L', 'upperleg01.R', 'lowerleg01.L', 'lowerleg01.R', 'foot.L', 'foot.R', 'spine03', 'spine01', 'neck01'}
            Human._T_BONES = s
        return Human._T_BONES

    def key(self, frame, loc=None, heading=None, pose=None):
        if loc is not None: self.rig.location = loc
        if heading is not None: self.rig.rotation_euler.z = R(heading)
        self.rig.keyframe_insert('location', frame=frame); self.rig.keyframe_insert('rotation_euler', frame=frame)
        if pose is not None: self.pose(pose, frame)

    @staticmethod
    def heading_to(p0, p1):
        d = Vector(p1) - Vector(p0)
        return math.degrees(math.atan2(d.x, -d.y))  # body front is -Y

    def walk(self, f0, f1, p0, p1, speed='walk', upper=None, phase=0.0):
        p0, p1 = Vector(p0), Vector(p1); d = p1 - p0
        hd = self.heading_to(p0, p1)
        stride = 1.45 if speed == 'walk' else 2.7
        cycles = max(0.5, d.length / stride)
        hip, knee, arm = (24, 38, 20) if speed == 'walk' else (42, 85, 48)
        lean = 4 if speed == 'walk' else 16
        z0 = p0.z
        for f in range(f0, f1 + 1, 2):
            t = (f - f0) / max(1, f1 - f0); ph = t * cycles * 2 * math.pi + phase
            s, c = math.sin(ph), math.cos(ph)
            self.rig.location = p0 + d * t; self.rig.location.z = z0 + 0.025 * abs(c)
            self.rig.rotation_euler.z = R(hd)
            self.rig.keyframe_insert('location', frame=f); self.rig.keyframe_insert('rotation_euler', frame=f)
            P = {'upperleg01.L': (-hip * s, 0, 0), 'upperleg01.R': (hip * s, 0, 0),
                 'lowerleg01.L': (knee * max(0, c) + 5, 0, 0), 'lowerleg01.R': (knee * max(0, -c) + 5, 0, 0),
                 'foot.L': (-8 * max(0, c), 0, 0), 'foot.R': (-8 * max(0, -c), 0, 0),
                 'upperarm01.L': (arm * s, 0, -38), 'upperarm01.R': (-arm * s, 0, 38),
                 'lowerarm01.L': (15 + 12 * max(0, s), 0, 0), 'lowerarm01.R': (15 + 12 * max(0, -s), 0, 0),
                 'spine03': (lean, 0, 0), 'spine01': (0, 3 * s, 0)}
            if upper: P.update(upper)
            self.pose(P, frame=f)
        return hd
