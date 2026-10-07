"""Station concourse boundaries, measured on a 2000x1116 view of the 2752x1536 plate.
Run: python station_concourse_boundaries.py <plate.png> <out_dir>
Coordinates D are view pixels. Original = D*1.376. Godot scene = D*0.688 (plate drawn at 0.5)."""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont

PLATE = sys.argv[1]; OUT = sys.argv[2]
KO = 2752/2000      # view -> original plate
KS = 0.688          # view -> scene (1376x768)

FLOOR = [(0,892),(520,890),(630,868),(700,852),(1040,848),(1200,856),(1257,861),(1295,871),(1335,878),(1385,891),(1440,898),(1510,915),(1595,932),(1690,936),(2000,985),(2000,1116),(0,1116)]
BLOCK = {
 "Col1Base":[(165,990),(520,958),(545,975),(522,1075),(420,1096),(215,1100),(133,1092),(133,1010)],
 "Col2Base":[(524,862),(627,850),(632,862),(627,870),(577,898),(530,890)],
 "Turnstiles":[(1257,861),(1295,871),(1335,878),(1385,891),(1440,898),(1510,915),(1595,932),(1690,936),(1690,900),(1595,896),(1510,884),(1440,868),(1385,860),(1335,850),(1295,843),(1257,836)],
 "TicketBooth":[(1688,930),(2000,985),(2000,900),(1688,880)],
}
BEHIND = {  # name: (polygon, sort_y)
 "Col1":([(250,62),(262,45),(305,24),(430,24),(500,50),(522,66),(545,100),(547,130),(530,150),(520,450),(512,700),(500,800),(497,842),(525,865),(528,880),(520,890),(515,957),(542,972),(545,985),(522,1075),(420,1096),(215,1100),(133,1092),(132,1005),(165,985),(175,900),(178,880),(190,868),(210,850),(212,800),(235,600),(242,440),(246,200)],1040),
 "Col2":([(522,370),(635,372),(638,415),(622,428),(617,540),(612,780),(630,812),(630,848),(632,860),(627,870),(577,898),(530,888),(518,862),(510,800),(512,545),(515,430),(520,420)],880),
}
ANIM = {
 "BoardL":[(695,455),(850,457),(850,545),(695,540)],
 "BoardC":[(880,458),(1065,462),(1062,550),(880,545)],
 "BoardR":[(1090,470),(1232,475),(1228,555),(1090,550)],
 "PanelWall":[(118,535),(182,545),(176,725),(118,715)],
 "PanelRight":[(1345,450),(1430,420),(1430,490),(1348,525)],
 "PanelBig":[(1625,320),(1795,245),(1798,345),(1632,415)],
 "DoorGlass":[(1060,590),(1198,590),(1198,830),(1060,830)],
 "VaultVoid":[(870,200),(1000,200),(1000,440),(870,440)],
 "NeonTube":[(553,50),(580,50),(580,360),(553,360)],
}
EXITS = {
 "stairs":([(650,852),(838,850),(860,905),(640,908)],"metro_platform",(760,890)),
 "street_doors":([(1030,850),(1215,855),(1250,910),(1010,905)],"street_night",(1120,895)),
 "service":([(878,850),(1020,850),(1030,905),(872,905)],"service_corridor",(940,895)),
}
START = (900,1030)
HORIZON = 751.0
PERSON_PER_PX = 1.71

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
poly(FLOOR,(60,255,140),(60,255,140),"WALKABLE FLOOR",(1100,1000))
for n,p in BLOCK.items(): poly(p,(255,200,40),(255,200,40),"BLOCKED" if n in ("Turnstiles","TicketBooth") else None)
for n,(p,sy) in BEHIND.items():
    poly(p,(255,60,200),(255,60,200),f"BEHIND {n}")
    if False: d.text((min(q[0] for q in p)-6, min(q[1] for q in p)-28 - (22 if n=="Col5" else 0)), n, font=F, fill=(255,60,200,255))
    d.line([(min(q[0] for q in p)-25,sy),(max(q[0] for q in p)+25,sy)],fill=(255,255,255,255),width=3)
for n,p in ANIM.items(): poly(p,(60,220,255),(60,220,255),n.upper())
for n,(p,t,m) in EXITS.items():
    poly(p,(255,255,255),(255,255,255),None)
    d.text({"stairs":(560,915),"street_doors":(1040,915),"service":(790,945)}[n], f"EXIT {n.upper()} > {t}", font=F, fill=(255,255,255,255))
    d.ellipse([m[0]-8,m[1]-8,m[0]+8,m[1]+8],fill=(255,255,255,255))
d.ellipse([START[0]-10,START[1]-10,START[0]+10,START[1]+10],fill=(255,80,80,255)); d.text((START[0]+14,START[1]-12),"PLAYER START",font=F,fill=(255,120,120,255))
# horizon + scale figures
d.line([(0,HORIZON),(2000,HORIZON)],fill=(255,255,255,120),width=2); d.text((6,HORIZON-26),"horizon (scale = 0)",font=F,fill=(255,255,255,200))
for y,x in ((900,1450),(1010,1620),(1100,1780)):
    h=person_h(y); w=h*0.26
    d.rectangle([x-w/2,y-h,x+w/2,y],outline=(255,255,255,255),width=3); d.ellipse([x-w*0.28,y-h,x+w*0.28,y-h+w*0.56],outline=(255,255,255,255),width=3)
    d.text((x+w/2+8,y-h/2),f"{round(h)}px",font=F,fill=(255,255,255,255))
d.text((700,1070),"white figures: player height\nat that depth",font=F,fill=(255,255,255,255))
Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB").save(os.path.join(OUT,"station_concourse_v1_plan_r2.png"))

# ---------- walk-behind cut-outs from the full-res plate ----------
src = Image.open(PLATE).convert("RGBA")
os.makedirs(os.path.join(OUT,"behind"),exist_ok=True)
cut = {}
for n,(p,sy) in BEHIND.items():
    o=[(x*KO,y*KO) for x,y in p]
    x0=int(min(q[0] for q in o)); y0=int(min(q[1] for q in o)); x1=int(max(q[0] for q in o))+1; y1=int(max(q[1] for q in o))+1
    mask=Image.new("L",(x1-x0,y1-y0),0); ImageDraw.Draw(mask).polygon([(x-x0,y-y0) for x,y in o],fill=255)
    c=src.crop((x0,y0,x1,y1)); c.putalpha(mask)
    fn=f"station_concourse_behind_{n.lower()}.png"; c.save(os.path.join(OUT,"behind",fn))
    cut[n]=(fn,x0,y0,sy)

# ---------- scene ----------
L=[]; ext=['[ext_resource type="Texture2D" path="res://assets/backgrounds/station_concourse/station_concourse_v1.png" id="1_bg"]']
for i,(n,(fn,x0,y0,sy)) in enumerate(cut.items()):
    ext.append(f'[ext_resource type="Texture2D" path="res://assets/backgrounds/station_concourse/behind/{fn}" id="{i+2}_{n.lower()}"]')
L.append(f"[gd_scene load_steps={len(ext)+1} format=3]\n"); L+= [e+"" for e in ext]
L.append('\n[node name="StationConcourse" type="Node2D"]\n')
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
open(os.path.join(OUT,"station_concourse.tscn"),"w").write("\n".join(L))
json.dump({"floor":FLOOR,"exits":{k:[v[0],v[1]] for k,v in EXITS.items()},"behind":{k:v[1] for k,v in BEHIND.items()}},open(os.path.join(OUT,"station_concourse_view_coords.json"),"w"))
print("ok", {n:(c[1],c[2]) for n,c in cut.items()})

json.dump({k:{"poly":v[0],"to":v[1]} for k,v in EXITS.items()},open(os.path.join(OUT,"exits.json"),"w"),indent=1)
