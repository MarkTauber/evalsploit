from __future__ import annotations

import base64
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import load_snippet, substitute, php_quote, confirm_dangerous
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("upload")
class UplModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            print("Usage: upload <local_path>  or  upload <local_path> : <remote_path>")
            return None
        parts = [p.strip() for p in args.split(":", 1)]
        local_path = Path(parts[0])
        if not local_path.exists():
            print("Local file not found")
            return None
        remote = ctx.pwd.rstrip("/") + "/" + local_path.name
        if len(parts) > 1:
            remote = ctx.resolve_path(parts[1])
        if not confirm_dangerous(ctx, "upload", f"{local_path} -> {remote}"):
            return None
        data_b64 = base64.b64encode(local_path.read_bytes()).decode("ascii")
        snip = load_snippet(ctx.config.snippet_upload or "upload", "upload")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"$_LOCAL": php_quote(remote), "$_BASE": php_quote(data_b64)})
        out = ctx.send(php)
        if "X" in out:
            print("Upload failed")
        else:
            print("Uploaded")
        return None


register("put")(UplModule)
register("upl")(UplModule)
