# Metro platform: overlay and animation spec

What the art and animation stage needs for `scenes/rooms/metro_platform.tscn`.
Plate: `assets/backgrounds/metro_platform/metro_platform_v2.png`, 2752 x 1536.
Scene units are plate pixels x 0.5. Sizes below are in **plate pixels**, which is the size to draw at.

## Layer order (back to front)

1. `Background`: the plate.
2. Animation overlays: sit directly on the plate, behind everything that moves.
3. `Actors` (y-sort): player, characters, and the five column cut-outs.
4. Foreground effects: floor fog, light flicker, glitch. Drawn over the actors.
5. UI.

## Walk-behind cut-outs (done)

In `assets/backgrounds/metro_platform/behind/`. Checked on 2026-10-07: every opaque pixel matches the plate at the scene's positions.

| File | Size | Plate position (top left) | Sort line (scene y) |
| --- | --- | --- | --- |
| `metro_platform_behind_col1.png` | 370 x 1068 | 123, 399 | 711.4 |
| `metro_platform_behind_col2.png` | 217 x 622 | 866, 675 | 635.0 |
| `metro_platform_behind_col3.png` | 152 x 439 | 1213, 778 | 597.2 |
| `metro_platform_behind_col4.png` | 97 x 326 | 1417, 847 | 580.7 |
| `metro_platform_behind_col5.png` | 70 x 257 | 1543, 888 | 569.7 |

## Animation slots (measured, in the scene)

Each slot is a four-corner shape under `AnimationSlots`. Draw the animation flat at the box size,
then pin its corners to the slot's corners (the left-wall slots are in perspective).

| Slot | What it is on the plate | Box, plate px (x, y) | Box size | Planned animation |
| --- | --- | --- | --- | --- |
| `ScreensL` | Two cyan screens at the left edge | 0, 771 | 195 x 212 | Glyph rain, slow |
| `Panel` | Cyan wall panel above the bench | 570, 845 | 165 x 160 | Glyph rain or grin flash |
| `PanelFar` | Small cyan panel down the wall | 1170, 925 | 69 x 96 | Glyph rain, small |
| `Sign` | Hanging sign with the magenta frame | 1541, 530 | 347 x 151 | Main screen: grin, glitch, glyphs |
| `Shaft` | Dark gap above the sign | 1607, 0 | 217 x 502 | Tall glyph rain column |

Glyph-rain source frames are 1672 x 941 (`dropzone-/art/fx/glyph_rain/`, four frames). They are big enough for every slot.

## Extra slots (measured 2026-10-07, in the scene)

Checked by drawing them over the plate. Boxes are the outer bounds; the scene holds the exact shape.

| Slot | What it is on the plate | Box, plate px (x, y) | Box size | Idea |
| --- | --- | --- | --- | --- |
| `TunnelMouth` | Dark tunnel arch, right | 2040, 812 | 336 x 412 | Headlight glow, something moving in the dark |
| `StairsNeon` | Stair arch with its neon frame | 1676, 796 | 220 x 340 | Neon flicker |
| `RingLight1` | Near magenta ceiling ring | 1056, 112 | 152 x 72 | Slow pulse |
| `RingLight2` | Far magenta ceiling ring | 1376, 418 | 100 x 44 | Slow pulse |
| `CageLight1` | Top caged lamp and its cone | 2080, 200 | 300 x 300 | Flicker |
| `CageLight2` | Middle caged lamp and cone | 2060, 488 | 190 x 212 | Flicker |
| `CageLight3` | Small far caged lamp and cone | 2036, 672 | 160 x 140 | Flicker |
| `TubeLight1` | Teal tube under the first bracket | 660, 576 | 252 x 100 | Buzz flicker |
| `TubeLight2` | Magenta tube under the second bracket | 1100, 722 | 148 x 66 | Buzz flicker |
| `TubeLight3` | Small teal tube, third bracket | 1360, 812 | 64 x 34 | Buzz flicker |
| `FloorFog` | Fog band along the back of the floor | 0, 1080 | 2040 x 300 | Drifting fog, drawn over the actors |

Floor reflections need no slot of their own: use the `WalkArea` shape.
## Boundaries (measured)

Floor, five column bases, bench, two exit zones, depth rule. Values and method are in `SUBWAY_BOUNDARIES.md`.
Checked on 2026-10-07 by drawing the scene's shapes over the plate: they sit on the floor, plinths, bench and exits as intended.

## Still open

- **Not yet run in Godot.** Use the walk test (below) to confirm, then nudge points if needed.
- Player size: the depth rule gives about 68 px at the back and 348 px at the front of a 768 px screen.
  If that is too big, lower `height_factor` in the walk test until it looks right and record the number here.
- The tunnel exit is at the far end of the platform. The track bed is not walkable.

## Walk test

Open `scenes/debug/walk_test.tscn` in Godot and press F6.
Arrow keys walk, left click walks to a point, F1 shows the helper shapes, keys 1 to 6 change room.
The white figure obeys the floor, blockers, depth rule and column sorting, and follows exits into the next room.
This is a test tool only. The real player comes from the character work.
