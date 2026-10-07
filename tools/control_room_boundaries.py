"""Control room boundaries, measured on a 2000x1116 view of the 2752x1536 plate.
Run: python boundaries.py <plate.png> <out_dir>
Coordinates D are view pixels. Original = D*1.376. Godot scene = D*0.688 (plate drawn at 0.5)."""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont

PLATE = sys.argv[1]; OUT = sys.argv[2]
KO = 2752/2000      # view -> original plate
KS = 0.688          # view -> scene (1376x768)

FLOOR = [(168,905),(500,912),(520,897),(600,896),(1255,896),(1480,912),(1500,935),(1530,950),(1605,958),(1640,960),(1650,990),(1668,1040),(1672,1116),(184,1116),(180,1050),(166,1030)]
PIT = [(1406, 974), (1392, 990), (1352, 1004), (1287, 1016), (1204, 1026), (1106, 1032), (1001, 1034), (896, 1032), (799, 1026), (715, 1016), (650, 1004), (610, 990), (596, 974), (610, 958), (650, 944), (715, 932), (798, 922), (896, 916), (1001, 914), (1106, 916), (1204, 922), (1287, 932), (1352, 944), (1392, 958)]
BLOCK = {
 "PillarBase":[(0,1000),(168,1000),(178,1040),(182,1065),(184,1116),(0,1116)],
 "FloorDisc":PIT,
 "BackConsole":[(598,800),(1255,800),(1258,893),(600,895)],
 "Bollard":[(520,825),(575,822),(578,892),(518,893)],
 "RightConsole":[(1462,825),(1560,805),(2000,795),(2000,1116),(1672,1116),(1668,1040),(1650,990),(1640,960),(1605,958),(1530,950),(1500,935),(1480,915)],
}
BEHIND = {  # name: (polygon, sort_y)
 "LeftPillar":([(0,0),(244,0),(240,120),(235,220),(222,300),(210,400),(197,500),(192,600),(190,790),(168,818),(176,850),(176,872),(168,900),(166,1030),(180,1040),(182,1065),(180,1116),(0,1116)],1090),
 "RightChair":([(1628,765),(1688,768),(1702,830),(1730,880),(1815,912),(1820,925),(1780,940),(1745,960),(1745,1000),(1790,1030),(1850,1075),(1852,1100),(1780,1116),(1672,1116),(1668,1070),(1700,1045),(1700,1010),(1665,985),(1645,920),(1626,830),(1622,790)],1090),
}
ANIM = {
 "Oculus":[(705,0),(1300,0),(1290,60),(1200,125),(1000,160),(800,125),(715,60)],
 "ScreenL":[(345,348),(520,405),(500,490),(322,438)],
 "MonitorWall":[(600,515),(1240,500),(1250,770),(598,775)],
 "ScreenR1":[(1578,382),(1745,297),(1783,395),(1597,468)],
 "ScreenR2":[(1606,598),(1812,550),(1824,722),(1616,735)],
 "ScreenFarR1":[(1865,100),(1990,25),(2000,290),(1890,300)],
 "ScreenFarR2":[(1905,500),(2000,455),(2000,700),(1940,695)],
 "StairVoid":[(1270,430),(1500,405),(1500,640),(1420,640),(1300,560)],
 "FloorDiscGlow":PIT,
}
EXITS = {
 "door":([(300,915),(440,915),(452,955),(290,955)],"service_corridor",(370,965)),
 "stairs_up":([(1275,898),(1480,914),(1492,930),(1272,922)],None,(1380,934)),
}
START = (1000,1085)
HORIZON = 749.0
PERSON_PER_PX = 1.42

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
poly(FLOOR,(60,255,140),(60,255,140),"WALKABLE FLOOR",(300,150))
for n,p in BLOCK.items(): poly(p,(255,200,40),(255,200,40),{"FloorDisc":"BLOCKED: DARK DISC (James decides)","BackConsole":"BLOCKED consoles","RightConsole":"BLOCKED desk"}.get(n),{"FloorDisc":(300,30),"RightConsole":(10,135)}.get(n,(6,4)))
for n,(p,sy) in BEHIND.items():
    poly(p,(255,60,200),(255,60,200),f"BEHIND {n}")
    d.line([(min(q[0] for q in p)-25,sy),(max(q[0] for q in p)+25,sy)],fill=(255,255,255,255),width=3)
for n,p in ANIM.items():
    if n!="FloorDiscGlow": poly(p,(60,220,255),(60,220,255),None if n=="FloorDiscGlow" else n.upper())
for n,(p,t,m) in EXITS.items():
    poly(p,(255,255,255),(255,255,255),None)
    d.text((m[0]-110,m[1]+16) if n=="stairs_up" else (m[0]-60,m[1]+16), f"EXIT {n.upper()} > {t or 'locked'}", font=F, fill=(255,255,255,255))
    d.ellipse([m[0]-8,m[1]-8,m[0]+8,m[1]+8],fill=(255,255,255,255))
d.ellipse([START[0]-10,START[1]-10,START[0]+10,START[1]+10],fill=(255,80,80,255)); d.text((START[0]+14,START[1]-12),"PLAYER START",font=F,fill=(255,120,120,255))
# horizon + scale figures
d.line([(0,HORIZON),(2000,HORIZON)],fill=(255,255,255,120),width=2); d.text((6,HORIZON-26),"horizon (scale = 0)",font=F,fill=(255,255,255,200))
for y,x in ((930,1560),(1020,1665),(1100,1830)):
    h=person_h(y); w=h*0.26
    d.rectangle([x-w/2,y-h,x+w/2,y],outline=(255,255,255,255),width=3); d.ellipse([x-w*0.28,y-h,x+w*0.28,y-h+w*0.56],outline=(255,255,255,255),width=3)
    d.text((x+w/2+8,y-h/2),f"{round(h)}px",font=F,fill=(255,255,255,255))
d.text((560,1085),"white figures: player height at that depth",font=F,fill=(255,255,255,255))
Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB").save(os.path.join(OUT,"control_room_v1_plan_r2.png"))

# ---------- walk-behind cut-outs from the full-res plate ----------
src = Image.open(PLATE).convert("RGBA")
os.makedirs(os.path.join(OUT,"behind"),exist_ok=True)
cut = {}
for n,(p,sy) in BEHIND.items():
    o=[(x*KO,y*KO) for x,y in p]
    x0=int(min(q[0] for q in o)); y0=int(min(q[1] for q in o)); x1=int(max(q[0] for q in o))+1; y1=int(max(q[1] for q in o))+1
    mask=Image.new("L",(x1-x0,y1-y0),0); ImageDraw.Draw(mask).polygon([(x-x0,y-y0) for x,y in o],fill=255)
    c=src.crop((x0,y0,x1,y1)); c.putalpha(mask)
    fn=f"control_room_behind_{n.lower()}.png"; c.save(os.path.join(OUT,"behind",fn))
    cut[n]=(fn,x0,y0,sy)

# ---------- scene ----------
L=[]; ext=['[ext_resource type="Texture2D" path="res://assets/backgrounds/control_room/control_room_v1.png" id="1_bg"]']
for i,(n,(fn,x0,y0,sy)) in enumerate(cut.items()):
    ext.append(f'[ext_resource type="Texture2D" path="res://assets/backgrounds/control_room/behind/{fn}" id="{i+2}_{n.lower()}"]')
L.append(f"[gd_scene load_steps={len(ext)+1} format=3]\n"); L+= [e+"" for e in ext]
L.append('\n[node name="ControlRoom" type="Node2D"]\n')
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
    L.append(f'[node name="{n}Zone" type="Polygon2D" parent="Exits"]\nvisible = false\ncolor = Color(1, 1, 1, 0.3)\npolygon = {pva(p)}\nmetadata/target = "{t or 'locked'}"\nmetadata/arrive = Vector2{sc(m)}\n')
open(os.path.join(OUT,"control_room.tscn"),"w").write("\n".join(L))
json.dump({"floor":FLOOR,"exits":{k:[v[0],v[1]] for k,v in EXITS.items()},"behind":{k:v[1] for k,v in BEHIND.items()}},open(os.path.join(OUT,"view_coords.json"),"w"))
json.dump({k:{"poly":v[0],"to":v[1]} for k,v in EXITS.items()},open(os.path.join(OUT,"exits.json"),"w"))
print("ok", {n:(c[1],c[2]) for n,c in cut.items()})
