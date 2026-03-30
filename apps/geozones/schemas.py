from dataclasses import dataclass

from apps.geozones.models import Check


@dataclass
class CheckResult:
    check: Check
