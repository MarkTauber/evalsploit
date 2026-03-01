"""Example plugin: send echo with optional message and print result. Harmless."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import Module, php_quote
from evalsploit.modules.registry import register

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register(
    "echo",
    description="Send echo to server (example plugin)",
    usage="echo [message]",
)
class ExampleEchoModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        msg = args.strip() if args.strip() else "1"
        php = f"echo {php_quote(msg)};"
        try:
            out = ctx.send(php)
            print(out)
        except Exception as e:
            print(f"Error: {e}")
        return None
