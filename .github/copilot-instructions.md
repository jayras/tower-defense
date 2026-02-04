# Tower Defense Game - Copilot Instructions

## Overview

This is a Python-based tower defense game inspired by "The Tower" mobile game, focusing on core gameplay mechanics without monetization or mobile-specific features. Players defend a central tower against waves of enemies approaching from all directions. The game uses geometric shapes for visuals to keep development simple.

## Architecture

- **Entry Point**: `main.py` - contains the main game loop and initialization (window 1000x700)
- **Game Modules**: Organized in `game/` directory with classes for:
  - Towers (central defensive tower with upgradeable stats: range 300px, health 100, multi-fire 1)
  - Enemies (10x10 wireframe squares, health 10, speed 2, damage 1, flash white on hit)
  - Projectiles (2x2 wireframe circles, speed 5, damage 5, homing on enemies)
  - Map/Level (circular area around the central tower)
  - Resources (gold earned from defeating enemies for upgrades - not yet implemented)
  - Waves (structured waves with 10 rounds of 5 enemies each, culminating in a boss round - boss not implemented)
- **Assets**: `assets/` directory for images, sounds, and other media files (minimal, as geometric shapes are used)
- **Tests**: `tests/` directory for unit and integration tests

## Development Workflow

1. **Environment Setup**:
   - Activate virtual environment: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

2. **Running the Game**:
   - `python main.py`

3. **Testing**:
   - `pytest` (if tests are added)

## Coding Conventions

- Use Pygame for graphics, input handling, and game loop
- Follow PEP 8 style guidelines
- Use classes for game entities with clear responsibilities
- Implement game states (menu, playing, paused, game over, upgrade screen)
- Use sprite groups for managing collections of game objects
- Use geometric shapes (wireframe polygons, rectangles, circles) for towers, enemies, and projectiles
- Tower firing: Projectile-based system - shoots only when previous projectiles are gone, no timer-based fire rate

## Dependencies

- `pygame`: Core game library
- Add others as needed (e.g., `pytest` for testing)

## Key Patterns

- **Game Loop**: Standard Pygame loop with event handling, updates, and rendering
- **Object-Oriented Design**: Each game entity as a class with update() and draw() methods
- **Collision Detection**: Use Pygame's sprite collision for projectiles/enemies
- **Wave System**: Enemies spawn in waves from around the central tower, with each wave consisting of 10 rounds ending in a boss enemy
- **Upgrade System**: Tower upgrades focus on stats like range, multi-fire (shooting multiple projectiles), etc., purchased with gold from defeated enemies
- **UI**: Display tower health; game over when tower health <=0

Current implementation includes basic gameplay: tower shoots homing projectiles at enemies, enemies damage tower on contact, hit reactions, and wave spawning. Reference Pygame documentation for specific API usage.