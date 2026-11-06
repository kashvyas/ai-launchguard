import json
from .agent import LaunchGuard


def main():
    copilot = LaunchGuard()
    cases = [
        ("campaign-copilot-v17", 100),
        ("cx-agent-v9", 100),
        ("internal-dev-agent-v3", 25),
    ]
    for feature, rollout in cases:
        print("\n" + "=" * 72)
        print(f"QUESTION: Can {feature} ship at {rollout}%?")
        result = copilot.assess(feature, rollout)
        print(json.dumps(result.as_dict(), indent=2))


if __name__ == "__main__":
    main()
