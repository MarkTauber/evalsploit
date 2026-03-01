"""config: show current evalsploit settings."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("config")
class ConfigShowModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        c = ctx.config
        w = 12
        print()
        print("  --- Connection ---")
        print(f"  {'url':<{w}} {c.url or '(empty)'}")
        print(f"  {'Z':<{w}} {c.Z}")
        print(f"  {'V':<{w}} {c.V}")
        print(f"  {'send_mode':<{w}} {c.send_mode}")
        print("  --- Behavior ---")
        print(f"  {'run_shell':<{w}} {c.run_shell}")
        print(f"  {'ls_style':<{w}} {c.ls_style}")
        print(f"  {'cat_style':<{w}} {c.cat_style}")
        print(f"  {'silent':<{w}} {c.silent}")
        print(f"  {'reverse_type':<{w}} {c.reverse_type}")
        print(f"  {'confirm':<{w}} {c.confirm}")
        proxy_mode = "random" if c.proxy_use_index is None else f"#{c.proxy_use_index + 1}"
        print(f"  {'proxy_enabled':<{w}} {c.proxy_enabled}")
        print(f"  {'proxy_mode':<{w}} {proxy_mode}  (in list: {len(c.proxy_list)}, validated: {len(c.proxy_validated)})")
        print("  --- Snippets (set X help) ---")
        for key in ("rm", "dl", "upload", "rename", "stat", "touch", "mf", "md", "copy"):
            attr = f"snippet_{key}"
            print(f"  {attr:<{w}} {getattr(c, attr, key)}")
        print()
        return None
