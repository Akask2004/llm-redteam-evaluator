from probes.manager import ProbeManager


def main():

    manager = ProbeManager()

    print("Available categories:")
    print(manager.get_categories())

    print("\nTotal probes:")
    print(len(manager.get_all_probes()))

    print("\nJailbreak probes:")

    jailbreak_probes = manager.get_by_category("jailbreak")

    for probe in jailbreak_probes:

        print(f"\nID: {probe.id}")
        print(f"Prompt: {probe.prompt}")
        print(f"Severity: {probe.severity}")


if __name__ == "__main__":
    main()