# Scene notes

## Scene 1: Metro platform (placeholder, locked as the quality standard)

- Plate: `assets/backgrounds/metro_platform/metro_platform_v1.png` (2752 x 1536)
- Scene: `scenes/rooms/metro_platform.tscn`, shown at half size in a 1376 x 768 viewport

First-pass data in the scene, all hidden in game and meant to be tuned in the editor:

| Node | Purpose |
| --- | --- |
| `WalkArea` | Where the player can walk. Stops at the yellow safety line. |
| `Blockers/Benches` | Furniture the player cannot cross. |
| `WalkBehind/LeftPillar`, `MidPillar` | Pillars the player walks behind. Needs cut-out layers drawn above the player. |
| `AnimationSlots/*` | Blank screens, sign and tall shaft where the glyph rain and grin animation go. |
| `PlayerStart`, `ExitStairs`, `ExitTunnel` | Spawn point and exits to later scenes. |

Polygons were estimated by eye from the plate and have not been tested in Godot yet.

## Adding a room

1. Make the plate in Firefly at 2752 x 1536 and save it in `assets/backgrounds/<room>/`.
2. Duplicate `scenes/rooms/metro_platform.tscn`, swap the texture and redraw the polygons.
3. Add exits in `data/rooms/` once the scene changer exists.
