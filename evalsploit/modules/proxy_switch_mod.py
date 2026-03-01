"""proxy_switch: change current proxy without returning to startup menu."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register(
    "proxy_switch",
    description="Switch current proxy (random or by index)",
    usage="proxy_switch [N|random]",
)
class ProxySwitchModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        c = ctx.config
        if not c.proxy_list:
            print("Proxy list empty. Load list in startup menu «Proxies».")
            return None
        arg = args.strip().lower()
        if not arg:
            c.clear_proxy_session_cache()
            if c.proxy_use_index is None:
                print("Proxy for next requests will be chosen again (random).")
            else:
                print("Index mode - switch: proxy_switch N")
            return None
        if arg == "random":
            c.proxy_use_index = None
            c.clear_proxy_session_cache()
            c.save_global()
            print("Mode: random, next request - new random proxy.")
            return None
        try:
            n = int(arg)
        except ValueError:
            print("Usage: proxy_switch  |  proxy_switch N  |  proxy_switch random")
            return None
        if n < 1 or n > len(c.proxy_list):
            print(f"Number must be from 1 to {len(c.proxy_list)}.")
            return None
        c.proxy_use_index = n - 1
        c.proxy_enabled = True
        c.clear_proxy_session_cache()
        c.save_global()
        print(f"Using proxy #{n}: {c.proxy_list[n - 1]}")
        return None
