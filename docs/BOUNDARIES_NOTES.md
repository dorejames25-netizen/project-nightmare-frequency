# Boundary notes for the other five rooms (round 2)

Written by the measuring pass. Each section lists what is in the scene and what still needs a human decision. Scene units are plate pixels x 0.5. The metro platform is in `SUBWAY_BOUNDARIES.md`.

## station_concourse (plate v1) boundaries
Coords: view 2000x1116 = plate/1.376; scene = view*0.688 (plate at 0.5). Script: boundaries.py <plate> <out_dir>.
Scene: gothic hall, giant left column (Col1) + smaller Col2, stairs down (left-centre), dark service passage (centre), street double doors (centre-right), turnstile row and ticket booth (right), three destination boards, wall panels.
FLOOR: open at left/bottom/right screen edges; back edge on the wall base y~850 (view), then follows the turnstile front line down to the booth plinth.
BLOCK: Col1Base, Col2Base, Turnstiles, TicketBooth (turnstile lanes treated as closed; the floor edge already excludes them).
BEHIND (only two real occluders): Col1 sort_y 715.5, Col2 sort_y 605.4 (scene units). The columns by the turnstiles and the booth sit behind unwalkable floor, so no cut-outs. Actors y-sort node kept.
ANIM: BoardL/C/R (black screens), PanelWall, PanelRight, PanelBig (cyan panels), DoorGlass (rainy door and fanlight), VaultVoid (dark vault above the boards), NeonTube.
EXITS: stairs -> metro_platform (arrive 523,612), street_doors -> street_night (arrive 770,616), service -> service_corridor (arrive 647,616); all scene units.
PlayerStart view (900,1030) = scene (619,709).
DEPTH: horizon view y 751 = scene 516.7. Door 2.1 m = 195 px at view y 848, turnstile ~1 m = 177 px at y 935; both give horizon ~751.
person_height_per_px = 1.71 (view) / same ratio in scene: player_h = 1.71*(feet_y - horizon). ~255 px at y 900, ~597 px at y 1100 (view).
Uncertain / needs a human:
- Which opening is "service": I chose the dark corridor right of the stairs (view x 885-1010). The dark bay at x 1330-1480 behind the turnstiles is unreachable.
- Turnstile lanes could be gates to the platform; currently blocked.
- Col1 capital top (view y~24) hugs the cornice; the neon pilaster behind it is not included.
- Near-floor scale (597 px at the bottom) is large; cap the floor lower or apply a global factor if needed.

## street_night boundaries (plate 2752x1536; view 2000x1116 = plate/1.376; scene = view*0.688)
- Scene: night street, left stone arcade/pier wall, right shopfronts, tram parked at far end, bus shelter, wet cobbles with two neon kerb strips.
- WalkArea = pavement + road (neon kerb strips are painted kerb lights, treated as walkable). Back edge follows building bases, then tram front and shelter front. Open at bottom and right screen edges. Left edge x~212 (arch pier face), then diagonal to bottom.
- Blockers: Tram, ShelterBase, RightPillarBase (wall corner pier at far right).
- NO walk-behind cut-outs: the pier, left pillar, tram and shelter all sit on the floor's back edge, with no floor behind them, so nothing can hide the player. behind/ is empty. Actors (y_sort) kept, no Front nodes.
- Sort lines: none.
- Depth: horizon view y 712 = scene y 489.9 (kerb lines converge at ~(1153,720); doors at 3 depths agree, tram height ok).
  person_height_per_px = 1.646 (scene units: player_px = 1.646*(feet_y-489.9)); player 1.8 m, door 2.1 m.
  Examples scene y 700 -> 346 px tall, y 770 (bottom) -> ~460 px. That is huge; recommend clamping scale (e.g. max 0.5-0.6 of that) or cropping the floor lower. Human decision.
- AnimationSlots: SignLeft, SignMid, Billboard (neon screens), WindowL/M/S/R (neon-framed glass), ArchGlowA/B, SkylineGlow (pink gap at street end), TramLamp, DoorLight.
- Exits (target "locked" when null): station -> station_concourse (bottom edge, arrive scene (757,709)); alley (far dark gap left of the tram, tiny at depth); right_doorway (door panel in right shopfront); tower_district (lit recess with stair rail, right of that door).
- UNCERTAIN, need a human call: which opening is "tower_district" neon-door lobby (I used the lit recess at view x1800-1930; other candidates: dark door at x840-880 left, no neon door is clearly drawn). Alley is a thin gap, maybe better as the dark door at x840-880.
- Pillar/pier bases on the left sit exactly on the back edge, so no blockers needed there.
- Player start view (1100,1000) = scene (757,688).
- Files: street_night.tscn, exits.json (view coords), boundaries.py (run: python boundaries.py <plate> <out>).

## service_corridor v1 boundaries (view 2000x1116; scene = view*0.688)
Scene: brick/pipe service corridor, amber LED arches, magenta bulkhead (control_door) at far end, arched side door (left),
grated walkway down the middle with a stone ledge on the left, crates + cart on the right, steam at floor level.
- WalkArea: left stone ledge + grating, back edge along left wall base, far edge at the base of the control door,
  right edge along crate stack / cart; open at the bottom screen edge (x 432-1665 view). Grating treated as walkable.
- Blockers: CrateStackL, CartBase, CratesRight (right-side crate bases at screen edge).
- Behind: ONE occluder, Cart (cart frame + crate on it), sort_y 990 view = 681.1 scene. cut-out: behind/service_corridor_behind_cart.png.
  No other occluders: the left piers/columns sit outside the walkable floor (player can never be behind them), crates are
  blocked or further back. Actors y-sort node kept.
- Anim slots: ScreenL, ScreenR, BigMonitor (right wall black amber-framed), DoorGlow (magenta bulkhead), LightMain, LightMid,
  SkylightVoid (black hole upper right), SteamL, SteamR1, SteamR2.
- Exits: control_door -> control_room (floor strip at the far door, arrive scene (801.6,512.5));
  side_door -> station_concourse (strip at left arched door, arrive (419.7,652.2)). PlayerStart scene (688,715.5).
- Depth: horizon view y 585 = scene y 402.5. Door heights (193 px at y708, ~495 px at y900) give 1.573 px/px; with door 2.1 m
  and person 1.8 m person_height_per_px = 1.348 (dimensionless). Person ~ 479 view px (330 scene) at y940, ~170 scene px at y 710.
Uncertain / human decisions:
- Door height assumption (2.1 m) drives player scale; near-edge player (y1116) would be ~716 view px tall: cap the floor or apply a global factor.
- Grating over a dark pit: is it walkable? Assumed yes. Pocket under cart front (x1545-1660,y1050-1116) is walkable floor.
- Right half of the floor edge hidden by smoke/crates is estimated. Cart cut-out includes a sliver of the big crate at bottom right.
- control_door exit zone sits on the grating end; side door is in a recess (floor in front of it ~ y 905-975).

## control_room boundaries (plate control_room_v1.png, view 2000x1116; scene = view*0.688)
Regenerate: python boundaries.py <plate> <out_dir>. exits.json polys are in view coords.

Scene contents
- WalkArea: floor from the wall/console base (view y ~896-912) to the screen bottom; left edge follows the foreground pillar, right edge follows the right desk/chair; open at the bottom.
- Blockers: PillarBase, FloorDisc (dark disc, ellipse), BackConsole (desk + two chairs), Bollard (stone stump left of consoles), RightConsole (curved desk + chair 1 + chair 2).
- Actors (y_sort on): LeftPillar (sort y 750 scene) and RightChair (foreground chair, sort y 750 scene). Both feet run off the bottom edge, so the player can only get behind them, never in front, except at the very bottom rows.
- AnimationSlots: Oculus, ScreenL, MonitorWall, ScreenR1, ScreenR2, ScreenFarR1, ScreenFarR2 (partly off-screen), StairVoid, FloorDiscGlow.
- Exits: door -> service_corridor (arrive 255,664 scene); stairs_up -> target "locked" (arrive 949,643 scene).
- PlayerStart: scene (688, 747), front centre.

Depth (scene units): horizon_y 515.3, person_height_per_px 1.42 (player px = 1.42*(feet_y-515.3)): about 270 px at the back floor (y 706), 340 at start. Fit from chair heights (back chairs, chair 1, foreground chair 2) at ~1.1-1.2 m; the door gave a slightly larger figure (probably a taller door than 2.1 m). Cap or scale globally if the front is too big.

Needs a human decision / uncertain
- DARK DISC: kept fully BLOCKED (also listed in Blockers/FloorDisc, ellipse view cx 1001, cy 974, rx 405, ry 60). Pit, hologram emitter or lift is James's call; if it becomes a lift, turn it into an exit zone.
- Right side: the area behind the right desk and chair 1 is blocked as one region; chair 1 has no cut-out (nothing walkable behind it).
- Dark void left of the pillar (view x 0-100) is included in the LeftPillar cut-out; ScreenFarR1/R2 polygons are rough since they run off-frame.
- Sort lines sit at the screen bottom, so a player at the very bottom edge is drawn in front; raise the floor bottom a few px if that looks odd.
- Door exit zone is shallow (view y 915-955); stairs_up zone is clipped to stay off the disc ring.
- Cut-out PNGs are binaries (LFS). The plate was not altered.

## tunnel (tunnel_v1.png) boundaries
Measured on 2000x1116 view (orig = view*1.376, scene = view*0.688). Regenerate: python boundaries.py <plate> out
- Scene: left brick ledge (walkable) beside a sunken track bed (NOT walkable, outside floor). One free-standing brick pier
  (with iron rib and green stone arch springing from it) in the left foreground. Sealed neon gate at the far end of the tracks.
- WalkArea: back edge on wall base (y~790 left of pier, y~705 right of it); right edge is the kerb top; open at left and bottom screen edges.
- Blocker: PierBase (diamond footprint). One BEHIND cut-out: Pier (tunnel_behind_pier.png), includes rib/arch root up to view y=300
  so a head behind the pier is covered. Sort line: Pier = 578.6 scene y (view 841). No other occluders: the cart/timbers are on the
  track bed, the ladder and sign pier sit on the back wall behind the floor edge. Actors y-sort node kept.
- AnimationSlots: BoardL, ScreenBlack (dead screen), GateNeon, BoardFar, BoardMid, BoardR, Void (dark shaft at top).
- Exits: gate -> null (metadata/target empty, metadata/locked = true; zone at the far dead end of the ledge, arrival is a dummy),
  ladder -> service_corridor (floor under the ladder), platform -> metro_platform (left screen edge strip).
- PlayerStart scene (426.6, 660.5).
- Depth: horizon_y = 416.3 scene (view 605, from rail and kerb vanishing point). person_height_per_px = 2.09 (scene units:
  height = 2.09*(feet_y - 416.3)). Gate used as a 2.1 m door, cross-checked against pier width ~0.9 m.
## Uncertain / needs a human decision
- Person scale is large near the front (~370 scene px at y 768, ~175 at y 580). Cap or apply a global factor in Godot.
- The platform exit position (left edge) is a guess: nothing in the art shows where the way back to the subway is. Confirm.
- Floor behind the pier is hidden; back edge there is interpolated. The far end of the ledge by the gate is only ~10 px deep.
- Gate zone only lets the player reach the dead end; confirm the intended interaction (locked message).
- Cut-out top edge is straight at view y=300 (inside the arch art; no visible seam since it is the same pixels).
