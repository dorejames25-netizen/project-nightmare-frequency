# Nightmare Frequency (game)

Cyberpunk-gothic noir adventure. High-detail comic-style still backgrounds, real-time
characters, invisible walk boundaries and depth layers to give a 3D feel.

The Godot project lives at the root of this repository. Open `project.godot` in Godot 4.7.

Art masters, prompts and the story guide live in the companion repository, **dropzone-**.
Only finished, game-ready assets are copied into this one.

## Folder guide

| Folder | What goes there |
| --- | --- |
| `scenes/rooms/` | One scene per room (fixed-camera still plus walk, layer and animation data) |
| `scenes/characters/` | Player, enemies and NPC scenes |
| `scenes/ui/` | Menus, HUD, dialogue |
| `scenes/fx/` | Reusable effects such as glyph rain and glitch |
| `scripts/` | Code, split into `core`, `player`, `rooms`, `ui`, `fx` |
| `autoload/` | Global singletons (game state, scene changer, audio) |
| `shaders/` | `.gdshader` files |
| `resources/` | `.tres` / `.res` resources |
| `data/rooms/` | Room data, such as exits and spawn points |
| `assets/backgrounds/<room>/` | Final background plate and any cut-out layers for each room |
| `assets/sprites/` | `player`, `enemies`, `npcs` |
| `assets/fx/` | Effect art, including `glyph_rain` |
| `assets/ui/`, `assets/fonts/`, `assets/audio/` | UI art, fonts, music, sfx, voice |
| `addons/` | Godot plugins |
| `docs/` | Notes for this project |

## Rules

- Large images, models and audio go through Git LFS (see `.gitattributes`).
- Keep `.import` and `.uid` files in the repo. Never commit `.godot/`.
- Scenes use a 1376 x 768 viewport. Background plates are made at 2752 x 1536 and shown at half size.
- Original names only. No real brands, logos or characters.

## Ownership

Copyright (c) 2026 James Dore. All rights reserved. See `LICENSE`.
