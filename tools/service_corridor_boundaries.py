"""Metro platform boundaries, measured on a 2000x1116 view of the 2752x1536 plate.
Run: python service_corridor_boundaries.py <plate.png> <out_dir>
Coordinates D are view pixels. Original = D*1.376. Godot scene = D*0.688 (plate drawn at 0.5)."""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont

PLATE = sys.argv[1]; OUT = sys.argv[2]
KO = 2752/2000      # view -> original plate
KS = 0.688          # view -> scene (1376x768)

FLOOR = [(432,1116),(432,1068),(490,1014),(548,1010),(553,906),(645,896),(655,893),(715,890),(735,873),(800,857),
         (850,822),(900,790),(950,750),(1000,730),(1060,712),(1268,712),(1300,772),(1327,822),(1350,852),(1370,872),
         (1405,902),(1438,945),(1545,1050),(1660,1040),(1665,1116)]
BLOCK = {
 "CrateStackL":[(1300,770),(1327,822),(1350,852),(1368,872),(1405,902),(1500,895),(1500,760)],
 "CartBase":[(1438,945),(1470,890),(1700,850),(1702,925),(1660,1010),(1545,1050)],
 "CratesRight":[(1655,912),(1705,925),(1810,978),(2000,985),(2000,1116),(1665,1116)],
}
BEHIND = {  # name: (polygon, sort_y)
 "Cart":([(1433,732),(1448,724),(1492,726),(1494,684),(1570,676),(1672,688),(1676,775),(1702,775),(1704,800),(1698,918),
          (1665,925),(1650,975),(1560,1040),(1548,1048),(1527,1042),(1535,1020),(1480,970),(1442,945),(1432,935),(1440,880),(1437,780)],990),
}
ANIM = {
 "ScreenL":[(822,520),(902,532),(900,634),(822,652)],
 "ScreenR":[(1428,527),(1500,515),(1500,640),(1430,622)],
 "BigMonitor":[(1625,410),(1830,402),(1832,640),(1632,630)],
 "DoorGlow":[(1082,518),(1252,520),(1252,708),(1082,708)],
 "LightMain":[(945,92),(1345,68),(1335,102),(962,128)],
 "LightMid":[(1052,312),(1265,312),(1260,328),(1060,328)],
 "SkylightVoid":[(1500,30),(1700,150),(1620,300),(1400,180)],
 "SteamL":[(745,868),(790,850),(850,800),(900,765),(960,735),(1040,705),(1065,712),(1040,760),(980,800),(900,850),(800,885)],
 "SteamR1":[(1295,645),(1335,640),(1335,725),(1295,730)],
 "SteamR2":[(1330,830),(1425,830),(1430,925),(1335,925)],
}
EXITS = {
 "control_door":([(1075,722),(1260,722),(1262,762),(1062,762)],"control_room",(1165,745)),
 "side_door":([(556,920),(650,905),(660,960),(560,975)],"station_concourse",(610,948)),
}
START = (1000,1040)
HORIZON = 585.0           # view y where a standing person shrinks to nothing
PERSON_PER_PX = (1.8/2.1)*1.573   # door 2.1 m: 193px at y708, 495px at y900 -> 1.573 px/px; person 1.8 m

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
poly(FLOOR,(60,255,140),(60,255,140),"WALKABLE FLOOR",(700,960))
for n,p in BLOCK.items(): poly(p,(255,200,40),(255,200,40),"BLOCKED "+n,(0,-30) if n!="CratesRight" else (30,20))
for n,(p,sy) in BEHIND.items():
    poly(p,(255,60,200),(255,60,200),None)
    d.text((1560,1070),f"BEHIND {n.upper()} (sort {sy})",font=F,fill=(255,60,200,255))
    d.line([(min(q[0] for q in p)-25,sy),(max(q[0] for q in p)+25,sy)],fill=(255,255,255,255),width=3)
for n,p in ANIM.items(): poly(p,(60,220,255),(60,220,255),n.upper() if n not in ("SteamL","SteamR1","SteamR2","LightMid","ScreenL","ScreenR","DoorGlow") else None)
for n,(x,y) in {"SteamL":(745,800),"ScreenL":(740,490),"ScreenR":(1405,490),"DoorGlow":(1085,495),"LightMid":(1280,300),"SteamR1":(1300,612),"SteamR2":(1215,880)}.items():
    d.text((x+1,y+1),n.upper(),font=F,fill=(0,0,0,255)); d.text((x,y),n.upper(),font=F,fill=(60,220,255,255))
for n,(p,t,m) in EXITS.items():
    poly(p,(255,255,255),(255,255,255),None)
    d.text((1000,775) if n=="control_door" else (400,985), f"EXIT {n.upper()} > {t}", font=F, fill=(255,255,255,255))
    d.ellipse([m[0]-8,m[1]-8,m[0]+8,m[1]+8],fill=(255,255,255,255))
d.ellipse([START[0]-10,START[1]-10,START[0]+10,START[1]+10],fill=(255,80,80,255)); d.text((START[0]+14,START[1]-12),"PLAYER START",font=F,fill=(255,120,120,255))
# horizon + scale figures
d.line([(0,HORIZON),(2000,HORIZON)],fill=(255,255,255,120),width=2); d.text((6,HORIZON-26),"horizon (scale = 0)",font=F,fill=(255,255,255,200))
for y,x in ((830,120),(940,260),(1060,450)):
    h=person_h(y); w=h*0.26
    d.rectangle([x-w/2,y-h,x+w/2,y],outline=(255,255,255,255),width=3); d.ellipse([x-w*0.28,y-h,x+w*0.28,y-h+w*0.56],outline=(255,255,255,255),width=3)
    d.text((x+w/2+8,y-h/2),f"{round(h)}px",font=F,fill=(255,255,255,255))
d.text((20,200),"white figures: player height\nat that depth",font=F,fill=(255,255,255,255))
Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB").save(os.path.join(OUT,"service_corridor_v1_plan_r2.png"))

# ---------- walk-behind cut-outs from the full-res plate ----------
src = Image.open(PLATE).convert("RGBA")
os.makedirs(os.path.join(OUT,"behind"),exist_ok=True)
cut = {}
for n,(p,sy) in BEHIND.items():
    o=[(x*KO,y*KO) for x,y in p]
    x0=int(min(q[0] for q in o)); y0=int(min(q[1] for q in o)); x1=int(max(q[0] for q in o))+1; y1=int(max(q[1] for q in o))+1
    mask=Image.new("L",(x1-x0,y1-y0),0); ImageDraw.Draw(mask).polygon([(x-x0,y-y0) for x,y in o],fill=255)
    c=src.crop((x0,y0,x1,y1)); c.putalpha(mask)
    fn=f"service_corridor_behind_{n.lower()}.png"; c.save(os.path.join(OUT,"behind",fn))
    cut[n]=(fn,x0,y0,sy)

# ---------- scene ----------
L=[]; ext=['[ext_resource type="Texture2D" path="res://assets/backgrounds/service_corridor/service_corridor_v1.png" id="1_bg"]']
for i,(n,(fn,x0,y0,sy)) in enumerate(cut.items()):
    ext.append(f'[ext_resource type="Texture2D" path="res://assets/backgrounds/service_corridor/behind/{fn}" id="{i+2}_{n.lower()}"]')
L.append(f"[gd_scene load_steps={len(ext)+1} format=3]\n"); L+= [e+"" for e in ext]
L.append('\n[node name="ServiceCorridor" type="Node2D"]\n')
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
    n="".join(w.capitalize() for w in n.split("_"))
    L.append(f'[node name="{n}Zone" type="Polygon2D" parent="Exits"]\nvisible = false\ncolor = Color(1, 1, 1, 0.3)\npolygon = {pva(p)}\nmetadata/target = "{t}"\nmetadata/arrive = Vector2{sc(m)}\n')
open(os.path.join(OUT,"service_corridor.tscn"),"w").write("\n".join(L))
json.dump({"floor":FLOOR,"exits":{k:{"poly":v[0],"to":v[1]} for k,v in EXITS.items()},"behind":{k:v[1] for k,v in BEHIND.items()}},open(os.path.join(OUT,"service_corridor_view_coords.json"),"w"))
json.dump({k:{"poly":[list(q) for q in v[0]],"to":v[1]} for k,v in EXITS.items()},open(os.path.join(OUT,"exits.json"),"w"),indent=1)
print("ok", {n:(c[1],c[2]) for n,c in cut.items()})
