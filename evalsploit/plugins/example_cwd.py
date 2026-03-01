"""Example plugin: show remote current working directory. Harmless."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import Module
from evalsploit.modules.registry import register

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register(
    "cwd",
    description="Show current working directory on server (example plugin)",
    usage="cwd",
)
class ExampleCwdModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        try:
            out = ctx.send("echo getcwd();")
            print(out.strip() or "(empty)")
        except Exception as e:
            print(f"Error: {e}")
        return None
