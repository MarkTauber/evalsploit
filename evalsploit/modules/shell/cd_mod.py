from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.registry import register

if TYPE_CHECKING:
    from evalsploit.context import SessionContext
from evalsploit.modules.base import Module


@register("cd")
class CdModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            print(ctx.pwd)
            return None
        raw = args.strip()
        if raw == "..":
            ctx.pwd = ctx.pwd.rstrip("/")
            ctx.pwd = ctx.pwd.rsplit("/", 1)[0] or "/"
            return None
        path = ctx.resolve_path(raw)
        if not ctx.file_exists(path):
            print("Directory does not exist")
            return None
        ctx.pwd = path.rstrip("/") or "/"
        return None
