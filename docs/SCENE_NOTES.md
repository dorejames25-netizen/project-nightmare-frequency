# Scene notes

Six connected rooms make up the first section. Each room is a fixed-camera still plate shown at half size in a 1376 x 768 viewport. Plates are 2752 x 1536 PNGs in `assets/backgrounds/<room>/<room>_v<N>.png`.

Room links and exit boxes live in `data/rooms/rooms.json`. Exits with `"to": null` are locked or not built yet.

| Room | Scene | Key colour | Exits |
| --- | --- | --- | --- |
| Metro platform (start) | `scenes/rooms/metro_platform.tscn` | magenta | stairs to concourse, tunnel |
| Station concourse | `scenes/rooms/station_concourse.tscn` | emerald green | stairs to platform, street doors, service passage |
| Street at night | `scenes/rooms/street_night.tscn` | teal | bottom edge to concourse; alley, right doorway, tower district (not built) |
| Service corridor | `scenes/rooms/service_corridor.tscn` | amber LED with magenta | far door to control room, side door to concourse |
| Control room | `scenes/rooms/control_room.tscn` | cold blue with magenta | door to corridor, stairs up (not built) |
| The tunnel | `scenes/rooms/tunnel.tscn` | magenta fog with green | ladder to service corridor, sealed gate (locked), back to platform |

## What is in each scene

All helper nodes are hidden in game. Turn on `visible` in the editor to see them.

| Node | Purpose |
| --- | --- |
| `Background` | The plate at half size |
| `WalkArea` | Where the player can walk |
| `Blockers/*` | Furniture the player cannot cross |
| `WalkBehind/*` | Columns and piers the player walks behind. Needs cut-out layers drawn above the player. |
| `AnimationSlots/*` | Blank or glowing screens, signs and shafts for the glyph rain and grin animations |
| `PlayerStart` | Spawn point |
| `Exits/*` | Marker at the foot of each exit, with `metadata/target` set to the room it leads to (or `locked`) |

All six rooms now have measured boundaries (round 2): floor, blockers, walk-behind cut-outs, animation slots, exit zones and a depth rule. Details are in `SUBWAY_BOUNDARIES.md` and `BOUNDARIES_NOTES.md`. They have not been tested in Godot yet, so expect to nudge points in the editor.
Player nodes go under `Actors` (y-sort). Walk-behind cut-outs are PNGs in `assets/backgrounds/<room>/behind/` and are added from the PC through Git LFS.

## Known art notes

- Control room: the dark disc in the floor reads as a pit, so it is blocked for now. Decide whether it is a hole, a hologram emitter or a lift.
- Tunnel: the left ledge is the walkable area. The track bed is not walkable.

## Adding a room

1. Make the plate at 2752 x 1536 and save it as `assets/backgrounds/<room>/<room>_v1.png`.
2. Duplicate a scene in `scenes/rooms/`, swap the texture and redraw the polygons.
3. Add the room and its exits to `data/rooms/rooms.json`.
