# Metro platform (subway): boundaries, round 2

Measured on a grid over the 2752 x 1536 plate (shown at 2000 x 1116). The first-pass rectangles are replaced.
Regenerate everything with `tools/metro_platform_boundaries.py <plate.png> <out_dir>`.

Scene coordinates = plate pixels x 0.5 (the plate is drawn at half size in a 1376 x 768 viewport).

## What the scene has now

| Node | What it is |
| --- | --- |
| `WalkArea` | The real floor. Back edge follows the wall base, right edge follows the platform kerb, left edge is open at the screen edge. |
| `Blockers/Col1Base` to `Col5Base` | Footprints of the five column plinths. |
| `Blockers/Bench` | Bench footprint on the floor. |
| `Actors` (y-sort on) | Put the player here. Holds `Col1Front` to `Col5Front`. |
| `Actors/ColNFront` | A cut-out of each column (shaft, capital, gargoyle, plinth) that draws over the player when the player stands behind it. The node's y is the sort line. |
| `AnimationSlots` | `ScreensL`, `Panel`, `PanelFar`, `Sign` (the neon sign screen), `Shaft` (dark void under the hanging poles). |
| `Exits/StairsZone` | Floor strip in front of the arched stairs. `metadata/target = "station_concourse"`. |
| `Exits/TunnelZone` | Far end of the platform: step down onto the tracks. `metadata/target = "tunnel"`. |
| `PlayerStart` | Front centre of the floor. |
| `Depth` | Perspective rule (below). |

Sort lines (scene y): Col1 711, Col2 635, Col3 598, Col4 581, Col5 570. Standing at a smaller y than the line puts the player behind the column.

## Depth scaling

Column heights fall in a straight line with distance, which gives a horizon at scene y 521.5. Taking a column as 3.2 m and the player as 1.8 m:

`player_height_px = 1.412 * (feet_y - 521.5)`

That is about 68 px at the back of the platform (y 570) and 348 px at the front edge (y 768). Both numbers are stored on the `Depth` node. If the near-edge size looks too big, cap the floor lower or multiply by a global factor.

## Needs checking in Godot

- The cut-out polygons hug the column silhouettes by eye. Walk the placeholder behind each column and nudge points if a bit of wall shows or the player is clipped.
- The tunnel is entered at the platform's far end. The track bed is not walkable.
- The files `assets/backgrounds/metro_platform/behind/*.png` are binaries, so they go in from the PC through Git LFS.
