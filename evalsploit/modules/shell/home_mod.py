from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.registry import register

if TYPE_CHECKING:
    from evalsploit.context import SessionContext
from evalsploit.modules.base import Module


@register("home", description="Go to server home directory (__DIR__)", usage="home")
class HomeModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        out = ctx.send("echo __DIR__;")
        pwd = out.strip()
        if pwd == "/tmp":
            pwd = ctx.send("echo getcwd();").strip()
        ctx.pwd = pwd or ctx.pwd
        return None
