"""Cowra breakout 3D shots (24 Nov 2026). Imported at the end of scene.py: `from cowra_shots import *` is not used;
scene.py exec()s this file so the shots share its helpers and SHOTS registry.

No. 12 POW Compound: an octagon about 800 yards (730 m) across, four camps split by two crossing roads, wire about
8 ft high, six 30-ft towers (Long, The Final Campaigns, p. 623). B camp (Japanese) = the north-west quarter here;
"Broadway" = the east-west road. Positions are approximate: every shot is tagged on screen as a reconstruction."""

CR = 365.0
MAROON = (0.36, 0.10, 0.09)        # prisoners' maroon clothing (Weir account)
DRYGRASS = ((0.17, 0.18, 0.10), (0.27, 0.27, 0.15))
SKIN = (0.55, 0.47, 0.38)


def octa(r=CR, a0=22.5):
    return [(r * math.cos(R(a0 + 45 * k)), r * math.sin(R(a0 + 45 * k))) for k in range(8)]


def wire_line(name, p0, p1, spacing=6.0, h=2.45, coil=True):
    """Barbed-wire fence: posts, strands and a coil along the foot (8 ft)."""
    m = mat('wpost', (0.20, 0.17, 0.13), rough=0.9); w = mat('wire', (0.30, 0.30, 0.30), rough=0.5, metal=0.6)
    a, b = Vector((p0[0], p0[1], 0)), Vector((p1[0], p1[1], 0)); d = b - a; n = max(1, int(d.length / spacing))
    ang = math.degrees(math.atan2(d.y, d.x))
    for i in range(n + 1):
        q = a + d * (i / n); cyl(f'{name}_p{i}', 0.07, 0.07, h, 5, (q.x, q.y, h / 2), m)
    mid = (a + b) / 2
    for z in (0.35, 0.8, 1.25, 1.7, 2.15, 2.4):
        box(f'{name}_s{z}', (d.length, 0.015, 0.015), (mid.x, mid.y, z), w, rot=(0, 0, ang))
    if coil:
        c = cyl(f'{name}_coil', 0.45, 0.45, d.length, 10, (mid.x, mid.y, 0.45), mat('coil', (0.27, 0.27, 0.27), rough=0.5, metal=0.6), rot=(0, 90, ang))
        c.modifiers.new('wf', 'WIREFRAME').thickness = 0.03


def hut(name, loc, heading=0, size=(18, 6)):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    wall = mat('hwall', (0.55, 0.52, 0.45), rough=0.95); roof = mat('hroof', (0.40, 0.40, 0.40), rough=0.6, metal=0.3)
    box(f'{name}_w', (size[1], size[0], 2.6), (0, 0, 1.3), wall, root)
    for sx in (-1, 1):
        box(f'{name}_r{sx}', (size[1] * 0.56, size[0] + 0.4, 0.08), (sx * size[1] * 0.25, 0, 3.15), roof, root, rot=(0, sx * 18, 0))
    return root


def tower(name, loc):
    wood = mat('twood', (0.30, 0.25, 0.18), rough=0.9)
    for dx in (-1.2, 1.2):
        for dy in (-1.2, 1.2):
            cyl(f'{name}_l{dx}{dy}', 0.1, 0.1, 9.2, 5, (loc[0] + dx, loc[1] + dy, 4.6), wood)
    box(f'{name}_cab', (3.4, 3.4, 2.2), (loc[0], loc[1], 10.2), wood)
    box(f'{name}_rf', (4.2, 4.2, 0.2), (loc[0], loc[1], 11.5), mat('troof', (0.25, 0.25, 0.25), rough=0.6, metal=0.3))


def camp(detail=False):
    """The whole compound: ground, two roads, octagon wire, inner fences on the roads, huts in all four camps."""
    ground((2400, 2400), DRYGRASS, name='paddock')
    rd = mat('croad', (0.42, 0.38, 0.30), rough=0.95)
    box('broadway', (2 * CR + 40, 22, 0.05), (0, 0, 0.03), rd)          # east-west: "Broadway"
    box('nsroad', (14, 2 * CR + 40, 0.05), (0, 0, 0.03), rd)
    pts = octa(); band = mat('band', (0.08, 0.075, 0.06), rough=1.0)
    for i in range(8):
        wire_line(f'oc{i}', pts[i], pts[(i + 1) % 8], spacing=6 if detail else 10)
        a, b = pts[i], pts[(i + 1) % 8]
        box(f'ocb{i}', (math.hypot(b[0] - a[0], b[1] - a[1]) + 4, 6, 0.04), ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0.06), band,
            rot=(0, 0, math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))))
    for sy in (-1, 1):
        wire_line(f'bw{sy}a', (-CR + 30, sy * 12), (-9, sy * 12), spacing=12, coil=False)
        wire_line(f'bw{sy}b', (9, sy * 12), (CR - 30, sy * 12), spacing=12, coil=False)
    for sx in (-1, 1):
        wire_line(f'ns{sx}a', (sx * 9, 13), (sx * 9, CR - 30), spacing=12, coil=False)
        wire_line(f'ns{sx}b', (sx * 9, -13), (sx * 9, -CR + 30), spacing=12, coil=False)
    huts = []
    for qx, qy, nm in ((-1, 1, 'B'), (1, 1, 'A'), (1, -1, 'C'), (-1, -1, 'D')):
        for r in range(5):
            for c in range(4):
                x = qx * (60 + c * 40); y = qy * (50 + r * 28)
                if math.hypot(x, y) > CR - 60: continue
                huts.append(hut(f'h{nm}{r}{c}', (x, y, 0), heading=90))
    for k, a in enumerate((0, 60, 120, 180, 240, 300)):
        tower(f'tw{k}', ((CR + 12) * math.cos(R(a + 30)), (CR + 12) * math.sin(R(a + 30))))
    return huts


def flash(name, loc, f0, f1, every=3, size=0.35, energy=3e4):
    """Machine-gun muzzle flash: blinking emissive blob + point light."""
    m = mat(name + '_m', (1, 0.8, 0.4), emit=(1.0, 0.75, 0.35), emit_strength=40)
    o = sphere(name, size, loc, (1, 1, 1), m, seg=8, rings=5)
    L = bpy.data.lights.new(name + '_L', 'POINT'); L.color = (1, 0.7, 0.35)
    lo = bpy.data.objects.new(name + '_L', L); kit._link(lo); lo.location = loc
    for f in range(max(1, f0 - 1), f1 + 2):
        on = f0 <= f <= f1 and (f - f0) % every == 0
        o.scale = (1, 1, 1) if on else (0.001, 0.001, 0.001); o.keyframe_insert('scale', frame=f)
        L.energy = energy if on else 0; L.keyframe_insert('energy', frame=f)
    for fc in o.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
    return o


def night_sky(moon=0.12):
    world((0.006, 0.008, 0.014), 1.0)
    sun('moon', (55, 0, 200), moon, color=(0.6, 0.7, 1.0), angle=2)


def wire_lamps(pts, z=6.0, energy=2.5e4):
    for i, (x, y) in enumerate(pts):
        L = bpy.data.lights.new(f'lamp{i}', 'POINT'); L.energy = energy; L.color = (1.0, 0.86, 0.6); L.shadow_soft_size = 0.3
        o = bpy.data.objects.new(f'lamp{i}', L); kit._link(o); o.location = (x, y, z)
        cyl(f'lpole{i}', 0.08, 0.08, z, 5, (x, y, z / 2), mat('lpole', (0.2, 0.2, 0.2)))


def mob(prefix, n, area0, area1, f0, f1, seed=1, body=MAROON, stagger=40):
    """n figures run from a box area0 to a box area1 (x0, y0, x1, y1) with staggered starts, then hold."""
    random.seed(seed); figs = []
    for i in range(n):
        p0 = (random.uniform(area0[0], area0[2]), random.uniform(area0[1], area0[3]), 0)
        p1 = (random.uniform(area1[0], area1[2]), random.uniform(area1[1], area1[3]), 0)
        f = person(f'{prefix}{i}', p0, body=body, head=SKIN)
        s0 = f0 + random.randint(0, stagger); f.key_root(max(1, s0 - 1), p0)
        dist = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        f.walk(s0, max(s0 + 10, min(f1, s0 + int(dist / 5.5 * 30))), p0, p1, speed='run')
        figs.append(f)
    return figs


def b_closeup(night=True):
    """B camp's north-west corner at 1:1 for the night shots: huts, the outer wire, Broadway."""
    ground((900, 900), DRYGRASS, name='paddock')
    box('broadway', (900, 22, 0.05), (0, 0, 0.03), mat('croad', (0.42, 0.38, 0.30), rough=0.95))
    huts = []
    for r in range(4):
        for c in range(4):
            huts.append(hut(f'hb{r}{c}', (-60 - c * 30, 40 + r * 22, 0), heading=90))
    wire_line('outer', (-200, 30), (-200, 160), spacing=5)
    wire_line('outer2', (-200, 160), (-40, 200), spacing=5)
    wire_line('inner', (-200, 14), (-10, 14), spacing=6, coil=False)
    if night:
        night_sky(0.25); bpy.context.scene.view_settings.exposure = 1.1
        world((0.012, 0.016, 0.026), 1.0)
        wire_lamps([(-196, 60), (-196, 120), (-150, 172), (-90, 186), (-150, 18), (-80, 18), (-110, 70), (-110, 110)], energy=2.2e4)
    return huts


def vickers_trailer(name, loc, heading=0):
    root = empty(name, loc); root.rotation_euler.z = R(heading)
    m = mat('trail', (0.25, 0.27, 0.20), rough=0.7); k = mat('gunk', INK, rough=0.4, metal=0.5)
    box(f'{name}_bed', (2.0, 3.0, 0.15), (0, 0, 0.75), m, root)
    for sx in (-1, 1):
        for sy in (-0.9, 0.9):
            cyl(f'{name}_wh{sx}{sy}', 0.35, 0.35, 0.18, 10, (sx * 1.05, sy, 0.35), k, root, rot=(0, 90, 0))
    cyl(f'{name}_tri', 0.05, 0.05, 0.6, 5, (0, 0.4, 1.1), k, root)
    cyl(f'{name}_gun', 0.11, 0.11, 1.1, 8, (0, 0.8, 1.42), k, root, rot=(90, 0, 0))
    cyl(f'{name}_brl', 0.03, 0.03, 0.5, 6, (0, 1.6, 1.42), k, root, rot=(90, 0, 0))
    return root


def gums(n, xr, yr, seed=4, skip=None):
    random.seed(seed)
    trunk = mat('gum', (0.75, 0.72, 0.66), rough=0.8); leaf = mat('gleaf', (0.24, 0.29, 0.15), rough=0.9)
    for i in range(n):
        x = random.uniform(*xr); y = random.uniform(*yr)
        if skip and skip(x, y): continue
        hgt = random.uniform(7, 15)
        cyl(f'tr{i}', 0.25, 0.18, hgt, 5, (x, y, hgt / 2), trunk)
        sphere(f'cr{i}', random.uniform(2.5, 4.5), (x, y, hgt + 1), (1, 1, 0.7), leaf, seg=7, rings=4)


@shot
def s_zero():
    """19 Feb 1942: Toyoshima's damaged Zero comes down low over the bush of Melville Island and belly-lands."""
    N = 420; reset(frames=N, samples=16); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0)
    world((0.50, 0.58, 0.68), 0.6); sun('sun', (40, 0, 120), 2.4, color=(1.0, 0.95, 0.85), angle=3)
    ground((3000, 3000), ((0.16, 0.17, 0.09), (0.25, 0.24, 0.12)), name='scrub')
    box('sand', (3000, 120, 0.1), (0, -260, 0.02), mat('sand', (0.78, 0.70, 0.55), rough=0.95))
    box('tsea', (3000, 1400, 0.1), (0, -1020, -0.02), mat('tseam', (0.10, 0.30, 0.34), rough=0.2))
    gums(700, (-400, 500), (-150, 800), seed=11, skip=lambda x, y: abs(x - 60) < 18 and -150 < y < 330)
    z = fighter('zero', (60, 700, 45), heading=180, props=True, color=(0.30, 0.33, 0.25))
    z.location = (60, 700, 45); z.rotation_euler = (R(-6), R(8), R(180)); z.keyframe_insert('location', frame=1); z.keyframe_insert('rotation_euler', frame=1)
    z.location = (62, 320, 6); z.rotation_euler = (R(-3), R(-4), R(180)); z.keyframe_insert('location', frame=230); z.keyframe_insert('rotation_euler', frame=230)
    z.location = (60, 150, -0.6); z.rotation_euler = (R(2), R(3), R(186)); z.keyframe_insert('location', frame=300); z.keyframe_insert('rotation_euler', frame=300)
    z.location = (58, 95, -0.7); z.rotation_euler = (R(2), R(5), R(194)); z.keyframe_insert('location', frame=360); z.keyframe_insert('rotation_euler', frame=360)
    dust('dust1', (40, 80, 10), (60, 150, 4), density=0.02, color=(0.6, 0.5, 0.35), anim_frames=N)
    cam = camera(lens=55)
    cam_key(cam, 1, (95, 90, 8), (60, 700, 45), lens=150)
    cam_key(cam, 120, (92, 95, 7), (61, 480, 28), lens=120)
    cam_key(cam, 230, (88, 100, 5), (62, 320, 6), lens=75)
    cam_key(cam, 300, (86, 105, 4), (60, 150, 0.5), lens=55)
    cam_key(cam, N, (84, 108, 3.6), (58, 95, 0.5), lens=50)


@shot
def s_camp_day():
    """No. 12 POW Compound from the air: the octagon, four camps, Broadway and the crossing road, six towers."""
    N = 480; reset(frames=N, samples=16); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0)
    world((0.50, 0.56, 0.64), 0.6); sun('sun', (50, 0, 150), 2.2, color=(1.0, 0.96, 0.88), angle=3)
    camp()
    cam = camera(lens=30)
    orbit(cam, 1, N, (0, 0, 0), 560, 380, -40, 25, target_z=0)


@shot
def s_camp_night():
    """Night: lamps along the wire, tower lights sweeping B camp (north-west quarter)."""
    N = 420; reset(frames=N, samples=16); glare_comp(threshold=1.0, mix=-0.7, vignette=0.0); night_sky()
    camp(detail=True)
    pts = octa(); lamp_pts = []
    for i in (2, 3, 4):
        a, b = pts[i], pts[(i + 1) % 8]
        for t in (0.15, 0.5, 0.85): lamp_pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    lamp_pts += [(-x, 14) for x in (60, 140, 220, 300)]
    wire_lamps(lamp_pts)
    for k, a in enumerate((90, 150)):
        tx, ty = (CR + 12) * math.cos(R(a + 30)), (CR + 12) * math.sin(R(a + 30))
        sp = spot(f'beam{k}', (tx, ty, 11), (-150, 150, 0), energy=4e7, angle=12, blend=0.4, color=(1, 0.95, 0.8))
        for f in range(1, N + 1, 30):
            t = f / N; aim(sp, (-150 + 120 * math.sin(t * 6 + k), 150 + 110 * math.cos(t * 5 + k * 2), 0)); sp.keyframe_insert('rotation_euler', frame=f)
    cam = camera(lens=35)
    cam_key(cam, 1, (-520, 520, 160), (-160, 160, 0))
    cam_key(cam, N, (-430, 450, 120), (-170, 150, 0))


@shot
def s_bugle():
    """Just before 2 a.m.: a lone figure between the huts raises a bugle; men come out of the huts, dressed."""
    N = 390; reset(frames=N, samples=16); glare_comp(threshold=1.0, mix=-0.7, vignette=0.0)
    b_closeup()
    bug = person('bugler', (-105, 95, 0), heading=-90, body=MAROON, head=SKIN)
    bug.hold(1, 'stand'); bug.hold(120, 'stand')
    bug.hold(150, {'shoulder_R': (100, 0, 25), 'elbow_R': (110, 0, 0), 'neck': (-12, 0, 0)})
    brass = mat('brass', (0.85, 0.65, 0.25), rough=0.3, metal=0.9)
    cyl('bugle', 0.03, 0.07, 0.45, 8, (0, 0.30, 0.05), brass, bug.j['head'], rot=(80, 0, 0))
    mob('m', 36, (-160, 50, -70, 110), (-195, 60, -185, 150), 170, N, seed=4, stagger=120)
    cam = camera(lens=40)
    cam_key(cam, 1, (-74, 95, 1.7), (-105, 95, 1.5))
    cam_key(cam, 160, (-82, 95, 1.7), (-105, 95, 1.7))
    cam_key(cam, N, (-64, 93, 6), (-150, 98, 1))


@shot
def s_charge():
    """2 a.m.: the mobs run at the wire; blankets go over it; huts behind begin to burn."""
    N = 450; reset(frames=N, samples=16); glare_comp(threshold=1.0, mix=-0.7, vignette=0.0)
    huts = b_closeup(); bpy.context.scene.view_settings.exposure = 1.7
    mob('w', 70, (-170, 40, -90, 130), (-199, 40, -199, 150), 1, N, seed=7, stagger=90)
    mob('n', 50, (-150, 110, -60, 150), (-160, 168, -50, 195), 20, N, seed=9, stagger=90)
    bl = mat('blanket', (0.22, 0.20, 0.17), rough=0.95)
    random.seed(5)
    for i in range(14):
        y = random.uniform(50, 145); f0 = random.randint(120, 360)
        for side in (-1, 1):
            b = box(f'bl{i}{side}', (1.3, 1.9, 0.05), (-200 + side * 0.5, y, 1.95), bl, rot=(0, side * 58, random.uniform(-6, 6)))
            b.scale = (0.001, 0.001, 0.001); b.keyframe_insert('scale', frame=f0 - 1); b.scale = (1, 1, 1); b.keyframe_insert('scale', frame=f0 + 4)
    for i, h in enumerate(huts[::3]):
        fire(f'fire{i}', (h.location.x, h.location.y, 0), (8, 10, 7), f0=150 + i * 45, f1=N, strength=60, smoke=False, light_k=1.6)
    cam = camera(lens=32)
    cam_key(cam, 1, (-225, 72, 6), (-175, 95, 1))
    cam_key(cam, N, (-222, 112, 5), (-165, 100, 1.5))


@shot
def s_vickers():
    """The Vickers on its trailer outside the north-west wire: two guards in greatcoats run to it and fire."""
    N = 420; reset(frames=N, samples=16); glare_comp(threshold=1.0, mix=-0.7, vignette=0.0)
    b_closeup()
    vickers_trailer('vk', (-225, 120, 0), heading=90)
    gc = (0.30, 0.27, 0.18)
    g1 = person('hardy', (-250, 100, 0), body=gc, hat='cap'); g2 = person('jones', (-252, 96, 0), body=gc, hat='cap')
    g1.walk(1, 100, (-250, 100, 0), (-226.8, 119.5, 0), speed='run'); g2.walk(10, 112, (-252, 96, 0), (-226.6, 121.3, 0), speed='run')
    g1.hold(104, 'crouch', heading=-90); g2.hold(116, 'kneel', heading=-90)
    flash('mf', (-222.9, 120, 1.42), 130, N - 20, every=3)
    mob('x', 60, (-185, 60, -120, 170), (-205, 90, -198, 150), 140, N, seed=12, stagger=150)
    cam = camera(lens=35)
    cam_key(cam, 1, (-238, 110, 2.4), (-224, 121, 1.2))
    cam_key(cam, N, (-236, 131, 3.4), (-205, 115, 1.0))


@shot
def s_broadway():
    """Broadway under fire: men flat in the side ditch, huts burning behind them, flashes from the far side."""
    N = 390; reset(frames=N, samples=16); glare_comp(threshold=1.0, mix=-0.7, vignette=0.0)
    huts = b_closeup()
    box('ditch', (300, 2.6, 0.02), (-100, 12.5, 0.06), mat('ditchm', (0.07, 0.065, 0.05), rough=1.0))
    random.seed(21)
    for i in range(40):
        f = person(f'd{i}', (-180 + i * 4.2 + random.uniform(-1, 1), 12.5 + random.uniform(-0.6, 0.6), 0.07),
                   heading=random.choice((80, 100, -80)), body=MAROON, head=SKIN)
        f.pose('lie')
    for i, h in enumerate(huts[:8]):
        fire(f'fb{i}', (h.location.x, h.location.y, 0), (8, 10, 8), f0=1, f1=N, strength=60, smoke=False, light_k=1.4)
    for i, x in enumerate((-150, -90, -30)):
        flash(f'ff{i}', (x, -40, 1.5), 20 + i * 7, N, every=4 + i, energy=2e4)
    cam = camera(lens=30)
    cam_key(cam, 1, (-80, 1, 9), (-115, 14, 0))
    cam_key(cam, N, (-112, 2, 8), (-150, 14, 0))


@shot
def s_dawn():
    """5:30-6 a.m.: first light over Camp B; burnt hut floors smoking, the wire, the gun trailer."""
    N = 450; reset(frames=N, samples=16); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0)
    world((0.36, 0.34, 0.36), 0.8); sun('sun', (84, 0, 100), 1.6, color=(1.0, 0.72, 0.5), angle=4)
    ground((900, 900), DRYGRASS, name='paddock')
    box('broadway', (900, 22, 0.05), (0, 0, 0.03), mat('croad', (0.42, 0.38, 0.30), rough=0.95))
    ash = mat('ash', (0.07, 0.065, 0.06), rough=1.0); char = mat('char', (0.04, 0.035, 0.03), rough=1.0)
    random.seed(8)
    for r in range(4):
        for c in range(4):
            x, y = -60 - c * 30, 40 + r * 22
            box(f'ash{r}{c}', (6.5, 18.5, 0.12), (x, y, 0.06), ash)
            for k in range(5):
                cyl(f'st{r}{c}{k}', 0.12, 0.12, random.uniform(0.4, 1.6), 5, (x + random.uniform(-3, 3), y + random.uniform(-9, 9), 0.5), char)
            if (r + c) % 2 == 0:
                dust(f'sm{r}{c}', (6, 6, 30), (x, y, 15), density=0.012, color=(0.25, 0.25, 0.25), anim_frames=N)
    wire_line('outer', (-200, 30), (-200, 160), spacing=5)
    wire_line('outer2', (-200, 160), (-40, 200), spacing=5)
    vickers_trailer('vk', (-225, 120, 0), heading=90)
    cam = camera(lens=35)
    cam_key(cam, 1, (-20, -40, 14), (-110, 90, 2))
    cam_key(cam, N, (-50, -10, 9), (-130, 100, 2))


@shot
def s_farm():
    """5 Aug, morning: three escaped prisoners in maroon are led up the path to a farmhouse verandah."""
    N = 420; reset(frames=N, samples=16); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0)
    world((0.50, 0.56, 0.64), 0.6); sun('sun', (35, 0, 60), 2.2, color=(1.0, 0.94, 0.84), angle=3)
    ground((1200, 1200), DRYGRASS, name='paddock')
    wb = mat('weather', (0.78, 0.74, 0.66), rough=0.9); iron = mat('iron', (0.55, 0.56, 0.56), rough=0.4, metal=0.6)
    box('house', (14, 10, 3.2), (0, 0, 1.6), wb)
    for sx in (-1, 1):
        box(f'roof{sx}', (8.4, 11.4, 0.1), (sx * 3.5, 0, 4.4), iron, rot=(0, sx * 24, 0))
    box('vfloor', (14, 3, 0.3), (0, -6.5, 0.4), mat('boards', (0.45, 0.36, 0.26), rough=0.9))
    box('vroof', (14.4, 3.4, 0.06), (0, -6.6, 3.1), iron, rot=(-8, 0, 0))
    for x in (-6.8, -2.3, 2.3, 6.8):
        cyl(f'post{x}', 0.08, 0.08, 2.8, 6, (x, -7.9, 1.8), mat('postm', (0.85, 0.84, 0.80)))
    box('path', (1.6, 60, 0.03), (2, -38, 0.02), mat('pathm', (0.55, 0.48, 0.38), rough=1.0))
    box('shed', (12, 16, 4.5), (28, 18, 2.25), iron)
    gums(30, (-120, 120), (10, 160), seed=4)
    person('may', (-2.5, -6.5, 0.55), heading=180, body=(0.55, 0.50, 0.62))
    stan = person('stan', (2.4, -60, 0), body=(0.35, 0.33, 0.28), hat='cap')
    stan.walk(1, 330, (2.4, -60, 0), (2.4, -10.5, 0), speed='walk'); stan.hold(334, 'point')
    for i in range(3):
        p0 = (1.4 + i * 0.9 - 0.9, -63 - i * 1.6, 0); p1 = (1.4 + i * 0.9 - 0.9, -13.5 - i * 1.4, 0)
        p = person(f'pw{i}', p0, body=MAROON, head=SKIN)
        p.walk(1, 330, p0, p1, speed='walk'); p.hold(334, 'stand')
    cam = camera(lens=40)
    cam_key(cam, 1, (-14, -22, 3.0), (2, -45, 1.2))
    cam_key(cam, N, (-12, -18, 2.6), (1, -10, 1.4))


# ---- second angles (24 Nov 2026): more distinct seconds so no clip is reused more than twice
@shot
def s_night_tower():
    """From a tower: lamps along the north-west wire, B camp's huts dark, the light pool moving across the ground."""
    N = 600; reset(frames=N, samples=16); glare_comp(threshold=1.0, mix=-0.7, vignette=0.0)
    b_closeup()
    tower('twc', (-212, 205))
    sp = spot('beamc', (-212, 205, 11), (-150, 150, 0), energy=6e7, angle=12, blend=0.4, color=(1, 0.95, 0.8))
    for f in range(1, N + 1, 20):
        t = f / N; aim(sp, (-180 + 110 * t, 170 - 120 * t + 15 * math.sin(t * 9), 0)); sp.keyframe_insert('rotation_euler', frame=f)
    cam = camera(lens=30)
    cam_key(cam, 1, (-209, 200, 15), (-150, 140, 0))
    cam_key(cam, N, (-203, 196, 14), (-100, 110, 0))


@shot
def s_broadway_day():
    """Daytime, low along Broadway: inner wire both sides, huts of B camp on the right, a guard tower ahead."""
    N = 600; reset(frames=N, samples=16); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0)
    world((0.50, 0.56, 0.64), 0.6); sun('sun', (50, 0, 150), 2.2, color=(1.0, 0.96, 0.88), angle=3)
    camp(detail=True)
    cam = camera(lens=35)
    cam_key(cam, 1, (60, -8, 11), (-40, 40, 0))
    cam_key(cam, N, (-150, -8, 10), (-250, 40, 0))


@shot
def s_charge_side():
    """Profile along the west wire: men reach it, blankets go over, others climb across."""
    N = 540; reset(frames=N, samples=16); glare_comp(threshold=1.0, mix=-0.7, vignette=0.0)
    b_closeup()
    mob('s', 60, (-185, 60, -150, 140), (-199, 70, -198, 125), 1, N, seed=31, stagger=200)
    bl = mat('blanket', (0.22, 0.20, 0.17), rough=0.95)
    random.seed(15)
    for i in range(16):
        y = random.uniform(72, 122); f0 = random.randint(60, 480)
        for side in (-1, 1):
            b = box(f'bs{i}{side}', (1.3, 1.9, 0.05), (-200 + side * 0.5, y, 1.95), bl, rot=(0, side * 58, random.uniform(-6, 6)))
            b.scale = (0.001, 0.001, 0.001); b.keyframe_insert('scale', frame=f0 - 1); b.scale = (1, 1, 1); b.keyframe_insert('scale', frame=f0 + 4)
    cam = camera(lens=35)
    cam_key(cam, 1, (-212, 60, 2.2), (-199, 95, 1.2))
    cam_key(cam, N, (-213, 82, 2.6), (-199, 120, 1.2))


@shot
def s_ash_walk():
    """First light: a slow walk at eye level between the ash floors of B camp, smoke rising."""
    N = 540; reset(frames=N, samples=16); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0)
    world((0.36, 0.34, 0.36), 0.8); sun('sun', (84, 0, 100), 1.6, color=(1.0, 0.72, 0.5), angle=4)
    ground((900, 900), DRYGRASS, name='paddock')
    ash = mat('ash', (0.07, 0.065, 0.06), rough=1.0); char = mat('char', (0.04, 0.035, 0.03), rough=1.0)
    random.seed(18)
    for r in range(4):
        for c in range(4):
            x, y = -60 - c * 30, 40 + r * 22
            box(f'ash{r}{c}', (18.5, 6.5, 0.12), (x, y, 0.06), ash)
            for k in range(6):
                cyl(f'st{r}{c}{k}', 0.12, 0.12, random.uniform(0.4, 1.8), 5, (x + random.uniform(-8, 8), y + random.uniform(-2.5, 2.5), 0.6), char)
            if (r * 4 + c) % 3 == 0:
                dust(f'sm{r}{c}', (5, 5, 25), (x, y, 12), density=0.012, color=(0.25, 0.25, 0.25), anim_frames=N)
    wire_line('outer', (-200, 30), (-200, 160), spacing=5)
    cam = camera(lens=32)
    cam_key(cam, 1, (-35, 84, 4.0), (-110, 80, 0.0))
    cam_key(cam, N, (-140, 84, 3.6), (-200, 80, 0.5))


@shot
def s_farm_verandah():
    """From the verandah: the path, the shed, the gums; four men walk up towards the house."""
    N = 450; reset(frames=N, samples=16); glare_comp(threshold=1.3, mix=-0.85, vignette=0.0)
    world((0.50, 0.56, 0.64), 0.6); sun('sun', (35, 0, 60), 2.2, color=(1.0, 0.94, 0.84), angle=3)
    ground((1200, 1200), DRYGRASS, name='paddock')
    iron = mat('iron', (0.55, 0.56, 0.56), rough=0.4, metal=0.6)
    box('vfloor', (14, 3, 0.3), (0, -6.5, 0.4), mat('boards', (0.45, 0.36, 0.26), rough=0.9))
    box('vroof', (14.4, 3.4, 0.06), (0, -6.6, 3.1), iron, rot=(-8, 0, 0))
    for x in (-6.8, -2.3, 2.3, 6.8):
        cyl(f'post{x}', 0.08, 0.08, 2.8, 6, (x, -7.9, 1.8), mat('postm', (0.85, 0.84, 0.80)))
    box('rail', (14, 0.08, 0.08), (0, -7.9, 1.4), mat('postm', (0.85, 0.84, 0.80)))
    box('path', (1.6, 60, 0.03), (2, -38, 0.02), mat('pathm', (0.55, 0.48, 0.38), rough=1.0))
    box('shed', (12, 16, 4.5), (-28, -40, 2.25), iron)
    gums(40, (-120, 120), (-160, -20), seed=9)
    stan = person('stan', (2.4, -60, 0), body=(0.35, 0.33, 0.28), hat='cap')
    stan.walk(1, 400, (2.4, -60, 0), (2.4, -12.0, 0), speed='walk')
    for i in range(3):
        p0 = (1.4 + i * 0.9 - 0.9, -63 - i * 1.6, 0); p1 = (1.4 + i * 0.9 - 0.9, -15.0 - i * 1.4, 0)
        p = person(f'pw{i}', p0, body=MAROON, head=SKIN)
        p.walk(1, 400, p0, p1, speed='walk')
    cam = camera(lens=45)
    cam_key(cam, 1, (-3.5, -6.0, 1.9), (2, -40, 1.2))
    cam_key(cam, N, (-3.0, -6.2, 1.9), (2, -20, 1.4))
