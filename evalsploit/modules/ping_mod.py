"""ping / check: test connection and measure latency."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Optional

from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("ping")
class PingModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        try:
            t0 = time.perf_counter()
            out = ctx.send("echo 1;")
            t1 = time.perf_counter()
            ms = round((t1 - t0) * 1000)
            ok = out.strip() == "1"
            if ok:
                print(f"OK ({ms} ms)")
            else:
                print(f"Reply unexpected ({ms} ms): {out.strip()!r}")
        except Exception as e:
            print(f"Failed: {e}")
        return None


register("check")(PingModule)
