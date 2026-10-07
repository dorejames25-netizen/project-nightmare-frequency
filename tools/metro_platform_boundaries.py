"""Metro platform boundaries, measured on a 2000x1116 view of the 2752x1536 plate.
Run: python metro_platform_boundaries.py <plate.png> <out_dir>
Coordinates D are view pixels. Original = D*1.376. Godot scene = D*0.688 (plate drawn at 0.5)."""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont

PLATE = sys.argv[1]; OUT = sys.argv[2]
KO = 2752/2000      # view -> original plate
KS = 0.688          # view -> scene (1376x768)

FLOOR = [(0,895),(345,897),(400,900),(600,900),(640,905),(790,862),(885,858),(990,850),(1030,840),
         (1100,832),(1125,830),(1170,828),(1400,826),(1480,834),(1432,1116),(0,1116)]
BLOCK = {
 "Col1Base":[(108,1005),(350,1000),(362,1030),(345,1068),(112,1068),(98,1032)],
 "Col2Base":[(645,905),(780,905),(790,925),(775,942),(652,942),(640,925)],
 "Col3Base":[(892,852),(985,852),(992,866),(980,884),(900,884),(888,868)],
 "Col4Base":[(1034,836),(1098,836),(1104,844),(1096,853),(1036,853),(1030,844)],
 "Col5Base":[(1124,822),(1170,822),(1174,827),(1168,833),(1126,833),(1122,827)],
 "Bench":[(402,872),(592,862),(590,900),(408,906)],
}
BEHIND = {  # name: (polygon, sort_y)
 "Col1":([(90,292),(305,290),(308,372),(336,380),(336,990),(358,1000),(357,1050),(340,1066),(108,1066),(100,1030),(106,998),(141,990),(141,496),(104,490),(104,345),(90,340)],1034),
 "Col2":([(630,491),(760,491),(762,512),(772,602),(772,898),(787,905),(787,935),(767,942),(654,942),(640,935),(640,905),(654,898),(654,602),(648,590),(645,512),(630,508)],923),
 "Col3":([(882,566),(986,566),(986,600),(982,848),(992,852),(992,880),(975,884),(900,884),(888,880),(888,852),(898,848),(898,600),(885,590)],868),
 "Col4":([(1030,616),(1100,616),(1100,640),(1092,830),(1100,836),(1100,852),(1032,852),(1032,836),(1040,830),(1040,640),(1030,632)],844),
 "Col5":([(1122,646),(1172,646),(1172,668),(1166,818),(1172,822),(1172,832),(1122,832),(1122,822),(1128,818),(1128,668),(1122,662)],828),
}
ANIM = {
 "ScreensL":[(0,560),(142,566),(142,714),(0,712)],
 "Panel":[(414,614),(534,618),(534,728),(414,730)],
 "PanelFar":[(850,672),(900,676),(900,742),(850,738)],
 "Sign":[(1120,385),(1372,385),(1372,495),(1120,495)],
 "Shaft":[(1168,0),(1326,0),(1326,365),(1168,365)],
 # extra slots, measured 2026-10-07 on a scene-unit grid (view = scene / 0.688)
 "TunnelMouth":[(1483,840),(1483,672),(1504,628),(1548,599),(1606,590),(1664,599),(1703,628),(1727,672),(1727,890)],
 "StairsNeon":[(1218,826),(1218,663),(1238,618),(1297,578),(1358,618),(1378,663),(1378,826)],
 "RingLight1":[(767,81),(878,81),(878,134),(767,134)],
 "RingLight2":[(1000,304),(1073,304),(1073,336),(1000,336)],
 "CageLight1":[(1512,145),(1730,145),(1730,363),(1512,363)],
 "CageLight2":[(1497,355),(1635,355),(1635,509),(1497,509)],
 "CageLight3":[(1480,488),(1596,488),(1596,590),(1480,590)],
 "TubeLight1":[(483,419),(663,474),(657,491),(480,436)],
 "TubeLight2":[(802,525),(907,560),(903,573),(799,538)],
 "TubeLight3":[(991,590),(1035,605),(1032,615),(988,600)],
 "FloorFog":[(0,843),(640,858),(792,814),(1017,792),(1483,785),(1483,887),(792,908),(640,952),(0,1003)],
}
EXITS = {
 "Stairs":([(1222,822),(1385,822),(1400,862),(1210,862)],"station_concourse",(1300,845)),
 "Tunnel":([(1405,830),(1480,834),(1474,872),(1400,868)],"tunnel",(1440,858)),
}
START = (900,1040)
HORIZON = 758.0           # view y where a standing person shrinks to nothing
PERSON_PER_PX = 0.5625*2.51   # person height (view px) per px below horizon

def person_h(y): return PERSON_PER_PX*(y-HORIZON)

def sc(p): return (round(p[0]*KS,1), round(p[1]*KS,1))
def pva(poly): return "PackedVector2Array(" + ", ".join(f"{sc(p)[0]}, {sc(p)[1]}" for p in poly) + ")"

# ---------- plan image ----------
im = Image.open(PLATE).convert("RGB").resize((2000,1116))
ov = Image.new("RGBA", im.size, (0,0,0,0)); d = ImageDraw.Draw(ov)
try: F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except: F = ImageFont.load_default()
def poly(pts, fill, line, label=None, lab_off=(6,4)):
    d.polygon(pts, fill=fill+(70,)); d.line(pts+[pts[0]], fill=line+(255,), width=4)
    if label:
        x=min(p[0] for p in pts)+lab_off[0]; y=min(p[1] for p in pts)+lab_off[1]
        d.text((x+1,y+1),label,font=F,fill=(0,0,0,255)); d.text((x,y),label,font=F,fill=line+(255,))
poly(FLOOR,(60,255,140),(60,255,140),"WALKABLE FLOOR",(500,170))
for n,p in BLOCK.items(): poly(p,(255,200,40),(255,200,40),"BLOCKED" if n=="Bench" else None)
for n,(p,sy) in BEHIND.items():
    poly(p,(255,60,200),(255,60,200),f"BEHIND {n}" if n in ("Col1","Col2","Col3") else None)
    if n in ("Col4","Col5"): d.text((min(q[0] for q in p)-6, min(q[1] for q in p)-28 - (22 if n=="Col5" else 0)), n, font=F, fill=(255,60,200,255))
    d.line([(min(q[0] for q in p)-25,sy),(max(q[0] for q in p)+25,sy)],fill=(255,255,255,255),width=3)
for n,p in ANIM.items(): poly(p,(60,220,255),(60,220,255),n.upper())
for n,(p,t,m) in EXITS.items():
    poly(p,(255,255,255),(255,255,255),None)
    d.text((1210,880) if n=="Stairs" else (1300,975), f"EXIT {n.upper()} > {t}", font=F, fill=(255,255,255,255))
    d.ellipse([m[0]-8,m[1]-8,m[0]+8,m[1]+8],fill=(255,255,255,255))
d.ellipse([START[0]-10,START[1]-10,START[0]+10,START[1]+10],fill=(255,80,80,255)); d.text((START[0]+14,START[1]-12),"PLAYER START",font=F,fill=(255,120,120,255))
# horizon + scale figures
d.line([(0,HORIZON),(2000,HORIZON)],fill=(255,255,255,120),width=2); d.text((6,HORIZON-26),"horizon (scale = 0)",font=F,fill=(255,255,255,200))
for y,x in ((830,1560),(940,1680),(1060,1830)):
    h=person_h(y); w=h*0.26
    d.rectangle([x-w/2,y-h,x+w/2,y],outline=(255,255,255,255),width=3); d.ellipse([x-w*0.28,y-h,x+w*0.28,y-h+w*0.56],outline=(255,255,255,255),width=3)
    d.text((x+w/2+8,y-h/2),f"{round(h)}px",font=F,fill=(255,255,255,255))
d.text((1560,300),"white figures: player height\nat that depth",font=F,fill=(255,255,255,255))
Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB").save(os.path.join(OUT,"metro_platform_v2_plan_r2.png"))

# ---------- walk-behind cut-outs from the full-res plate ----------
src = Image.open(PLATE).convert("RGBA")
os.makedirs(os.path.join(OUT,"behind"),exist_ok=True)
cut = {}
for n,(p,sy) in BEHIND.items():
    o=[(x*KO,y*KO) for x,y in p]
    x0=int(min(q[0] for q in o)); y0=int(min(q[1] for q in o)); x1=int(max(q[0] for q in o))+1; y1=int(max(q[1] for q in o))+1
    mask=Image.new("L",(x1-x0,y1-y0),0); ImageDraw.Draw(mask).polygon([(x-x0,y-y0) for x,y in o],fill=255)
    c=src.crop((x0,y0,x1,y1)); c.putalpha(mask)
    fn=f"metro_platform_behind_{n.lower()}.png"; c.save(os.path.join(OUT,"behind",fn))
    cut[n]=(fn,x0,y0,sy)

# ---------- scene ----------
L=[]; ext=['[ext_resource type="Texture2D" path="res://assets/backgrounds/metro_platform/metro_platform_v2.png" id="1_bg"]']
for i,(n,(fn,x0,y0,sy)) in enumerate(cut.items()):
    ext.append(f'[ext_resource type="Texture2D" path="res://assets/backgrounds/metro_platform/behind/{fn}" id="{i+2}_{n.lower()}"]')
L.append(f"[gd_scene load_steps={len(ext)+1} format=3]\n"); L+= [e+"" for e in ext]
L.append('\n[node name="MetroPlatform" type="Node2D"]\n')
L.append('[node name="Background" type="Sprite2D" parent="."]\nposition = Vector2(688, 384)\nscale = Vector2(0.5, 0.5)\ntexture = ExtResource("1_bg")\n')
L.append(f'[node name="WalkArea" type="Polygon2D" parent="."]\nvisible = false\ncolor = Color(0.24, 1, 0.55, 0.3)\npolygon = {pva(FLOOR)}\n')
L.append('[node name="Blockers" type="Node2D" parent="."]\nvisible = false\n')
for n,p in BLOCK.items(): L.append(f'[node name="{n}" type="Polygon2D" parent="Blockers"]\ncolor = Color(1, 0.78, 0.16, 0.3)\npolygon = {pva(p)}\n')
L.append('[node name="Actors" type="Node2D" parent="."]\ny_sort_enabled = true\n')
for i,(n,(fn,x0,y0,sy)) in enumerate(cut.items()):
    sye=round(sy*KS,1)
    L.append(f'[node name="{n}Front" type="Node2D" parent="Actors"]\nposition = Vector2(0, {sye})\n')
    L.append(f'[node name="Sprite" type="Sprite2D" parent="Actors/{n}Front"]\nposition = Vector2({round(x0*0.5,1)}, {round(y0*0.5-sye,1)})\nscale = Vector2(0.5, 0.5)\ncentered = false\ntexture = ExtResource("{i+2}_{n.lower()}")\n')
L.append('[node name="AnimationSlots" type="Node2D" parent="."]\nvisible = false\n')
for n,p in ANIM.items(): L.append(f'[node name="{n}" type="Polygon2D" parent="AnimationSlots"]\ncolor = Color(0.24, 0.86, 1, 0.3)\npolygon = {pva(p)}\n')
L.append(f'[node name="PlayerStart" type="Marker2D" parent="."]\nposition = Vector2{sc(START)}\n')
L.append('[node name="Depth" type="Node2D" parent="."]\nmetadata/horizon_y = %s\nmetadata/person_height_per_px = %.4f\n' % (round(HORIZON*KS,1), PERSON_PER_PX))
L.append('[node name="Exits" type="Node2D" parent="."]\n')
for n,(p,t,m) in EXITS.items():
    L.append(f'[node name="{n}Zone" type="Polygon2D" parent="Exits"]\nvisible = false\ncolor = Color(1, 1, 1, 0.3)\npolygon = {pva(p)}\nmetadata/target = "{t}"\nmetadata/arrive = Vector2{sc(m)}\n')
open(os.path.join(OUT,"metro_platform.tscn"),"w").write("\n".join(L))
json.dump({"floor":FLOOR,"exits":{k:[v[0],v[1]] for k,v in EXITS.items()},"behind":{k:v[1] for k,v in BEHIND.items()}},open(os.path.join(OUT,"metro_platform_view_coords.json"),"w"))
print("ok", {n:(c[1],c[2]) for n,c in cut.items()})
