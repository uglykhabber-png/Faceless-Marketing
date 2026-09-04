import argparse
import json
from pathlib import Path

from .audit import audit_repository
from .core import Campaign, build_utm
from .decision import prioritize
from .intelligence import intelligence_report
from .reporting import to_markdown
from .sarif import report_to_sarif


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ethical OSS growth intelligence utilities")
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
    discover = sub.add_parser("discover", help="Analyze evidence-backed discoverability gaps")
    discover.add_argument("path", nargs="?", default=".")
    discover.add_argument("--json", action="store_true", dest="as_json")
    decision = sub.add_parser("recommend", help="Score one explicit opportunity")
    decision.add_argument("--id", required=True, dest="recommendation_id")
    decision.add_argument("--title", required=True)
    decision.add_argument("--action", required=True)
    decision.add_argument("--expected-value", required=True, type=float)
    decision.add_argument("--evidence", required=True, type=float)
    decision.add_argument("--reach", type=float, default=1.0)
    decision.add_argument("--effort", type=float, default=1.0)
    decision.add_argument("--risk", type=float, default=1.0)
    decision.add_argument("--confidence", type=float, default=1.0)
    report = sub.add_parser("report", help="Render a repository audit plus discoverability report")
    report.add_argument("path", nargs="?", default=".")
    report.add_argument("--json", action="store_true", dest="as_json")
    args = parser
    return args


def main(argv=None):
    args = _build_parser().parse_args(argv)
    if args.command == "utm":
        campaign = Campaign(args.name, args.channel, args.objective)
        print(build_utm(args.url, campaign))
        return 0
    if args.command == "audit":
        if args.as_json and args.as_sarif:
            raise SystemExit("choose only one of --json or --sarif")
        result = audit_repository(Path(args.path))
        if args.as_sarif:
            print(json.dumps(report_to_sarif(result), indent=2, sort_keys=True))
        elif args.as_json:
            print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        else:
            print(f"OSS intelligence audit score: {result.score}/100")
            for finding in result.findings:
                print(f"[{finding.severity.upper()}] {finding.rule_id}: {finding.title}")
                print(f"  {finding.message}")
                print(f"  Fix: {finding.remediation}")
            if not result.findings:
                print("No findings.")
        return 0
    if args.command == "discover":
        result = intelligence_report(Path(args.path))
        payload = result.as_dict()
        if args.as_json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(f"Discoverability score: {result.score}/100")
            for gap in result.gaps:
                print(f"[{gap.gap_id}] {gap.title}: {gap.rationale}")
        return 0
    if args.command == "recommend":
        result = prioritize(recommendation_id=args.recommendation_id, title=args.title, action=args.action, expected_value=args.expected_value, evidence=args.evidence, reach=args.reach, effort=args.effort, risk=args.risk, confidence=args.confidence)
        print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        return 0
    if args.command == "report":
        audit = audit_repository(Path(args.path)).as_dict()
        intel = intelligence_report(Path(args.path)).as_dict()
        payload = {"schema_version": 1, "score": audit["score"], "findings": audit["findings"], "gaps": intel["gaps"]}
        print(json.dumps(payload, indent=2, sort_keys=True) if args.as_json else to_markdown(payload))
        return 0
    raise RuntimeError("unreachable command")


if __name__ == "__main__":
    raise SystemExit(main())
