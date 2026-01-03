# Tower Defense Game - Copilot Instructions

## Overview

This is a Python-based tower defense game inspired by "The Tower" mobile game, focusing on core gameplay mechanics without monetization or mobile-specific features. Players defend a central tower against waves of enemies approaching from all directions. The game uses geometric shapes for visuals to keep development simple.

## Architecture

- **Entry Point**: `main.py` - contains the main game loop and initialization
- **Game Modules**: Organized in `game/` directory with classes for:
  - Towers (central defensive tower with upgradeable stats)
  - Enemies (various geometric shapes with different behaviors)
  - Projectiles (attacks from the tower)
  - Map/Level (circular area around the central tower)
  - Resources (gold earned from defeating enemies for upgrades)
  - Waves (structured waves with 10 rounds culminating in a boss round)
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
- Use geometric shapes (circles, rectangles, etc.) for towers, enemies, and projectiles

## Dependencies

- `pygame`: Core game library
- Add others as needed (e.g., `pytest` for testing)

## Key Patterns

- **Game Loop**: Standard Pygame loop with event handling, updates, and rendering
- **Object-Oriented Design**: Each game entity as a class with update() and draw() methods
- **Collision Detection**: Use Pygame's rect collision for towers/enemies/projectiles
- **Wave System**: Enemies spawn in waves from around the central tower, with each wave consisting of 10 rounds ending in a boss enemy
- **Upgrade System**: Tower upgrades focus on stats like range, fire rate, multi-fire (shooting multiple projectiles), etc., purchased with gold from defeated enemies

Since the codebase currently lacks implementation, these guidelines establish the foundation for development. Reference Pygame documentation for specific API usage.