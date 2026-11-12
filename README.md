# Roblox 2017 port (HTML) — Brickhub

A fan-made, single-file browser recreation of a 2017-era Roblox-style game client, built in plain HTML/JavaScript (no libraries).

**Play:** open `index.html` in a browser. Everything (textures, sounds, models, animations) is embedded in that one file.

## What's inside
- Custom 3D engine (canvas 2D) with studded baseplate, skybox, shadows and camera collision
- 2017-style in-game UI: top bar, chat, player list, backpack/hotbar, Esc menu (Players / Settings / Help), Developer Console (F9)
- Animated R6 noob character (Idle, Walk, Jump, Fall, Tool, Idle2), random death crumble animations, spawn forcefield
- Classic gear: Linked Sword, Rocket Launcher, Time Bomb, Slingshot, Rocket Boots
- Shift Lock, optional Click to Move, 2008-style classic character sounds and modern action sounds
- Game browser, avatar editor (body colors), and **Brickhub Studio** (3D map editor with Explorer, Properties, Toolbox, Output, Play/Stop)
- Built-in game: **Tool Showcase**

Multiplayer, game submissions/releases and the AI content check only work when the page is hosted as a Claude artifact (they use its `room`, `db` and `sample` capabilities). Opened as a plain file it runs single-player.

## Folder layout
- `index.html` – the whole game
- `assets/sounds` – sound effects used by the game
- `assets/textures` – UI, sky and gear textures used by the game
- `assets/models` – gear OBJ models and the animated R6 noob (glTF)

## Credits
- Textures, sounds and fonts: from the Roblox client content folder © Roblox. Stud textures ripped by Goldtex; GUI elements ripped by thatmusicweeb; particles/console/activity icons by SonicFan, Friday, TheCoolKid.
- Linked Sword, Rocket Launcher, Time Bomb & Slingshot models ripped by HellFire2345 / Miles56.
- Character: "R6 Roblox Noob [Animated]" by Fog (https://sketchfab.com/fog_), CC-BY-4.0; "r6 roblox noob" by Basically Games (https://sketchfab.com/Pofdpoi), CC-BY-4.0.
- Studio Explorer icons: Retrogen theme by ldwbubby.
- Map inspired by the classic Roblox place Crossroads.

Not affiliated with or endorsed by Roblox Corporation.
