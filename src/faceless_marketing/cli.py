import argparse

from .core import Campaign, build_utm


def main() -> None:
    parser = argparse.ArgumentParser(description="Ethical faceless marketing utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    utm = subparsers.add_parser("utm", help="Build a URL with UTM parameters")
    utm.add_argument("url")
    utm.add_argument("--name", required=True)
    utm.add_argument("--channel", required=True)
    utm.add_argument("--objective", default="discoverability")

    args = parser.parse_args()

    if args.command == "utm":
        campaign = Campaign(args.name, args.channel, args.objective)
        print(build_utm(args.url, campaign))


if __name__ == "__main__":
    main()
