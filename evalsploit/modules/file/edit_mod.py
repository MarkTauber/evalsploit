from __future__ import annotations

import base64
import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from evalsploit.config import project_root
from evalsploit.modules.base import load_snippet, substitute, php_quote, confirm_dangerous
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("edit")
class EditModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        if not args.strip():
            return None
        path = ctx.resolve_path(args.strip())
        if not ctx.file_exists(path):
            print("File does not exist")
            return None
        if not confirm_dangerous(ctx, "edit", path):
            return None
        # Download to temp
        snip = load_snippet(ctx.config.snippet_dl or "dl", "dl")
        if not snip:
            return "Snippet not found"
        php = substitute(snip, {"$_LOCAL": php_quote(path)})
        out = ctx.send(php)
        if out.strip() in ("X", "0"):
            print("Download failed")
            return None
        edit_dir = project_root() / "data" / "edit_tmp"
        edit_dir.mkdir(parents=True, exist_ok=True)
        name = Path(path).name
        local_path = edit_dir / name
        try:
            local_path.write_bytes(base64.b64decode(out))
        except Exception as e:
            print(f"Error: {e}")
            return None
        editor = os.environ.get("EDITOR", "notepad")
        os.system(f'{editor} "{local_path}"')
        input("Press Enter after editing to upload...")
        # Upload back
        data_b64 = base64.b64encode(local_path.read_bytes()).decode("ascii")
        up_snip = load_snippet(ctx.config.snippet_upload or "upload", "upload")
        if not up_snip:
            return "Snippet not found"
        php = substitute(up_snip, {"$_LOCAL": php_quote(path), "$_BASE": php_quote(data_b64)})
        ctx.send(php)
        try:
            local_path.unlink()
        except Exception:
            pass
        print("Updated")
        return None
