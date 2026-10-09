# Lava Escape Repair Lab — Completed

A vertical platformer survival game built with Python and Pygame. This version implements all four lab tasks.

## Requirements
- Python 3.10 or newer (Python 3.13 is supported with a compatible Pygame release)
- Windows, Linux, or macOS with a graphical desktop

## Install and run (Windows PowerShell)

Open PowerShell in this folder:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

If you already installed dependencies for Python 3.13, you can run:

```powershell
py -3.13 main.py
```

## Controls
- A / D or Left / Right Arrow: move
- Space / W / Up Arrow: jump
- R: restart after a run or while playing
- Close the game window: exit

## Lab tasks implemented

1. **Platform underside collision fix:** landing only occurs while falling and when the player's feet cross the platform's top edge. Jumping upward through a platform no longer snaps the player to its top.
2. **Crumbling platforms:** orange platforms shake after landing and disappear after about 0.8 seconds.
3. **Spring platforms:** green platforms give the player a stronger upward launch.
4. **Danger HUD and lava surges:** the HUD shows a lava danger meter. Periodic surge phases temporarily increase the lava's rise speed and show a warning.

The original game-over, victory, camera tracking, height counter, procedural platforms, and restart behavior are retained.

## Submission checklist

- [ ] Before video: record 10 seconds of the original game showing the collision bug. This must be captured from the original version before replacing it.
- [ ] After video: record 10 seconds showing the corrected collision and new features.
- [ ] Submit the share link to the ChatGPT conversation used for the lab, with complete history.

## Suggested after-video recording
Show the player jumping up through the underside of a platform, then landing on top. If possible, show an orange crumbling platform, a green spring platform, and the danger/surge HUD. The platform types are procedurally generated, so you may need to restart for a useful layout.
