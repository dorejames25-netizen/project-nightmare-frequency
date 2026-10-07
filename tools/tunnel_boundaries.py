"""Tunnel boundaries, measured on a 2000x1116 view of the 2752x1536 plate.
Run: python tunnel_boundaries.py <plate.png> <out_dir>
Coordinates D are view pixels. Original = D*1.376. Godot scene = D*0.688 (plate drawn at 0.5)."""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont

PLATE = sys.argv[1]; OUT = sys.argv[2]
KO = 2752/2000      # view -> original plate
KS = 0.688          # view -> scene (1376x768)

FLOOR = [(0,810),(372,790),(655,708),(850,704),(1000,700),(1090,692),(1142,668),(1000,765),(800,892),(600,1020),(449,1116),(0,1116)]
BLOCK = {
 "PierBase":[(375,856),(542,868),(652,826),(485,814)],
}
BEHIND = {  # name: (polygon, sort_y)
 "Pier":([(353,300),(366,380),(375,460),(377,550),(376,700),(375,856),(400,860),(542,868),(652,826),(652,700),(650,550),(660,420),(676,300)],841),
}
ANIM = {
 "BoardL":[(198,458),(352,458),(352,588),(198,588)],
 "ScreenBlack":[(902,485),(1027,485),(1027,576),(902,576)],
 "GateNeon":[(1133,480),(1330,480),(1330,692),(1133,692)],
 "BoardFar":[(1460,560),(1488,560),(1488,600),(1460,600)],
 "BoardMid":[(1540,545),(1585,545),(1585,600),(1540,600)],
 "BoardR":[(1688,510),(1775,510),(1775,595),(1688,595)],
 "Void":[(1135,20),(1330,20),(1330,270),(1135,270)],
}
EXITS = {
 "gate":([(960,702),(1095,692),(1138,670),(1040,740),(980,760)],None,(1010,728)),
 "ladder":([(800,708),(930,706),(940,762),(790,762)],"service_corridor",(865,742)),
 "platform":([(0,850),(80,850),(80,1100),(0,1100)],"metro_platform",(140,960)),
}
START = (620,960)
HORIZON = 605.0
PERSON_PER_PX = 2.09

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
poly(FLOOR,(60,255,140),(60,255,140),"WALKABLE FLOOR (ledge)",(120,250))
for n,p in BLOCK.items(): poly(p,(255,200,40),(255,200,40),"BLOCKED")
for n,(p,sy) in BEHIND.items():
    poly(p,(255,60,200),(255,60,200),f"BEHIND {n}")
    d.line([(min(q[0] for q in p)-25,sy),(max(q[0] for q in p)+25,sy)],fill=(255,255,255,255),width=3)
for n,p in ANIM.items(): poly(p,(60,220,255),(60,220,255),n.upper() if n in ("BoardL","ScreenBlack","GateNeon","Void","BoardR") else None)
for n,(p,t,m) in EXITS.items():
    poly(p,(255,255,255),(255,255,255),None)
    lp={"gate":(1010,640),"ladder":(760,790),"platform":(90,1060)}[n]; d.text(lp, f"EXIT {n.upper()} > {t or chr(110)+chr(117)+chr(108)+chr(108)+' (sealed, locked)'}", font=F, fill=(255,255,255,255))
    d.ellipse([m[0]-8,m[1]-8,m[0]+8,m[1]+8],fill=(255,255,255,255))
d.ellipse([START[0]-10,START[1]-10,START[0]+10,START[1]+10],fill=(255,80,80,255)); d.text((START[0]+14,START[1]-12),"PLAYER START",font=F,fill=(255,120,120,255))
# horizon + scale figures
d.line([(0,HORIZON),(2000,HORIZON)],fill=(255,255,255,120),width=2); d.text((6,HORIZON-26),"horizon (scale = 0)",font=F,fill=(255,255,255,200))
for y,x in ((700,1480),(780,1640),(860,1830)):
    h=person_h(y); w=h*0.26
    d.rectangle([x-w/2,y-h,x+w/2,y],outline=(255,255,255,255),width=3); d.ellipse([x-w*0.28,y-h,x+w*0.28,y-h+w*0.56],outline=(255,255,255,255),width=3)
    d.text((x+w/2+8,y-h/2),f"{round(h)}px",font=F,fill=(255,255,255,255))
d.text((1480,200),"white figures: player height\nat that depth",font=F,fill=(255,255,255,255))
Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB").save(os.path.join(OUT,"tunnel_v1_plan_r2.png"))

# ---------- walk-behind cut-outs from the full-res plate ----------
src = Image.open(PLATE).convert("RGBA")
os.makedirs(os.path.join(OUT,"behind"),exist_ok=True)
cut = {}
for n,(p,sy) in BEHIND.items():
    o=[(x*KO,y*KO) for x,y in p]
    x0=int(min(q[0] for q in o)); y0=int(min(q[1] for q in o)); x1=int(max(q[0] for q in o))+1; y1=int(max(q[1] for q in o))+1
    mask=Image.new("L",(x1-x0,y1-y0),0); ImageDraw.Draw(mask).polygon([(x-x0,y-y0) for x,y in o],fill=255)
    c=src.crop((x0,y0,x1,y1)); c.putalpha(mask)
    fn=f"tunnel_behind_{n.lower()}.png"; c.save(os.path.join(OUT,"behind",fn))
    cut[n]=(fn,x0,y0,sy)

# ---------- scene ----------
L=[]; ext=['[ext_resource type="Texture2D" path="res://assets/backgrounds/tunnel/tunnel_v1.png" id="1_bg"]']
for i,(n,(fn,x0,y0,sy)) in enumerate(cut.items()):
    ext.append(f'[ext_resource type="Texture2D" path="res://assets/backgrounds/tunnel/behind/{fn}" id="{i+2}_{n.lower()}"]')
L.append(f"[gd_scene load_steps={len(ext)+1} format=3]\n"); L+= [e+"" for e in ext]
L.append('\n[node name="Tunnel" type="Node2D"]\n')
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
    L.append(f'[node name="{n}Zone" type="Polygon2D" parent="Exits"]\nvisible = false\ncolor = Color(1, 1, 1, 0.3)\npolygon = {pva(p)}\nmetadata/target = "{t or ""}"\nmetadata/arrive = Vector2{sc(m)}\n' + ('metadata/locked = true\n' if t is None else ''))
open(os.path.join(OUT,"tunnel.tscn"),"w").write("\n".join(L))
json.dump({k:{"poly":[list(q) for q in v[0]],"to":v[1]} for k,v in EXITS.items()},open(os.path.join(OUT,"exits.json"),"w"),indent=1)
print("ok", {n:(c[1],c[2]) for n,c in cut.items()})
