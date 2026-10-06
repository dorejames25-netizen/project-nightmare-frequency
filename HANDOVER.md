# Handover: Nightmare Frequency

Update this file at the end of every work session, and any time something big changes. If a session crashes or runs out of context, the next session starts here.

**Last updated:** 2026-10-06 22:10
**Owner:** James Dore

## 1. What this is
Nightmare Frequency (working title): a cyberpunk-gothic noir adventure. Fixed-camera comic-style still backgrounds (all art made by James in Adobe Firefly), invisible walk boundaries, walk-behind layers, animated overlays. Sprites and lighting come later.

## 2. Repos
| Repo | Purpose |
|---|---|
| `project-nightmare-frequency` | Godot 4.7 game (scenes, scripts, data, plates via Git LFS) |
| `dropzone-` | Art, prompts, story, docs |

Both have a proprietary licence: Copyright (c) 2026 James Dore. All rights reserved.

## 3. Standing rules
- Original names only. No brand names or exact religious names in project files.
- Modern lighting only (LED strips, neon tubes, recessed spots, light panels, caged work lights, holo fixtures). No lanterns, gas lamps, candles or torches.
- One key colour per room. Ink outlines, painted grimy texture, wet reflective floors.
- Plates are 2752x1536, 16:9, no people/text/UI. Screens and shafts are left blank for animation.
- Glyph rain (druid/Mayan-style glyphs, numbers) is its own animation, used on screens and skylines.
- Shell commands are given as separate pastable code blocks.
- Binaries (png etc.) go in via Git LFS from James's PC only. The cloud session cannot push LFS.

## 4. Story in one paragraph
The Makers made humans as a hybrid workforce in the age of the Ancients. An extinction event (the Wiping) ended an earlier age. Humans rebuilt and launched satellites, the Makers linked in and released the data virus Nightmare Frequency. It controls bionic upgrades and minds and warps VR into reality. It took over everything in one day; the public is unaware. Black-ops team Project Nightmare Frequency (scientists plus a secretly funded world organisation) fights back. Time is a force called Aion ("aions ago"). Full detail is in the World Guide PDF.

## 5. Rooms (status)
| Room | Plate | Key colour | Scene |
|---|---|---|---|
| metro_platform | v2 | magenta | built, polygons untested |
| station_concourse | v1 | emerald | built, polygons untested |
| street_night | v1 | teal | built, polygons untested |
| service_corridor | v1 | amber + magenta | built, polygons untested |
| control_room | v1 | cold blue + magenta | built, floor disc undecided (pit / hologram / lift) |
| tunnel | v1 | magenta fog + green | built, polygons untested |

Not built yet: upper control level, neon-door lobby / tower district.
Connections are in `docs/ROOM_LAYOUT.md` and `data/rooms/rooms.json`.

## 6. Where things stand
- Done: both repos structured and licensed, six plates plus plans made, six Godot scenes generated, world guide updated (Draft 2).
- Plates are NOT in either repo yet. Zips were given to James: `dropzone_art_part1.zip`, `dropzone_art_part2.zip` (into `dropzone-`), `game_assets_update.zip` (into the game repo).

## 6b. Latest state (22:10)
- PowerShell crashed on James's PC. Local repos at `C:\GitHub\dropzone-` and `C:\GitHub\project-nightmare-frequency` may hold uncommitted or unpushed work. Check `git status` and `git log origin/main..HEAD` before anything else.
- New artwork and plans are now in the `dropzone-` folder on James's PC. Plans came as single images. Zips are still in there; leave them. They move to an external backup when local work is finished, then the online repo gets updated.
- Cloud session cannot see his PC. Work continues in a Claude desktop task linked to his computer.
- `HANDOVER.md` is pushed to main in both repos.

## 7. Next steps
0. Read every folder in `C:\GitHub\dropzone-` (zips included), check image sizes (plates should be 2752x1536), compare with this file, and report what is new.
1. James extracts the zips, then pull, add, commit, push in each repo.
2. Add `story/Nightmare_Frequency_World_Guide.pdf` and style references (no real faces) by hand.
3. Open Godot and tune the first-pass walk polygons.
4. Decide the control-room floor disc.
5. Write prompts for the two unbuilt rooms.
6. Glyph-rain animation prompt and assets.
7. Merge the Sands of Time codex into the guide when provided (original names needed).
8. Set repos private before real art/story is pushed.

## 8. Session log
- 2026-10-06 22:10: handover updated after PowerShell crash; session moved to desktop link.
- 2026-10-06: modern-lighting redo of all six plates, Godot scenes and rooms.json generated, zips delivered. Session crashed; this handover added.
