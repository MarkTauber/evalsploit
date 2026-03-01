"""php: console to send arbitrary PHP code to the backdoor."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("php")
class PhpConsoleModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        print("PHP console. Enter code (single line), 'exit' to quit.")
        while True:
            try:
                line = input("php> ").strip()
            except EOFError:
                break
            if line.lower() == "exit":
                break
            if not line:
                continue
            out = ctx.send(line)
            print(out)
        return None
