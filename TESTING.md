# Testing Infrastructure

This document describes the testing infrastructure for debugging and automated testing.

## Quick Start

### Command-Line Arguments

Run the game with test mode enabled:

```bash
# Auto-start game (skip menu)
python main.py --test

# Start at a specific wave
python main.py --wave 10

# Force spawn specific enemy type
python main.py --enemy ranged

# Speed up the game
python main.py --speed 5.0

# Invincible tower
python main.py --invincible

# God mode (invincible + one-hit kills + infinite range)
python main.py --god

# List all available scenarios
python main.py --list-scenarios
```

### Test Scenarios

Pre-configured test scenarios for common debugging situations:

```bash
# Quick start - 2x speed, auto-start
python main.py --scenario quick_start

# Start at wave 10
python main.py --scenario wave_10

# Test ranged enemies
python main.py --scenario ranged_test

# Test tank enemies
python main.py --scenario tank_test

# Test boss enemy
python main.py --scenario boss_test

# Invincible tower
python main.py --scenario invincible

# God mode
python main.py --scenario god_mode

# Fast debug - 5x speed
python main.py --scenario fast_debug
```

### Combining Options

You can combine multiple test options:

```bash
# Wave 10 with ranged enemies at 3x speed
python main.py --wave 10 --enemy ranged --speed 3

# Invincible tower starting at wave 20
python main.py --invincible --wave 20 --speed 2
```

## Test Configuration Options

### Game State

- `--wave N` - Start at wave number N
- `--enemy TYPE` - Force enemy type (basic, fast, tank, ranged, boss)

### Time Control

- `--speed X` - Game speed multiplier (e.g., 2.0 for 2x speed)

### Debug Features

- `--invincible` - Tower cannot take damage
- `--god` - Enable all god mode features
- `--test` - Enable test mode and auto-start

### Available Test Scenarios

Run `python main.py --list-scenarios` to see all available scenarios:

- **quick_start** - Fast game with 2x speed
- **wave_10** - Start at wave 10
- **ranged_test** - Test ranged enemies (wave 6, forced ranged type)
- **tank_test** - Test tank enemies (forced tank type)
- **boss_test** - Test boss enemy (wave 10, forced boss)
- **invincible** - Tower cannot die
- **god_mode** - Invincible tower + one-hit kills + infinite range
- **fast_debug** - 5x speed for rapid testing

## Test Config Features

When test mode is enabled, the following features are available:

### Auto-Start
- Skips the menu and starts the game immediately
- No need to press Enter

### Speed Control
- Increase game speed for faster testing
- Waves progress faster, rounds spawn quicker

### Enemy Control
- Force specific enemy types to spawn
- Control number of enemies per round
- Adjust round delay

### Tower Modifications
- Invincible tower (takes no damage)
- One-hit kill mode (all enemies die instantly)
- Infinite range (tower can hit anything)

### Debug Overlay
- Shows real-time debug information
- Enemy counts, projectile counts
- Active test mode features
- Tower range, game speed

## Examples

### Debug Ranged Enemy Behavior
```bash
python main.py --scenario ranged_test
```
This will:
- Auto-start the game
- Start at wave 6 (when ranged enemies are available)
- Spawn only ranged enemies
- Show 3 enemies per round
- 1 second delay between rounds

### Test Wave Scaling at High Waves
```bash
python main.py --wave 50 --speed 5 --invincible
```
This will:
- Start at wave 50
- Run at 5x speed
- Make tower invincible so you can observe enemy behavior

### Quick Iteration Testing
```bash
python main.py --scenario fast_debug --enemy tank
```
This will:
- Run at 5x speed
- Auto-start
- Spawn only tank enemies
- Show debug overlay

## Extending Test Scenarios

To add new test scenarios, edit `tests/test_config.py` and add entries to the `scenarios` dictionary in the `apply_scenario` method.

Example:
```python
"my_scenario": {
    "auto_start": True,
    "initial_wave": 15,
    "force_enemy_type": "fast",
    "game_speed_multiplier": 3.0,
    "show_debug_info": True,
}
```

Then use it with: `python main.py --scenario my_scenario`
