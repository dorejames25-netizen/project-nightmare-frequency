"""Street night boundaries, measured on a 2000x1116 view of the 2752x1536 plate.
Run: python street_night_boundaries.py <plate.png> <out_dir>
Coordinates D are view pixels. Original = D*1.376. Godot scene = D*0.688 (plate drawn at 0.5)."""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont

PLATE = sys.argv[1]; OUT = sys.argv[2]
KO = 2752/2000      # view -> original plate
KS = 0.688          # view -> scene (1376x768)

FLOOR = [(214,893),(535,889),(540,897),(650,898),(727,870),(843,834),(950,798),(1050,771),(1090,760),(1100,750),
         (1160,750),(1163,775),(1185,802),(1217,822),(1280,831),(1348,824),(1372,842),(1470,858),(1556,862),(1598,858),
         (1700,896),(1800,898),(1925,933),(1930,968),(1976,982),(2000,984),(2000,1116),(70,1116),(212,1062)]
BLOCK = {
 "Tram":[(1160,742),(1163,775),(1185,802),(1217,823),(1280,832),(1348,825),(1352,790),(1345,742)],
 "ShelterBase":[(1372,818),(1405,815),(1556,842),(1556,862),(1470,858),(1376,840)],
 "RightPillarBase":[(1930,952),(1976,962),(1982,984),(1932,972)],
}
BEHIND = {}   # no real foreground occluders: every object is at the floor back edge or fixed in front of it
ANIM = {
 "SignLeft":[(935,345),(1015,345),(1015,470),(935,470)],
 "SignMid":[(1465,290),(1588,290),(1588,465),(1465,465)],
 "Billboard":[(1655,285),(1940,55),(1928,315),(1665,448)],
 "WindowL":[(335,590),(437,590),(437,780),(335,780)],
 "WindowM":[(740,568),(823,600),(823,752),(740,758)],
 "WindowS":[(895,633),(935,640),(935,745),(895,747)],
 "WindowR":[(1602,568),(1690,578),(1690,762),(1602,758)],
 "ArchGlowA":[(258,272),(285,268),(395,490),(368,497)],
 "ArchGlowB":[(410,175),(440,177),(590,490),(565,495)],
 "SkylineGlow":[(1068,452),(1215,452),(1200,520),(1163,735),(1110,735),(1095,560),(1065,500)],
 "TramLamp":[(1273,761),(1301,761),(1301,789),(1273,789)],
 "DoorLight":[(1835,548),(1928,520),(1930,545),(1840,552)],
}
EXITS = {
 "station":([(700,1060),(1500,1060),(1560,1116),(640,1116)],"station_concourse",(1100,1030)),
 "alley":([(1010,788),(1050,775),(1090,760),(1100,752),(1112,775),(1090,800),(1020,806)],None,(1060,802)),
 "right_doorway":([(1712,898),(1800,899),(1805,940),(1700,928)],None,(1755,938)),
 "tower_district":([(1805,903),(1925,934),(1928,972),(1810,942)],None,(1865,958)),
}
START = (1100,1000)
HORIZON = 712.0
PERSON_PER_PX = (1.8/2.1)*1.92   # door-equivalent 1.92 view px per px below horizon; person = 1.8/2.1 of a door

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
poly(FLOOR,(60,255,140),(60,255,140),"WALKABLE FLOOR",(750,240))
for n,p in BLOCK.items(): poly(p,(255,200,40),(255,200,40),None); d.text((1700,992) if n=="RightPillarBase" else (min(q[0] for q in p),min(q[1] for q in p)-26),"BLOCK "+n,font=F,fill=(255,200,40,255))
for n,(p,sy) in BEHIND.items():
    poly(p,(255,60,200),(255,60,200),f"BEHIND {n}" if n in ("Col1","Col2","Col3") else None)
    if n in ("Col4","Col5"): d.text((min(q[0] for q in p)-6, min(q[1] for q in p)-28 - (22 if n=="Col5" else 0)), n, font=F, fill=(255,60,200,255))
    d.line([(min(q[0] for q in p)-25,sy),(max(q[0] for q in p)+25,sy)],fill=(255,255,255,255),width=3)
for n,p in ANIM.items(): poly(p,(60,220,255),(60,220,255),n.upper())
for n,(p,t,m) in EXITS.items():
    poly(p,(255,255,255),(255,255,255),None)
    LP={"station":(780,1075),"alley":(760,790),"right_doorway":(1330,935),"tower_district":(1540,1050)}[n]
    d.text(LP, f"EXIT {n.upper()} > {t or 'locked'}", font=F, fill=(255,255,255,255))
    d.ellipse([m[0]-8,m[1]-8,m[0]+8,m[1]+8],fill=(255,255,255,255))
d.ellipse([START[0]-10,START[1]-10,START[0]+10,START[1]+10],fill=(255,80,80,255)); d.text((START[0]+14,START[1]-12),"PLAYER START",font=F,fill=(255,120,120,255))
# horizon + scale figures
d.line([(0,HORIZON),(2000,HORIZON)],fill=(255,255,255,120),width=2); d.text((1500,HORIZON-30),"horizon (scale = 0)",font=F,fill=(255,255,255,200))
for y,x in ((880,220),(980,400),(1060,600)):
    h=person_h(y); w=h*0.26
    d.rectangle([x-w/2,y-h,x+w/2,y],outline=(255,255,255,255),width=3); d.ellipse([x-w*0.28,y-h,x+w*0.28,y-h+w*0.56],outline=(255,255,255,255),width=3)
    d.text((x+w/2+8,y-h/2),f"{round(h)}px",font=F,fill=(255,255,255,255))
d.text((30,640),"white figures: player height\nat that depth (1.8 m)",font=F,fill=(255,255,255,255))
Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB").save(os.path.join(OUT,"street_night_v1_plan_r2.png"))

# ---------- walk-behind cut-outs from the full-res plate ----------
src = Image.open(PLATE).convert("RGBA")
os.makedirs(os.path.join(OUT,"behind"),exist_ok=True)
cut = {}
for n,(p,sy) in BEHIND.items():
    o=[(x*KO,y*KO) for x,y in p]
    x0=int(min(q[0] for q in o)); y0=int(min(q[1] for q in o)); x1=int(max(q[0] for q in o))+1; y1=int(max(q[1] for q in o))+1
    mask=Image.new("L",(x1-x0,y1-y0),0); ImageDraw.Draw(mask).polygon([(x-x0,y-y0) for x,y in o],fill=255)
    c=src.crop((x0,y0,x1,y1)); c.putalpha(mask)
    fn=f"street_night_behind_{n.lower()}.png"; c.save(os.path.join(OUT,"behind",fn))
    cut[n]=(fn,x0,y0,sy)

# ---------- scene ----------
L=[]; ext=['[ext_resource type="Texture2D" path="res://assets/backgrounds/street_night/street_night_v1.png" id="1_bg"]']
for i,(n,(fn,x0,y0,sy)) in enumerate(cut.items()):
    ext.append(f'[ext_resource type="Texture2D" path="res://assets/backgrounds/street_night/behind/{fn}" id="{i+2}_{n.lower()}"]')
L.append(f"[gd_scene load_steps={len(ext)+1} format=3]\n"); L+= [e+"" for e in ext]
L.append('\n[node name="StreetNight" type="Node2D"]\n')
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
    t = t or "locked"; n = "".join(w.capitalize() for w in n.split("_"))
    L.append(f'[node name="{n}Zone" type="Polygon2D" parent="Exits"]\nvisible = false\ncolor = Color(1, 1, 1, 0.3)\npolygon = {pva(p)}\nmetadata/target = "{t}"\nmetadata/arrive = Vector2{sc(m)}\n')
open(os.path.join(OUT,"street_night.tscn"),"w").write("\n".join(L))
json.dump({k:{"poly":[list(q) for q in v[0]],"to":v[1]} for k,v in EXITS.items()},open(os.path.join(OUT,"exits.json"),"w"),indent=1)
json.dump({"floor":FLOOR,"block":BLOCK,"anim":ANIM},open(os.path.join(OUT,"street_night_view_coords.json"),"w"))
print("ok", {n:(c[1],c[2]) for n,c in cut.items()})
