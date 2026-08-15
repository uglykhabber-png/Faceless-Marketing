import argparse
import json
from .core import Campaign, build_utm

def main():
    p = argparse.ArgumentParser(description="Ethical faceless marketing utilities")
    sub = p.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("utm")
    u.add_argument("url")
    u.add_argument("--name", required=True)
    u.add_argument("--channel", required=True)
    u.add_argument("--objective", default="discoverability")
    a = u.parse_args()
    c = Campaign(a.name, a.channel, a.objective)
    print(build_utm(a.url, c))

if __name__ == "__main__":
    main()
