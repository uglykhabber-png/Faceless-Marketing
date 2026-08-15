import argparse
import json
from pathlib import Path

from .audit import audit_repository
from .core import Campaign, build_utm
from .sarif import report_to_sarif


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ethical OSS growth utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    utm = sub.add_parser("utm", help="Build deterministic UTM URL")
    utm.add_argument("url")
    utm.add_argument("--name", required=True)
    utm.add_argument("--channel", required=True)
    utm.add_argument("--objective", default="discoverability")

    audit = sub.add_parser("audit", help="Audit a local repository")
    audit.add_argument("path", nargs="?", default=".")
    audit.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON")
    audit.add_argument("--sarif", action="store_true", dest="as_sarif", help="Emit SARIF 2.1.0 JSON")

    return parser


def main(argv=None):
    args = _build_parser().parse_args(argv)

    if args.command == "utm":
        campaign = Campaign(args.name, args.channel, args.objective)
        print(build_utm(args.url, campaign))
        return 0

    if args.command == "audit":
        if args.as_json and args.as_sarif:
            raise SystemExit("choose only one of --json or --sarif")
        report = audit_repository(Path(args.path))
        if args.as_sarif:
            print(json.dumps(report_to_sarif(report), indent=2, sort_keys=True))
        elif args.as_json:
            print(json.dumps(report.as_dict(), indent=2, sort_keys=True))
        else:
            print(f"OSS discoverability score: {report.score}/100")
            if not report.findings:
                print("No findings.")
            for finding in report.findings:
                print(f"[{finding.severity.upper()}] {finding.rule_id}: {finding.title}")
                print(f"  {finding.message}")
                print(f"  Fix: {finding.remediation}")
        return 0

    raise RuntimeError("unreachable command")


if __name__ == "__main__":
    raise SystemExit(main())
