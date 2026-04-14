from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class AppSettings:
    run_ttl: timedelta = timedelta(hours=1)


settings = AppSettings()
