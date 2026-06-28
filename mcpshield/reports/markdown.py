from pathlib import Path
from .models import ScanSummary


class MarkdownReport:

    def generate(self, summary: ScanSummary, output: str):

        lines = []

        lines.append("# MCP Fortress Scan Report")
        lines.append("")
        lines.append(f"Generated: **{summary.generated}**")
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- Total Findings: {summary.total}")
        lines.append(f"- Critical: {summary.critical}")
        lines.append(f"- High: {summary.high}")
        lines.append(f"- Medium: {summary.medium}")
        lines.append(f"- Low: {summary.low}")
        lines.append("")
        lines.append("## Findings")
        lines.append("")

        if not summary.findings:
            lines.append("No findings detected.")
        else:
            for i, finding in enumerate(summary.findings, 1):
                lines.append(f"### {i}. {finding.title}")
                lines.append("")
                lines.append(f"Severity: **{finding.severity}**")
                lines.append("")
                lines.append(f"Detector: `{finding.detector}`")
                lines.append("")
                lines.append(finding.description)
                lines.append("")

        Path(output).write_text("\n".join(lines), encoding="utf-8")

        return output
