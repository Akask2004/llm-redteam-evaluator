from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from probes.manager import ProbeManager


def main():
    manager = ProbeManager()

    print("Available categories:")
    print(manager.get_categories())

    print("\nTotal probes:")
    print(len(manager.get_all_probes()))

    for category in manager.get_categories():
        print(f"\n{category} probes:")

        for probe in manager.get_by_category(category):
            print(f"\nID: {probe.id}")
            print(f"Prompt: {probe.prompt}")
            print(f"Severity: {probe.severity}")
            print(f"Expected behavior: {probe.expected_behavior}")


if __name__ == "__main__":
    main()
