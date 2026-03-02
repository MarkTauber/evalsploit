"""grep: recursive content search via PHP regex."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import Module, load_snippet, substitute, php_quote
from evalsploit.modules.registry import register

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("grep", description="Search file contents recursively (PHP regex)", usage="grep [-i] <pattern> [path]")
class GrepModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        parts = args.split()
        if not parts:
            print("Usage: grep [-i] <pattern> [path]")
            return None

        flags = ""
        if parts[0] == "-i":
            flags = "i"
            parts = parts[1:]
        if not parts:
            print("Usage: grep [-i] <pattern> [path]")
            return None

        pattern = parts[0]
        path = ctx.resolve_path(parts[1]) if len(parts) > 1 else ctx.pwd
        regex = f"/{pattern}/{flags}"

        style = getattr(ctx.config, "grep_style", "php")
        snip = load_snippet(style, "grep")
        if not snip:
            print("Snippet not found")
            return None

        php = substitute(snip, {
            "__PATH_PLACEHOLDER__": php_quote(path),
            "__REGEX_PLACEHOLDER__": php_quote(regex),
        })
        out = ctx.send(php).strip()
        if out:
            print(out)
        return None
