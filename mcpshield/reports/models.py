from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Finding:
    detector: str
    severity: str
    title: str
    description: str


@dataclass
class ScanSummary:
    generated: str = field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    )

    findings: List[Finding] = field(default_factory=list)

    @property
    def total(self):
        return len(self.findings)

    @property
    def critical(self):
        return sum(f.severity.lower() == "critical" for f in self.findings)

    @property
    def high(self):
        return sum(f.severity.lower() == "high" for f in self.findings)

    @property
    def medium(self):
        return sum(f.severity.lower() == "medium" for f in self.findings)

    @property
    def low(self):
        return sum(f.severity.lower() == "low" for f in self.findings)
