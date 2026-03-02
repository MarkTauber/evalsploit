"""find: recursive filename search via PHP regex."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import Module, load_snippet, substitute, php_quote
from evalsploit.modules.registry import register

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("find", description="Search filenames recursively (PHP regex)", usage="find <pattern> [path]")
class FindModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        parts = args.split()
        if not parts:
            print("Usage: find <pattern> [path]")
            return None

        pattern = parts[0]
        path = ctx.resolve_path(parts[1]) if len(parts) > 1 else ctx.pwd

        style = getattr(ctx.config, "find_style", "php")
        snip = load_snippet(style, "find")
        if not snip:
            print("Snippet not found")
            return None

        php = substitute(snip, {
            "__PATH_PLACEHOLDER__": php_quote(path),
            "__PATTERN_PLACEHOLDER__": php_quote(pattern),
        })
        out = ctx.send(php).strip()
        if out:
            print(out)
        return None
