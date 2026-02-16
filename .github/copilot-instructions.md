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

## Player Scoring and Progression
- Players earn gold for defeating enemies, which can be used to purchase tower upgrades during the game (not yet implemented).
- Additionally Players earn tokens for defeating enemies, which can be used to purchase permanent upgrades between games (not yet implemented).
   - Permanent upgrades raise the floor for the next game, allowing players to progress further in waves and earn more gold and tokens.
- Randomly during the game players will be presented with a clickable box to give them a few tickets which can be redeemed for unlocks and modules to assist in the game (not yet implemented).
- Tickets are also earned by daily quests and achievements (not yet implemented).
- As player progesses through waves, they will encounter different enemy types with varying stats and behaviors, increasing the challenge and rewards.
- Waves get progressivly harder, with more enemies, stronger enemies, and faster enemies.  Boss waves will be significantly more difficult but will also provide greater rewards.
- After 200 waves, players will have the option to go to the next "floor" which will be significantly harder but will also provide greater rewards.  This will allow for endless progression and replayability as players strive to reach higher floors and earn more rewards.

## Upgrades and Unlocks
- Initially playes will only be able to upgrade basic stats of the tower like attack damage, range, health, regen.
- At certain wave milestones (to be determined), players will unlock new stats and abilities to upgrade like multi-fire, projectile speed, etc.
- At a milestone (to be determined), playes will unlock the ability to purchase modules which will provide unique effects and abilities to the tower.  Modules will be purchasable with tickets and will have a cost that scales with the power of the module.  Players will be able to equip a limited number of modules at a time, adding a layer of strategy to the game as players decide which modules to equip for each run.

### Attack Upgrades


## Enemy Statistics
- Health, Attack, Speed, Mass.
- Mass is static and will be used in physics calculations for collision responses, knockback, and other interactions.
- 
- Spawn chances will be based on enemy type.  "What to Spawn" will be determined by a weighted random selection based on the current wave and enemy types available.
- Boss Spawns will be 0% on all waves not equal to 10, and 100% on wave 10.
- Enemy types are:
   - **Basic Enemy**: Health 10, Attack 1, Speed 2
   - **Fast Enemy**: Speed = Basic Enemy Speed * 2.1, other stats are same as basic enemy. (not implemented yet)
   - **Tank Enemy**: Health = Basic Enemy Health * 5, Speed is Basic Enemy Speed * 0.6 (not implemented yet)
   - **Ranged Enemy**: Same stats as Basic Enemy, but flies to "Range Ring" and shoots from a distance (not implemented yet)
   - **Boss Enemy**: Health = Basic Enemy Health * 20, Attack = Basic Enemy Attack, Speed = Basic Enemy Speed * 0.4 (not implemented yet)

   ### Enemy Upgrades
   - Formulas will return what stats to add for a given wave number.  Higher the wave, the higher the increase.  "Current Stats" will be stored in the wave manager and applied to all enemies spawned in that wave.  This will allow for dynamic difficulty scaling as the player progresses through waves.  This will also allow for a wave skip mechanic where the enemy upgrades will be skipped for a wave remaining "flat" until the next wave. (Other wave skip mechanics will be implemented as well like currency given as if the wave was completed, etc.)
   - Health Upgrade: (Base Seed) * (Growth Rate) ^ (Wave Number - 1)
   - Attack Upgrade: (Base Seed) * (Growth Rate) ^ (Wave Number - 1)
   