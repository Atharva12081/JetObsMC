"""Base observable interface for future extension plugins."""

from __future__ import annotations

from dataclasses import dataclass

from ..jet import Jet


@dataclass
class Observable:
    """Skeleton interface for scalable observable implementations."""

    name: str
    irc_safe: bool
    complexity: str

    def compute(self, jet: Jet) -> float:
        """Compute observable value for a given jet."""
        raise NotImplementedError(
            "Observable.compute must be implemented by subclasses"
        )
