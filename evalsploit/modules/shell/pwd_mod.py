from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.registry import register

if TYPE_CHECKING:
    from evalsploit.context import SessionContext
from evalsploit.modules.base import Module


@register("pwd", description="Print current working directory", usage="pwd")
class PwdModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        print(ctx.pwd)
        return None
