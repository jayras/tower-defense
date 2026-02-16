import sys
import argparse
from app.app import GameApp
from tests.test_config import test_config


def main():
    # Parse command-line arguments for test mode
    parser = argparse.ArgumentParser(description="Tower Defense Game")
    parser.add_argument("--test", action="store_true", help="Enable test mode")
    parser.add_argument("--scenario", type=str, help="Load a test scenario")
    parser.add_argument("--wave", type=int, help="Start at specific wave number")
    parser.add_argument("--enemy", type=str, help="Force enemy type (basic/fast/tank/ranged/boss)")
    parser.add_argument("--speed", type=float, help="Game speed multiplier")
    parser.add_argument("--invincible", action="store_true", help="Tower cannot die")
    parser.add_argument("--god", action="store_true", help="Enable god mode")
    parser.add_argument("--list-scenarios", action="store_true", help="List available scenarios")
    
    args = parser.parse_args()
    
    # Handle list scenarios
    if args.list_scenarios:
        print("Available test scenarios:")
        for scenario in test_config.list_scenarios():
            print(f"  - {scenario}")
        sys.exit(0)
    
    # Apply test configuration
    if args.scenario:
        if test_config.apply_scenario(args.scenario):
            print(f"Loaded test scenario: {args.scenario}")
        else:
            print(f"Unknown scenario: {args.scenario}")
            print("Use --list-scenarios to see available scenarios")
            sys.exit(1)
    
    if args.test:
        test_config.enabled = True
        test_config.auto_start = True
    
    if args.wave:
        test_config.enabled = True
        test_config.auto_start = True
        test_config.initial_wave = args.wave
    
    if args.enemy:
        test_config.enabled = True
        test_config.auto_start = True
        test_config.force_enemy_type = args.enemy
    
    if args.speed:
        test_config.enabled = True
        test_config.game_speed_multiplier = args.speed
    
    if args.invincible:
        test_config.enabled = True
        test_config.auto_start = True
        test_config.invincible_tower = True
    
    if args.god:
        test_config.enabled = True
        test_config.auto_start = True
        test_config.invincible_tower = True
        test_config.one_hit_kill = True
        test_config.infinite_range = True
    
    # Run the game
    GameApp().run()


if __name__ == "__main__":
    main()

